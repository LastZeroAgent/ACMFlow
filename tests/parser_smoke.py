from __future__ import annotations

import re
from typing import Any
from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


class ACMProblemParser:
    def __init__(self, md_content: str):
        self.md_content = md_content
        self.parsed_data: dict[str, Any] = {}

    def parse(self) -> dict[str, Any]:
        self._parse_title()
        self._parse_problem_description()
        self._parse_input_format()
        self._parse_output_format()
        self._parse_samples()
        self._parse_hints()
        self._parse_solution_idea()
        self._parse_code()
        self._parse_test_cases()
        return self.parsed_data

    def _parse_title(self) -> None:
        title_match = re.search(r"# ACM 算法题目：(.*)", self.md_content)
        if title_match:
            self.parsed_data["title"] = title_match.group(1)

    def _parse_problem_description(self) -> None:
        desc_match = re.search(r"\[详细的题目描述\]\n(.+?)\n\n##", self.md_content, re.DOTALL)
        if desc_match:
            self.parsed_data["problem_description"] = desc_match.group(1).strip()

    def _parse_input_format(self) -> None:
        input_match = re.search(r"\[输入数据的格式说明\]\n(.+?)\n\n##", self.md_content, re.DOTALL)
        if input_match:
            self.parsed_data["input_format"] = input_match.group(1).strip()

    def _parse_output_format(self) -> None:
        output_match = re.search(r"\[输出数据的格式说明\]\n(.+?)\n\n\|", self.md_content, re.DOTALL)
        if output_match:
            self.parsed_data["output_format"] = output_match.group(1).strip()

    def _parse_samples(self) -> None:
        samples_match = re.search(
            r"\| 样例编号 \| 输入 \| 输出 \|\n\|(.+?)\n\n##", self.md_content, re.DOTALL
        )
        if not samples_match:
            return
        sample_lines = samples_match.group(1).strip().split("\n")
        samples = []
        for line in sample_lines:
            parts = line.split("|")
            if len(parts) >= 4:
                samples.append(
                    {"id": parts[1].strip(), "input": parts[2].strip(), "output": parts[3].strip()}
                )
        self.parsed_data["samples"] = samples

    def _parse_hints(self) -> None:
        hints_match = re.search(r"\[解题提示或注意事项\]\n(.+?)\n\n---", self.md_content, re.DOTALL)
        if hints_match:
            self.parsed_data["hints"] = hints_match.group(1).strip()

    def _parse_solution_idea(self) -> None:
        idea_match = re.search(r"\[详细的解题思路分析\]\n(.+?)\n\n```", self.md_content, re.DOTALL)
        if idea_match:
            self.parsed_data["solution_idea"] = idea_match.group(1).strip()

    def _parse_code(self) -> None:
        codes = {}
        for match in re.finditer(r"```(\w+)\n(.+?)\n```", self.md_content, re.DOTALL):
            codes[match.group(1)] = match.group(2).strip()
        self.parsed_data["codes"] = codes

    def _parse_test_cases(self) -> None:
        test_cases_match = re.search(r"\[测试数据的说明和验证\]\n(.+?)\n---", self.md_content, re.DOTALL)
        if not test_cases_match:
            return
        test_cases = []
        test_cases_part = test_cases_match.group(1).strip()
        for match in re.finditer(
            r"case(\d+)\.in\n```\n(.+?)\n```\ncase\1\.out\n```\n(.+?)\n```",
            test_cases_part,
            re.DOTALL,
        ):
            test_cases.append(
                {"id": match.group(1), "input": match.group(2).strip(), "output": match.group(3).strip()}
            )
        self.parsed_data["test_cases"] = test_cases


def main() -> None:
    md_content = """# ACM 算法题目：素数计数器
[详细的题目描述]
给定两个整数 a 和 b，请统计闭区间 [a, b] 内素数的个数。

## [输入数据的格式说明]
输入包含一行，两个整数 a 和 b。

## [输出数据的格式说明]
输出一个整数。

| 样例编号 | 输入 | 输出 |
|----------|------|------|
| 1 | 2 10 | 4 |

[解题提示或注意事项]
注意边界处理。

---

[详细的解题思路分析]
遍历并判断素数。

```python
print(4)
```

[测试数据的说明和验证]
**case1.in**
```
2 10
```
**case1.out**
```
4
```
---
"""
    parser = ACMProblemParser(md_content)
    data = parser.parse()
    print("题目标题:", data.get("title"))
    print("题目描述:", data.get("problem_description"))
    print("样例数量:", len(data.get("samples", [])))
    print("测试用例数量:", len(data.get("test_cases", [])))


if __name__ == "__main__":
    main()
