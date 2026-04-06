"""
ReAct Agent 核心实现
思路：Thought（思考）→ Action（行动）→ Observation（观察）→ 循环直到完成任务
"""

from llm_client import LLMClient
from memory import ConversationMemory
from tools import ListTopicsTool, SearchNoteTool, ReadNoteTool
import re

SYSTEM_PROMPT = """你是一个笔记查阅助理，专门帮助用户理解 AI Agent 相关基础概念。

## 你拥有以下工具：
{tool_descriptions}


## 工作流程（严格遵守）：

每次回复必须按照以下格式，直到任务完成：

Thought: [分析用户问题，决定是否需要查找笔记]
Action: [工具名称]
Action Input: [工具的输入参数]

当工具返回结果后，你会收到：
Observation: [工具返回的结果]

然后继续思考，直到任务完成，最后输出：
Thought: [最终思考，确认已获取足够信息]
Final Answer: [给用户的最终回答]

## 回答风格要求：
1. 使用中文回答
2. 先讲概念，再给例子
3. 最后给"下一步建议"
4. 如果本地笔记里没有相关内容，明确说"本地笔记中未找到该主题"，不做猜测

## 重要规则：
1. 每次只能调用一个工具
2. 如果不需要工具（例如用户只问一般性问题），直接输出 Final Answer
3. 优先使用 search_note 查找相关笔记
4. 如果搜索无结果，再尝试 list_topics 查看有哪些可用主题
5. Action 字段只能填写工具名称，不能有其他内容
6. 如果工具返回错误或无结果，说明可用主题或提示用户
7. 对于不在笔记中的内容，明确告知而非杜撰
"""


class ReActAgent:
    MAX_ITERATIONS = 10

    def __init__(self):
        self.tools = {
            "list_topics": ListTopicsTool(),
            "search_note": SearchNoteTool(), 
            "read_note": ReadNoteTool(),
        }
        
        tool_descriptions = "\n".join(
            f"- **{name}**：{tool.description}"
            for name, tool in self.tools.items()
        )
        
        self.llm = LLMClient()
        self.memory = ConversationMemory(
            max_turns=20,
            system_prompt=SYSTEM_PROMPT.format(tool_descriptions=tool_descriptions),
        )

    def run(self, task: str) -> str:
        print(f"任务开始：{task}")
        
        self.memory.add_message("user", task)

        for iteration in range(1, self.MAX_ITERATIONS + 1):
            print(f"第 {iteration} 轮迭代")
            try:
                response = self.llm.chat(self.memory.get_messages())
            except Exception as e:
                return (
                    "模型请求失败，请检查网络、API Key 或 Base URL 配置。"
                    f"错误信息：{e}"
                )
            print(f"LLM 输出：{response}")

            parsed = self._parse_response(response)

            if parsed["type"] == "final_answer":
                self.memory.add_message("assistant", response)
                final = parsed["content"]
                print("任务完成！")
                return final

            elif parsed["type"] == "action":
                tool_name = parsed["tool"]
                tool_input = parsed["input"]
                print(f"🔧调用工具：{tool_name}")
                observation = self._execute_tool(tool_name, tool_input)
                print(f"📋 工具返回：{observation}")
                self.memory.add_message("assistant", response)
                self.memory.add_message("user", f"Observation: {observation}")
            else:
                print(f"⚠️输出解析失败，提示 LLM 修正")
                self.memory.add_message("assistant", response)
                self.memory.add_message(
                    "user",
                    "你的输出格式不正确。请严格按照 Thought/Action/Action Input 或 Final Answer 格式回复。",
                )

        return "任务未能在规定步骤内完成，请尝试简化任务描述。"

    def _parse_response(self, response: str) -> dict:
        final_match = re.search(
            r"Final\s*Answer\s*:\s*([\s\S]+)$", response, re.IGNORECASE
        )
        if final_match:
            return {"type": "final_answer", "content": final_match.group(1).strip()}

        action_match = re.search(r"Action:\s*(\w+)", response)
        input_match = re.search(
            r"Action Input:\s*(.+?)(?:\nThought|\nAction|\nObservation|$)",
            response,
            re.DOTALL,
        )

        if action_match and input_match:
            return {
                "type": "action",
                "tool": action_match.group(1).strip(),
                "input": input_match.group(1).strip(),
            }

        return {"type": "unknown"}

    def _execute_tool(self, tool_name: str, tool_input: str) -> str:
        if tool_name not in self.tools:
            available = ", ".join(self.tools.keys())
            return f"错误：工具 '{tool_name}' 不存在。可用工具：{available}"

        try:
            return self.tools[tool_name].run(tool_input)
        except Exception as e:
            return f"工具执行异常：{str(e)}"

    def reset(self):
        self.memory.clear()
        print("Agent 状态已重置")