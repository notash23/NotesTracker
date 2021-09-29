from tkinter import *
import numpy as np
import cv2
from PIL import ImageGrab
import pytesseract
import pyautogui
import threading

pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
x: int = 0
x1: int
y: int
y1: int
prevText: str = ""
TypeOn = True
seeImage = True


def record():
    global prevText, x, y, x1, y1
    while seeImage:
        img = ImageGrab.grab(bbox=(x, y, x1, y1))
        img_np = np.array(img)
        frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(frame)
        Set = text.split()
        WriteSet = [word for word in Set if word not in prevText]
        WriteText = " ".join(WriteSet)
        if TypeOn:
            pyautogui.typewrite(WriteText)
        else:
            with open("C:\\Users\\Akash\\Documents\\write", 'w+') as f:
                f.write(WriteText)
                f.close()

        prevText = Set
        cv2.waitKey(300)
    sys.exit()


def images():
    global x1, y1
    # win = Window()
    # canvas = tk.Canvas(win, bg='white', highlightthickness=0)
    # canvas.pack(fill=BOTH, expand=True)
    # canvas.create_rectangle(x, y, x1, y1, outline="blue", fill="blue", tags="erect")
    # Window.launch()

    new = Tk()
    new.attributes("-fullscreen", True)
    new.wm_attributes('-transparentcolor', 'white')
    canvas = Canvas(new, bg='white', highlightthickness=0)
    canvas.pack(fill=BOTH, expand=True)
    canvas.create_rectangle(x, y, x1, y1, outline="black", fill="white", tags="erect", width=10)

    # TODO: add a custom title bar with x having a function call that destroy window and sets seeImage to False
    # TODO: handle newlines
    new_root = Toplevel()
    new_root["bg"] = "#3478F5"
    new_root.title("Copy Paster")
    new_root.geometry(f"500x300+0+0")

    Choice = Label(new_root, text="Choose which function should be used", font=("Helvetica", 18), fg="#862464",
                   bg="#3478F5")
    Choice.pack(pady=25)

    Chosen = Label(new_root, text="Type", font=("Helvetica", 18), fg="#862464",
                   bg="#3478F5")
    Chosen.pack(pady=25)

    def switch():
        global TypeOn

        # Determine is on or off
        if TypeOn:
            Type.config(text="Write")
            Chosen.config(text="Write")
            TypeOn = False
        else:
            Type.config(text="Type")
            Chosen.config(text="Type")
            TypeOn = True

    def startSetup():
        global seeImage
        new_root.destroy()
        new.destroy()
        seeImage = False
        setup()

    Type = Button(new_root, text="Type", pady=5, command=switch, bg="#3480F5", font=("Helvetica", 14))
    Type.pack()

    filler = Label(new_root,
                   bg="#3478F5")
    filler.pack(pady=5)

    reset = Button(new_root, text="Reset Region", pady=5, command=startSetup, bg="#3480F5", font=("Helvetica", 14))
    reset.pack()

    thread = threading.Thread(target=record)
    thread.start()

    new_root.mainloop()


def setup():
    def StartRect(event):
        global x, y
        if x:
            canvas.delete("erect")
        x, y = event.x, event.y

    def EndRect(event):
        global x, y, x1, y1
        x1, y1 = event.x, event.y
        DrawRect()

    def DrawRect():
        canvas.create_rectangle(x, y, x1, y1, outline="blue", fill="blue", tags="erect")

    def Done(event):
        if x1:
            SelectLayer.destroy()
            images()

    SelectLayer = Tk()
    SelectLayer.attributes("-fullscreen", True)
    SelectLayer.attributes("-alpha", 0.4)

    SelectLayer.wm_attributes('-transparentcolor', 'blue')
    canvas = Canvas(SelectLayer, bg='white', highlightthickness=0)
    canvas.pack(fill=BOTH, expand=True)
    SelectLayer.bind("<Button-1>", StartRect)
    SelectLayer.bind("<ButtonRelease>", EndRect)
    SelectLayer.bind('<Return>', Done)
    SelectLayer.mainloop()


def GetDASelectLayer():
    root.destroy()
    setup()


# TODO: Find a good color theme
root = Tk()
root["bg"] = "#3478F5"
root.title("Copy Paster")
root.geometry("500x200")

MainLabel = Label(root, text="Press the button below", font=("Helvetica", 18), fg="#862464", bg="#3478F5")
MainLabel.pack(pady=25)

button = Button(root, text="Select region", pady=10, command=GetDASelectLayer, bg="#3480F5")
button.pack()

root.mainloop()
