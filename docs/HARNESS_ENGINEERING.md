# Harness Engineering

## 目标

这个仓库现在按职责拆成四层，避免主程序、测试脚本、演示脚本和说明文档继续混在根目录：

- `src/create_problem_api/`：生产代码
- `tests/`：本地测试与 smoke harness
- `scripts/`：演示、批量执行、报告生成脚本
- `docs/`：工程说明与工具文档

## 当前边界

### 生产代码

- `src/create_problem_api/api.py`：FastAPI 入口与 `/promblemserve`
- `src/create_problem_api/model_adapter.py`：模型适配层
- `src/create_problem_api/problem_helper.py`：题目解析与落盘
- `src/create_problem_api/pairwise.py`：对拍/运行工具与 MCP server
- `src/create_problem_api/config.py`：配置读取

### 测试与验证

- `tests/parser_smoke.py`：解析器 smoke test
- `tests/test_pairwise.py`：对拍工具 smoke test

### 脚本

- `scripts/pairwise_quick_demo.py`：快速演示
- `scripts/pairwise_examples.py`：批量/详细示例
- `reports/`：脚本生成的报告输出目录

## 根目录保留原则

根目录只保留一个 Python 入口和项目级文件：

- `main.py`：兼容旧启动命令
- `config.ini`：项目配置

新的实现不要再直接堆回根目录。

## 约束

1. 新的业务逻辑默认进入 `src/create_problem_api/`
2. 新的测试默认进入 `tests/`
3. 临时脚本如果会复用，进入 `scripts/`；一次性草稿不要长期留在根目录
4. 文档更新时，同步改 `AGENTS.md` 和这里的结构说明
5. `problem/normal/` 仍然视为用户数据区，不做批量重写

## 常用命令

```bash
python main.py
python tests/parser_smoke.py
python tests/test_pairwise.py
python scripts/pairwise_quick_demo.py
python scripts/pairwise_examples.py
```
