import os
import pyttsx3
from playsound import playsound


def thread_voice(welcome_msg):  # say 'welcome' to the user
    audio = '/audio3.mp3'
    audio_path = os.path.dirname(os.path.abspath(__file__))
    audio_path = audio_path + audio
    playsound(audio_path)
    engine = pyttsx3.init()
    # set portuguese language
    pt_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_MARIA_11.0"
    engine.setProperty('voice', pt_voice)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.5)
    engine.setProperty('rate', 200)
    engine.say(welcome_msg)
    engine.runAndWait()
