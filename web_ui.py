import streamlit as st
import os
import time
import uuid
from transcibe_audio import transcribe_audio
from content_generation import draft_post, refined_post
from post_on_linkedin import post_to_linkedin
from post_to_linkedin_with_images import post_to_linkedin_with_images

st.title("🎙️ LinkedIn Content Generator")
st.header("1. Upload Your Voice Note")

rerun = False
print('this is also executing')

uploaded_file = st.file_uploader("Upload an audio file", type=["wav", "mp3", "m4a"])
st.session_state["transcribed"] = True
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
        

# Step 2: Show transcription and allow user to trigger post generation
if st.session_state.get("transcribed"):
    transcription_text = st.text_area("📝 Transcribed Text", st.session_state.get("transcription", ""), height=200)
    st.session_state["transcription"] = transcription_text
    print('this is also executing')

    if st.button("✨ Generate LinkedIn Post"):
        st.session_state.pop("refined_content", None)
        st.session_state["generate_post"] = True  # <-- SET FLAG TO GENERATE POST
        rerun = False
        print('this is also executing: generate post')
    
uploaded_images = st.file_uploader(
    "📸 Upload images for your post (you can select multiple):", 
    type=["jpg", "jpeg", "png"],
    accept_multiple_files=True
)
if uploaded_images:
    st.subheader("🖼️ Uploaded Image Previews")
    for img in uploaded_images:
        st.image(img, width=300)


# Step 3: Generate and edit post only when flag is set
if st.session_state.get("generate_post"):
    if not rerun:
        print(
        "Post is generating..."
        )
        st.subheader("✍️ Final LinkedIn Post (Editable)")
        rerun = False

        if "refined_content" not in st.session_state:
            draft = draft_post(idea=st.session_state["transcription"])
            refined = refined_post(draft_post=draft)
            st.session_state["refined_content"] = refined.replace("**", "")
            st.session_state["edited_post"] = st.session_state["refined_content"]  # Initial value

        # print(st.session_state["transcription"])
        # draft = draft_post(idea=st.session_state["transcription"])
        # # print(draft)
        # # print('-'*30)
        # refined_content = refined_post(draft_post=draft)
        # st.session_state["refined_content"] = refined_content.replace("**", "")
        print("Post generated.")

        edited_post = st.text_area(
        "Make final edits if needed:",
        value=st.session_state["edited_post"],
        height=300,
        key="edited_post_input"
        )

        st.session_state["edited_post"] = edited_post

        with st.expander("🕵️ View Original Refined Output"):
            st.code(st.session_state["refined_content"], language="markdown")
        
        if st.button("🚀 Post to LinkedIn"):
            # print('edited post: ')
            # print(edited_post[:50])
            st.session_state["post_to_linkedin"] = True
            st.session_state["uploaded_images"] = uploaded_images if uploaded_images else []




if st.session_state.get("post_to_linkedin"):
    print('Posting to linkedIn')
    print(st.session_state["edited_post"][:50])

    uploaded_images = st.session_state.get("uploaded_images", [])

    if uploaded_images:
        status_code, response = post_to_linkedin_with_images(st.session_state["edited_post"], uploaded_images)
    else:
        status_code, response = post_to_linkedin(st.session_state["edited_post"])

    # status_code, response = post_to_linkedin(st.session_state["edited_post"])
    # status_code, response = post_to_linkedin('Test')
    if status_code == 201:
        st.success("✅ Successfully posted to LinkedIn!")
    else:
        st.error(f"❌ Failed to post: {status_code}\n{response}")
    
    time.sleep(3)
    st.session_state["generate_post"] = False
    
    st.session_state["post_to_linkedin"] = False
    st.session_state.pop("refined_content", None)
    st.session_state.pop("edited_post", None)
    st.session_state.pop("uploaded_images", None)
    rerun = False
    # for key in ["generate_post", "post_to_linkedin", "refined_content", "edited_post"]:
    #     st.session_state.pop(key, None)

