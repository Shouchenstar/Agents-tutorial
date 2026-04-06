from pathlib import Path
from datetime import datetime


LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "qa_log.txt"


def ensure_log_dir():
    LOG_DIR.mkdir(parents=True, exist_ok=True)


def log_qa(question: str, answer: str):
    ensure_log_dir()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    content = (
        f"[{now}]\n"
        f"Q: {question}\n"
        f"A: {answer}\n"
        f"{'-' * 50}\n"
    )

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(content)