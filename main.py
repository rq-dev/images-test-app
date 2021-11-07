from tkinter import *
from tkinter import messagebox
from platform import system


platformD = system()
if platformD == 'Darwin':

    app_icon = "icons/icons8-image.icns"

elif platformD == 'Windows':

    app_icon = "icons/icons8-image.ico"

else:

    app_icon = "icons/icons8-image.ico"


def increase_counter():
    global counter
    counter += 1
    window.title("Image Test App {}".format(counter))


def show_about():
    messagebox.showinfo("GUI Python")


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
                 command=increase_counter)
button1.place(relx=0.2, rely=0.7, anchor="w", width=130, bordermode=OUTSIDE)
button2 = Button(text="Second Image",
                 font="16",
                 justify="center",
                 command=increase_counter)
button2.place(relx=0.8, rely=0.7, anchor="e", width=130, bordermode=OUTSIDE)

window.config(menu=main_menu)
window.mainloop()
