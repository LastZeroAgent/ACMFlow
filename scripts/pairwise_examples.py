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
    print("\n" + "=" * 70)
    print("示例2: 调试单个题目")
    print("=" * 70)
    result = await compare_problem(PROBLEM_DIR)
    print(json.dumps(result, ensure_ascii=False, indent=2))


async def example_3_interactive_comparison() -> None:
    print("\n" + "=" * 70)
    print("示例3: 比较两个解法")
    print("=" * 70)
    result = await compare_solutions(
        [f"{PROBLEM_DIR}/code/solution.py", f"{PROBLEM_DIR}/code/solution_1.py"],
        f"{PROBLEM_DIR}/testcases",
    )
    print(json.dumps(result, ensure_ascii=False, indent=2))


async def example_4_validate_single_test() -> None:
    print("\n" + "=" * 70)
    print("示例4: 调试单个输入")
    print("=" * 70)
    result = await run_code(f"{PROBLEM_DIR}/code/solution.py", "121")
    print(json.dumps(result, ensure_ascii=False, indent=2))


async def example_5_generate_report() -> None:
    result = await compare_problem(PROBLEM_DIR)
    REPORT_FILE.parent.mkdir(exist_ok=True)
    REPORT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n报告已生成: {REPORT_FILE}")


async def main() -> None:
    await example_1_verify_all_problems()
    await example_2_debug_specific_problem()
    await example_3_interactive_comparison()
    await example_4_validate_single_test()
    await example_5_generate_report()


if __name__ == "__main__":
    asyncio.run(main())
