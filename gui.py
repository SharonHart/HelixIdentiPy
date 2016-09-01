from Tkinter import *
from main import main as main_go
from PIL import Image, ImageTk
import tkFileDialog
import ttk

icon_path = 'UI/icon.gif'
logo_path = "UI/logo.jpg"
fields = ('Threshold', 'Theta (degrees)', 'Midpoint Distance (angstrom)', 'Line Distance (angstrom)', 'Start at stage', 'MAP file')
input_path = None


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
    start = get_start(entries['Start at stage'].get())

    # messagebox.showinfo("Work in progress",
    #                     "Please wait till' it's done... You'll get a message (for now just click OK).")
    main_go(thresh, theta, mid, line, start, input_path)
    # messagebox.showinfo("Work is DONE!", "You may now enter another session folder.")


def makeform(root, fields):
    entries = {}
    cntr = 0
    for field in fields:
        row = Frame(root)
        lab = Label(row, width=35, text=field + ": ", anchor='w')
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
        elif cntr == 5:
            ent = Entry(row)
            ent.insert(0, "")

        row.pack(side=TOP, fill=X, padx=5, pady=5)
        lab.pack(side=LEFT)
        ent.pack(side=RIGHT, expand=YES, fill=X)
        entries[field] = ent
        cntr += 1
    return entries


def choose_file(e):
    global input_path
    input_path = tkFileDialog.askopenfilename()
    print "Reading File: " + input_path
    e['MAP file'].insert(0, input_path.split('/')[len(input_path.split('/'))-1])



def main():
    root = Tk()
    root.wm_title("HelixIdentiPy (ver 0.1) - Find helices!")

    # Set window icon
    icon = PhotoImage(file=icon_path)
    root.tk.call('wm', 'iconphoto', root._w, icon)

    # Instantiate top panel with logo
    img = Image.open(logo_path)
    photo = ImageTk.PhotoImage(img)
    top_panel = Frame(root)

    # Instantiate bottom panel with parameters
    botoom_panel = Frame(root)
    panel = Label(top_panel, image=photo)
    panel.pack(side=TOP, fill="both", expand="yes")
    ents = makeform(botoom_panel, fields)
    path_botton = Button(botoom_panel, text="Browse...", command=(lambda e=ents: choose_file(e)))
    path_botton.pack(padx=5, pady=5)
    go_button = Button(botoom_panel, text='GO!', command=(lambda e=ents: gogo(e)))
    go_button.pack(side=TOP, padx=0, pady=0)

    # Show panels
    top_panel.pack(side=TOP)
    botoom_panel.pack(side=BOTTOM, expand="yes")
    root.mainloop()

if __name__ == '__main__':
    main()

