# -*- coding: utf-8 -*-
"""
Created on Thu Jun 11 23:12:55 2020

@author: Project-C
"""

from pynput import keyboard
from time import sleep
import threading
from playsound import playsound


def doit(args):
    t = threading.currentThread()
    while getattr(t, "do_run", True):
        playsound('audio.mp3')
        print('Global hotkey activated!')
        sleep(90)
    print("Stopping as you wish.")
    
thread = threading.Thread(target=doit, args=("task",))

def on_activate():
    global thread
    thread = threading.Thread(target=doit, args=("task",))
    thread.start()

def on_deactivate():
    thread.do_run = False
    thread.join()


with keyboard.GlobalHotKeys({
        '<ctrl>+<alt>+f': on_activate,
        '<ctrl>+<alt>+h': on_deactivate}) as h:
    h.join()