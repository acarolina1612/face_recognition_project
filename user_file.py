import os
import time
import datetime
import tkinter as tk
from PIL import ImageTk
from return_path import return_path


def thread_file(saudacao, info, result):  # create customer's file
    path = r'./imgs'

    now = datetime.datetime.now()
    mes = now.strftime('%m')
    dia = now.strftime('%d')
    hora = now.strftime("%H")
    minutos = now.strftime("%M")

    w = tk.Toplevel()
    icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
    icon_path = return_path(icon_path, r'./Interface/faceicon.ico')
    w.iconbitmap(default=icon_path)
    w.wm_title('Ficha do usuário')
    w.geometry('600x600')
    w.resizable(0, 0)
    logo = ImageTk.PhotoImage(file=path + '/' + '%s' % result + '_' + '%s' % dia + '_' +
                                   '%s' % mes + '_' + '%s' % hora
                                   + 'h' + '%s' % minutos + '.jpg')

    label_right = tk.Label(w)

    w1 = tk.Label(label_right,
                  padx=70,
                  text=info,
                  font=('Helvetica', 16)).pack(side='bottom')
    w2 = tk.Label(label_right, image=logo, width=450, height=450, relief='sunken').pack(
        side="bottom")
    w3 = tk.Label(label_right,
                  text=saudacao,
                  font=('Helvetica', 20)).pack(side='top')
    label_right.pack(anchor='center')
    w.update()
    time.sleep(3)
    w.destroy()
