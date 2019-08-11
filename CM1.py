import sys
import os
import tkinter as tk
from tkinter import messagebox as msb
from PIL import ImageTk, Image
from functools import partial

root = tk.Tk()
root.title("Copy Master 5000")
root.configure(background='#88CAD4')


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
        buttons[i].config(image=photos[i], width="35", height="35", bg="white", command=action_with_arg)
        buttons[i].grid(row=3 + i, column=1, padx=5, pady=5)

        b_save = tk.Button(root, bg="lightgreen")
        b_save.config(text='Save current entries', command=save)
        b_save.grid(row=22, column=1, columnspan=4, padx=5, pady=5)


def insert():
    if current_range <= 20:
        for j in range(current_range):
            entries[j].insert("1.0", inputs[j])
    else:
        for j in range(20):
            entries[j].insert("1.0", inputs[j])
        msb.showinfo("Out of scope", "Only 20 lines allowed in current version! Please adjust input file")


def copy(entry):
    text = entry.get("1.0", tk.END)
    root.clipboard_clear()
    root.clipboard_append(text)


def save():
    save_list = []
    for k in range(current_range):
        save_list.append(entries[k].get("1.0", tk.END))

    with open(input_path, 'w', encoding="UTF-8") as f:
        for item in save_list:
            f.write("%s" % item)


create()
insert()
root.mainloop()
