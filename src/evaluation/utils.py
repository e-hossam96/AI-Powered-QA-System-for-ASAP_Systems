from pathlib import Path


def read_eval_data(path: Path) -> list[str] | None:
    with open(path, "r", encoding="utf-8") as f:
        data = f.read().strip()
        data = data.split("\n")
    if not data:
        data = None
    return [{"query": q} for q in data]
