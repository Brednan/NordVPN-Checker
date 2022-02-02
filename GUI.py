import tkinter as tk
from tkinter.constants import CENTER, NW
from tools.Main_Window import Root, MainWindow, TitleBar
from PIL import Image, ImageTk
from tools.GUI_Classes import *
from tools.FileHandler import File_Entries
from tools.Event_Manager import *
import threading
entries = File_Entries()

root = Root('./resources/nordvpn_logo.ico', '1200x740')
window = MainWindow(master=root.root, icon_path='./resources/nordvpn_logo.ico', geometry=(1300, 820), background='#272727')

app_icon = ImageTk.PhotoImage(Image.open('./resources/nordvpn_logo.png').resize((25, 25)))
X_button = ImageTk.PhotoImage(Image.open('./resources/X_Button.png').resize((25, 25)))
min_icon = ImageTk.PhotoImage(Image.open('./resources/Minimize_Button.png').resize((25, 25)))
clear_button_icon = ImageTk.PhotoImage(Image.open('resources\clear_icon.png').resize((20, 20)))
save_button_icon = ImageTk.PhotoImage(Image.open('resources\save_icon.png').resize((20, 20)))

titlebar = TitleBar(master=root.root, background='#323232', scale=(1300, 30), window=window.window, app_icon=(app_icon, (25, 25)), x_button_icon=X_button, min_icon=min_icon)
content = tk.Frame(master=window.window, highlightbackground='#00BDFF', highlightcolor='#00BDFF', width=1300 * 0.98, height=820 * 0.93, highlightthickness=1, bg='#292929')
content.bind('<Button-1>', lambda event, widget=content: widget.focus_set())
content.place(x=650, y=425, anchor=CENTER)
status = Status(content, font=('default', 10), position=((1300*0.98) - 140, (820*0.93) - 25), bg='#292929')

first_section = Frames(content, bd_color='#00C5FF', bg_color='#212121', width=250, height=200, position=(30, 20))
add_combos_button = Import_Buttons(first_section.frame, fg='white', bg='#0078CB', width=18, height=1, placement=(125, 40), font=('default', 15), relief='flat', text='Add Combos', command=lambda: entries.import_text(combos_entry.text, Popup_Message))
add_https_proxies = Import_Buttons(first_section.frame, fg='white', bg='#0078CB', width=18, height=1, placement=(125, 100), font=('default', 15), relief='flat', text='Add HTTPS Proxies', command=lambda: entries.import_text(https_entry.text, Popup_Message))
add_socks4_proxies = Import_Buttons(first_section.frame, fg='white', bg='#0078CB', width=18, height=1, placement=(125, 160), font=('default', 15), relief='flat', text='Add SOCKS4 Proxies', command=lambda: entries.import_text(socks4_entry.text, Popup_Message))

second_section = Frames(content, bd_color='#00C5FF', bg_color='#212121', width=250, height=230, position=(30, 250))
max_threads = Max_Threads(second_section.frame, min_val=3, max_val=400, default_val=200, size=200, position=(120, 60), bg_color=second_section.bg_color, font=('default', 14))
timeout = Timeout(second_section.frame, min_val=1, max_val=10000, default_val=5000, size=200, position=(120, 145), bg_color=second_section.bg_color, font=('default', 14))
proxyless = Proxyless(second_section, font=('default', 14), position=(120, 195))

third_section = Frames(content, bd_color='#00C5FF', bg_color='#212121', width=250, height=160, position=(30, 510))
checked_count = Checked(frame=third_section, font=('default', 13), color='white', position=(7, 53))
remaining_count = Remaining(frame=third_section, font=('default', 13), color='white', position=(7, 76))
hits_count = Hits(frame=third_section, font=('default', 13), color='#27FF00', position=(7, 7))
failed_count = Failed(frame=third_section, font=('default', 13), color='red', position=(7, 30))
proxies_count = Proxies(frame=third_section, font=('default', 13), color='white', position_active=(7, 99), position_failed=(7, 122))

combos_entry = Entries(content, color='white', font=('default', 11), position=(300, 50), bg='#262626', size=(320, 660), border='#00C5FF', clear_button_icon=clear_button_icon, button_bg='white', label_font=(('default', 15), 'Combos'), label_bg='#292929')
https_entry = Entries(content, color='white', font=('default', 11), position=(660, 50), bg='#262626', size=(220, 300), border='#00C5FF', clear_button_icon=clear_button_icon, button_bg='white', label_font=(('default', 15), 'Https Proxies'), label_bg='#292929')
socks4_entry = Entries(content, color='white', font=('default', 11), position=(660, 410), bg='#262626', size=(220, 300), border='#00C5FF', clear_button_icon=clear_button_icon, button_bg='white', label_font=(('default', 15), 'SOCKS4 Proxies'), label_bg='#292929')
results = Output(content, color='white', font=('default', 11), position=(920, 50), bg='#262626', size=(320, 660), border='#00C5FF', icons=(clear_button_icon, save_button_icon), button_bg='white', label_font=(('default', 15), 'Working'), label_bg='#292929', Popup_Message_Obj=Popup_Message)

submission = Submission(status=status, combos=combos_entry, popup_obj=Popup_Message, proxies=(https_entry, socks4_entry), output=results, threads=max_threads, timeout=timeout.timeout_scale.get(), working=hits_count, failed=failed_count, proxies_count=proxies_count, remaining=remaining_count, proxyless=proxyless)
finish = Finish(status)

start_button = Start_Button(content, color=('white', '#0FC500'), font=('default', 15), position=(220, 720), scale=(10, 1))
start_button.button.config(command=lambda: threading.Thread(target=submission.on_submit).start())

finish_button = Finish_Button(content, color=('white', '#F08A00'), font=('default', 15), position=(90, 720), scale=(10, 1))
finish_button.button.config(command=lambda: threading.Thread(target=finish.on_submit).start())

window.window.mainloop()