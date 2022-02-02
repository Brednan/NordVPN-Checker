from tkinter.filedialog import askopenfile, asksaveasfilename

class File_Entries():
    def import_text(self, textbox, Popup_Message_Obj):
        try:
            entry = askopenfile(filetypes=(('Text Document', '*.txt'),))
            textbox.insert('end', entry.read())
        except Exception as e:
            if str(e) == "'NoneType' object has no attribute 'read'":
                pass
            else:
                Popup_Message_Obj(geometry=(200, 50), message='Error parsing file!')

class File_Save():
    def save_text(self, textbox, Popup_Message_Obj):
        try:
            file_dir = asksaveasfilename(filetypes=[('Text Document', '*.txt')])
            file = open(file_dir + '.txt', 'w')
            file.write(textbox.get('0.0', 'end'))
            file.close()
        except:
            Popup_Message_Obj(geometry=(200, 50), message='Error saving file!')