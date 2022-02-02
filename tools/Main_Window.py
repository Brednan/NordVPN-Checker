import tkinter as tk
from tkinter.constants import CENTER, EW, NE, NW

logo_path = r'D:\Desktop\New Hacking Folder\Development\NordVPN Checker\resources\nordvpn_logo.png'

class Root():
    def __init__(self, icon_path, geometry):
        self.root = tk.Tk()
        self.root.iconbitmap(icon_path)
        self.root.attributes('-alpha', 0)
        self.root.geometry(geometry)

class MainWindow():
    def __init__(self, master, icon_path, geometry:tuple, background):
        self.background = background
        self.window = tk.Toplevel(master)
        self.window.iconbitmap(icon_path)
        self.window.bind('<FocusIn>', self.on_window_focus)
        self.window.geometry(f'{geometry[0]}x{geometry[1]}')
        self.window.title('NordVPN Account Checker')
        self.window.resizable(width=False, height=False)
        self.window.configure(background=self.background)
        self.window.overrideredirect(1)
        self.master = master
        master.bind('<FocusIn>', self.on_root_focus)
        self.window.bind('<Alt-Key-F4>', self.on_altf4)
    
    def on_root_focus(self, e):
        try:
            self.window.focus_set()
        except:
            pass

    def on_altf4(self, e):
        self.master.destroy()
    
    def on_window_focus(self, e):
        self.window.deiconify()
        self.window.overrideredirect(1)

class TitleBar():
    def __init__(self, master, x_button_icon, min_icon, window, scale:tuple, background:str, app_icon:tuple):
        """
        Icons Must be no bigger than (25, 25)
        """
        self.root = master
        self.window = window
        self.background = background

        self.title_bar = tk.Frame(master=window, bg=background, relief='raised', width=scale[0], height=scale[1])
        self.title_bar.place(x=0, y=0, anchor=NW)
        self.title_bar.bind('<B1-Motion>', self.move_window)
        self.title_bar.bind('<Button-1>', lambda event, widget=self.title_bar: widget.focus_set())

        canvas = tk.Canvas(master=self.title_bar, bg=background, width=app_icon[1][0], height=app_icon[1][1], highlightthickness=0)
        canvas.place(x=20, y=15, anchor=CENTER)
        canvas.create_image(0, 0, image=app_icon[0], anchor=NW)

        x_button = tk.Button(master=self.title_bar, bg=background, image=x_button_icon, width=10, height=10, relief='flat')
        x_button.place(x=scale[0] - 5, y=9, anchor=NE)
        x_button.bind('<Button-1>', self.exit_app)
        x_button.bind('<Enter>', self.exit_button_hover)
        x_button.bind('<Leave>', self.exit_button_leave)
        self.x_button = x_button

        minimize_button = tk.Button(master=self.title_bar, bg=background, image=min_icon, width=10, height=10, relief='flat')
        minimize_button.place(x=scale[0]- 30, y=9, anchor=NE)
        minimize_button.bind('<Button-1>', self.min_button_click)
        minimize_button.bind('<Enter>', self.min_button_hover)
        minimize_button.bind('<Leave>', self.min_button_leave)
        self.minimize_button = minimize_button


        title = tk.Label(master=self.title_bar, font=('default', 10), text='NordVPN Account Checker | By xJorn', fg='#00BDFF', bg=background)
        title.place(x=650, y=15, anchor=CENTER)
        title.bind('<B1-Motion>', self.move_window)


    def move_window(self, e):
        self.root.geometry(f'+{e.x_root}+{e.y_root}')
        self.window.geometry(f'+{e.x_root}+{e.y_root}')

    def exit_app(self, e):
        self.root.destroy()

    def exit_button_hover(self, e):
        self.x_button.config(background='#CDCDCD')
    
    def exit_button_leave(self, e):
        self.x_button.config(background=self.background)

    def min_button_hover(self, e):
        self.minimize_button.config(background='#CDCDCD')
    
    def min_button_leave(self, e):
        self.minimize_button.config(background=self.background)

    def min_button_click(self, e):
        self.root.focus_force()
        self.window.overrideredirect(0)
        self.window.iconify()
