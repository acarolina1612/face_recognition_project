import os
import sys
import tkinter as tk
import json
import cv2
from tkinter import ttk, messagebox
from tkinter import filedialog

NORM_FONT = ("Verdana", 10)
LARGE_FONT = ("Verdana", 12)
result = "Desconhecido"


class App(tk.Tk):

    def __init__(self, *args, **kwargs):  # arguments and keyword arguments
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default='faceicon.ico')
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

        AddAndRemove = tk.Label(self, text='Cadastro/Remoção de usuários', width=0, height=0, padx=10, pady=12,
                                font=LARGE_FONT)
        AddAndRemove.grid(row=0, column=0, stick='nsew')
        AddAndRemoveFrame = ttk.Frame(self, width=400, height=360, relief='raised')
        AddAndRemoveFrame.grid(row=1, column=0, sticky="nsew")

        button = ttk.Button(AddAndRemoveFrame, text="Adicionar usuário",
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

            Name = ttk.Combobox(popup, values=sorted(Nomes))
            Name.pack(pady=15, padx=20)
            Name.focus_set()

            def next_step():
                if Name.get():
                    # the user entered data in the mandatory entry: proceed to next step
                    f = open(r'./coordinates.txt', 'r')
                    data_set = json.loads(f.read())
                    Names = []

                    for key, value in data_set.items():
                        Nomes.append(key)
                    f.close()

                    RemoveName = Name.get()
                    popup.destroy()

                    Clear(RemoveName)
                    messagebox.showinfo("Remover Usuário", "Usuário removido!")

                else:
                    # the mandatory field is empty
                    messagebox.showinfo("Remover Usuário", "Selecione um usuário!")
                    Name.focus_set()
                    popup.destroy()
                    popupmsg(msg)

            B1 = ttk.Button(frm, text="OK", command=lambda: next_step())
            B1.pack(side='left')

            B2 = ttk.Button(frm, text="Cancelar", command=popup.destroy)
            B2.pack(side='left')

            frm.pack(side='bottom')

            popup.eval('tk::PlaceWindow . center')
            popup.mainloop()

        button2 = ttk.Button(AddAndRemoveFrame, text="Remover usuário",
                             command=lambda: popupmsg("Selecione o nome do usuário que será removido"))
        button2.pack(padx=0, pady=10)

        RecogUser = tk.Label(self, text='Reconhecimento de usuários', width=0, height=0, padx=10, pady=12,
                             font=LARGE_FONT)
        RecogUser.grid(row=0, column=1, stick='nsew')
        RecogUserFrame = ttk.Frame(self, width=400, height=360, relief='raised')
        RecogUserFrame.grid(row=1, column=1, sticky="nsew")

        button3 = ttk.Button(RecogUserFrame, text="Reconhecer usuário",
                             command=lambda: face_recog.Recog("camera", "", "", ""))
        button3.pack(padx=150, pady=165)


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)

        bframe = tk.Frame(self)
        cframe = tk.Frame(self)

        Name = tk.Label(bframe, text="Nome e sobrenome", width=0, height=0, padx=40, pady=50,
                        font=LARGE_FONT)
        Name.grid(row=0, column=0, stick='nsew')
        NameFrame = ttk.Frame(bframe, width=600, height=360)
        NameFrame.grid(row=1, column=0)

        NameFunc = tk.Entry(NameFrame)
        NameFunc.pack(pady=10, padx=10)
        NameFunc.focus_set()

        Company = tk.Label(bframe, text="Empresa", width=0, height=0, padx=10, pady=30,
                           font=LARGE_FONT)
        Company.grid(row=3, column=0, stick='nsew')
        CompanyFrame = ttk.Frame(bframe, width=400, height=360)
        CompanyFrame.grid(row=4, column=0)

        Combo = ttk.Combobox(CompanyFrame, values=["ICA", "PUC-Rio", "Externo"])
        Combo.set("ICA")
        Combo.pack(pady=10, padx=10)
        Combo.focus_set()

        def add_pic(company):
            path = filedialog.askopenfile(title='Selecione a foto',
                                          filetypes=[('Image Files', ['.jpeg', '.jpg', '.JPG', '.png', '.gif',
                                                                      '.tiff', '.tif', '.bmp'])])

            if not path:
                PageOne("", "")

            else:
                im = cv2.imread(path.name)
                # cv2.imshow('Foto', im)
                face_recog.Recog.create_manual_data("", "", path.name, im, company)
                controller.show_frame(StartPage)

        def add_manual(new_name, company):
            face_recog.Recog.create_manual_data("", "input", new_name, "", company)
            controller.show_frame(StartPage)

        def next_step():
            if NameFunc.get():
                # the user entered data in the mandatory entry: proceed to next step
                new_name = NameFunc.get()
                NameFunc.delete(0, 'end')
                company = Combo.get()

                # add person in dataset
                popup2 = tk.Tk()
                popup2.wm_title("Adicionar Usuário")

                label = ttk.Label(popup2, text='Selecione uma foto ou pegue as coordenadas do usuário',
                                  font=NORM_FONT)
                label.pack(side="top", fill="x", pady=10)

                frm = tk.Frame(popup2, borderwidth=1)

                B1 = ttk.Button(frm, text="Inserir foto",
                                command=lambda: [add_pic(company), popup2.destroy()])
                B1.pack(side='left')

                B2 = ttk.Button(frm, text="Pegar coordenadas",
                                command=lambda: [add_manual(new_name, company), popup2.destroy()])
                B2.pack(side='right')

                frm.pack(side='bottom', pady='15')

                popup2.eval('tk::PlaceWindow . center')
                popup2.mainloop()
                controller.show_frame(StartPage)

            else:
                # the mandatory field is empty
                messagebox.showinfo("Adicionar Usuário", "Escreva o nome do usuário!")
                NameFunc.focus_set()

        Ok = ttk.Button(CompanyFrame, text='OK', command=lambda: next_step())
        Ok.pack(sid='left')

        Cancel = ttk.Button(CompanyFrame, text='Cancelar',
                            command=lambda: [controller.show_frame(StartPage), NameFunc.delete(0, 'end')])
        Cancel.pack(side='left')

        bframe.pack(side='left')

        AdicionarUsuario = tk.Label(cframe, text='Adicionar Usuário', width=0, height=0, padx=0, pady=0,
                                    font=LARGE_FONT)
        AdicionarUsuario.grid(row=0, column=3)
        AdicionarUsuarioFrame = ttk.Frame(cframe, width=400, height=300, relief='sunken')
        AdicionarUsuarioFrame.grid(row=1, column=3, padx=50)

        cframe.pack(side='right')


class Clear:  # clear the person and its coordinates from the txt
    def __init__(self, RemoveName):
        self.RemoveName = RemoveName

        f = open(r'./coordinates.txt', 'r')  # read
        g = open(r'./coordinates_new.txt', 'w')  # write

        with g as dest_file:
            with f as source_file:
                for line in source_file:
                    element = json.loads(line.strip())
                    if RemoveName in element:
                        del element[RemoveName]
                    dest_file.write(json.dumps(element))
        f.close()
        g.close()

        os.remove(r'./coordinates.txt')
        os.rename(r'./coordinates_new.txt', r'./coordinates.txt')


def main():
    app = App()
    app.eval('tk::PlaceWindow . center')
    app.mainloop()
    app.bind('<Escape>', sys.exit())


if __name__ == '__main__':
    main()
