# from transcibe_audio import transcribe_audio
# transcription = transcribe_audio.run("audio_inputs\\31532206-1585-4d18-9506-43931fd53605.m4a")
# print(transcription)

import whisper

model = whisper.load_model("base")  # We can use "tiny", "base", "small", "medium", "large"


result = model.transcribe('Chloe_05.mp3')
print(result)