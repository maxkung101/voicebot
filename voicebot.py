#!/usr/bin/env python3
import time, pygame.mixer, random, copy, os
import tkinter as tk
import speech_recognition as sr
import numpy as np
import sounddevice as sd
from tkinter import messagebox, ttk

def getName():
    voices_app = open("settings.csv", "r")
    data = []
    data_line = voices_app.readline().split(',')
    data.append(data_line)
    voices_app.close()
    return data[0][0]

# Set up GUI
root=tk.Tk()
width_value = root.winfo_screenwidth()
height_value = root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (width_value, height_value))
root.resizable(False, False)
root.title("Voicebot")
root.configure(background="#4a4a4a")

# Set up microphone
r = sr.Recognizer()
m = sr.Microphone()
heard = False

# Set up settings
options = [ "Frankie", "Captain Falcon Yes", "Crystal"]
clicked = tk.StringVar()

# Check if memory file exists.
try:
    clicked.set(getName())
except:
    clicked.set("Frankie")
    f = open("settings.csv", "w")
    f.write("Frankie")
    f.close()

sounds = pygame.mixer
sounds.init()

# Frankie voice clips
hello_fra = sounds.Sound("wav/frankie/hello/hello.wav")
frankie = []
frankieDIR = "wav/frankie/core/"
frankieDirectory = os.fsencode(frankieDIR)
for file in os.listdir(os.fsencode(frankieDirectory)):
     filename = os.fsdecode(file)
     if filename.endswith(".wav"):
         frankie.append(sounds.Sound(frankieDIR + filename))
         continue
     else:
         continue

# Captain Falcon voice clips
hello_fal = sounds.Sound("wav/falcon/hello/c-falcon_HELLO.wav")
falcon = []
falconDIR = "wav/falcon/core/"
falconDirectory = os.fsencode(falconDIR)
for file in os.listdir(os.fsencode(falconDirectory)):
     filename = os.fsdecode(file)
     if filename.endswith(".wav"):
         falcon.append(sounds.Sound(falconDIR + filename))
         continue
     else:
         continue

# Crystal voice clips
hello_cry = sounds.Sound("wav/crystal/hello/hello.wav")
crystal = []
crystalDIR = "wav/crystal/core/"
crystalDirectory = os.fsencode(crystalDIR)
for file in os.listdir(os.fsencode(crystalDirectory)):
     filename = os.fsdecode(file)
     if filename.endswith(".wav"):
         crystal.append(sounds.Sound(crystalDIR + filename))
         continue
     else:
         continue

startLenny = False
temp = 0

def audio_callback(indata, frames, time, status):
    global heard
    volume_norm = np.linalg.norm(indata) * 10
    soundlevel = int(volume_norm)
    if heard:
        pass
    else:
        if soundlevel > 10:
            heard = True
        else:
            pass

def playHello(line):
    if line == "Captain Falcon Yes":
        hello_fal.play()
        temp = hello_fal.get_length()
    elif line == "Crystal":
        hello_cry.play()
        temp = hello_cry.get_length()
    else:
        hello_fra.play()
        temp = hello_fra.get_length()
    while temp>0:
        root.update()
        time.sleep(1)
        temp -= 1

def sayIt(line):
    if line == "Captain Falcon Yes":
        x = random.randint(0, len(falcon)-1)
        falcon[x].play()
        temp = falcon[x].get_length()
    elif line == "Crystal":
        x = random.randint(0, len(crystal)-1)
        crystal[x].play()
        temp = crystal[x].get_length()
    else:
        x = random.randint(0, len(frankie)-1)
        frankie[x].play()
        temp = frankie[x].get_length()
    while temp>0:
        root.update()
        time.sleep(1)
        temp -= 1

def lennyMain():
    global startLenny
    if startLenny:
        startLenny = False
        sounds.stop()
        btn_text.set("Start")
        my_notebook.tab(1,state="normal")
        entry_text.set("Push button to start")
        temp = 0
    else:
        btn_text.set("Stop")
        my_notebook.tab(1,state="disabled")
        entry_text.set("Starting " + getName())
        startLenny = True
        playHello(getName())
        if startLenny: entry_text.set("Spammer's turn to talk")
        randomLine()

def randomLine():
    global heard
    root.update()
    if startLenny:
        if heard:
            with m as source:
                #adjust for ambient noise
                r.adjust_for_ambient_noise(source)
                audio = r.listen(source)
            if startLenny:
                entry_text.set(getName() + " is speaking")
                sayIt(getName())
                heard = False
            else:
                sounds.stop()
                temp = 0
            if startLenny:
                entry_text.set("Spammer's turn to talk")
                randomLine()
            else:
                sounds.stop()
                temp = 0
        else:
            stream = sd.InputStream(callback=audio_callback)
            with stream:
               sd.sleep(1000)
            randomLine()
    else:
        sounds.stop()
        temp = 0

def changeVoice(value):
    f = open("settings.csv", "w")
    f.write(value)
    f.close()

def on_closing():
    global startLenny
    startLenny = False
    sounds.stop()
    root.destroy()

class MyDialog:

    def __init__(self, parent):
        global width_value, height_value
        top = self.top = tk.Toplevel(parent)
        self.top.geometry("%dx%d+0+0" % (width_value-50, height_value-50))
        self.top.configure(background="#4f4f4f")
        self.titleLabel = tk.Label(top, text="About", font="arial 20", background="#4f4f4f", fg="white")
        self.titleLabel.pack()
        self.title2Label = tk.Label(top, text="Credits", font="arial 20 bold", background="#4f4f4f", fg="white")
        self.title2Label.pack()
        self.myLabel = tk.Label(top, text="Programmed by Max Kung", font="arial 16", background="#4f4f4f", fg="white")
        self.myLabel.pack()
        self.title3Label = tk.Label(top, text="Voices", font="arial 20 bold", background="#4f4f4f", fg="white")
        self.title3Label.pack()
        self.myLabel2 = tk.Label(top, text="Max Kung", font="arial 16", background="#4f4f4f", fg="white")
        self.myLabel2.pack()
        self.myLabel3 = tk.Label(top, text="Nintendo Co., Ltd.", font="arial 16", background="#4f4f4f", fg="white")
        self.myLabel3.pack()
        self.myCloseButton = tk.Button(top, text="Close", font="arial 16", background="#111111", fg="white", border=0, command=self.top.destroy, width = 10, height = 2)
        self.myCloseButton.pack()

def aboutClick():
    inputDialog = MyDialog(root)
    root.wait_window(inputDialog.top)

style = ttk.Style()
style.theme_create( "MyStyle", parent="alt", settings={
        "TNotebook": {"configure": {"tabmargins": [0, 0, 0, 0] } },
        "TNotebook.Tab": {"configure": {"padding": [40, 20], "font" : ('arial', '15') }, }})
style.theme_use("MyStyle")

my_notebook = ttk.Notebook(root, width=200, height=200)
my_notebook.pack()

my_frame1 = tk.Frame(my_notebook, width=width_value-2, height=height_value-2, bg="#4a4a4a")
my_frame2 = tk.Frame(my_notebook, width=width_value-2, height=height_value-2, bg="#4a4a4a")

my_frame1.pack()
my_frame2.pack()

my_notebook.add(my_frame1, text="Home")
my_notebook.add(my_frame2, text="Settings")

#name
name=tk.Label(my_frame1,text="Voicebot",font="arial 30 bold",background="#4a4a4a",fg="white").pack()

#entry box
entry_text = tk.StringVar()
entry=tk.Label(my_frame1,textvariable=entry_text,font="arial 15",background="#4a4a4a",fg="white").pack()
entry_text.set("Push button to start")

#button
btn_text = tk.StringVar()
btn=tk.Button(my_frame1,font="arial 20",textvariable=btn_text,background="#111111",fg="white",border=0,command=lennyMain, width = 10,height = 2).pack()
btn_text.set("Start")

#dropdown
name_drop=tk.Label(my_frame2,text="Voice: ",font="arial 16 bold",background="#4a4a4a",fg="white").grid(row=0,column=0)
drop = tk.OptionMenu(my_frame2, clicked, *options, command=changeVoice).grid(row=0,column=1)

#about button
abtn_text = tk.StringVar()
abtn=tk.Button(my_frame2,font="arial 20",textvariable=abtn_text,background="#111111",fg="white",border=0, command=aboutClick, width = 10,height = 2).grid(row=2,column=1)
abtn_text.set("About")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
