import streamlit as st
import os
import time
from memory_engine import file_reader, memory_store, search
# Ensure memory.json exists and is valid
import json
if not os.path.exists("data/memory.json"):
    with open("data/memory.json", "w", encoding="utf-8") as f:
        json.dump({}, f)

# ----------------------------
# Page setup
st.set_page_config(page_title="Memory OS", layout="centered")
st.title("🧠 Personal Memory OS")
st.write("Upload documents, extract text, and ask questions.")

# ----------------------------
# Upload document
uploaded_file = st.file_uploader("Upload a document", type=["pdf", "docx", "txt"])
if uploaded_file:
    file_path = os.path.join("data", uploaded_file.name)

    # Save file
    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    # Extract text and save to memory
    text = file_reader.extract_text(file_path)
    memory_store.save_memory(uploaded_file.name, text)
    st.success("Memory stored successfully!")

    # Show text preview
    st.subheader("📄 Preview of file contents:")
    st.text(text[:1000])

# ----------------------------
# Ask a question
st.subheader("🔍 Ask something based on your memories:")
question = st.text_input("")
if question:
    answer = search.find_answer(question)
    st.write("📌", answer if answer else "Sorry, I couldn’t find anything relevant.")

# ----------------------------
# Stored Memories dropdown with view + delete
with st.expander("🧠 Stored Memories"):
    uploaded_files = [
        f for f in os.listdir("data")
        if f.endswith((".pdf", ".docx", ".txt")) and f != "memory.json"
    ]

    if uploaded_files:
        for file in uploaded_files:
            file_path = os.path.join("data", file)
            upload_time = time.ctime(os.path.getmtime(file_path))
            icon = "📄"

            # File info
            st.markdown(f"**{icon} {file}**")
            st.caption(f"🕓 Uploaded: {upload_time}")

            # File view
            if file.endswith(".pdf"):
                with open(file_path, "rb") as f:
                    st.download_button("🔍 View PDF", f, file_name=file)
            elif file.endswith(".txt"):
                with open(file_path, "r", encoding="utf-8") as f:
                    st.text_area("📖 File Preview", f.read(), height=200)
            else:
                st.info("📁 DOCX preview not supported here. Please download manually.")

            # Confirm delete
            confirm_delete = st.checkbox(f"Delete '{file}'?", key=f"chk_{file}")
            if confirm_delete:
                if st.button(f"❌ Confirm Delete {file}", key=f"btn_{file}"):
                    os.remove(file_path)

                    # Also remove from memory.json
                    memory = memory_store.get_all_memories()
                    if file in memory:
                        del memory[file]
                        with open("data/memory.json", "w", encoding="utf-8") as f:
                            import json
                            json.dump(memory, f, indent=2)

                    st.rerun()

            st.markdown("---")
    else:
        st.write("No documents uploaded yet.")