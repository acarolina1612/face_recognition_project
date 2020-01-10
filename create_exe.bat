@echo off
call pyinstaller ^
--onefile ^
--windowed ^
--add-data "models;models" ^
--add-data "audio3.mp3;." ^
--add-data "faceicon.ico;." ^
--hidden-import=pyttsx3.drivers ^
--hidden-import=pyttsx3.drivers.dummy ^
--hidden-import=pyttsx3.drivers.espeak ^
--hidden-import=pyttsx3.drivers.nsss ^
--hidden-import=pyttsx3.drivers.sapi5 ^
--icon=faceicon.ico ^
face_recog.py