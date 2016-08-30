from Tkinter import *
from Tkinter import Tk
from main import main as main_go
from PIL import Image, ImageTk
import tkFileDialog
import ttk
pic_path = "helix.jpg"
fields = ('Threshold', 'Theta (degrees)', 'Midpoint Distance (angstrom)', 'Line Distance (angstrom)', 'Start at stage:')


def get_start(value):
    if value == "start":
        return 0
    elif value == "after_templates":
        return 1
    elif value == "after_correlation":
        return 2
    elif value == "after_graph":
        return 3
    elif value == "just_plot":
        return 4
    else:
        return 0


def gogo(entries):
    #   name = (entries['Session Name'].get())
    thresh = None if entries['Threshold'].get() == "default"  else (int(entries['Threshold'].get()))
    theta = (int(entries['Theta (degrees)'].get()))
    mid = (int(entries['Midpoint Distance (angstrom)'].get())) #todo
    line = (int(entries['Line Distance (angstrom)'].get())) #todo
    start = get_start(entries['Start at stage:'].get())
    path = tkFileDialog.askopenfilename()
    print(path)
    # messagebox.showinfo("Work in progress",
    #                     "Please wait till' it's done... You'll get a message (for now just click OK).")
    main_go(thresh, theta, mid, line, start, path)
    # messagebox.showinfo("Work is DONE!", "You may now enter another session folder.")


def makeform(root, fields):
    entries = {}
    cntr = 0
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=22, text=field + ": ", anchor='w')
        if cntr == 0:
            ent = Entry(row)
            ent.insert(0, "default")
        elif cntr == 1:
            ent = Entry(row)
            ent.insert(0, "20")
        elif cntr == 2:
            ent = Entry(row)
            ent.insert(0, "13")
        elif cntr == 3:
            ent = Entry(row)
            ent.insert(0, "4")
        elif cntr == 4:
            ent = ttk.Combobox(row)
            ent['values'] = ('start', 'after_templates','after_correlation', 'after_graph', 'just_plot')
            ent.insert(0, "start")
        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
        cntr += 1
    return entries

def main():
    root = Tk()
    root.wm_title("HelixIdentiPy (ver 0.1) - Find helices!")
    img = Image.open(pic_path)
    photo = ImageTk.PhotoImage(img)

    right_panel = Frame(root)
    left_panel = Frame(root)

    panel = Label(right_panel, image=photo)
    panel.pack(side=BOTTOM, fill="both", expand="yes")

    ents = makeform(left_panel, fields)
    b2 = Button(left_panel, text='GO!', command=(lambda e=ents: gogo(e)))
    b2.pack(side=BOTTOM, padx=5, pady=5)

    left_panel.pack(side=LEFT)
    right_panel.pack(side=RIGHT, expand="yes")

    # root.iconbitmap(r'helixico.ico')
    # root.iconname('helixico.ico')
    root.mainloop()

if __name__ == '__main__':
    main()

