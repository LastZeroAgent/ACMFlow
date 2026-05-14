"""
对拍工具完整示例集。

展示 pairwise 模块的全部使用模式:
  1. 批量验证所有题目
  2. 调试单个题目
  3. 交互式对比两个解法
  4. 单输入验证
  5. 生成报告
"""

from __future__ import annotations

import asyncio
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.create_problem_api.pairwise import compare_problem, compare_solutions, run_code


PROBLEM_DIR = "problem/normal/回文数判定"
REPORT_FILE = Path("reports/pairwise_report.json")


async def example_1_verify_all_problems() -> None:
    """示例1: 批量验证 problem/normal/ 下所有题目。"""
    print("\n" + "=" * 70)
    print("示例1: 批量验证全部题目")
    print("=" * 70)

    problem_base = Path("problem/normal")
    results = {}
    for problem_dir in sorted(problem_base.iterdir()):
        if not problem_dir.is_dir():
            continue
        result = await compare_problem(str(problem_dir))
        results[problem_dir.name] = {
            "passed": result.get("passed", False),
            "total_tests": result.get("total_tests", 0),
            "solutions": len(result.get("solutions", {})),
        }
    print(json.dumps(results, ensure_ascii=False, indent=2))


async def example_2_debug_specific_problem() -> None:
    """示例2: 调试特定题目的完整对拍结果。"""
    print("\n" + "=" * 70)
    print("示例2: 调试单个题目")
    print("=" * 70)
    result = await compare_problem(PROBLEM_DIR)
    print(json.dumps(result, ensure_ascii=False, indent=2))


async def example_3_interactive_comparison() -> None:
    """示例3: 对比两个 Python 解法文件的输出一致性。"""
    print("\n" + "=" * 70)
    print("示例3: 比较两个解法")
    print("=" * 70)
    result = await compare_solutions(
        [f"{PROBLEM_DIR}/code/solution.py", f"{PROBLEM_DIR}/code/solution_1.py"],
        f"{PROBLEM_DIR}/testcases",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


async def example_4_validate_single_test() -> None:
    """示例4: 验证单个测试输入的代码输出。"""
    print("\n" + "=" * 70)
    print("示例4: 调试单个输入")
    print("=" * 70)
    result = await run_code(f"{PROBLEM_DIR}/code/solution.py", "121")
    print(json.dumps(result, ensure_ascii=False, indent=2))


async def example_5_generate_report() -> None:
    """示例5: 对拍并生成 JSON 报告文件。"""
    result = await compare_problem(PROBLEM_DIR)
    REPORT_FILE.parent.mkdir(exist_ok=True)
    REPORT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n报告已生成: {REPORT_FILE}")


async def main() -> None:
    """顺序执行全部 5 个示例。"""
    await example_1_verify_all_problems()
    await example_2_debug_specific_problem()
    await example_3_interactive_comparison()
    await example_4_validate_single_test()
    await example_5_generate_report()


if __name__ == "__main__":
    asyncio.run(main())
