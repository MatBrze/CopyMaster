import tkinter as tk
from PIL import ImageTk, Image

root = tk.Tk()
root.title("Copy Master 5000")
root.configure(background='#88CAD4')
logo_path = "C:/Users/mateu/PycharmProjects/CopyMaster/Images/icon-clipboard.png"
icon_path = "C:/Users/mateu/PycharmProjects/CopyMaster/Images/CM_Icon.png"
input_path = "C:/Users/mateu/PycharmProjects/CopyMaster/Data/input.txt"

icon = ImageTk.PhotoImage(Image.open(icon_path))
panel = tk.Label(root, image=icon)
panel.grid(row=1, column=1, columnspan=3)

root.mainloop()
