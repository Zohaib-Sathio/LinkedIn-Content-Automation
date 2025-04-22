import streamlit as st
import os
import uuid

st.title("🎙️ LinkedIn Content Generator")

st.header("1. Upload Your Voice Note")

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])

# Process the uploaded file
if uploaded_file is not None:
    file_id = str(uuid.uuid4())
    file_ext = uploaded_file.name.split('.')[-1]
    file_path = f"audio_inputs/{file_id}.{file_ext}"

    os.makedirs("audio_inputs", exist_ok=True)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())

    st.success(f"✅ File uploaded and saved at: {file_path}")
    st.audio(file_path, format=f"audio/{file_ext}")

    st.session_state["audio_path"] = file_path
else:
    st.info("Upload an audio file to continue.")
