from __future__ import annotations

import asyncio
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.create_problem_api.pairwise import compare_problem, run_code


PROBLEM_DIR = "problem/normal/回文数判定"
REPORT_FILE = Path("reports/pairwise_report.json")


async def quick_verify() -> None:
    print("\n" + "=" * 70)
    print("快速验证示例")
    print("=" * 70 + "\n")

    result = await compare_problem(PROBLEM_DIR)
    print(f"验证题目: {PROBLEM_DIR}")
    print(f"总测试数: {result['total_tests']}")
    print(f"是否全部通过: {'是' if result['passed'] else '否'}")


async def single_test_debug() -> None:
    print("\n" + "=" * 70)
    print("单个测试调试")
    print("=" * 70 + "\n")

    for test_input in ["121", "1221", "12321"]:
        result = await run_code(f"{PROBLEM_DIR}/code/solution.py", test_input)
        output = result["output"].strip() if result["status"] == "success" else result.get("error", "")
        print(f"{test_input:>6} -> {output}")


async def save_report() -> None:
    result = await compare_problem(PROBLEM_DIR)
    REPORT_FILE.parent.mkdir(exist_ok=True)
    report = {
        "problem": PROBLEM_DIR,
        "workspace": str(Path("").resolve()),
        "total_tests": result["total_tests"],
        "passed": result["passed"],
        "solutions": result.get("solutions", {}),
    }
    REPORT_FILE.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n报告已保存到: {REPORT_FILE}")


async def main() -> None:
    await quick_verify()
    await single_test_debug()
    await save_report()


if __name__ == "__main__":
    asyncio.run(main())
