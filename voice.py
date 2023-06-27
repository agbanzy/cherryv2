# File: /cherryAI/voice.py

import speech_recognition as sr
from gtts import gTTS
import os

# Function to convert speech to text
def speech_to_text(audio_file_path):
    r = sr.Recognizer()
    with sr.AudioFile(audio_file_path) as source:
        audio_data = r.record(source)
        text = r.recognize_google(audio_data)
        return text

# Function to convert text to speech
def text_to_speech(text, language='en', slow=False):
    speech = gTTS(text=text, lang=language, slow=slow)
    speech.save("output.mp3")
    os.system("start output.mp3")  # this line may vary depending on your OS and the audio player you want to use
