"""
ACMFlow API 服务模块。

基于 FastAPI 的 HTTP 服务，提供 ACM 算法题目生成的 REST API 端点。
主要端点:
  - GET /                   测试页面
  - GET /promblemserve      题目生成（核心接口）
  - GET /oneup              随机毒鸡汤
"""

from __future__ import annotations

import requests
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from .config import PROJECT_ROOT, load_config
from .model_adapter import ChartGPT
from .problem_helper import process_problem

app = FastAPI()
acmer = ChartGPT()
config = load_config()
FRONT_DIR = PROJECT_ROOT / "front"
TEST_PAGE = FRONT_DIR / "test-client.html"


def get_formatted_prompt(user_prompt: str) -> str:
    """组装完整的 Prompt：系统提示 + 格式指令 + 用户需求."""
    try:
        system_prompt = config.get("prompt", "system_prompt")
        format_instruction = config.get("prompt", "format_instruction")
        return f"{system_prompt}\n\n{format_instruction}\n\n用户需求：{user_prompt}"
    except Exception as exc:
        print(f"配置读取失败，使用原始提示词: {exc}")
        return user_prompt


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
    expose_headers=["*"],
    max_age=600,
)

app.mount("/front", StaticFiles(directory=FRONT_DIR), name="front")


@app.get("/")
def get_test_page():
    """返回前端测试页面 (test-client.html)。"""
    return FileResponse(TEST_PAGE)


@app.get("/oneup")
def get_oneup():
    """获取随机毒鸡汤文本。调用外部 API 并原样返回。"""
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "zh-CN,zh;q=0.9",
    }
    try:
        response = requests.get(
            "https://api.fly63.com/api/dujitang/api.php",
            headers=headers,
            timeout=10,
        )
        response.raise_for_status()
        return response.text
    except requests.exceptions.RequestException as exc:
        raise HTTPException(status_code=500, detail=f"请求失败: {exc}") from exc


@app.get("/promblemserve")
def get_problemserve(Prompt: str):
    """
    核心接口：接收自然语言题目描述，调用 LLM 生成完整 ACM 题目包。

    参数:
        Prompt: 用户的自然语言题目需求描述

    返回:
        JSON 包含 save_result（解析和落盘结果）和 status 字段
    """
    try:
        formatted_prompt = get_formatted_prompt(Prompt)
        ai_response = acmer.chat("adminuser", formatted_prompt, "deepseek")
        result = process_problem(ai_response)
        return {
            "save_result": result,
            "status": "success" if result.get("status") == "success" else "partial_success",
        }
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"处理题目时出错: {exc}") from exc


def run() -> None:
    """启动 uvicorn 服务，监听 127.0.0.1:9202。"""
    uvicorn.run(app, host="127.0.0.1", port=9202, log_level="info")
