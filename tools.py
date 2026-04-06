from notes import notes


def list_topics_raw() -> list[str]:
    return list(notes.keys())


def find_topic_by_text_raw(text: str) -> str | None:
    q = text.strip().lower()

    for topic, item in notes.items():
        aliases = item.get("aliases", [])
        for alias in aliases:
            if alias.lower() in q:
                return topic
    return None

class ListTopicsTool:
    """列出当前本地笔记中支持的所有主题。"""
    name = "list_topics"
    description = "列出当前本地笔记中支持的所有主题。"

    def run(self, _: str = "") -> str:
        return "当前支持的主题有： " + "、".join(list_topics_raw())


class ReadNoteTool:
    """读取某个主题的本地笔记，并返回结构化说明。"""
    name = "read_note"
    description = "读取某个主题的本地笔记，并返回结构化说明。"

    def run(self, topic: str) -> str:
        item = notes.get(topic.lower())
        if not item:
            return f"没有找到主题：{topic}"

        return (
            f"【主题】{topic}\n"
            f"【概念】{item['concept']}\n"
            f"【例子】{item['example']}\n"
            f"【下一步】{item['next_step']}"
        )


class SearchNoteTool:
    """根据用户的问题，在本地笔记里查找最相关的主题。"""
    name = "search_note"
    description = "根据用户的问题，在本地笔记里查找最相关的主题。"

    def run(self, question: str) -> str:
        topic = find_topic_by_text_raw(question)
        if not topic:
            return "没有在本地笔记中找到相关主题。你可以先调用 list_topics 看看当前支持哪些主题。"

        item = notes[topic]
        return (
            f"【匹配主题】{topic}\n"
            f"【概念】{item['concept']}\n"
            f"【例子】{item['example']}\n"
            f"【下一步】{item['next_step']}"
        )