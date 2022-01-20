#!/usr/bin/env python3
import time, pygame.mixer, random, copy
import tkinter as tk
import speech_recognition as sr
import numpy as np
import sounddevice as sd
from tkinter import messagebox, ttk
#from tkinter.messagebox import askyesno # For raspberry pi only
#from subprocess import call # For raspberry pi only

def getName():
    voices_app = open("settings.csv", "r")
    data = []
    data_line = voices_app.readline().split(',')
    data.append(data_line)
    voices_app.close()
    return data[0][0]

root=tk.Tk()
width_value = root.winfo_screenwidth()
height_value = root.winfo_screenheight()
root.geometry("%dx%d+0+0" % (width_value, height_value))
root.resizable(False, False)
root.title("Voicebot")
root.configure(background="#4a4a4a")

r = sr.Recognizer()
m = sr.Microphone()
heard = False

options = [ "Frankie", "Captain Falcon Yes"]
clicked = tk.StringVar()
clicked.set(getName())

sounds = pygame.mixer
sounds.init()

# Frankie voice clips
hello_fra = sounds.Sound("wav/frankie/hello.wav")
frankie = []
frankie.append(sounds.Sound("wav/frankie/company.wav"))
frankie.append(sounds.Sound("wav/frankie/goodday.wav"))
frankie.append(sounds.Sound("wav/frankie/hearing.wav"))
frankie.append(sounds.Sound("wav/frankie/imsorry.wav"))
frankie.append(sounds.Sound("wav/frankie/sayitagain.wav"))
frankie.append(sounds.Sound("wav/frankie/tellme.wav"))
frankie.append(sounds.Sound("wav/frankie/tellmemore.wav"))
frankie.append(sounds.Sound("wav/frankie/yeah.wav"))
frankie.append(sounds.Sound("wav/frankie/yes.wav"))

# Captain Falcon voice clips
hello_fal = sounds.Sound("wav/falcon/c-falcon_HELLO.wav")
falcon = []
falcon.append(sounds.Sound("wav/falcon/c-falcon_YES.wav"))

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
                audio = r.listen(source)
            if startLenny: 
                entry_text.set(getName() + " is speaking")
                sayIt(getName())
                heard = False
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

#def create_window(): # For raspberry pi only
    #answer = askyesno(title="Confirmation",
                      #message="Are you sure you want to power off?")
    #if answer:
        #call("sudo shutdown -h now", shell=True)

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

#power button - For raspberry pi only
#name_power=tk.Label(my_frame2,text="Power: ",font="arial 16 bold",background="#4a4a4a",fg="white").grid(row=1,column=0)
#powr_text = tk.StringVar()
#powr=tk.Button(my_frame2,font="arial 16",textvariable=powr_text,background="#111111",fg="white",border=0,command=create_window, width = 9,height = 1).grid(row=1,column=1)
#powr_text.set("Shutdown")

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
