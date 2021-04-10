"""
(c) Copyright 2021 MJA Software
"""


import time
from datetime import datetime as dt
import pyautogui
try:
    import tkinter as tk
    from tkinter import ttk
except ImportError:
    import Tkinter as tk
    from Tkinter import ttk


# Default keyboard button 'shift'
BUTTON_NAME = 'shift'
# Default interval between key presses 2 minutes
INTERVAL_BUTTON_PRESS = 120
pyautogui.FAILSAFE = False


class ButtonPresser:
    clock = True

    def __init__(self, parent):
        self.parent = parent
        self.start_time = time.time()
        self.elapsed_time = time.strftime('%H:%M:%S', time.gmtime(0))
        self.button_name = BUTTON_NAME
        self.interval_button_press = tk.IntVar(parent, INTERVAL_BUTTON_PRESS)

        default_index = pyautogui.KEYBOARD_KEYS.index(self.button_name)

        self.combo_box = ttk.Combobox(parent, values=pyautogui.KEYBOARD_KEYS, font="Arial 20", width=10)
        self.combo_box.place(relx=0.25, rely=0.1, anchor=tk.CENTER)
        # self.combo_box.place(x=20, y=10)
        self.combo_box.current(default_index)

        validation_command = (parent.register(seconds_validation), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        self.entry_interval = tk.Entry(parent, validate='key', validatecommand=validation_command,
                                       textvariable=self.interval_button_press, font="Arial 20", width=10)
        self.entry_interval.place(relx=0.75, rely=0.1, anchor=tk.CENTER)

        # label displaying time
        self.label_time = tk.Label(parent, font="Arial 30", width=20)
        self.label_time.place(relx=0.5, rely=0.3, anchor=tk.CENTER)
        # self.label.pack()

        self.text_button_press = tk.StringVar(parent, f"Not Pressing {self.button_name}")
        self.label_pressed = tk.Label(parent, textvariable=self.text_button_press, font="Arial 20", width=20,
                                      fg='gray', bg='light gray')
        self.label_pressed.place(relx=0.5, rely=0.55, anchor=tk.CENTER)

        self.button_start = tk.Button(parent, text='Start', command=self.on_start, font="Arial 25", width=10,
                                      fg='green')
        self.button_start.place(relx=0.25, rely=0.78, anchor=tk.CENTER)

        self.button_stop = tk.Button(parent, text='Stop', command=self.on_stop, state='disabled', font="Arial 25",
                                     width=10, fg='red')
        self.button_stop.place(relx=0.75, rely=0.78, anchor=tk.CENTER)

        label_about = tk.Label(parent, text='(c) copyright 2021 MJA Software')
        label_about.place(relx=0.5, rely=0.95, anchor=tk.CENTER)

    def refresh_label(self):
        """ refresh the content of the label every second """
        seconds = (time.time() - self.start_time)
        self.elapsed_time = time.strftime('%H:%M:%S', time.gmtime(seconds))

        seconds = int(seconds)

        interval = int(self.interval_button_press.get())

        if seconds % interval == 0:
            pyautogui.press(self.button_name)
            self.text_button_press.set(f"Pressing {self.button_name}")
            self.label_pressed.configure(fg='red', bg='yellow')
            # print(f"Pressing: {self.button_name}")
        else:
            self.text_button_press.set(f"Not Pressing {self.button_name}")
            self.label_pressed.configure(fg='gray', bg='light gray')

        # display the new time
        self.label_time.configure(text=f"Elapsed Time: {self.elapsed_time}")

        # request tkinter to call self.refresh after 1s (the delay is given in ms)
        if self.clock:
            self.label_time.after(1000, self.refresh_label)

    def on_start(self):
        self.button_start.configure(state='disabled')
        self.button_stop.configure(state='normal')
        # start the timer
        self.clock = True
        self.start_time = time.time()
        self.label_time.after(1000, self.refresh_label)
        self.button_name = self.combo_box.get()
        self.combo_box.configure(state='disabled')
        self.entry_interval.configure(state='disabled')
        print('onstart', self.interval_button_press.get())

    def on_stop(self):
        self.button_stop.configure(state='disabled')
        self.button_start.configure(state='normal')
        self.combo_box.configure(state='normal')
        self.entry_interval.configure(state='normal')
        self.clock = False
        with open('log.txt', 'a') as file:
            file.write(f"{dt.now()} -> Elapsed Time: {self.elapsed_time}\n")


# def seconds_validation(action, index, value_if_allowed, prior_value, text,
#                        validation_type, trigger_type, widget_name):
def seconds_validation(_, __, value_if_allowed, ___, ____, _____, ______, _______):
    """Validates if correct value for seconds is being inserted in Entry"""
    try:
        value = int(value_if_allowed)
        if value <= 0 or value > 86400:
            return False
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    root = tk.Tk()
    size_x = 500
    size_y = 300
    pos_x = 40
    pos_y = 20
    root.wm_geometry("%dx%d+%d+%d" % (size_x, size_y, pos_x, pos_y))
    root.title("Auto Presser")
    # root.iconbitmap('icon.ico')

    timer = ButtonPresser(root)
    root.mainloop()
