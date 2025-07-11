import os    #to check memory.json exists on disk
import json
 
MEMORY_FILE = "data/memory.json"   #path where memory is stored

def load_memory():   #reads MEMORY_FILE and returns its content
    if not os.path.exists(MEMORY_FILE):
        return {}
    with open(MEMORY_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_memory(file_name, text):
    memory = load_memory()
    memory[file_name] = text
    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(memory, f, indent=2)

def get_all_memories():
    return load_memory()
