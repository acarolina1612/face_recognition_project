import os
import pyttsx3
from playsound import playsound
from return_path import return_path


def thread_voice(saudacao):  # say 'welcome' to the user
    audio_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    audio_path = return_path(audio_path, 'audio3.mp3')
    playsound(audio_path)
    engine = pyttsx3.init()
    # set portuguese language
    pt_voice = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_PT-BR_MARIA_11.0"
    engine.setProperty('voice', pt_voice)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.5)
    engine.setProperty('rate', 200)
    engine.say(saudacao)
    engine.runAndWait()
