import os
import time
import datetime
import tkinter as tk
from PIL import ImageTk


def thread_file(welcome_msg, info, result):  # create customer's file
    path = os.path.abspath(os.pardir)  # get the parent folder path. In this case is
    # face_recognition_project
    path = path + '\\face_recognition_project\\Validacao_de_Pessoas\\imgs'

    now = datetime.datetime.now()
    month = now.strftime('%m')
    day = now.strftime('%d')
    hour = now.strftime("%H")
    minutes = now.strftime("%M")

    w = tk.Toplevel()
    icon = 'faceicon.ico'
    icon_path = os.path.abspath(os.pardir)  # get the parent folder path. In this case is
    # face_recognition_project
    icon_path = icon_path + '\\face_recognition_project\\Interface\\' + icon
    w.iconbitmap(default=icon_path)
    w.wm_title('Ficha do usuário')
    w.geometry('600x600')
    w.resizable(0, 0)
    logo = ImageTk.PhotoImage(file=path + '\\' + '%s' % result + '_' + '%s' % day + '_' +
                                   '%s' % month + '_' + '%s' % hour
                                   + 'h' + '%s' % minutes + '.jpg')

    label_right = tk.Label(w)

    w1 = tk.Label(label_right,
                  padx=70,
                  text=info,
                  font=('Helvetica', 16)).pack(side='bottom')
    w2 = tk.Label(label_right, image=logo, width=450, height=450, relief='sunken').pack(
        side="bottom")
    w3 = tk.Label(label_right,
                  text=welcome_msg,
                  font=('Helvetica', 20)).pack(side='top')
    label_right.pack(anchor='center')
    w.update()
    time.sleep(3)
    w.destroy()
