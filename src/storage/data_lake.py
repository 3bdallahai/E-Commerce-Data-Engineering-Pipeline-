import json


def save_to_jsonl(file_path, data):
    """
    Append a single record to a JSONL file.

    Args:
        file_path (str): Path to JSONL file
        data (dict): Data to write
    """
    with open(file_path, "a", encoding="utf-8") as f:
        line = json.dumps(
            data,
            default=lambda o: o.isoformat() if hasattr(o, "isoformat") else str(o)
        )
        f.write(line + "\n")