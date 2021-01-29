# Facial recognition
Facial Recognition program in Python with tkinter interface and anti spoofing.

The executable on dist folder can run in any computer device with a camera.

The recognized person's name is saved in a .xlsx file with time and place of work.

The recognized person's picture is taken at the moment of recognition and saved at the imgs folder, a user file appears with a welcome message and a voice speaks a welcome message after a short noise.

Users can be added to database through 1 picture and data augmentation or manually moving his head to get coordinates.

Other codes can be found in Older Files folder (anti spoofing codes and etc.).

## How to run:
    Run the bat program in an anaconda environment with all dependencies (files .txt, .xlsx and folder imgs are necessary) or run face_recog.py.

## Requirements:
    Python3 (3.5 ++ is recommended)

## Dependencies:
    numpy==1.16.1
    pandas==0.24.2
    tensorflow==1.14.0
    setuptools==41.0.0
    keras==2.2.4
    opencv-python
    tkinter
    pillow
    openpyxl
    xlrd
    xlsxwriter
    pyttsx3
    playsound
    imutils

    
### Info on the models:

Facial Recognition Architecture: Facenet Inception Resnet V1 

_Pretrained model is provided in Davidsandberg repo_

More information on the model: https://arxiv.org/abs/1602.07261

Face detection method: MTCNN

More info on MTCNN Face Detection: https://kpzhang93.github.io/MTCNN_face_detection_alignment/

Anti spoofing model: https://github.com/ee09115/spoofing_detection

### Framework and Libs:

Tensorflow: The infamous Google's Deep Learning Framework

OpenCV: Image processing (VideoCapture, resizing,..)

Openpyxl: Works with excel sheets to get exact time of recognition

Imutils: rotates images to add user through pictures

Pyttsx3: speaks a welcome message

Playsound: plays a short noise before welcome message

![GIF Demo](https://media.giphy.com/media/TKp44Imbxl5fi8QqRP/giphy.gif)

Authors: Gabriel Taranto and Felipe Borges

## Credits:
    - David Vu https://github.com/vudung45
    - Valter Costa https://github.com/ee09115
    - Pretrained models https://github.com/davidsandberg/facenet
