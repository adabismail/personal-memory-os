import re   #used to search fro patterns or words in text
from memory_engine import memory_store

def find_answer(question):   #main search function, give ques, will answer
    memory = memory_store.get_all_memories()  #loads all stored text from memory.json
    matches = []
    keyword = question.lower()

    # Compile once
    pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)

    for doc, text in memory.items():
        # Check match strictly
        if pattern.search(text):
            excerpt = get_excerpt(text, keyword, window=1000)
            highlighted = pattern.sub(f"**{keyword}**", excerpt)
            matches.append(f"📌 [{doc}]\n{highlighted}")
    return "\n\n".join(matches)

def get_excerpt(text, keyword, window=1000):
    pattern = re.compile(rf"\b{re.escape(keyword)}\b", re.IGNORECASE)
    match = pattern.search(text)
    if not match:
        return ""
    idx = match.start()
    start = max(0, idx - window)
    end = min(len(text), idx + window)
    return text[start:end].strip()







