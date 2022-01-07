from tkinter import *
from tkinter import messagebox
from platform import system
from tkinter.filedialog import askopenfilename
from PIL import ImageTk, Image
from math import log10, sqrt
import cv2
import numpy as np

FIRST_IMAGE = ""
SECOND_IMAGE = ""

platformD = system()
if platformD == 'Darwin':

    app_icon = "icons/icons8-image.icns"

elif platformD == 'Windows':

    app_icon = "icons/icons8-image.ico"

else:

    app_icon = "icons/icons8-image.ico"

