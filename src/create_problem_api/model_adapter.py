from __future__ import annotations

import logging

from openai import OpenAI

from .config import load_config


logger = logging.getLogger(__name__)


class ModelBase:
    """Base class for model adapters."""

    def __init__(self, api_key: str | None = None, base_url: str | None = None):
        self.api_key = api_key
        self.base_url = base_url
        self.client: OpenAI | None = None
        self._initialize_client()

    def _initialize_client(self) -> None:
        if self.api_key and self.base_url:
            self.client = OpenAI(api_key=self.api_key, base_url=self.base_url)
            return
        raise ValueError("API 密钥和基础 URL 不能为空")

    def chat(self, user_id: str, message: str) -> str:
        raise NotImplementedError


class SparkModel(ModelBase):
    """Xunfei Spark adapter via the OpenAI-compatible client."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        stream: bool = False,
    ):
        if api_key is None or base_url is None:
            config = load_config()
            if config.has_section("spark"):
                api_key = api_key or config.get("spark", "api_key", fallback=None)
                base_url = base_url or config.get("spark", "base_url", fallback=None)
            else:
                logger.warning("配置文件缺少 [spark] 段")

        super().__init__(api_key, base_url)
        self.model_name = "x1"
        self.stream_enabled = stream
        self.full_response = ""

    def chat(self, user_id: str, message: str) -> str:
        if not self.client:
            logger.error("模型客户端尚未初始化")
            return "服务未初始化，请稍后再试"

        try:
            self.full_response = ""
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": message}],
                model=self.model_name,
                stream=self.stream_enabled,
                user=user_id,
            )

            if not self.stream_enabled:
                return response.choices[0].message.content or ""

            for chunk in response:
                delta = chunk.choices[0].delta
                if getattr(delta, "content", None):
                    self.full_response += delta.content
            return self.full_response
        except Exception as exc:
            logger.error("模型调用出错: %s", exc)
            return f"模型调用出错: {exc}"


class DeepSeekModel(ModelBase):
    """DeepSeek adapter via the OpenAI-compatible client."""

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        model: str | None = None,
        stream: bool = False,
    ):
        if api_key is None or base_url is None:
            config = load_config()
            if config.has_section("deepseek"):
                api_key = api_key or config.get("deepseek", "api_key", fallback=None)
                base_url = base_url or config.get("deepseek", "base_url", fallback=None)
                model = model or config.get("deepseek", "model", fallback="deepseek-chat")
                stream = stream or config.getboolean("deepseek", "stream", fallback=False)
            else:
                logger.warning("配置文件缺少 [deepseek] 段")

        super().__init__(api_key, base_url)
        self.model_name = model or "deepseek-chat"
        self.stream_enabled = stream
        self.full_response = ""

    def chat(self, user_id: str, message: str) -> str:
        if not self.client:
            logger.error("模型客户端尚未初始化")
            return "服务未初始化，请稍后再试"

        try:
            self.full_response = ""
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": message}],
                model=self.model_name,
                stream=self.stream_enabled,
                user=user_id,
            )

            if not self.stream_enabled:
                return response.choices[0].message.content or ""

            for chunk in response:
                delta = chunk.choices[0].delta
                if getattr(delta, "content", None):
                    self.full_response += delta.content
            return self.full_response
        except Exception as exc:
            logger.error("模型调用出错: %s", exc)
            return f"模型调用出错: {exc}"


class ChartGPT:
    """Facade used by the API layer."""

    def __init__(self, default_model: str | None = None):
        self.models: dict[str, ModelBase] = {}
        self.default_model = default_model or "spark"
        self.register_model("spark", SparkModel())
        self.register_model("deepseek", DeepSeekModel())

    def register_model(self, model_name: str, model_instance: ModelBase) -> None:
        if not isinstance(model_instance, ModelBase):
            raise TypeError("模型必须继承自 ModelBase")
        self.models[model_name] = model_instance

    def chat(self, user_id: str, message: str, model_name: str | None = None) -> str:
        model = self.models.get(model_name or self.default_model)
        if not model:
            logger.error("模型 %s 不存在", model_name)
            return f"模型 {model_name} 不存在，请使用有效的模型"
        return model.chat(user_id, message)

    def SparkChat(self, usr_id: str, msg: str) -> str:
        return self.chat(usr_id, msg, "spark")
