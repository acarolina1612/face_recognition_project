import tkinter as tk
import time
from PIL import Image, ImageTk
from tkinter import font


new_name = 'Gabriel Taranto'
empresa = 'ICA'

w = tk.Tk()
w.iconbitmap(default="faceicon.ico")
w.wm_title('Ficha do usuário')
w.geometry('600x600')
w.resizable(0, 0)
logo = ImageTk.PhotoImage(file="C:/FaceRec-master/imgs/python_logo_small.jpg")

label_right = tk.Label(w)
label_left = tk.Label(w)

saudacao = '\n' + 'Bem vindo, ' + new_name + '!'
info = 'Empresa: ' + empresa

w1 = tk.Label(label_right,
              padx = 70,
              text=info,
              font = ('Helvetica',16)).pack(side='bottom')
w2 = tk.Label(label_right, image=logo, width = 450, height = 450, relief = 'sunken').pack(side="bottom")
w3 = tk.Label(label_right,
              text=saudacao,
              font=('Helvetica',20)).pack(side='top')
label_right.pack(anchor='center')

w.update()
#time.sleep(2)
#w.destroy()
w.mainloop()