from tkinter import * 
from main import *


root = Tk()
root.title("Emil A1-F6 IQ Spel!")
root.geometry("960x620")

my_frame = Frame(root)
my_frame.pack(pady=10)


entry = Entry(root, width=20, font=("Helvetica", 20))
entry.pack(side=BOTTOM)


root.mainloop()
