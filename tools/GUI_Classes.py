import tkinter as tk
from tkinter import font, scrolledtext
from tkinter.constants import CENTER, NW, SW
from .FileHandler import File_Save
from PIL import Image, ImageTk
from . import Event_Manager
import threading

file_save = File_Save

class Import_Buttons():
    def __init__(self, window, fg, bg, width, height, placement:tuple, font:tuple, relief, text, command):
        self.button = tk.Button(master=window, text=text, fg=fg, bg=bg, width=width, height=height, font=font, relief=relief, command=command)
        self.button.place(x=placement[0], y=placement[1], anchor=CENTER)

class Frames():
    def __init__(self, window, bd_color, bg_color, width, height, position:tuple):
        self.bg_color = bg_color
        self.frame = tk.Frame(window, width=width, height=height, highlightthickness=1, highlightbackground=bd_color, highlightcolor=bd_color, bg=bg_color)
        self.frame.place(x=position[0], y=position[1], anchor=NW)

class Max_Threads():
    def __init__(self, window, min_val, max_val, default_val, size, position:tuple, bg_color, font):
        self.label = tk.Label(window, text='Max Threads', font=font, fg='white', bg=bg_color)
        self.label.place(x=120, y=20, anchor=CENTER)

        self.slider =  tk.Scale(window, from_=min_val, to=max_val, orient='horizontal', length=size, font=('default', 10), bg=bg_color, fg='white', troughcolor='white', highlightthickness=0)
        self.slider.set(default_val)
        self.slider.place(x=position[0], y=position[1] - 5, anchor=CENTER)

class Timeout():
    def __init__(self, frame, min_val, max_val, default_val, size, position:tuple, bg_color, font):
        self.timeout_label = tk.Label(frame, text='Timeout (MS)', font=font, bg=bg_color, fg='white')
        self.timeout_label.place(x=120, y=position[1] - 40, anchor=CENTER)
        
        self.timeout_scale = tk.Scale(frame, from_=min_val, to=max_val, length=size, bg=bg_color, orient='horizontal', highlightthickness=0, fg='white', troughcolor='white')
        self.timeout_scale.set(default_val)
        self.timeout_scale.place(x=position[0], y=position[1], anchor=CENTER)

class Proxyless():
    def __init__(self, frame, font, position:tuple):
        self.is_proxyless = tk.IntVar(value=0)

        self.checkbox = tk.Checkbutton(frame.frame, text='Proxyless', variable=self.is_proxyless, font=font, bg=frame.bg_color, fg='white', highlightthickness=0, activebackground=frame.bg_color, activeforeground='white', selectcolor=frame.bg_color)
        self.checkbox.place(x=position[0], y=position[1], anchor=CENTER)

class Checked():
    def __init__(self, frame, font, color, position):
        self.frame = frame
        self.checked = 0
        self.checked_text_var = tk.StringVar(value=f'Checked: {self.checked}')

        self.checked_text = tk.Label(frame.frame, font=font, bg=frame.bg_color, fg=color, textvariable=self.checked_text_var)
        self.checked_text.place(x=position[0], y=position[1], anchor=NW)

    def update_checked(self):
        self.checked += 1
        self.checked_text_var = tk.StringVar(value=f'Checked: {self.checked}')
        self.checked_text.config(textvariable=self.checked_text_var)

class Remaining():
    def __init__(self, frame, font, color, position:tuple):
        self.frame = frame
        self.remaining = 0
        self.remaining_text_var = tk.StringVar(value=f'Remaining: {self.remaining}')

        self.remaining_text = tk.Label(frame.frame, font=font, bg=frame.bg_color, fg=color, textvariable=self.remaining_text_var)
        self.remaining_text.place(x=position[0], y=position[1], anchor=NW)

    def update_remaining(self):
        self.remaining -= 1
        self.remaining_text_var = tk.StringVar(value=f'Remaining: {self.remaining}')
        self.remaining_text.config(textvariable=self.remaining_text_var)

    def start(self, amount):
        self.remaining = amount
        self.remaining_text_var = tk.StringVar(value=f'Remaining: {self.remaining}')
        self.remaining_text.config(textvariable=self.remaining_text_var)

class Hits():
    def __init__(self, frame, font, color, position:tuple):
        self.frame = frame
        self.hits = 0
        self.hits_text_var = tk.StringVar(value=f'Hits: {self.hits}')

        self.hits_text = tk.Label(frame.frame, font=font, bg=frame.bg_color, fg=color, textvariable=self.hits_text_var)
        self.hits_text.place(x=position[0], y=position[1], anchor=NW)

    def update_hits(self):
        self.hits += 1
        self.hits_text_var = tk.StringVar(value=f'Hits: {self.hits}')
        self.hits_text.config(textvariable=self.hits_text_var)
    
    def start(self):
        self.hits = 0
        self.hits_text_var = tk.StringVar(value=f'Hits: {self.hits}')
        self.hits_text.config(textvariable=self.hits_text_var)

class Failed():
    def __init__(self, frame, font, color, position:tuple):
        self.frame = frame
        self.failed = 0
        self.failed_text_var = tk.StringVar(value=f'Failed: {self.failed}')

        self.failed_text = tk.Label(frame.frame, font=font, bg=frame.bg_color, fg=color, textvariable=self.failed_text_var)
        self.failed_text.place(x=position[0], y=position[1], anchor=NW)

    def update_failed(self):
        self.failed += 1
        self.failed_text_var = tk.StringVar(value=f'Failed: {self.failed}')
        self.failed_text.config(textvariable=self.failed_text_var)
    
    def start(self):
        self.failed = 0
        self.failed_text_var = tk.StringVar(value=f'Failed {self.failed}')
        self.failed_text.config(textvariable=self.failed_text_var)

class Proxies():
    def __init__(self, frame, font, color, position_active:tuple, position_failed:tuple):
        self.frame = frame
        self.active_proxies = 0
        self.active_text_var = tk.StringVar(value=f'Active Proxies: {self.active_proxies}')

        self.failed_proxies = 0
        self.failed_text_var = tk.StringVar(value=f'Failed Proxies: {self.failed_proxies}')

        self.active_text = tk.Label(frame.frame, font=font, bg=frame.bg_color, fg=color, textvariable=self.active_text_var)
        self.active_text.place(x=position_active[0], y=position_active[1], anchor=NW)

        self.failed_text = tk.Label(frame.frame, font=font, bg=frame.bg_color, fg=color, textvariable=self.failed_text_var)
        self.failed_text.place(x=position_failed[0], y=position_failed[1], anchor=NW)

    def update_proxies(self):
        self.active_proxies = self.active_proxies - 1
        self.failed_proxies = self.failed_proxies + 1

        self.active_text_var = tk.StringVar(value=f'Active Proxies: {self.active_proxies}')
        self.active_text.config(textvariable=self.active_text_var)
        
        self.failed_text_var = tk.StringVar(value=f'Failed Proxies: {self.failed_proxies}')
        self.failed_text.config(textvariable=self.failed_text_var)

class Start_Button():
    def __init__(self, window, color:tuple, font, position:tuple, scale:tuple):
        self.button = tk.Button(window, fg=color[0], bg=color[1], font=font, text='Start', relief='flat', highlightthickness=0, width=scale[0], height=scale[1])
        self.button.place(x=position[0], y=position[1], anchor=CENTER)

class Finish_Button():
    def __init__(self, window, color:tuple, font, position:tuple, scale:tuple):
        self.button = tk.Button(window, fg=color[0], bg=color[1], font=font, text='Finish', relief='flat', highlightthickness=0, width=scale[0], height=scale[1])
        self.button.place(x=position[0], y=position[1], anchor=CENTER)

class Entries():
    def __init__(self, window, color, font, bg, position:tuple, size:tuple, border, clear_button_icon, button_bg, label_font:tuple, label_bg):
        self.label = tk.Label(window, bg=label_bg, fg=color, font=label_font[0], text=label_font[1])
        self.label.place(x=position[0], y=position[1] - 30, anchor=NW)

        self.text = scrolledtext.ScrolledText(window, font=font, fg=color, bg=bg, insertbackground=color, highlightcolor=border, highlightbackground=border, highlightthickness=1)
        self.text.place(x=position[0], y=position[1], anchor=NW, width=size[0], height=size[1])

        self.clear_button = tk.Button(window, image=clear_button_icon, relief='flat', borderwidth=0, bg=button_bg, command=self.clear_text)
        self.clear_button.place(x=position[0], y=position[1] + size[1] + 3, anchor=NW)

    def clear_text(self):
        self.text.delete('0.0', 'end')

class Output():
    def __init__(self, window, color, font, bg, position:tuple, size:tuple, border, icons:tuple, button_bg, label_font:tuple, label_bg, Popup_Message_Obj):
        self.Popup_Message_Obj = Popup_Message_Obj
        
        self.label = tk.Label(window, bg=label_bg, fg=color, font=label_font[0], text=label_font[1])
        self.label.place(x=position[0], y=position[1] - 30, anchor=NW)

        self.text = scrolledtext.ScrolledText(window, font=font, fg=color, bg=bg, insertbackground=color, highlightcolor=border, highlightbackground=border, highlightthickness=1)
        self.text.place(x=position[0], y=position[1], anchor=NW, width=size[0], height=size[1])

        self.clear_button = tk.Button(window, image=icons[0], relief='flat', borderwidth=0, bg=button_bg, command=self.clear_text)
        self.clear_button.place(x=position[0], y=position[1] + size[1] + 3, anchor=NW)

        self.save_button = tk.Button(window, image=icons[1], relief='flat', borderwidth=0, bg=button_bg, command=self.export_text)
        self.save_button.place(x=position[0] + 25, y=position[1] + size[1] + 3)

    def clear_text(self):
        self.text.delete('0.0', 'end')

    def export_text(self):
        file_save.save_text(file_save, textbox=self.text, Popup_Message_Obj=self.Popup_Message_Obj)

class Popup_Message():
    def __init__(self, geometry:tuple, message):
        self.window = tk.Tk()
        self.window.geometry(f'{geometry[0]}x{geometry[1]}')
        self.window.resizable(width=False, height=False)
        self.window.title('')
        self.window.iconbitmap('././resources/Error_Message_Icon.ico')

        text = tk.Label(self.window, text=message, font=('default', 15))
        text.place(x=geometry[0]/2, y=geometry[1]/2, anchor=CENTER)

        self.window.mainloop()

class Status():
    def __init__(self, frame, font, position:tuple, bg):
        self.status_var = tk.StringVar(value='None')

        self.status_text = tk.Label(frame, font=font, text=f'Status: {self.status_var.get()}', bg=bg, fg='white')
        self.status_text.place(x=position[0], y=position[1], anchor=NW)

    def in_progress(self):
        self.status_var.set(value='In Progress')
    
    def finishing(self):
        self.status_var.set(value='Finishing')
    
    def deactivate(self):
        self.status_var.set(value='None')

    def update_status_display(self):
        self.status_text.config(text=f'Status: {self.status_var.get()}')