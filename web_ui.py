import streamlit as st
import os
import uuid
from transcibe_audio import transcribe_audio
from content_generation import draft_post, refined_post

st.title("🎙️ LinkedIn Content Generator")
st.header("1. Upload Your Voice Note")

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])

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

    if st.button("🧠 Transcribe Audio"):
        transcription = transcribe_audio.run(st.session_state["audio_path"])
        st.session_state["transcription"] = transcription
        st.session_state["transcribed"] = True  # <-- SET THE FLAG
    
else:
    st.session_state["transcribed"] = True

# Step 2: Show transcription and allow user to trigger post generation
if st.session_state.get("transcribed"):
    transcription_text = st.text_area("📝 Transcribed Text", st.session_state.get("transcription", ""), height=200)
    st.session_state["transcription"] = transcription_text

    if st.button("✨ Generate LinkedIn Post"):
        st.session_state["generate_post"] = True  # <-- SET FLAG TO GENERATE POST

# Step 3: Generate and edit post only when flag is set
if st.session_state.get("generate_post"):
    st.subheader("✍️ Final LinkedIn Post (Editable)")

    print(st.session_state["transcription"])
    draft = draft_post(idea=st.session_state["transcription"])
    print(draft)
    print('-'*30)
    refined_content = refined_post(draft_post=draft)

    edited_post = st.text_area("Make final edits if needed:", value=refined_content, height=300)

    with st.expander("🕵️ View Original Refined Output"):
        st.code(refined_content, language="markdown")
