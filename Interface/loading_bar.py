import threading
import os
from Etapa_de_reconhecimento.return_path import return_path
from tkinter import Tk, ttk, Frame


class LoadBar(Frame):
    def __init__(self, root):
        Frame.__init__(self, root)

        w = 405
        h = 23
        ws = root.winfo_screenwidth()
        hs = root.winfo_screenheight()
        x = (ws / 2) - (w / 2)
        y = (hs / 2) - (h / 2)

        root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        root.resizable(0, 0)

        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)))
        icon_path = return_path(icon_path, 'faceicon.ico')
        Tk.iconbitmap(root, default=icon_path)
        Tk.wm_title(root, 'Carregando modelos')
        self.progress = ttk.Progressbar(self, orient="horizontal",
                                        length=400, mode="determinate")
        self.progress.pack(anchor='center', expand=1)

        self.bytes = 0
        self.maxbytes = 0

        self.progress["value"] = 0
        self.maxbytes = 50000
        self.progress["maximum"] = 50000
        self.read_bytes()

    def read_bytes(self):
        self.bytes += 250
        self.progress["value"] = self.bytes
        if self.bytes < self.maxbytes:
            # read more bytes after 100 ms
            self.after(100, self.read_bytes)
        else:
            self.master.destroy()


def run():
    root = Tk()
    c = LoadBar(root)
    c.pack()
    root.mainloop()


def main():
    t = threading.Thread(target=run)
    t.start()
    t.join()


if __name__ == '__main__':
    main()
