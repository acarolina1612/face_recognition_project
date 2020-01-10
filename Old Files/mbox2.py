import tkinter
import mbox

root = tkinter.Tk()

Mbox = mbox.Mbox
Mbox.root = root


Mbox('Tem certeza?')


root.mainloop()