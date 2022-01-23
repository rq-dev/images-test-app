import tkinter
from tkinter import *
from tkinter import messagebox
from platform import system
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from math import log10, sqrt, log
import cv2
import numpy as np
import datetime
import os
from skimage import io
from sklearn.cluster import KMeans
from sklearn.utils import shuffle
import re
import matplotlib

FIRST_IMAGE = Image.open("Test_Images/image_Baboon512rgb.png")
SECOND_IMAGE = Image.open("Test_Images/image_Baboon512rgb.png")
COLORS = 256
RED = 3
GREEN = 4
BLUE = 3
OPTIONS = ["3 / 3 / 4", "3 / 4 / 3", "4 / 3 / 3"]

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
        original = FIRST_IMAGE
        o_pix = original.load()
    else:
        original = SECOND_IMAGE
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


def median_cut_quantize(img, img_arr):
    # when it reaches the end, color quantize
    r_average = np.mean(img_arr[:, 0])
    g_average = np.mean(img_arr[:, 1])
    b_average = np.mean(img_arr[:, 2])

    for data in img_arr:
        img[data[3]][data[4]] = [r_average, g_average, b_average]


def split_into_buckets(img, img_arr, depth):
    if len(img_arr) == 0:
        return

    if depth == 0:
        median_cut_quantize(img, img_arr)
        return

    r_range = np.max(img_arr[:, 0]) - np.min(img_arr[:, 0])
    g_range = np.max(img_arr[:, 1]) - np.min(img_arr[:, 1])
    b_range = np.max(img_arr[:, 2]) - np.min(img_arr[:, 2])

    space_with_highest_range = 0

    if g_range >= r_range and g_range >= b_range:
        space_with_highest_range = 1
    elif b_range >= r_range and b_range >= g_range:
        space_with_highest_range = 2
    elif r_range >= b_range and r_range >= g_range:
        space_with_highest_range = 0

    # sort the image pixels by color space with highest range
    # and find the median and divide the array.
    img_arr = img_arr[img_arr[:, space_with_highest_range].argsort()]
    median_index = int((len(img_arr) + 1) / 2)

    # split the array into two blocks
    split_into_buckets(img, img_arr[0:median_index], depth - 1)
    split_into_buckets(img, img_arr[median_index:], depth - 1)


def doMC(img):
    setCOLOR()
    global FIRST_IMAGE
    original = img.copy()
    saveImageWithName(img, 'bmp', 'tempmc')
    sample_img = io.imread('tempmc.bmp')
    deleteImage('tempmc.bmp')
    flattened_img_array = []
    colors = round(log(COLORS, 2))
    for rindex, rows in enumerate(sample_img):
        for cindex, color in enumerate(rows):
            flattened_img_array.append([color[0], color[1], color[2], rindex, cindex])

    flattened_img_array = np.array(flattened_img_array)

    # start the splitting process
    split_into_buckets(sample_img, flattened_img_array, colors)
    io.imsave('res.bmp', sample_img)
    image_final = Image.open('res.bmp')
    deleteImage("res.bmp")

    FIRST_IMAGE = image_final
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
    saveImageWithName(img, 'bmp', 'temptolgb')
    image_raw = io.imread('temptolgb.bmp')
    image = np.array(image_raw, dtype=np.float64) / 255
    h, w, d = image.shape
    image_array = np.reshape(image, (h * w, d))
    image_array_sample = shuffle(image_array, random_state=0)[:1000]
    kmeans = KMeans(n_clusters=COLORS).fit(image_array_sample)
    labels = kmeans.predict(image_array)
    image_out = np.zeros((h, w, d))
    label_idx = 0
    for i in range(h):
        for j in range(w):
            image_out[i][j] = kmeans.cluster_centers_[labels[label_idx]]
            label_idx += 1

    matplotlib.image.imsave('namelgbtemp.bmp', image_out)
    image_final = Image.open('namelgbtemp.bmp')
    deleteImage('namelgbtemp.bmp')
    deleteImage('temptolgb.bmp')
    FIRST_IMAGE = image_final
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


def doUQRGB(img):
    setCOLOR()
    global FIRST_IMAGE
    original = img.copy()
    pixels = img.load()
    bits = v_red.get()
    if bits == "3 / 3 / 4":
        b_r = 224
        b_g = 224
        b_b = 240
    elif bits == "3 / 4 / 3":
        b_r = 224
        b_g = 240
        b_b = 224
    elif bits == "4 / 3 / 3":
        b_r = 240
        b_g = 224
        b_b = 224

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            R, G, B = pixels[i, j]
            R = R & b_r
            G = G & b_g
            B = B & b_b
            # R = R & 128
            # G = G & 128
            # B = B & 128
            # print(bin(R), bin(G), bin(B))
            pixels[i, j] = (R, G, B)
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


def doUQY(img):
    setCOLOR()
    global FIRST_IMAGE
    original = img.copy()
    pixels = img.load()
    pixels_original = original.load()
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            R, G, B = pixels[i, j]
            y = int(((77 / 256 * R) + (150 / 256 * G) + (29 / 256 * B)))
            cb = int((144 / 256) * (B - y) + 128)
            cr = int((183 / 256) * (R - y) + 128)
            pixels[i, j] = (y, cb, cr)

    saveImageWithName(img, 'bmp', 't')
    img2 = Image.open('t.bmp')
    pixels = img2.load()
    deleteImage('t.bmp')
    bits = v_red.get()
    if bits == "3 / 3 / 4":
        b_r = 224
        b_g = 224
        b_b = 240
    elif bits == "3 / 4 / 3":
        b_r = 224
        b_g = 240
        b_b = 224
    elif bits == "4 / 3 / 3":
        b_r = 240
        b_g = 224
        b_b = 224

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            R, G, B = pixels[i, j]
            R = R & b_r
            G = G & b_g
            B = B & b_b
            # R = R & 128
            # G = G & 128
            # B = B & 128
            # print(bin(R), bin(G), bin(B))
            pixels[i, j] = (R, G, B)

    saveImageWithName(img, 'bmp', 't')
    img3 = Image.open('t.bmp')
    pixels = img2.load()
    deleteImage('t.bmp')
    for i in range(img.size[0]):
        for j in range(img.size[1]):
            R, G, B = pixels[i, j]
            y = int(((77 / 256 * R) + (150 / 256 * G) + (29 / 256 * B)))
            cb = int((144 / 256) * (B - y) + 128)
            cr = int((183 / 256) * (R - y) + 128)

            R = int(y + (256 / 183) * (cr - 128))
            G = int(y - (5329 / 15481) * (cb - 128) - (11103 / 15481) * (cr - 128))
            B = int(y + (256 / 144) * (cb - 128))
            pixels[i, j] = (R, G, B)
    # toRGB(FIRST_IMAGE, 0)
    FIRST_IMAGE = img3
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
button1 = Button(text="Load First Image",
                 font="16",
                 justify="center",
                 command=openFirstImage)
button1.grid(row=12, column=1, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
button_save_bmp_1 = Button(text="SAVE",
                           font="16",
                           justify="center",
                           command=lambda: saveImageToBMP(FIRST_IMAGE))
button_save_bmp_1.grid(row=13, column=1, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
button2 = Button(text="Load Second Image",
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
buttonUQ = Button(text="Uniform quantization RGB",
                          font="16",
                          justify="center",
                          command=lambda: doUQRGB(FIRST_IMAGE))
buttonUQ.grid(row=18, column=1, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
buttonUQY = Button(text="Uniform quantization Y",
                          font="16",
                          justify="center",
                          command=lambda: doUQY(FIRST_IMAGE))
buttonUQY.grid(row=18, column=2, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
entry = tkinter.Entry(window, bg="white", fg="black")
entry.grid(row=17, column=4, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
entry.insert(END, COLORS)
buttonReset = Button(text="Reset default",
                          font="16",
                          justify="center",
                          command=lambda: reset())
buttonReset.grid(row=18, column=4, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")
v_red = StringVar(window)
v_red.set(OPTIONS[0])
s_red = OptionMenu(window, v_red, *OPTIONS)
s_red.grid(row=17, column=5, padx=5, pady=5, columnspan=1, rowspan=1, sticky="w")

window.config(menu=main_menu)
# window.grid_columnconfigure(6, weight=2)
# window.grid_rowconfigure(30, weight=2)
window.mainloop()
