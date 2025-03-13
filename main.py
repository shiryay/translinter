import sys
import tkinter as tk
from tkinter import filedialog, messagebox
import validate
import update
from validate import Validator
from update import Updater

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Translation Linter')
        self.geometry('260x120')
        self.updater = Updater()
        self.file_path = None
        
        self.create_widgets()
        self.updater.check_for_rules_update()

    def create_widgets(self):
        # File selection buttons
        self.select_btn = tk.Button(self, text='Select File', command=self.select_file)
        self.select_btn.place(x=20, y=20, width=100, height=30)

        # Update button
        self.update_rules_btn = tk.Button(self, text='Update Rules', command=self.updater.update_rules)
        self.update_rules_btn.place(x=20, y=70, width=100, height=30)

        # Exit button
        self.update_check_btn = tk.Button(self, text='Exit', command=sys.exit)
        self.update_check_btn.place(x=140, y=70, width=100, height=30)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
        if file_path:
            self.file_path = file_path
            validator = Validator(self.file_path)
            validator.validate()
            del validator


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
