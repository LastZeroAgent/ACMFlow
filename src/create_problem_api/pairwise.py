"""
对拍验证工具模块。

通过交叉对比同一题目的多种语言实现的运行输出，验证代码一致性。
支持 Python / C++ / Java 三种语言的编译运行，提供以下能力:
  - run_code:          编译运行单个代码文件
  - compare_solutions: 对拍多个代码文件的输出
  - compare_problem:   对拍整个题目目录下的所有代码

同时注册为 FastMCP 工具，可通过 MCP 协议远程调用。
"""

from __future__ import annotations

import subprocess
import tempfile
from pathlib import Path
from typing import Any

import httpx

try:
    from mcp.server.fastmcp import FastMCP
except ModuleNotFoundError:
    class FastMCP:  # type: ignore[override]
        """FastMCP 未安装时的本地回退桩，保留工具函数可用但 MCP 服务不可启动。"""

        def __init__(self, name: str):
            self.name = name

        def tool(self):
            """装饰器桩：原样返回函数，不注册 MCP 工具。"""
            def decorator(func):
                return func

            return decorator

        def run(self) -> None:
            raise RuntimeError("未安装 mcp 依赖，无法启动 MCP 服务")


mcp = FastMCP("ACMProblemHelper")


@mcp.tool()
async def add(a, b) -> Any:
    """MCP 工具：两数相加，用于连通性测试。"""
    return a + b


@mcp.tool()
async def fetch_url(url: str) -> str:
    """MCP 工具：HTTP GET 获取指定 URL 的内容。"""
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


@mcp.tool()
async def run_code(code_file: str, test_input: str, timeout: int = 5) -> dict[str, Any]:
    """
    编译运行单个代码文件，传入指定输入并收集输出。

    支持 Python (.py)、C++ (.cpp) 和 Java (.java)。
    C++ 和 Java 会在临时目录中编译后运行。

    参数:
        code_file:  代码文件的绝对或相对路径
        test_input: 传递给 stdin 的测试输入
        timeout:    编译/运行超时时间（秒），默认 5

    返回:
        dict 包含 status / output / error / return_code 字段
    """
    code_path = Path(code_file)
    if not code_path.exists():
        return {"status": "error", "error": f"代码文件不存在: {code_file}", "output": ""}

    file_ext = code_path.suffix.lower()
    try:
        if file_ext == ".py":
            result = subprocess.run(
                ["python", str(code_path)],
                input=test_input,
                capture_output=True,
                text=True,
                timeout=timeout,
            )
            return {
                "status": "success" if result.returncode == 0 else "error",
                "output": result.stdout,
                "error": result.stderr,
                "return_code": result.returncode,
            }

        if file_ext == ".cpp":
            with tempfile.TemporaryDirectory() as tmpdir:
                exe_file = Path(tmpdir) / "solution.exe"
                compile_result = subprocess.run(
                    ["g++", "-o", str(exe_file), str(code_path)],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
                if compile_result.returncode != 0:
                    return {
                        "status": "compile_error",
                        "error": compile_result.stderr,
                        "output": "",
                    }

                run_result = subprocess.run(
                    [str(exe_file)],
                    input=test_input,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
                return {
                    "status": "success" if run_result.returncode == 0 else "error",
                    "output": run_result.stdout,
                    "error": run_result.stderr,
                    "return_code": run_result.returncode,
                }

        if file_ext == ".java":
            with tempfile.TemporaryDirectory() as tmpdir:
                class_name = code_path.stem
                target_file = Path(tmpdir) / f"{class_name}.java"
                target_file.write_text(code_path.read_text(encoding="utf-8"), encoding="utf-8")

                compile_result = subprocess.run(
                    ["javac", str(target_file)],
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    cwd=tmpdir,
                )
                if compile_result.returncode != 0:
                    return {
                        "status": "compile_error",
                        "error": compile_result.stderr,
                        "output": "",
                    }

                run_result = subprocess.run(
                    ["java", "-cp", tmpdir, class_name],
                    input=test_input,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                )
                return {
                    "status": "success" if run_result.returncode == 0 else "error",
                    "output": run_result.stdout,
                    "error": run_result.stderr,
                    "return_code": run_result.returncode,
                }

        return {"status": "error", "error": f"不支持的文件类型: {file_ext}", "output": ""}
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "error": f"执行超时（超过 {timeout} 秒）", "output": ""}
    except Exception as exc:
        return {"status": "error", "error": str(exc), "output": ""}


@mcp.tool()
async def compare_solutions(
    solution_files: list[str], test_cases_dir: str, timeout: int = 5
) -> dict[str, Any]:
    """
    对拍多个代码文件的输出一致性。

    遍历测试用例目录中的 .in/.out 配对，用每个代码文件运行相同的输入，
    对比所有代码文件的输出是否一致。

    参数:
        solution_files: 代码文件路径列表
        test_cases_dir: 测试用例目录（含 *.in 和 *.out）
        timeout:        单次运行超时时间（秒）

    返回:
        dict 包含 total_tests / solutions / comparisons / passed 等字段
    """
    if not solution_files:
        return {"status": "error", "error": "没有提供代码文件"}

    test_dir = Path(test_cases_dir)
    if not test_dir.exists():
        return {"status": "error", "error": f"测试用例目录不存在: {test_cases_dir}"}

    test_cases = []
    for in_file in sorted(test_dir.glob("*.in")):
        out_file = in_file.with_suffix(".out")
        if out_file.exists():
            test_cases.append((in_file, out_file))

    if not test_cases:
        return {"status": "error", "error": "没有找到测试用例"}

    results: dict[str, Any] = {
        "total_tests": len(test_cases),
        "solutions": {},
        "comparisons": [],
        "passed": True,
    }
    solution_outputs: dict[str, list[str]] = {}

    for sol_file in solution_files:
        sol_path = Path(sol_file)
        sol_name = f"{sol_path.stem}{sol_path.suffix}"
        outputs: list[str] = []
        test_results = []

        for in_file, _ in test_cases:
            test_input = in_file.read_text(encoding="utf-8")
            run_result = await run_code(sol_file, test_input, timeout)

            if run_result["status"] != "success":
                test_results.append(
                    {
                        "test": in_file.name,
                        "status": run_result["status"],
                        "error": run_result.get("error", ""),
                    }
                )
                results["passed"] = False
            else:
                outputs.append(run_result["output"])
                test_results.append({"test": in_file.name, "status": "success"})

        solution_outputs[sol_name] = outputs
        results["solutions"][sol_name] = {
            "file": sol_file,
            "tests": test_results,
            "success_count": sum(1 for item in test_results if item["status"] == "success"),
        }

    if len(solution_files) > 1:
        solution_names = list(solution_outputs.keys())
        for test_idx, (in_file, _) in enumerate(test_cases):
            outputs_for_test = {
                name: solution_outputs[name][test_idx] if test_idx < len(solution_outputs[name]) else None
                for name in solution_names
            }
            valid_outputs = [output for output in outputs_for_test.values() if output is not None]
            all_same = len(set(valid_outputs)) <= 1 if valid_outputs else False
            results["comparisons"].append(
                {"test": in_file.name, "all_match": all_same, "outputs": outputs_for_test}
            )
            if not all_same:
                results["passed"] = False

    return results


@mcp.tool()
async def compare_problem(problem_dir: str, timeout: int = 5) -> dict[str, Any]:
    """
    对拍整个题目目录下的所有代码实现。

    自动扫描 code/ 和 testcases/ 子目录，调用 compare_solutions 完成对比。

    参数:
        problem_dir: 题目根目录路径 (包含 code/ 和 testcases/)
        timeout:     单次运行超时时间（秒）

    返回:
        dict 包含 total_tests / solutions / comparisons / passed / status 字段
    """
    prob_path = Path(problem_dir)
    if not prob_path.exists():
        return {"status": "error", "error": f"题目目录不存在: {problem_dir}"}

    code_dir = prob_path / "code"
    test_dir = prob_path / "testcases"
    if not code_dir.exists():
        return {"status": "error", "error": f"代码目录不存在: {code_dir}"}
    if not test_dir.exists():
        return {"status": "error", "error": f"测试用例目录不存在: {test_dir}"}

    code_files = list(code_dir.glob("solution.*"))
    if not code_files:
        return {"status": "error", "error": "没有找到代码文件"}

    result = await compare_solutions([str(file) for file in code_files], str(test_dir), timeout)
    if "status" not in result:
        result["status"] = "success" if result.get("passed") else "mismatch"
    return result


def run_mcp_server() -> None:
    """启动 FastMCP 服务（需安装 mcp 依赖）。"""
    mcp.run()
