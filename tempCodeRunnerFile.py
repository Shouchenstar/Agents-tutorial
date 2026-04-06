from agent import ReActAgent
from logger import log_qa

WELCOME_TEXT = """
欢迎使用「OpenAI 本地笔记问答助手」！

你可以输入：
- 什么是 agent？
- 什么是 tool？
- 什么是 workflow？
- topics
- exit
"""

agent = ReActAgent()

def answer_question(question: str) -> str:
    result = agent.run(question)
    return result

def main():
    print(WELCOME_TEXT)
    
    while True:
        question = input("请输入你的问题：").strip()
        if question.lower() == "exit":
            print("感谢使用，再见！")
            break
        
        answer = answer_question(question)
        print(answer)
        log_qa(question, answer)
        
    
if __name__ == "__main__":
    main()