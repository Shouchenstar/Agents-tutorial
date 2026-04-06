notes = {
    "agent": {
        "aliases": ["agent", "智能体", "代理"],
        "concept": "Agent 是一个可以根据目标处理任务、并在需要时调用工具的智能体。",
        "example": "比如一个学习助手，可以回答问题、读取笔记、整理内容。",
        "next_step": "你下一步可以学习 tool 的概念。"
    },
    "tool": {
        "aliases": ["tool", "tools", "工具", "函数工具"],
        "concept": "Tool 是给 Agent 使用的能力，比如查数据、读文件、做计算。",
        "example": "比如 read_note() 这个函数，就是一个读取笔记的工具。",
        "next_step": "你下一步可以学习 memory 的概念。"
    },
    "memory": {
        "aliases": ["memory", "记忆", "上下文记忆"],
        "concept": "Memory 是让系统保留上下文或历史信息的机制。",
        "example": "比如你上一轮问了 agent，这一轮再问“它和 tool 有什么区别”，系统还能接上。",
        "next_step": "你下一步可以学习 handoff 或 workflow。"
    },
    "handoff": {
        "aliases": ["handoff", "交接", "任务交接", "转交"],
        "concept": "Handoff 是把任务从一个 Agent 转交给另一个更适合的 Agent。",
        "example": "比如一个研究 Agent 收集资料，再把任务交给写作 Agent。",
        "next_step": "你下一步可以学习多 Agent 协作。"
    },
    "workflow": {
        "aliases": ["workflow", "工作流", "流程"],
        "concept": "Workflow 是把任务拆成多个步骤，并按顺序或条件执行的流程。",
        "example": "比如先检查输入，再生成回答，最后保存结果。",
        "next_step": "你下一步可以学习 LangGraph。"
    },
    "prompt": {
        "aliases": ["prompt", "提示词", "提示"],
        "concept": "Prompt 是你给模型的输入指令，用来告诉它要做什么、怎么做。",
        "example": "比如“请用中文、面向初学者解释什么是 Agent”。",
        "next_step": "你下一步可以学习如何写更稳定的 instructions。"
    },
    "rag": {
        "aliases": ["rag", "检索增强", "检索增强生成"],
        "concept": "RAG 是先检索外部资料，再结合资料生成回答的方法。",
        "example": "比如先查你的笔记或文档，再基于查到的内容回答问题。",
        "next_step": "你下一步可以学习向量库和检索流程。"
    }
}