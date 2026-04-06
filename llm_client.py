"""
LLM 客户端封装
统一管理大模型调用
"""

import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class LLMClient:
    """大模型调用客户端"""

    def __init__(self, skill_path: str = None):
        self.model = os.getenv("MODEL_NAME", "gpt-4o-mini")
        self.client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
            base_url=os.getenv("OPENAI_BASE_URL"),
        )


    def chat(self, messages: list, temperature: float = 0.7) -> str:
        """
        发送对话请求
        
        Args:
            messages: 对话历史，格式为 [{"role": "user/assistant/system", "content": "..."}]
            temperature: 温度参数，越高越随机（0~2）
            
        Returns:
            模型回复的文本内容
        """
        full_messages = []
        full_messages.extend(messages)

        response = self._create_openai_chat_completion(full_messages, temperature)

        if response is None:
            raise RuntimeError("模型请求失败：未拿到有效响应（response 为 None）。")

        if not getattr(response, "choices", None):
            raise RuntimeError("模型请求失败：响应中不存在 choices 字段或为空。")

        content = response.choices[0].message.content
        return content if content is not None else ""

    def _create_openai_chat_completion(self, messages: list, temperature: float):
        """创建 OpenAI 兼容聊天请求；若模型仅允许温度=1，则自动回退重试。"""
        try:
            return self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
            )
        except Exception as e:
            err_text = str(e).lower()
            if "invalid temperature" in err_text and "only 1 is allowed" in err_text:
                return self.client.chat.completions.create(
                    model=self.model,
                    messages=messages,
                    temperature=1,
                )
            raise RuntimeError(f"模型请求异常：{e}") from e


# python -m pydoc llm_client
# 使用示例
if __name__ == "__main__":
    client = LLMClient()
    
    messages = [
        {"role": "system", "content": "你是一个有帮助的助手。"},
        {"role": "user", "content": "你好"},
    ]
    
    reply = client.chat(messages)
    print(f"模型回复：{reply}")
