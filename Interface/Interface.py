import os
import sys
import tkinter as tk
import json
import cv2
import threading
import face_recog
from tkinter import ttk, messagebox
from tkinter import filedialog
from return_path import return_path
from Interface import loading_bar

t_1 = threading.Thread(target=loading_bar.main)
t_1.start()


NORM_FONT = ("Verdana", 10)
LARGE_FONT = ("Verdana", 12)
result = "Desconhecido"


class App(tk.Tk):

    def __init__(self, *args, **kwargs):  # arguments and keyword arguments
        tk.Tk.__init__(self, *args, **kwargs)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        icon_path = return_path(icon_path, r'./Interface/faceicon.ico')

        tk.Tk.iconbitmap(self, default=icon_path)
        tk.Tk.wm_title(self, "Reconhecimento facial")

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

        button = ttk.Button(insercaoERemocaoFrame, text="Adicionar usuário",
                            command=lambda: controller.show_frame(PageOne))
        button.pack(padx=150, pady=100)

        def popupmsg(msg):
            popup = tk.Tk()
            popup.wm_title("Remover Usuário")

            label = ttk.Label(popup, text=msg, font=NORM_FONT)
            label.pack(side="top", fill="x", pady=10)

            frm = tk.Frame(popup, borderwidth=1)

            f = open(r'./coordinates.txt', 'r')
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
                    f = open(r'./coordinates.txt', 'r')
                    data_set = json.loads(f.read())
                    Nomes = []

                    for key, value in data_set.items():
                        Nomes.append(key)
                    f.close()

                    RemoverNome = Nome.get()
                    popup.destroy()

                    Clear(RemoverNome)
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

            frm.pack(side='bottom')

            popup.eval('tk::PlaceWindow . center')
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
                             command=lambda: face_recog.Recog("camera", "", "", ""))
        button3.pack(padx=150, pady=165)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        bframe = tk.Frame(self)
        cframe = tk.Frame(self)

        Nome = tk.Label(bframe, text="Nome e sobrenome", width=0, height=0, padx=40, pady=50,
                        font=LARGE_FONT)
        Nome.grid(row=0, column=0, stick='nsew')
        NomeFrame = ttk.Frame(bframe, width=600, height=360)
        NomeFrame.grid(row=1, column=0)

        NomeFunc = tk.Entry(NomeFrame)
        NomeFunc.pack(pady=10, padx=10)
        NomeFunc.focus_set()

        Turma = tk.Label(bframe, text="Empresa", width=0, height=0, padx=10, pady=30,
                         font=LARGE_FONT)
        Turma.grid(row=3, column=0, stick='nsew')
        TurmaFrame = ttk.Frame(bframe, width=400, height=360)
        TurmaFrame.grid(row=4, column=0)

        Combo = ttk.Combobox(TurmaFrame, values=["ICA", "PUC-Rio", "Externo"])
        Combo.set("ICA")
        Combo.pack(pady=10, padx=10)
        Combo.focus_set()

        def add_pic(new_name, turma):
            path = filedialog.askopenfile(title='Selecione a foto',
                                          filetypes=[('Image Files', ['.jpeg', '.jpg', '.JPG', '.png', '.gif',
                                                                      '.tiff', '.tif', '.bmp'])])

            if not path:
                PageOne("", "")

            else:
                im = cv2.imread(path.name)
                # cv2.imshow('Foto', im)
                face_recog.Recog.create_manual_data("", "", path.name, im, turma)
                controller.show_frame(StartPage)

        def add_manual(new_name, turma):
            face_recog.Recog.create_manual_data("", "input", new_name, "", turma)
            controller.show_frame(StartPage)

        def next_step():
            if NomeFunc.get():
                # the user entered data in the mandatory entry: proceed to next step
                new_name = NomeFunc.get()
                NomeFunc.delete(0, 'end')
                turma = Combo.get()

                # add person in dataset
                popup2 = tk.Tk()
                popup2.wm_title("Adicionar Usuário")

                label = ttk.Label(popup2, text='Selecione uma foto ou pegue as coordenadas do usuário',
                                  font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)

                frm = tk.Frame(popup2, borderwidth=1)

                B1 = ttk.Button(frm, text="Inserir foto",
                                command=lambda: [add_pic(new_name, turma), popup2.destroy()])
                B1.pack(side='left')

                B2 = ttk.Button(frm, text="Pegar coordenadas",
                                command=lambda: [add_manual(new_name, turma), popup2.destroy()])
                B2.pack(side='right')

                frm.pack(side='bottom', pady='15')

                popup2.eval('tk::PlaceWindow . center')
                popup2.mainloop()
                controller.show_frame(StartPage)

            else:
                # the mandatory field is empty
                messagebox.showinfo("Adicionar Usuário", "Escreva o nome do usuário!")
                NomeFunc.focus_set()

        Ok = ttk.Button(TurmaFrame, text='OK', command=lambda: next_step())
        Ok.pack(sid='left')

        Cancelar = ttk.Button(TurmaFrame, text='Cancelar',
                              command=lambda: [controller.show_frame(StartPage), NomeFunc.delete(0, 'end')])
        Cancelar.pack(side='left')

        bframe.pack(side='left')

        AdicionarUsuario = tk.Label(cframe, text='Adicionar Usuário', width=0, height=0, padx=0, pady=0,
                                    font=LARGE_FONT)
        AdicionarUsuario.grid(row=0, column=3)
        AdicionarUsuarioFrame = ttk.Frame(cframe, width=400, height=300, relief='sunken')
        AdicionarUsuarioFrame.grid(row=1, column=3, padx=50)

        cframe.pack(side='right')


class Clear:  # clear the person and its coordinates from the txt
    def __init__(self, RemoverNome):
        self.RemoverNome = RemoverNome

        f = open(r'./coordinates.txt', 'r')  # read
        g = open(r'./coordinates_new.txt', 'w')  # write

        with g as dest_file:
            with f as source_file:
                for line in source_file:
                    element = json.loads(line.strip())
                    if RemoverNome in element:
                        del element[RemoverNome]
                    dest_file.write(json.dumps(element))
        f.close()
        g.close()

        os.remove(r'./coordinates.txt')
        os.rename(r'./coordinates_new.txt', r'./coordinates.txt')


app = App()
app.eval('tk::PlaceWindow . center')
app.mainloop()
app.bind('<Escape>', sys.exit())
