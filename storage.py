from pathlib import Path

DATA_DIR = Path(__file__).parent / "data"


def load_records(filename):
    path = DATA_DIR / filename
    if not path.exists():
        return []

    rows = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                parts = [p.strip() for p in line.split("|")]
                rows.append(parts)
    return rows



def save_records(filename, rows):
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / filename
    with open(path, "w", encoding="utf-8") as f:
        for row in rows:
            line = " | ".join(str(item).strip() for item in row)
            f.write(line + "\n")


def append_record(filename, row):
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / filename
    with open(path, "a", encoding="utf-8") as f:
        line = " | ".join(str(item).strip() for item in row)
        f.write(line + "\n")