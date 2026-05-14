"""
题目解析与持久化模块。

负责将 LLM 返回的 Markdown 响应解析为结构化的题目包，包含:
  - 题目描述 (problem.md)
  - 题解说明 (solution.md)
  - 多语言参考代码 (code/)
  - 测试用例 (testcases/)
  - 元数据 (metadata.json)

解析采用多模式正则策略，按优先级尝试多种 Markdown 格式，兼容不同 LLM 的输出习惯。
"""

from __future__ import annotations

import json
import logging
import re
from datetime import datetime
from pathlib import Path

from .config import PROJECT_ROOT, load_config

logger = logging.getLogger(__name__)


class ProblemHelper:
    """Parse the model markdown response and persist a problem bundle."""

    def __init__(self):
        self.problemId = ""
        self.description = ""
        self.input = ""
        self.output = ""
        self.timeLimit = 1000
        self.memoryLimit = 256
        self.stackLimit = 128
        self.difficulty = 0
        self.auth = 1
        self.codeShare = True
        self.examples = []
        self.spjLanguage = ""
        self.spjCode = ""
        self.spjCompileOk = False
        self.uploadTestcaseDir = ""
        self.testCaseScore = []
        self.isRemote = False
        self.isUploadCase = True
        self.type = 0
        self.hint = ""
        self.source = ""
        self.cid = "null"
        self.isRemoveEndBlank = False
        self.openCaseResult = True
        self.judgeMode = "default"
        self.judgeCaseMode = "default"
        self.userExtraFile = ""
        self.judgeExtraFile = ""
        self.isFileIO = False
        self.ioReadFileName = "null"
        self.ioWriteFileName = "null"

        config = load_config()
        self.problem_dir = Path(
            config.get("save_path", "normal", fallback=str(PROJECT_ROOT / "problem" / "normal"))
        )
        self.problem_dir.mkdir(parents=True, exist_ok=True)

    def format_and_save_problem(self, ai_response: str) -> dict:
        """
        主入口：解析 LLM 返回的 Markdown 并落盘为完整题目包。

        依次提取标题、题目描述、测试用例、题解、代码文件和元数据，
        写入 problem/normal/<title>/ 目录结构。

        参数:
            ai_response: LLM 返回的原始 Markdown 文本

        返回:
            dict 包含 status / title / path / testcase_count / code_file_count 等
        """
        try:
            title = self._extract_title(ai_response)
            if not title:
                raise ValueError("无法提取题目名称")

            problem_folder = self.problem_dir / self._sanitize_filename(title)
            problem_folder.mkdir(exist_ok=True)

            testcases_dir = problem_folder / "testcases"
            testcases_dir.mkdir(exist_ok=True)

            self._save_problem_description(problem_folder, ai_response, title)
            testcase_count = self._save_testcases(testcases_dir, ai_response)
            self._save_solution(problem_folder, ai_response, title)
            code_count = self._save_code_files(problem_folder, ai_response)
            self._save_metadata(problem_folder, title, testcase_count)

            logger.info("题目 '%s' 保存成功，路径 %s", title, problem_folder)
            return {
                "status": "success",
                "message": f"题目 '{title}' 保存成功",
                "path": str(problem_folder),
                "title": title,
                "testcase_count": testcase_count,
                "code_file_count": code_count,
                "description": self.description,
                "problemId": self.problemId,
                "input": self.input,
                "output": self.output,
                "timeLimit": self.timeLimit,
                "memoryLimit": self.memoryLimit,
                "stackLimit": self.stackLimit,
                "difficulty": self.difficulty,
                "auth": self.difficulty,
                "codeShare": self.codeShare,
                "examples": self.examples,
                "spjLanguage": self.spjLanguage,
                "spjCode": self.spjCode,
                "spjCompileOk": self.spjCompileOk,
                "uploadTestcaseDir": self.uploadTestcaseDir,
                "testCaseScore": self.testCaseScore,
                "isRemote": self.isRemote,
                "isUploadCase": self.isUploadCase,
                "type": self.type,
                "hint": self.hint,
                "source": self.source,
                "cid": self.cid,
                "isRemoveEndBlank": self.isRemoveEndBlank,
                "openCaseResult": self.openCaseResult,
                "judgeMode": self.judgeMode,
                "judgeCaseMode": self.judgeCaseMode,
                "userExtraFile": self.userExtraFile,
                "judgeExtraFile": self.judgeExtraFile,
                "isFileIO": self.isFileIO,
                "ioReadFileName": self.ioReadFileName,
                "ioWriteFileName": self.ioWriteFileName,
            }
        except Exception as exc:
            logger.error("处理题目时出错: %s", exc)
            return {"status": "error", "message": f"处理题目时出错: {exc}"}

    def _extract_title(self, content: str) -> str:
        """按多优先级正则匹配提取题目标题，失败返回 '未知题目'。"""
        patterns = [
            r"# (.*?)\n",
            r"题目文件[：:]\s*`(.*?)\.md`",
            r"## 题目描述\n(.*?)\n",
            r"```markdown\n# (.*?)\n",
        ]
        for pattern in patterns:
            match = re.search(pattern, content)
            if match:
                title = match.group(1).strip()
                title = self._clean_title(title)
                if title and title not in ("题目名称", "题目标题"):
                    return title
        return "未知题目"

    @staticmethod
    def _clean_title(title: str) -> str:
        """Remove markdown artifacts and placeholder boilerplate from a title."""
        title = re.sub(r"[：:]", "-", title)
        title = re.sub(r"[`*_#]", "", title)
        title = re.sub(r"题目文件\s*", "", title)
        title = re.sub(r"\.md\s*", "", title)
        return title.strip()

    @staticmethod
    def _clean_br(text: str) -> str:
        """Replace HTML <br> tags with actual newlines."""
        return re.sub(r"<br\s*/?>", "\n", text, flags=re.IGNORECASE)

    @staticmethod
    def _sanitize_filename(filename: str) -> str:
        filename = re.sub(r'[<>:"/\\|?*`]', "_", filename).strip()
        filename = re.sub(r'\s+', " ", filename)
        return filename or "untitled_problem"

    def _save_problem_description(self, problem_folder: Path, content: str, title: str) -> None:
        """提取题目正文并写入 problem.md。"""
        problem_content = self._extract_problem_content(content, title)
        formatted_content = self._format_acm_problem(problem_content, title)
        (problem_folder / "problem.md").write_text(formatted_content, encoding="utf-8")

    def _extract_problem_content(self, content: str, title: str) -> str:
        markdown_match = re.search(r"```markdown\n(.*?)\n```", content, re.DOTALL)
        if markdown_match:
            return markdown_match.group(1)

        title_match = re.search(
            rf"# {re.escape(title)}(.*?)(?=\n---|\n### 测试数据|$)",
            content,
            re.DOTALL,
        )
        if title_match:
            return f"# {title}{title_match.group(1)}"

        return content

    def _format_acm_problem(self, content: str, title: str) -> str:
        formatted = f"# {title}\n## 题目描述\n"

        description = self._extract_problem_description(content)
        formatted += description + "\n\n"
        self.description = description

        input_format = self._extract_input_format(content)
        formatted += "## 输入格式\n" + input_format + "\n\n"
        self.input = input_format

        output_format = self._extract_output_format(content)
        formatted += "## 输出格式\n" + output_format + "\n\n"
        self.output = output_format

        examples = self._extract_examples(content)
        self.examples = examples
        if examples:
            formatted += "## 样例\n\n"
            for index, (input_data, output_data) in enumerate(examples[:2], 1):
                formatted += f"### 样例 {index}\n\n"
                formatted += f"**输入：**\n```\n{input_data.strip()}\n```\n\n"
                formatted += f"**输出：**\n```\n{output_data.strip()}\n```\n\n"

        formatted += "## 数据范围\n"
        formatted += self._extract_data_range(content) + "\n"
        return formatted

    def _extract_problem_description(self, content: str) -> str:
        patterns = [
            r"## \[详细的题目描述\]\n(.*?)(?=\n##|\n\[|$)",
            r"\[详细的题目描述\]\n(.*?)(?=\n\[|$)",
            r"## 题目描述\n(.*?)(?=\n##|$)",
            r"# .*?\n\n(.*?)(?=\n##|\n\[|$)",
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                description = match.group(1).strip()
                if description:
                    return description
        return "题目描述待补充"

    def _extract_input_format(self, content: str) -> str:
        patterns = [
            r"## \[输入数据的格式说明\]\n(.*?)(?=\n##|\n\[|$)",
            r"\[输入数据的格式说明\]\n(.*?)(?=\n\[|$)",
            r"### 输入格式\n(.*?)(?=\n###|\n##|$)",
            r"## 输入格式\n(.*?)(?=\n##|$)",
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(1).strip()
        return "输入格式待补充"

    def _extract_output_format(self, content: str) -> str:
        patterns = [
            r"## \[输出数据的格式说明\]\n(.*?)(?=\n##|\n\[|\n\||$)",
            r"\[输出数据的格式说明\]\n(.*?)(?=\n\[|\n\||$)",
            r"### 输出格式\n(.*?)(?=\n###|\n##|$)",
            r"## 输出格式\n(.*?)(?=\n##|$)",
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                return match.group(1).strip()
        return "输出格式待补充"

    def _extract_data_range(self, content: str) -> str:
        patterns = [
            r"## \[解题提示或注意事项\]\n(.*?)(?=\n##|\n\[|$)",
            r"\[解题提示或注意事项\]\n(.*?)(?=\n\[|$)",
            r"## 数据范围\n(.*?)(?=\n##|$)",
            r"（(.*?)）",
            r"(\d+ .*? \d+)",
        ]
        for pattern in patterns:
            match = re.search(pattern, content, re.DOTALL)
            if match:
                range_text = match.group(1).strip()
                if range_text:
                    if pattern == r"（(.*?)）":
                        return f"- 时间限制：1 秒\n- 内存限制：256MB\n- {range_text}"
                    return range_text
        return "- 时间限制：1 秒\n- 内存限制：256MB"

    def _extract_examples(self, content: str) -> list[tuple[str, str]]:
        examples: list[tuple[str, str]] = []

        table_match = re.search(
            r"\| 样例编号 \| 输入.*?\| 输出 \|(.*?)(?=\n\[|\n```|$)",
            content,
            re.DOTALL,
        )
        if table_match:
            lines = table_match.group(0).strip().split("\n")
            for line in lines[2:]:
                if "|" not in line:
                    continue
                parts = [part.strip() for part in line.split("|")[1:-1]]
                if len(parts) >= 3:
                    examples.append((parts[1], parts[2]))

        if not examples:
            input_pattern = r"#### 输入 \d+\n(.*?)\n\n#### 输出 \d+\n(.*?)(?=\n\n|\n####|$)"
            for input_data, output_data in re.findall(input_pattern, content, re.DOTALL):
                examples.append((input_data.strip(), output_data.strip()))

        if not examples:
            example_match = re.search(
                r"### 样例输入\n(.*?)### 样例输出\n(.*?)(?=\n###|\n##|$)",
                content,
                re.DOTALL,
            )
            if example_match:
                examples.append((example_match.group(1).strip(), example_match.group(2).strip()))

        return [(self._clean_br(inp), self._clean_br(out)) for inp, out in examples]

    def _save_testcases(self, testcases_dir: Path, content: str) -> int:
        """解析并保存测试用例到 *.in /*.out 文件，返回用例数量。"""
        test_cases = self._extract_test_cases(content)
        for index, (input_data, output_data) in enumerate(test_cases, 1):
            input_text = self._clean_br(input_data.replace("\\n", "\n"))
            output_text = self._clean_br(output_data)
            (testcases_dir / f"{index}.in").write_text(input_text.strip(), encoding="utf-8")
            (testcases_dir / f"{index}.out").write_text(output_text.strip(), encoding="utf-8")
        logger.info("已保存 %d 组测试用例", len(test_cases))
        return len(test_cases)

    def _extract_test_cases(self, content: str) -> list[tuple[str, str]]:
        """
        多策略提取测试用例。

        优先级从高到低尝试 6 种正则模式，适配不同 LLM 的输出风格，
        包括粗体标记、编号标题、纯围栏代码块、表格和文件列表。
        """
        test_cases: list[tuple[str, str]] = []

        # Pattern 1: Bold caseN.in / caseN.out blocks
        case_pattern = (
            r"\*\*case(\d+)\.in\*\*\s*\n```\n(.*?)\n```"
            r"\s*\n+\s*\*\*case\1\.out\*\*\s*\n```\n(.*?)\n```"
        )
        for _, input_data, output_data in re.findall(case_pattern, content, re.DOTALL):
            test_cases.append((input_data.strip(), output_data.strip()))

        # Pattern 2: Numbered case headers (case 1: / case1:)
        if not test_cases:
            case_header_pattern = (
                r"(?:####|###|\*\*)\s*[Cc]ase\s*(\d+)\s*(?:\.in)?\s*(?:####|\*\*)?\s*\n"
                r"```\n(.*?)\n```\s*\n+"
                r"(?:####|###|\*\*)\s*[Cc]ase\s*\1\s*(?:\.out)?\s*(?:####|\*\*)?\s*\n"
                r"```\n(.*?)\n```"
            )
            for _, input_data, output_data in re.findall(case_header_pattern, content, re.DOTALL):
                test_cases.append((input_data.strip(), output_data.strip()))

        # Pattern 3: Plain-fenced caseN blocks (no bold marker)
        if not test_cases:
            plain_case_pattern = (
                r"case(\d+)\.in\s*\n```\n(.*?)\n```\s*\n+"
                r"(?:\*\*)?case\1\.out(?:\*\*)?\s*\n```\n(.*?)\n```"
            )
            for _, input_data, output_data in re.findall(plain_case_pattern, content, re.DOTALL):
                test_cases.append((input_data.strip(), output_data.strip()))

        # Pattern 4: Table-based extraction (样例编号 table)
        table_match = re.search(
            r"\| 样例编号 \| 输入.*?\| 输出 \|(.*?)(?=\n\[|\n```|$)",
            content,
            re.DOTALL,
        )
        if table_match:
            lines = table_match.group(0).strip().split("\n")
            for line in lines[2:]:
                if "|" in line and line.count("|") >= 4:
                    parts = [part.strip() for part in line.split("|")[1:-1]]
                    if len(parts) >= 3:
                        inp = self._clean_br(parts[1].replace("\\n", "\n"))
                        out = self._clean_br(parts[2].replace("\\n", "\n"))
                        test_cases.append((inp, out))

        # Pattern 5: File listing table (| `case1.in` | `...` | `...` |)
        if not test_cases:
            file_pattern = (
                r"\| `case(\d+)\.in`\s*\|\s*`([^`]*)`\s*\|\s*`([^`]*)`\s*\|"
            )
            for _, input_data, output_data in re.findall(file_pattern, content):
                test_cases.append((input_data.replace("\\n", "\n"), output_data))

        # Pattern 6: "#### 输入 N" / "#### 输出 N" format in solution section
        if not test_cases:
            alt_pattern = (
                r"####\s*输入\s*(\d+)\s*\n(.*?)\n\n####\s*输出\s*\1\s*\n(.*?)(?=\n\n|\n####|$)"
            )
            for _, input_data, output_data in re.findall(alt_pattern, content, re.DOTALL):
                test_cases.append((input_data.strip(), output_data.strip()))

        return test_cases

    def _save_solution(self, problem_folder: Path, content: str, title: str) -> None:
        """提取题解内容并写入 solution.md。"""
        solution_content = self._extract_solution_content(content)
        if solution_content:
            formatted_solution = self._format_solution(solution_content, title)
            (problem_folder / "solution.md").write_text(formatted_solution, encoding="utf-8")

    def _extract_solution_content(self, content: str) -> str | None:
        # Priority 1: Extract from ```markdown block inside 题解 file section
        sol_md_match = re.search(
            r"###\s*题解文件.*?\n```markdown\n(.*?)\n```",
            content, re.DOTALL,
        )
        target = sol_md_match.group(1) if sol_md_match else content

        # Pattern 1: Standard format with 解题思路 heading
        pattern = r"##\s*解题思路\n(.*?)(?=\n##\s*多语言实现|\n###\s|\n```\w|\n---\n|$)"
        match = re.search(pattern, target, re.DOTALL)
        if match:
            solution = match.group(1).strip()
            if solution and len(solution) > 30:
                return solution

        # Pattern 2: Legacy bracket markers
        pattern = (
            r"\[解题提示或注意事项\]\n(.*?)\n---\n\n\[详细的解题思路分析\]\n(.*?)(?=\n\[|$)"
        )
        match = re.search(pattern, content, re.DOTALL)
        if match:
            tips = match.group(1).strip()
            solution = match.group(2).strip()
            return f"## 解题提示\n{tips}\n\n## 解题思路\n{solution}".strip()

        # Pattern 3: Simple heading-based extraction from full content
        for pat in [
            r"\[详细的解题思路分析\]\n(.*?)(?=\n\[|$)",
            r"### 题解\n(.*?)$",
            r"## 题解\n(.*?)$",
            r"#### 解题思路\n(.*?)$",
        ]:
            match = re.search(pat, content, re.DOTALL)
            if match:
                text = match.group(1).strip()
                if text and len(text) > 20:
                    return text

        # Pattern 4: Grab everything between 题解 heading and next top-level section
        match = re.search(
            r"(?:###|##)\s*题解.*?\n(.*?)(?=\n---\n|\n### 测试数据|$)",
            content, re.DOTALL,
        )
        if match:
            text = match.group(1).strip()
            if text and len(text) > 20:
                return text

        return None

    def _format_solution(self, solution_content: str, title: str) -> str:
        return f"""# {title} - 题解

## 算法分析

{solution_content}

## 相关知识点
- 算法设计与分析
- 时间复杂度优化
- 数据结构应用

## 扩展思考
1. 是否存在更优的算法？
2. 在不同数据规模下的表现如何？
3. 相关的变形题目有哪些？

---
*生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""

    def _save_metadata(self, problem_folder: Path, title: str, testcase_count: int = 0) -> None:
        """生成并写入 metadata.json。"""
        metadata = {
            "title": title,
            "created_at": datetime.now().isoformat(),
            "difficulty": "简单",
            "tags": ["算法基础"],
            "time_limit": "1s",
            "memory_limit": "256MB",
            "source": "AI生成",
            "testcase_count": testcase_count,
        }
        (problem_folder / "metadata.json").write_text(
            json.dumps(metadata, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def _save_code_files(self, problem_folder: Path, content: str) -> int:
        """解析多语言代码块并写入 code/ 目录，返回保存的代码文件数。"""
        code_dir = problem_folder / "code"
        code_dir.mkdir(exist_ok=True)

        code_blocks = self._extract_code_blocks(content)
        solution_code_blocks = self._extract_solution_code_blocks(content)
        if solution_code_blocks:
            code_blocks.extend(solution_code_blocks)

        for language, code in code_blocks:
            extension = self._get_file_extension(language)
            filename = f"solution.{extension}"

            counter = 1
            original_filename = filename
            while (code_dir / filename).exists():
                name, ext = original_filename.rsplit(".", 1)
                filename = f"{name}_{counter}.{ext}"
                counter += 1

            (code_dir / filename).write_text(code, encoding="utf-8")
            logger.info("保存代码文件: %s", filename)

        return len(code_blocks)

    def _extract_code_blocks(self, content: str) -> list[tuple[str, str]]:
        """从 Markdown 中提取所有受支持语言的围栏代码块。"""
        code_blocks: list[tuple[str, str]] = []
        code_pattern = r"```(\w+)\n(.*?)\n```"
        for language, code in re.findall(code_pattern, content, re.DOTALL):
            if language.lower() in {
                "cpp",
                "c++",
                "python",
                "py",
                "java",
                "javascript",
                "js",
                "c",
                "go",
                "rust",
                "php",
                "ruby",
                "swift",
                "kotlin",
            }:
                cleaned_code = code.strip()
                if cleaned_code:
                    code_blocks.append((language.lower(), cleaned_code))
        return code_blocks

    def _extract_solution_code_blocks(self, content: str) -> list[tuple[str, str]]:
        """从题解区域单独提取代码块，补充主代码块列表。"""
        code_blocks: list[tuple[str, str]] = []
        solution_match = re.search(r"\[详细的解题思路分析\]\n(.*?)(?=\n\[|$)", content, re.DOTALL)
        if not solution_match:
            return code_blocks

        solution_content = solution_match.group(1)
        for language, code in re.findall(r"```(\w+)\n(.*?)\n```", solution_content, re.DOTALL):
            if language.lower() in {
                "cpp",
                "c++",
                "python",
                "py",
                "java",
                "javascript",
                "js",
                "c",
                "go",
                "rust",
                "php",
                "ruby",
                "swift",
                "kotlin",
            }:
                cleaned_code = code.strip()
                if cleaned_code:
                    code_blocks.append((language.lower(), cleaned_code))
        return code_blocks

    def _get_file_extension(self, language: str) -> str:
        extension_map = {
            "cpp": "cpp",
            "c++": "cpp",
            "python": "py",
            "py": "py",
            "java": "java",
            "javascript": "js",
            "js": "js",
            "c": "c",
            "go": "go",
            "rust": "rs",
            "php": "php",
            "ruby": "rb",
            "swift": "swift",
            "kotlin": "kt",
        }
        return extension_map.get(language.lower(), "txt")


def process_problem(ai_response: str) -> dict:
    """便捷函数：一行调用完成解析和保存。"""
    return ProblemHelper().format_and_save_problem(ai_response)
