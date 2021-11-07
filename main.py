from tkinter import *
from tkinter import messagebox
from platform import system
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image


FIRST_IMAGE = ""
SECOND_IMAGE = ""


platformD = system()
if platformD == 'Darwin':

    app_icon = "icons/icons8-image.icns"

elif platformD == 'Windows':

    app_icon = "icons/icons8-image.ico"

else:

    app_icon = "icons/icons8-image.ico"


def openFirstImage():
    global FIRST_IMAGE
    canvas1 = Canvas(window, height=512, width=512)
    canvas1.pack()
    FIRST_IMAGE = askopenfilename()
    first = ImageTk.PhotoImage(Image.open(FIRST_IMAGE))
    window.first = first
    canvas1.create_image((0, 0), anchor="nw", image=first)


def openSecondImage():
    global SECOND_IMAGE
    SECOND_IMAGE = askopenfilename()


def show_about():
    messagebox.showinfo("Made By Roman Yaschenko")


counter = 0
window = Tk()
window.title("Image Test App")
window.geometry("1000x700")
window.iconbitmap(app_icon)
main_menu = Menu()
main_menu.add_cascade(label="About", command=show_about)
button1 = Button(text="First Image",
                 font="16",
                 justify="center",
                 command=openFirstImage)
button1.place(relx=0.2, rely=0.7, anchor="w", width=130, bordermode=OUTSIDE)
button2 = Button(text="Second Image",
                 font="16",
                 justify="center",
                 command=openSecondImage)
button2.place(relx=0.8, rely=0.7, anchor="e", width=130, bordermode=OUTSIDE)

window.config(menu=main_menu)
window.mainloop()
