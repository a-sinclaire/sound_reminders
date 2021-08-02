from tkinter import ttk

from playsound import playsound
import time
import threading
import os
from infi.systray import SysTrayIcon
import tkinter as tk

LARGE_FONT = ("Verdana", 12)
NORM_FONT = ("Helvetica", 10)
SMALL_FONT = ("Helvetica", 8)


def popupmsg(msg):
    popup = tk.Tk()
    popup.wm_title("Sound Reminder Break Time!")
    label = ttk.Label(popup, text=msg, font=NORM_FONT)
    label.pack(side="top", fill="x", pady=10)
    B1 = ttk.Button(popup, text="Okay", command=popup.destroy)
    B1.pack()
    popup.mainloop()


def drink_thread(name, stop, mute):
    print("Thread {}: starting".format(name))
    while True:
        # every 15 minutes and play sip reminder noise
        time.sleep(15 * 60)
        if stop():
            break
        if not mute():
            playsound("D:/_Files/Programming/Python/soundReminders/Assets/sip.wav")
    print("Thread {}: finished".format(name))


def break_thread(name, stop, mute):
    print("Thread {}: starting".format(name))
    while True:
        # every 75 minutes and play break reminder
        time.sleep(75 * 60)
        if stop():
            break
        if not mute():
            playsound("D:/_Files/Programming/Python/soundReminders/Assets/bell.wav")
            popupmsg("Back From Break")
    print("Thread {}: finished".format(name))


STOP_THREADS = False
MUTE = False


def stop_program(systray):
    global STOP_THREADS
    STOP_THREADS = True


def mute_unmute(systray):
    global MUTE
    MUTE = not MUTE


if __name__ == "__main__":
    menu_options = (("Stop Sound Reminders", None, stop_program), ("MUTE/UNMUTE", None, mute_unmute),)
    systray = SysTrayIcon("D:/_Files/Programming/Python/soundReminders/Assets/alarm_check.ico", "Sound Reminders", menu_options)
    systray.start()

    x = threading.Thread(target=drink_thread, args=("drink_thread", lambda: STOP_THREADS, lambda: MUTE))
    x.start()
    y = threading.Thread(target=break_thread, args=("break_thread", lambda: STOP_THREADS, lambda: MUTE))
    y.start()

    x.join()
    y.join()

    systray.shutdown()
