import os
import time
from tkinter import *
import cv2
import pytesseract

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
root = Tk()
root.title("OCR")
pad = 3
# root.attributes("-fullscreen", True)
# root.state("zoomed")
mylabel = Label(root, text="Enter the path of the screenshot... use '/' instead of '\\'")
mylabel.pack(pady=50, padx=250)
e = Entry(root, width=75)
e.pack()
thelabel = Label(root, text="What will the name of the file be?")
thelabel.pack(pady=25, padx=300)
z = Entry(root, width=75)
z.pack()


def onclick():
    mylabel.config(text="okidoki. On it")
    path = e.get()
    images = os.listdir(path)
    file = open('C:/Users/Akash/Documents/' + z.get() + '.txt', 'w')
    for i in images:
        img = cv2.imread(path + '/' + i)
        text = pytesseract.image_to_string(img)
        file.write(text)
    file.close()
    mylabel.config(text="oki goshujin-sama! Its done!!")
    time.sleep(3)
    sys.exit()


button = Button(root, text="enter", pady=10, command=onclick)
button.pack()
root.mainloop()
