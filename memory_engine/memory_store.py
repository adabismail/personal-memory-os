import os
import json
import tempfile

MEMORY_FILE = "data/memory.json"

def _ensure_data_folder():
    os.makedirs(os.path.dirname(MEMORY_FILE) or ".", exist_ok=True)

def _write_json_atomic(path, obj):
    dirn = os.path.dirname(path) or "."
    with tempfile.NamedTemporaryFile("w", dir=dirn, delete=False, encoding="utf-8") as tmp:
        json.dump(obj, tmp, indent=2, ensure_ascii=False)
        tmp.flush()
    os.replace(tmp.name, path)

def load_memory():
    _ensure_data_folder()
    # create valid file if missing or zero bytes
    if not os.path.exists(MEMORY_FILE) or os.path.getsize(MEMORY_FILE) == 0:
        _write_json_atomic(MEMORY_FILE, {})
        return {}
    try:
        # use utf-8-sig,so if BOM is present its handled automatically
        with open(MEMORY_FILE, "r", encoding="utf-8-sig") as f:
            return json.load(f)
    except json.JSONDecodeError:
        # corrupted file is reset safely
        _write_json_atomic(MEMORY_FILE, {})
        return {}
    except Exception:
        return {}

def save_memory(file_name, text):
    memory = load_memory()
    memory[file_name] = text
    _write_json_atomic(MEMORY_FILE, memory)

def get_all_memories():
    return load_memory()
