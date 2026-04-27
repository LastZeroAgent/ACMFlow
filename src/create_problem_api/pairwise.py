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
        """Fallback shim so local helpers remain usable without the MCP package."""

        def __init__(self, name: str):
            self.name = name

        def tool(self):
            def decorator(func):
                return func

            return decorator

        def run(self) -> None:
            raise RuntimeError("未安装 mcp 依赖，无法启动 MCP 服务")


mcp = FastMCP("ACMProblemHelper")


@mcp.tool()
async def add(a, b) -> Any:
    return a + b


@mcp.tool()
async def fetch_url(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.text


@mcp.tool()
async def run_code(code_file: str, test_input: str, timeout: int = 5) -> dict[str, Any]:
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
    mcp.run()
