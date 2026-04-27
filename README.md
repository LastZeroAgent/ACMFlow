# 🎓 CreateProblemAPI - ACM题目生成服务

![Python](https://img.shields.io/badge/Python-3.13+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

一个 **AI驱动的ACM算法题目生成和验证系统**，支持自然语言提示生成完整的算法题目，包含题目描述、解决方案代码（多语言）、测试用例和元数据。

## ✨ 核心特性

- 🤖 **AI题目生成** - 通过星火大模型自然语言生成ACM题目
- 📝 **结构化输出** - 自动解析并保存为标准ACM题目格式
- 🔄 **多语言支持** - 自动生成 Python、C++、Java 三种语言的解决方案
- 🧪 **自动测试用例** - AI自动生成带标准答案的测试用例
- ⚡ **MCP对拍工具** - 验证不同语言的代码产生一致的结果
- 🚀 **REST API服务** - FastAPI 驱动的高性能HTTP接口
- 📊 **题目管理** - 完整的题目库管理和查询系统

## 📋 项目结构

```
CreateProblemAPI/
├── main.py                           # API启动入口
├── Transformat.py                    # MCP对拍工具兼容层
├── config.ini                        # 配置文件（含API密钥）
├── README.md                         # 本文件
│
├── src/create_problem_api/
│   ├── api.py                        # FastAPI应用和路由
│   ├── model_adapter.py              # AI模型适配层（支持星火/DeepSeek）
│   ├── problem_helper.py             # Markdown解析和文件生成
│   ├── config_loader.py              # 配置加载模块
│   └── pairwise.py                   # MCP对拍工具实现
│
├── tests/
│   ├── parser_smoke.py               # 解析器单元测试
│   └── test_pairwise.py              # 对拍工具测试
│
├── scripts/
│   └── pairwise_quick_demo.py        # 对拍工具演示脚本
│
├── problem/normal/                   # 生成的题目库
│   ├── 回文数判定/
│   │   ├── problem.md                # 题目描述
│   │   ├── solution.md               # 解决方案说明
│   │   ├── metadata.json             # 题目元数据
│   │   ├── code/                     # 多语言代码
│   │   │   ├── solution.py
│   │   │   ├── solution.cpp
│   │   │   └── solution.java
│   │   └── testcases/                # 测试用例
│   │       ├── 1.in / 1.out
│   │       ├── 2.in / 2.out
│   │       └── ...
│   └── ...
│
├── docs/
│   ├── HARNESS_ENGINEERING.md        # 架构设计文档
│   └── Lingk.md
│
├── front/
│   └── ProblemHelper.html            # Web前端（可选）
│
├── PAIRWISE_TOOL.md                  # 对拍工具使用指南
└── PAIRWISE_SUMMARY.md               # 对拍工具项目总结
```

## 🚀 快速开始

### 1. 环境要求

- **Python** 3.13+
- **编译器** (可选)
  - C++ 解决方案: `g++` 或 `clang`
  - Java 解决方案: JDK (javac + java)

### 2. 安装

```bash
# 克隆项目
git clone <repository>
cd CreateProblemAPI

# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境
# Windows:
.\.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

# 安装依赖
pip install -r requirements.txt
```

### 3. 配置

编辑 `config.ini` 文件：

```ini
[spark]
api_key = your_xunfei_api_key
base_url = https://spark-api-open.xf-yun.com/v2

[deepseek]
api_key = your_deepseek_api_key
base_url = https://api.deepseek.com

[save_path]
normal = ./problem/normal
```

### 4. 启动服务

```bash
# 启动REST API服务
python main.py

# 服务将在 http://127.0.0.1:7665 启动
```

## 📚 API文档

### 生成题目

**请求**
```http
GET /promblemserve?Prompt=生成一个回文数判定问题
```

**响应**
```json
{
  "success": true,
  "message": "题目生成成功",
  "data": {
    "title": "回文数判定",
    "description": "判断一个整数是否为回文数...",
    "problem_dir": "problem/normal/回文数判定",
    "files": {
      "problem.md": "已生成",
      "solution.md": "已生成",
      "code": ["solution.py", "solution.cpp", "solution.java"],
      "testcases": 10
    }
  }
}
```

### 获取题目列表

```http
GET /list
```

### 获取题目详情

```http
GET /problem/{title}
```

## 🔧 核心使用场景

### 场景1: 生成新题目

```python
import requests

response = requests.get(
    "http://127.0.0.1:7665/promblemserve",
    params={"Prompt": "生成一个寻找两个有序数组的中位数问题"}
)
result = response.json()
print(f"题目: {result['data']['title']}")
print(f"保存路径: {result['data']['problem_dir']}")
```

### 场景2: 验证题目的所有解决方案

```python
import asyncio
from src.create_problem_api.pairwise import compare_problem

async def verify():
    result = await compare_problem("problem/normal/回文数判定")
    print(f"验证结果: {'✓ 通过' if result['passed'] else '✗ 失败'}")
    print(f"总测试数: {result['total_tests']}")
    for sol_name, info in result['solutions'].items():
        print(f"  {sol_name}: {info['success_count']}/{result['total_tests']}")

asyncio.run(verify())
```

### 场景3: 对比特定解决方案

```python
import asyncio
from src.create_problem_api.pairwise import compare_solutions

async def compare():
    result = await compare_solutions(
        [
            "problem/normal/回文数判定/code/solution.py",
            "problem/normal/回文数判定/code/solution.cpp",
        ],
        "problem/normal/回文数判定/testcases"
    )
    print(f"对拍结果: {result['passed']}")

asyncio.run(compare())
```

### 场景4: 调试单个代码文件

```python
import asyncio
from src.create_problem_api.pairwise import run_code

async def debug():
    result = await run_code(
        "problem/normal/回文数判定/code/solution.py",
        test_input="121"
    )
    print(f"输出: {result['output']}")
    print(f"状态: {result['status']}")

asyncio.run(debug())
```

## 🧪 测试

### 运行所有测试

```bash
# 解析器测试
python tests/parser_smoke.py

# 对拍工具测试
python tests/test_pairwise.py
```

### 运行演示

```bash
# 对拍工具演示
python scripts/pairwise_quick_demo.py

# 生成验证报告
python scripts/pairwise_quick_demo.py > report.txt
```

## 🔍 MCP对拍工具指南

### 功能概述

对拍工具用于验证生成题目的多个语言解决方案是否产生一致的输出。

### 主要函数

#### 1. `run_code()` - 运行单个代码

```python
result = await run_code(
    code_file="path/to/solution.py",
    test_input="121",
    timeout=5
)
```

**返回值**
```json
{
  "status": "success|error|compile_error|timeout",
  "output": "程序输出",
  "error": "错误信息",
  "return_code": 0
}
```

#### 2. `compare_solutions()` - 对比多个解决方案

```python
result = await compare_solutions(
    solution_files=[
        "problem/normal/题目/code/solution.py",
        "problem/normal/题目/code/solution.cpp",
    ],
    test_cases_dir="problem/normal/题目/testcases",
    timeout=5
)
```

**返回值**
```json
{
  "total_tests": 10,
  "passed": true,
  "solutions": {...},
  "comparisons": [...]
}
```

#### 3. `compare_problem()` - 对整个题目进行对拍

```python
result = await compare_problem(
    problem_dir="problem/normal/回文数判定",
    timeout=5
)
```

### 支持的语言

| 语言 | 文件扩展 | 要求 |
|------|--------|------|
| Python | `.py` | Python 3.13+ |
| C++ | `.cpp` | g++ / clang |
| Java | `.java` | JDK 8+ |

### 详细文档

- 📖 [对拍工具使用指南](PAIRWISE_TOOL.md)
- 📊 [对拍工具项目总结](PAIRWISE_SUMMARY.md)

## 📊 输出格式规范

生成的题目遵循以下目录结构：

```
problem/normal/<题目名>/
├── problem.md              # 题目描述和输入输出格式
├── solution.md             # 解决方案说明和思路
├── metadata.json           # 题目元数据
├── code/
│   ├── solution.py         # Python解决方案
│   ├── solution.cpp        # C++解决方案
│   ├── solution.java       # Java解决方案
│   ├── solution_1.py       # 备选方案（如有）
│   └── ...
└── testcases/
    ├── 1.in               # 测试用例1输入
    ├── 1.out              # 测试用例1输出
    ├── 2.in
    ├── 2.out
    └── ...
```

### Metadata格式

```json
{
  "title": "回文数判定",
  "difficulty": "Easy|Medium|Hard",
  "category": "Math|String|Array|...",
  "time_limit": 1,
  "memory_limit": 256,
  "test_cases": 10,
  "solutions": {
    "python": "solution.py",
    "cpp": "solution.cpp",
    "java": "solution.java"
  }
}
```

## 🔐 安全性

⚠️ **重要提示**

- `config.ini` 包含 API 密钥，**不要提交到版本控制**
- 添加到 `.gitignore`:
  ```
  config.ini
  .venv/
  __pycache__/
  *.pyc
  problem/normal/  # 可选
  ```

## 📈 性能优化

### 对拍工具性能建议

1. **编译缓存** - C++ 编译较慢，可以缓存编译结果
2. **并发执行** - 使用 `asyncio.gather()` 并发对拍多个题目
3. **超时配置** - 为复杂算法设置更长的超时时间

```python
# 并发对拍多个题目
results = await asyncio.gather(
    compare_problem("problem/normal/题目1"),
    compare_problem("problem/normal/题目2"),
    compare_problem("problem/normal/题目3"),
)
```

## 🛠️ 开发

### 项目架构

```
用户请求
    ↓
FastAPI app (api.py)
    ↓
Model Adapter (model_adapter.py)
    ├─→ 星火大模型 API
    └─→ DeepSeek API
    ↓
Problem Parser (problem_helper.py)
    ├─→ Markdown 解析
    ├─→ 代码提取
    └─→ 文件生成
    ↓
本地文件系统
```

### 添加新模型支持

编辑 `src/create_problem_api/model_adapter.py`:

```python
class YourModelAdapter(ModelBase):
    def __init__(self, api_key, base_url, model_name):
        super().__init__(api_key, base_url)
        self.model_name = model_name
    
    async def chat(self, prompt):
        # 实现your_model API 调用
        pass
```

### 修改Markdown解析规则

编辑 `src/create_problem_api/problem_helper.py` 的解析正则表达式。

## 📝 常见问题

### Q: 如何修改生成的题目？

A: 直接编辑 `problem/normal/<题目名>/` 目录下的相应文件。

### Q: 如何添加新的测试用例？

A: 在 `problem/normal/<题目名>/testcases/` 目录下添加 `N.in` 和 `N.out` 文件。

### Q: 对拍工具显示超时怎么办？

A: 增加 `timeout` 参数或检查代码是否存在无限循环：

```python
result = await compare_problem(
    "problem/normal/题目",
    timeout=10  # 增加超时时间
)
```

### Q: 支持哪些AI模型？

A: 目前支持：
- ✅ 星火大模型 (Xunfei Spark)
- ✅ DeepSeek
- 可扩展支持其他模型

## 📚 相关文档

- [架构设计文档](docs/HARNESS_ENGINEERING.md)
- [对拍工具使用指南](PAIRWISE_TOOL.md)
- [对拍工具项目总结](PAIRWISE_SUMMARY.md)
- [CLAUDE.md - 开发指南](CLAUDE.md)
- [AGENTS.md - Agent工作指南](AGENTS.md)

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📄 许可证

MIT License

## 👨‍💻 联系方式

有问题或建议？欢迎提交Issue或联系开发者。

---

**最后更新**: 2026-04-27  
**版本**: 1.0.0  
**状态**: ✅ 生产就绪

---

## 快速命令参考

```bash
# 安装依赖
pip install -r requirements.txt

# 启动服务
python main.py

# 运行测试
python tests/test_pairwise.py

# 生成题目（REST API）
curl "http://127.0.0.1:7665/promblemserve?Prompt=生成一个排序问题"

# 验证题目
python scripts/pairwise_quick_demo.py

# 启动MCP服务
python Transformat.py
```

---

**Made with ❤️ for Algorithm Education**
