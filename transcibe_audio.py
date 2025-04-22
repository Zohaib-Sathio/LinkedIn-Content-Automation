import whisper
from langchain.tools import tool

model = whisper.load_model("base")  # We can use "tiny", "base", "small", "medium", "large"

@tool
def transcribe_audio(file_path: str) -> str:
    """
    Transcribes speech from an audio file into text using Whisper.
    Args:
        file_path (str): Path to the audio file.
    Returns:
        str: Transcribed text from audio.
    """
    result = model.transcribe(file_path)
    return result["text"]
