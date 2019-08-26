import sys
import os
import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
from functools import partial


root = tk.Tk()
root.title("Copy Master 5000")


def _on_mousewheel(event):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")


menu_frame = tk.Frame(root)
menu_frame.grid(row=0, column=1, columnspan=3, sticky='N,W')

logo_frame = tk.Frame(root)
logo_frame.grid(row=1, column=1, columnspan=3)

frame_canvas = tk.Frame(root)
frame_canvas.configure(background='#64727f')
frame_canvas.grid(row=3, column=1)

canvas = tk.Canvas(frame_canvas)
canvas.grid(row=0, column=1, sticky='news')
root.bind_all("<MouseWheel>", _on_mousewheel)


scrollbar = tk.Scrollbar(frame_canvas, orient="vertical")
scrollbar.grid(row=0, column=3, sticky='ns')

widgets_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=widgets_frame, anchor='nw')


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


logo_path = resource_path("Images/icon-clipboard.png")
icon_path = resource_path("Images/CM_Icon.png")
initial_path = resource_path("Data/input.txt")

icon = ImageTk.PhotoImage(Image.open(icon_path))
panel = tk.Label(logo_frame, image=icon)
panel.grid(row=0, column=1, columnspan=3)
initial_length = 10
entries = []
buttons = []
photos = []


def new():
    for w in list(widgets_frame.children.values()):
        w.grid_forget()
    canvas.config(width=270, height=55)
    no_entries_label = tk.Label(widgets_frame, text="Number of entries to create:")
    no_entries_label.grid(row=0, column=2)

    no_entries = tk.Entry(widgets_frame)
    no_entries.grid(row=1, column=2, padx=10, pady=5)

    create_button = tk.Button(widgets_frame, text="Create", bg="#bdf2f5")
    create_button.grid(row=1, column=1, padx=10, pady=5)

    def set_create():
        try:
            create_widgets(int(no_entries.get()))
        except ValueError:
            action_with_arg = partial(create_widgets, 10)
            create_button.config(command=action_with_arg)

    create_button.config(command=set_create)
    remove()


def initial():
    try:
        remove()
    except IndexError:
        pass
    create_widgets(check_length(initial_path))
    insert(initial_path)


def inputs_list(path=initial_path):
    with open(path, 'r', encoding="UTF-8") as f:
        inputs = []
        for line in f:
            line = line.strip()
            inputs.append(line)
    return inputs


def check_length(path=initial_path):
    return len(inputs_list(path))


def create_widgets(number_of_entries):
    global entries, buttons
    entries = []
    buttons = []
    for w in list(widgets_frame.children.values()):
        w.grid_forget()
    for i in range(number_of_entries):
        entries.append(tk.Text(widgets_frame, width=25, height=1))
        entries[i].grid(row=0 + i, column=2, columnspan=3, padx=10, pady=5)
        buttons.append(tk.Button(widgets_frame))
        photos.append(tk.PhotoImage(file=logo_path))
        action_with_arg = partial(copy, entries[i])
        buttons[i].config(image=photos[i], width="35", height="35", bg="#bdf2f5", command=action_with_arg)
        buttons[i].grid(row=0 + i, column=1, padx=5, pady=5)
        root.update()
    if number_of_entries >= 10:
        canvas.config(width=270, height=510)
        scrollbar.config(command=canvas.yview)
        canvas.config(scrollregion=canvas.bbox("all"))
    else:
        canvas_size = number_of_entries * 51
        canvas.config(width=270, height=canvas_size)
        scrollbar.config(command=canvas.yview)
        canvas.config(scrollregion=canvas.bbox("all"))


def remove():
    for j in entries:
        j.delete("1.0", tk.END)


def insert(path):
    for j in range(check_length(path)):
        entries[j].insert("1.0", inputs_list(path)[j])
    # reset()


def copy(entry):
    text = entry.get("1.0", tk.END).strip()
    root.clipboard_clear()
    root.clipboard_append(text)


def save():
    save_list = []
    for k in entries:
        save_list.append(k.get("1.0", tk.END))

    with open(initial_path, 'w', encoding="UTF-8") as f:
        for item in save_list:
            f.write("%s" % item)
    f.close()


def save_as():
    f = filedialog.asksaveasfile(mode='w', defaultextension=".txt")
    if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
        return
    save_list = []
    for k in entries:
        save_list.append(k.get("1.0", tk.END))
    for item in save_list:
        f.write("%s" % item)
    f.close()


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
        remove()
        insert(root.filename)
    except FileNotFoundError:
        pass


menubar = tk.Menu(menu_frame)

filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="New", command=new)
filemenu.add_command(label="Clear", command=remove)
filemenu.add_command(label="Open", command=open_file)
filemenu.add_command(label="Save", command=save)
filemenu.add_command(label="Save as...", command=save_as)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=root.quit)
menubar.add_cascade(label="File", menu=filemenu)

viewmenu = tk.Menu(menubar, tearoff=0)
viewmenu.add_command(label="On Top", command=on_top)
viewmenu.add_command(label="Off Top", command=off_top)
menubar.add_cascade(label="View", menu=viewmenu)

initial()
root.config(menu=menubar)

root.mainloop()
