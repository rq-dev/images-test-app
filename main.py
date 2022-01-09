import tkinter
from tkinter import *
from tkinter import messagebox
from platform import system
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from math import log10, sqrt
import cv2
import numpy as np
import datetime
import os

FIRST_IMAGE = Image.open("Test_Images/image_Baboon512rgb.png")
SECOND_IMAGE = Image.open("Test_Images/image_Baboon512rgb.png")
COLORS = 256

platformD = system()
if platformD == 'Darwin':

    app_icon = "icons/icons8-image.icns"

elif platformD == 'Windows':

    app_icon = "icons/icons8-image.ico"

else:

    app_icon = "icons/icons8-image.ico"


def reset():
    global FIRST_IMAGE
    global SECOND_IMAGE
    global COLORS
    FIRST_IMAGE = Image.open("Test_Images/image_Baboon512rgb.png")
    SECOND_IMAGE = Image.open("Test_Images/image_Baboon512rgb.png")
    entry.delete(0, "end")
    entry.insert(END, "256")
    initial()


def initial():
    canvas1 = Canvas(window, height=512, width=512)
    canvas2 = Canvas(window, height=512, width=512)
    canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
    canvas2.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
    first = ImageTk.PhotoImage(FIRST_IMAGE.resize((512, 512), Image.ANTIALIAS))
    window.first = first
    canvas1.create_image((0, 0), anchor="nw", image=first)
    second = ImageTk.PhotoImage(SECOND_IMAGE.resize((512, 512), Image.ANTIALIAS))
    window.second = second
    canvas2.create_image((0, 0), anchor="nw", image=second)


def openFirstImage():
    global FIRST_IMAGE
    canvas1 = Canvas(window, height=512, width=512)
    canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
    FIRST_IMAGE = Image.open(askopenfilename())
    first = ImageTk.PhotoImage(FIRST_IMAGE.resize((512, 512), Image.ANTIALIAS))
    window.first = first
    canvas1.create_image((0, 0), anchor="nw", image=first)


def openSecondImage():
    global SECOND_IMAGE
    canvas2 = Canvas(window, height=512, width=512)
    canvas2.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
    SECOND_IMAGE = Image.open(askopenfilename())
    second = ImageTk.PhotoImage(SECOND_IMAGE.resize((512, 512), Image.ANTIALIAS))
    window.second = second
    canvas2.create_image((0, 0), anchor="nw", image=second)


def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if mse == 0:
        return "INF"
    max_pixel = 255.0
    psnr = 20 * log10(max_pixel / sqrt(mse))
    return psnr


def saveImageToBMP(img):
    picture = img.save("{}.bmp".format(datetime.datetime.now()))


def saveImageWithName(img, ext, name):
    picture = img.save("{0}.{1}".format(name, ext))


def showPSNR():
    clearPSNR()
    saveImageWithName(FIRST_IMAGE, "bmp", "temp1")
    saveImageWithName(SECOND_IMAGE, "bmp", "temp2")
    original = cv2.imread("temp1.bmp")
    compressed = cv2.imread("temp2.bmp", 1)
    value = StringVar()
    value.set(str(PSNR(original, compressed)))
    label1 = Label(textvariable=value, fg="#eee", bg="#333")
    label1.grid(row=15, column=2, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
    deleteImage("temp1.bmp")
    deleteImage("temp2.bmp")


def clearPSNR():
    value = StringVar()
    value.set(str("                                       "))
    label1 = Label(textvariable=value, fg="#eee", bg="#333")
    label1.grid(row=15, column=2, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")


def show_about():
    messagebox.showinfo("Made By Roman Yaschenko")


def deleteImage(name):
    os.remove(name)


def toGrayEqual(img, c):
    global FIRST_IMAGE
    pixels = img.load()
    print(pixels)
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            R, G, B = pixels[i, j]
            y = int((int(R) + int(G) + int(B)) / 3)
            pixels[i, j] = (y, y, y)
    FIRST_IMAGE = img
    if c == 0:
        canvas1 = Canvas(window, height=512, width=512)
        canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
        first = ImageTk.PhotoImage(FIRST_IMAGE.resize((512, 512), Image.ANTIALIAS))
        window.first = first
        canvas1.create_image((0, 0), anchor="nw", image=first)
    else:
        canvas1 = Canvas(window, height=512, width=512)
        canvas1.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
        second = ImageTk.PhotoImage(FIRST_IMAGE.resize((512, 512), Image.ANTIALIAS))
        window.second = second
        canvas1.create_image((0, 0), anchor="nw", image=second)


def toGray(img, c):
    global SECOND_IMAGE
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            R, G, B = pixels[i, j]
            y = int(((77 / 256 * R) + (150 / 256 * G) + (29 / 256 * B)))
            pixels[i, j] = (y, y, y)
    SECOND_IMAGE = img
    if c == 0:
        canvas1 = Canvas(window, height=512, width=512)
        canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
        first = ImageTk.PhotoImage(SECOND_IMAGE.resize((512, 512), Image.ANTIALIAS))
        window.first = first
        canvas1.create_image((0, 0), anchor="nw", image=first)
    else:
        canvas1 = Canvas(window, height=512, width=512)
        canvas1.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
        second = ImageTk.PhotoImage(SECOND_IMAGE.resize((512, 512), Image.ANTIALIAS))
        window.second = second
        canvas1.create_image((0, 0), anchor="nw", image=second)


def toYCC(img, c):
    global FIRST_IMAGE
    global SECOND_IMAGE
    original = img.copy()
    pixels = img.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            R, G, B = pixels[i, j]
            y = int(((77 / 256 * R) + (150 / 256 * G) + (29 / 256 * B)))
            cb = int((144 / 256) * (B - y) + 128)
            cr = int((183 / 256) * (R - y) + 128)
            pixels[i, j] = (y, cb, cr)
    if c == 0:
        FIRST_IMAGE = img
        canvas1 = Canvas(window, height=512, width=512)
        canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
        first = ImageTk.PhotoImage(FIRST_IMAGE.resize((512, 512), Image.ANTIALIAS))
        window.first = first
        canvas1.create_image((0, 0), anchor="nw", image=first)
        SECOND_IMAGE = original
        canvas2 = Canvas(window, height=512, width=512)
        canvas2.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
        second = ImageTk.PhotoImage(SECOND_IMAGE.resize((512, 512), Image.ANTIALIAS))
        window.second = second
        canvas2.create_image((0, 0), anchor="nw", image=second)

    else:
        SECOND_IMAGE = img
        canvas2 = Canvas(window, height=512, width=512)
        canvas2.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
        second = ImageTk.PhotoImage(SECOND_IMAGE.resize((512, 512), Image.ANTIALIAS))
        window.second = second
        canvas2.create_image((0, 0), anchor="nw", image=second)
        FIRST_IMAGE = original
        canvas1 = Canvas(window, height=512, width=512)
        canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
        first = ImageTk.PhotoImage(FIRST_IMAGE.resize((512, 512), Image.ANTIALIAS))
        window.first = first
        canvas1.create_image((0, 0), anchor="nw", image=first)


def toRGB(img, c):
    global FIRST_IMAGE
    global SECOND_IMAGE
    pixels = img.load()
    if c == 0:
        original = SECOND_IMAGE
        o_pix = original.load()
    else:
        original = FIRST_IMAGE
        o_pix = original.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            R, G, B = o_pix[i, j]
            y = int(((77 / 256 * R) + (150 / 256 * G) + (29 / 256 * B)))
            cb = int((144 / 256) * (B - y) + 128)
            cr = int((183 / 256) * (R - y) + 128)

            R = int(y + (256 / 183) * (cr - 128))
            G = int(y - (5329 / 15481) * (cb - 128) - (11103 / 15481) * (cr - 128))
            B = int(y + (256 / 144) * (cb - 128))
            pixels[i, j] = (R, G, B)
    if c == 0:
        FIRST_IMAGE = img
        canvas1 = Canvas(window, height=512, width=512)
        canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
        first = ImageTk.PhotoImage(FIRST_IMAGE.resize((512, 512), Image.ANTIALIAS))
        window.first = first
        canvas1.create_image((0, 0), anchor="nw", image=first)
        canvas2 = Canvas(window, height=512, width=512)
        canvas2.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
        second = ImageTk.PhotoImage(original.resize((512, 512), Image.ANTIALIAS))
        window.second = second
        canvas2.create_image((0, 0), anchor="nw", image=second)
    else:
        SECOND_IMAGE = img
        canvas2 = Canvas(window, height=512, width=512)
        canvas2.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
        second = ImageTk.PhotoImage(SECOND_IMAGE.resize((512, 512), Image.ANTIALIAS))
        window.second = second
        canvas2.create_image((0, 0), anchor="nw", image=second)
        canvas1 = Canvas(window, height=512, width=512)
        canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
        first = ImageTk.PhotoImage(original.resize((512, 512), Image.ANTIALIAS))
        window.first = first
        canvas1.create_image((0, 0), anchor="nw", image=first)


def doMC(img):
    setCOLOR()
    global FIRST_IMAGE
    original = img.copy()
    img = img.quantize(COLORS, 0)
    FIRST_IMAGE = img
    canvas1 = Canvas(window, height=512, width=512)
    canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
    first = ImageTk.PhotoImage(FIRST_IMAGE.resize((512, 512), Image.ANTIALIAS))
    window.first = first
    canvas1.create_image((0, 0), anchor="nw", image=first)
    canvas2 = Canvas(window, height=512, width=512)
    canvas2.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
    second = ImageTk.PhotoImage(original.resize((512, 512), Image.ANTIALIAS))
    window.second = second
    canvas2.create_image((0, 0), anchor="nw", image=second)


def doLBG(img):
    setCOLOR()
    global FIRST_IMAGE
    original = img.copy()
    img = img.quantize(COLORS, 1)
    FIRST_IMAGE = img
    canvas1 = Canvas(window, height=512, width=512)
    canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
    first = ImageTk.PhotoImage(FIRST_IMAGE.resize((512, 512), Image.ANTIALIAS))
    window.first = first
    canvas1.create_image((0, 0), anchor="nw", image=first)
    canvas2 = Canvas(window, height=512, width=512)
    canvas2.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
    second = ImageTk.PhotoImage(original.resize((512, 512), Image.ANTIALIAS))
    window.second = second
    canvas2.create_image((0, 0), anchor="nw", image=second)


def doUQ(img):
    setCOLOR()
    global FIRST_IMAGE
    original = img.copy()
    img = img.quantize(COLORS, 2)
    FIRST_IMAGE = img
    canvas1 = Canvas(window, height=512, width=512)
    canvas1.grid(row=0, column=1, padx=5, pady=5, columnspan=2, rowspan=10, sticky="e")
    first = ImageTk.PhotoImage(FIRST_IMAGE.resize((512, 512), Image.ANTIALIAS))
    window.first = first
    canvas1.create_image((0, 0), anchor="nw", image=first)
    canvas2 = Canvas(window, height=512, width=512)
    canvas2.grid(row=0, column=4, padx=5, pady=5, columnspan=2, rowspan=10, sticky="w")
    second = ImageTk.PhotoImage(original.resize((512, 512), Image.ANTIALIAS))
    window.second = second
    canvas2.create_image((0, 0), anchor="nw", image=second)


def setCOLOR():
    global COLORS
    COLORS = int(entry.get())


counter = 0
window = Tk()
window.title("Image Test App")
window.geometry("1054x800")
window.maxsize(width=1054, height=800)
window.minsize(width=900, height=700)
window.iconbitmap(app_icon)
main_menu = Menu()
main_menu.add_cascade(label="About", command=show_about)
initial()
button1 = Button(text="First Image",
                 font="16",
                 justify="center",
                 command=openFirstImage)
button1.grid(row=12, column=1, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
button_save_bmp_1 = Button(text="SAVE",
                           font="16",
                           justify="center",
                           command=lambda: saveImageToBMP(FIRST_IMAGE))
button_save_bmp_1.grid(row=13, column=1, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
button2 = Button(text="Second Image",
                 font="16",
                 justify="center",
                 command=openSecondImage)
button2.grid(row=12, column=4, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
button_save_bmp_2 = Button(text="SAVE",
                           font="16",
                           justify="center",
                           command=lambda: saveImageToBMP(SECOND_IMAGE))
button_save_bmp_2.grid(row=13, column=4, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonGray = Button(text="To gray ew",
                    font="16",
                    justify="center",
                    command=lambda: toGrayEqual(FIRST_IMAGE, 0))
buttonGray.grid(row=14, column=1, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonGrayWeight = Button(text="To gray",
                          font="16",
                          justify="center",
                          command=lambda: toGray(SECOND_IMAGE, 1))
buttonGrayWeight.grid(row=14, column=4, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonPSNR = Button(text="PSNR",
                    font="16",
                    justify="center",
                    command=showPSNR)
buttonPSNR.grid(row=15, column=1, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonToYCC = Button(text="To YCC",
                          font="16",
                          justify="center",
                          command=lambda: toYCC(FIRST_IMAGE, 0))
buttonToYCC.grid(row=16, column=1, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonToRGB = Button(text="To RGB",
                          font="16",
                          justify="center",
                          command=lambda: toRGB(FIRST_IMAGE, 0))
buttonToRGB.grid(row=16, column=2, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonToYCC2 = Button(text="To YCC",
                          font="16",
                          justify="center",
                          command=lambda: toYCC(SECOND_IMAGE, 1))
buttonToYCC2.grid(row=16, column=4, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonToRGB2 = Button(text="To RGB",
                          font="16",
                          justify="center",
                          command=lambda: toRGB(SECOND_IMAGE, 1))
buttonToRGB2.grid(row=16, column=5, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonMC = Button(text="Median cut",
                          font="16",
                          justify="center",
                          command=lambda: doMC(FIRST_IMAGE))
buttonMC.grid(row=17, column=1, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonLBG = Button(text="LBG",
                          font="16",
                          justify="center",
                          command=lambda: doLBG(FIRST_IMAGE))
buttonLBG.grid(row=17, column=2, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonUQ = Button(text="Uniform quantization",
                          font="16",
                          justify="center",
                          command=lambda: doUQ(FIRST_IMAGE))
buttonUQ.grid(row=18, column=1, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
entry = tkinter.Entry(window, bg="white", fg="black")
entry.grid(row=17, column=4, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
entry.insert(END, COLORS)
buttonReset = Button(text="Reset default",
                          font="16",
                          justify="center",
                          command=lambda: reset())
buttonReset.grid(row=18, column=4, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
window.config(menu=main_menu)
# window.grid_columnconfigure(6, weight=2)
# window.grid_rowconfigure(30, weight=2)
window.mainloop()
