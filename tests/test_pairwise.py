"""
对拍工具集成测试模块。

以异步方式验证 pairwise 模块的三个核心能力:
  1. 单个代码文件运行
  2. 多个代码文件输出对比
  3. 整个题目目录的对拍

需要在 problem/normal/ 下有已生成的题目数据才可运行。
"""

from __future__ import annotations

import asyncio
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.create_problem_api.pairwise import compare_problem, compare_solutions, run_code


PROBLEM_DIR = "problem/normal/回文数判定"


async def test_single_solution() -> None:
    """测试1: 运行单个 Python 代码文件并检查输出。"""
    print("=" * 60)
    print("测试1: 运行单个 Python 解决方案")
    print("=" * 60)

    code_file = f"{PROBLEM_DIR}/code/solution.py"
    with open(f"{PROBLEM_DIR}/testcases/1.in", encoding="utf-8") as handle:
        test_input = handle.read()

    result = await run_code(code_file, test_input)
    print(f"输入: {test_input.strip()}")
    print(f"状态: {result['status']}")
    print(f"输出: {result['output'].strip()}")
    if result.get("error"):
        print(f"错误: {result['error']}")
    print()


async def test_compare_solutions_case() -> None:
    """测试2: 对拍 Python 和 C++ 两个解决方案的输出一致性。"""
    print("=" * 60)
    print("测试2: 对拍多个解决方案")
    print("=" * 60)

    code_files = [f"{PROBLEM_DIR}/code/solution.py", f"{PROBLEM_DIR}/code/solution.cpp"]
    result = await compare_solutions(code_files, f"{PROBLEM_DIR}/testcases")

    print(f"总测试数: {result.get('total_tests', 0)}")
    print(f"是否全部通过: {result.get('passed', False)}")
    for sol_name, sol_info in result.get("solutions", {}).items():
        print(f"  {sol_name}: {sol_info['success_count']} / {result.get('total_tests', 0)}")
    print()


async def test_compare_problem_case() -> None:
    """测试3: 对拍整个题目目录下的所有代码实现。"""
    print("=" * 60)
    print("测试3: 对拍整个题目")
    print("=" * 60)

    result = await compare_problem(PROBLEM_DIR)
    print(f"题目目录: {PROBLEM_DIR}")
    print(f"总测试数: {result.get('total_tests', 0)}")
    print(f"是否全部通过: {result.get('passed', False)}")
    print(f"状态: {result.get('status', 'unknown')}")
    if result.get("error"):
        print(f"错误: {result['error']}")
    print()


async def main() -> None:
    """顺序执行三个集成测试用例。"""
    print("\n开始对拍工具测试...\n")
    for test_func in (test_single_solution, test_compare_solutions_case, test_compare_problem_case):
        try:
            await test_func()
        except Exception as exc:
            print(f"{test_func.__name__} 失败: {exc}\n")
    print("=" * 60)
    print("测试完成")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(main())
