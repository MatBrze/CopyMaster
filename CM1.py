import sys
import os
import tkinter as tk
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
initial_path = resource_path("Data/input.txt")

icon = ImageTk.PhotoImage(Image.open(icon_path))
panel = tk.Label(root, image=icon)
panel.grid(row=1, column=1, columnspan=3)
initial_length = 10
buttons = []
photos = []
entries = []


def initial():
    create_widgets(initial_length)
    insert(initial_path)


def inputs_list(path=initial_path):
    with open(path, 'r', encoding="UTF-8") as f:
        inputs = []
        for line in f:
            line = line.strip()
            inputs.append(line)
    return inputs


def create_widgets(number_of_entries):
    for i in range(number_of_entries):
        entries.append(tk.Text(root, width=25, height=1))
        entries[i].grid(row=3 + i, column=2, columnspan=3, padx=10, pady=5)
        buttons.append(tk.Button(root))
        photos.append(tk.PhotoImage(file=logo_path))
        action_with_arg = partial(copy, entries[i])
        buttons[i].config(image=photos[i], width="35", height="35", bg="#bdf2f5", command=action_with_arg)
        buttons[i].grid(row=3 + i, column=1, padx=5, pady=5)


current_range = len(inputs_list())
# create_widgets_command = partial(create_widgets, current_range)


def remove():
    for w in list(root.children.values()):
        print(w)


def insert(path):
    for j in range(len(inputs_list(path))):
        entries[j].insert("1.0", inputs_list(path)[j])


# insert_from_path = partial(insert, input_path)


def copy(entry):
    text = entry.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)


def save():
    save_list = []
    for k in range(current_range):
        save_list.append(entries[k].get("1.0", tk.END))

    with open(initial_path, 'w', encoding="UTF-8") as f:
        for item in save_list:
            f.write("%s" % item)


def on_top():
    root.lift()
    root.call('wm', 'attributes', '.', '-topmost', True)


def off_top():
    root.lift()
    root.call('wm', 'attributes', '.', '-topmost', False)


def open_file():
    try:
        root.filename = filedialog.askopenfilename(initialdir="/", title="Select file",
                                                   filetypes=(("text files", "*.txt"), ("all files", "*.*")))
        inputs_list(root.filename)
        length = len(inputs_list(root.filename))
        create_widgets(length)
        insert(root.filename)
    except FileNotFoundError:
        pass


menubar = tk.Menu(root)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=initial)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

viewmenu = tk.Menu(menubar, tearoff=0)
viewmenu.add_command(label="On Top", command=on_top)
viewmenu.add_command(label="Off Top", command=off_top)
menubar.add_cascade(label="View", menu=viewmenu)


root.config(menu=menubar)

initial()
root.mainloop()
