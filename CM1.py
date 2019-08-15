import sys
import os
import tkinter as tk
from tkinter import messagebox as msb
from tkinter import filedialog
from PIL import ImageTk, Image
from functools import partial


root = tk.Tk()
root.title("Copy Master 5000")
root.configure(background='#64727f')


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


logo_path = resource_path("Images/icon-clipboard.png")
icon_path = resource_path("Images/CM_Icon.png")
input_path = resource_path("Data/input.txt")

icon = ImageTk.PhotoImage(Image.open(icon_path))
panel = tk.Label(root, image=icon)
panel.grid(row=1, column=1, columnspan=3)

with open(input_path, 'r', encoding="UTF-8") as f:
    inputs = []
    for line in f:
        line = line.strip()
        inputs.append(line)

current_range = len(inputs)
buttons = []
photos = []
entries = []


def create():
    for i in range(current_range):
        entries.append(tk.Text(root, width=25, height=1))
        entries[i].grid(row=3 + i, column=2, columnspan=3, padx=10, pady=5)
        buttons.append(tk.Button(root))
        photos.append(tk.PhotoImage(file=logo_path))
        action_with_arg = partial(copy, entries[i])
        buttons[i].config(image=photos[i], width="35", height="35", bg="#bdf2f5", command=action_with_arg)
        buttons[i].grid(row=3 + i, column=1, padx=5, pady=5)


def insert():
    if current_range <= 20:
        for j in range(current_range):
            entries[j].insert("1.0", inputs[j])
    else:
        for j in range(20):
            entries[j].insert("1.0", inputs[j])
        msb.showinfo("Out of scope", "Only 20 lines allowed in current version! Please adjust input file")


def copy(entry):
    text = entry.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)


def save():
    save_list = []
    for k in range(current_range):
        save_list.append(entries[k].get("1.0", tk.END))

    with open(input_path, 'w', encoding="UTF-8") as f:
        for item in save_list:
            f.write("%s" % item)


def on_top():
    root.lift()
    root.call('wm', 'attributes', '.', '-topmost', True)


def open_file():
    root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                               filetypes=(("jpeg files", "*.jpg"), ("all files", "*.*")))


menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=create)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save)
filemenu.add_command(label="Save as...")
filemenu.add_command(label="Load", command=insert)
filemenu.add_command(label="Close")
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

editmenu = tk.Menu(menubar, tearoff=0)
editmenu.add_command(label="Undo")
editmenu.add_separator()
editmenu.add_command(label="Cut")
editmenu.add_command(label="Copy")
editmenu.add_command(label="Paste")
editmenu.add_command(label="Delete")
editmenu.add_command(label="Select All")
menubar.add_cascade(label="Edit", menu=editmenu)

viewmenu = tk.Menu(menubar, tearoff=0)
viewmenu.add_command(label="On Top", command=on_top)
menubar.add_cascade(label="View", menu=viewmenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="Help Index")
helpmenu.add_command(label="About...")
menubar.add_cascade(label="Help", menu=helpmenu)


root.config(menu=menubar)

root.mainloop()
