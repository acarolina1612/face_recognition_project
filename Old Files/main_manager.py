import copy
import datetime
import json
import os
import sys
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from tkinter import filedialog

import cv2

import anti_spoofing_manager
import face_recognize_manager

NORM_FONT = ("Verdana", 10)
LARGE_FONT = ("Verdana", 12)


class App(tk.Tk):

    def __init__(self, *args, **kwargs):  # arguments and keyword arguments

        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.iconbitmap(self, default="faceicon.ico")
        tk.Tk.wm_title(self, "Reconhecimento Facial")

        self.geometry("800x400")
        self.resizable(0, 0)
        container = tk.Frame(self)

        container.pack(side="top", fill="both", expand=True)

        self.frames = {}

        for F in (StartPage, PageOne):
            frame = F(container, self)

            self.frames[F] = frame

            frame.grid(row=0, column=2, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):

        tk.Frame.__init__(self, parent)

        insercaoERemocao = tk.Label(self, text='Cadastro/Remoção de usuários', width=0, height=0, padx=10, pady=12,
                                    font=LARGE_FONT)
        insercaoERemocao.grid(row=0, column=0, stick='nsew')
        insercaoERemocaoFrame = ttk.Frame(self, width=400, height=360, relief='raised')
        insercaoERemocaoFrame.grid(row=1, column=0, sticky="nsew")

        def add_manager():  # call add person in dataset
            popup2 = tk.Tk()
            popup2.wm_title("Adicionar Usuário")

            label = ttk.Label(popup2, text='Selecione uma foto ou pegue as coordenadas do usuário', font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)

            frm = tk.Frame(popup2, borderwidth=1)

            def open_file():  # picture must be saved with user's name and surname
                popup2.destroy()
                path = filedialog.askopenfile(title='Selecione a foto',
                                              filetypes=[('Image Files', ['.jpeg', '.jpg', '.png', '.gif',
                                                                          '.tiff', '.tif', '.bmp'])])

                if not path:
                    PageOne("", "")

                else:
                    im = cv2.imread(path.name)
                    # cv2.imshow('Foto', im)
                    face_recognize_manager.RecognizePerson.create_manual_data("", im, path.name, turma)

            def new_person():
                popup2.destroy()
                controller.show_frame(PageOne)

            B1 = ttk.Button(frm, text="Inserir foto",
                            command=lambda: open_file())
            B1.pack(side='left')

            B2 = ttk.Button(frm, text="Pegar coordenadas",
                            command=lambda: new_person())
            B2.pack(side='right')

            frm.pack(side='bottom', pady='15')

            popup2.mainloop()

        button = ttk.Button(insercaoERemocaoFrame, text="Adicionar usuário",
                            command=lambda: add_manager())
        button.pack(padx=150, pady=100)

        def popupmsg(msg):
            popup = tk.Tk()
            popup.wm_title("Remover Usuário")

            label = ttk.Label(popup, text=msg, font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)

            frm = tk.Frame(popup, borderwidth=1)

            f = open(r'./facerec_ICA.txt', 'r')
            data_set = json.loads(f.read())
            Nomes = []

            for key, value in data_set.items():
                Nomes.append(key)
            f.close()

            Nome = ttk.Combobox(popup, values=sorted(Nomes))
            Nome.pack(pady=15, padx=20)
            Nome.focus_set()

            def next_step():
                if Nome.get():
                    # the user entered data in the mandatory entry: proceed to next step
                    f = open(r'./facerec_ICA.txt', 'r')
                    data_set = json.loads(f.read())
                    Nomes = []

                    for key, value in data_set.items():
                        Nomes.append(key)
                    f.close()

                    RemoverNome = Nome.get()
                    popup.destroy()

                    MyManager.Clear(RemoverNome)
                    messagebox.showinfo("Remover Usuário", "Usuário removido!")

                else:
                    # the mandatory field is empty
                    messagebox.showinfo("Remover Usuário", "Selecione um usuário!")
                    Nome.focus_set()
                    popup.destroy()
                    popupmsg(msg)

            B1 = ttk.Button(frm, text="OK", command=lambda: next_step())
            B1.pack(side='left')

            B2 = ttk.Button(frm, text="Cancelar", command=popup.destroy)
            B2.pack(side='left')

            frm.pack(side='bottom', pady='15')

            popup.mainloop()

        button2 = ttk.Button(insercaoERemocaoFrame, text="Remover usuário",
                             command=lambda: popupmsg("Selecione o nome do usuário que será removido"))
        button2.pack(padx=0, pady=10)

        ReconhecimentoUsuarios = tk.Label(self, text='Reconhecimento de usuários', width=0, height=0, padx=10, pady=12,
                                          font=LARGE_FONT)
        ReconhecimentoUsuarios.grid(row=0, column=1, stick='nsew')
        ReconhecimentoUsuariosFrame = ttk.Frame(self, width=400, height=360, relief='raised')
        ReconhecimentoUsuariosFrame.grid(row=1, column=1, sticky="nsew")

        button3 = ttk.Button(ReconhecimentoUsuariosFrame, text="Reconhecer usuário",
                             command=lambda: MyManager.recog_manager(""))
        button3.pack(padx=150, pady=165)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        bframe = tk.Frame(self)
        cframe = tk.Frame(self)

        Nome = tk.Label(bframe, text="Nome e sobrenome", width=0, height=0, padx=40, pady=20,
                        font=LARGE_FONT)
        Nome.grid(row=0, column=0, stick='nsew')
        NomeFrame = ttk.Frame(bframe, width=600, height=360)
        NomeFrame.grid(row=1, column=0)

        NomeFunc = tk.Entry(NomeFrame)
        NomeFunc.pack(pady=10, padx=10)
        NomeFunc.focus_set()

        def next_step2():
            if NomeFunc.get():
                # if the user enters data in the mandatory entry, proceed to next step
                new_name = NomeFunc.get()
                NomeFunc.delete(0, 'end')
                face_recognize_manager.RecognizePerson.create_manual_data("", "", new_name)
                controller.show_frame(StartPage)

            else:
                # if the mandatory field is empty
                messagebox.showinfo("Adicionar Usuário", "Escreva o nome do usuário!")
                NomeFunc.focus_set()

        Ok = ttk.Button(NomeFrame, text='OK', command=lambda: next_step2())
        Ok.pack(sid='left')

        Cancelar = ttk.Button(NomeFrame, text='Cancelar',
                              command=lambda: [controller.show_frame(StartPage), NomeFunc.delete(0, 'end')])
        Cancelar.pack(side='left')

        bframe.pack(side='left')

        AdicionarUsuario = tk.Label(cframe, text='Adicionar Usuário', width=0, height=0, padx=0, pady=0,
                                    font=LARGE_FONT)
        AdicionarUsuario.grid(row=0, column=3)
        AdicionarUsuarioFrame = ttk.Frame(cframe, width=400, height=300, relief='sunken')
        AdicionarUsuarioFrame.grid(row=1, column=3, padx=50)

        cframe.pack(side='right')


class MyManager:

    def recog_manager(self):  # call anti spoofing and recognize person

        path = r'D:/FaceRec-master/imgs/Intrusos'
        sample_number = 1
        count = 0
        wait = 0
        decrease = 2
        frames = 1
        result = 'Unknown'
        stack_frames = []
        number_falses = 0  # limit the number of false to prevent intruder to break in
        intruder = 0
        intruder_denied = 0

        now = datetime.datetime.now()
        mes = now.strftime('%m')
        dia = now.strftime('%d')
        hora = now.strftime('%H')
        minutos = now.strftime("%M")

        # # Open webcam
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            print("Erro ao iniciar a câmera.\nDesconecte e conecte o cabo USB da câmera.")
            exit(0)

        width = 640
        height = 480
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)

        while True:
            ret, frame = cap.read()
            frame = cv2.flip(frame, 1)

            if ret is False:
                break

            frame2 = copy.deepcopy(frame)  # create a deep copy of the frame to avoid modifications from anti spoofing
            stack_frames.append(frame2)  # stack frames to use in recognize person

            text_as, number_falses = anti_spoofing_manager.MySpoof.load_spoof("", frame, sample_number, count,
                                                                              decrease,
                                                                              number_falses)  # call anti spoofing

            cv2.imshow('Manager', frame)
            cv2.resizeWindow('Manager', 640, 480)

            if text_as == "False":
                wait = 0
                decrease = 2

            if text_as == "True":
                wait += 1

                if wait == 10 or wait == 20 or wait == 30 or wait == 40:
                    decrease -= 1
                    if decrease == 0:  # anti spoofing is ok!
                        wait = 0
                        decrease = 2
                        cv2.destroyAllWindows()

                        for i in range(len(stack_frames)):

                            text_recog, frames_to_recog, frames, result = \
                                face_recognize_manager.RecognizePerson.camera_recog(stack_frames[i], frames, result,
                                                                                    ret)  # call recognize person
                            # with the video from anti spoofing

                            cv2.imshow('Recog', frames_to_recog)
                            cv2.resizeWindow('Recog', 640, 480)

                            cv2.waitKey(1)

                            if text_recog == "True":  # recognize is ok, access granted
                                print('Bem vindo, %s' % result, '!')
                                cv2.destroyAllWindows()
                                cap.release()
                                break
                            if text_recog == "False":
                                intruder += 1
                                if intruder > len(stack_frames):
                                    intruder_denied += 1
                                    if intruder_denied == 2:  # access denied when the person is not recognized 2 times
                                        cv2.imwrite(os.path.join(path,
                                                                 'Intruder' + '_' + '%s' % dia + '_' + '%s' % mes + '_'
                                                                 + '%s' % hora + 'h' + '%s' % minutos + '.jpg'),
                                                    frames_to_recog)
                                        print('Intruso detectado!')
                                        cv2.destroyAllWindows()
                                        cap.release()
                                        break
                                    else:
                                        continue
                                else:
                                    continue

            key = cv2.waitKey(1)  # 0 to forever delay (frozen frame), 1 for 1 millisecond delay
            if key == ord("q"):
                cv2.destroyAllWindows()  # clear all windows
                cap.release()  # release the camera
                break

            if number_falses >= 100:  # access denied
                cv2.destroyAllWindows()  # clear all windows
                cap.release()  # release the camera
                print('Tempo excedido!')
                break

    class Clear:  # clear the person coordinates from txt
        def __init__(self, RemoverNome):
            self.RemoverNome = RemoverNome

            f = open(r'./facerec_ICA.txt', 'r')  # read
            g = open(r'./facerec_ICA_new.txt', 'w')  # write

            with g as dest_file:
                with f as source_file:
                    for line in source_file:
                        element = json.loads(line.strip())
                        if RemoverNome in element:
                            del element[RemoverNome]
                        dest_file.write(json.dumps(element))
            f.close()
            g.close()

            os.remove(r'./facerec_ICA.txt')  # remove the old dataset
            os.rename(r'./facerec_ICA_new.txt', r'./facerec_ICA.txt')  # create a new dataset with the person's
            # coordinates erased and rename the new dataset with the original name


app = App()
app.mainloop()
app.bind('<Escape>', sys.exit())
