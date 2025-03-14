import sys
import tkinter as tk
import validate
import update
from validate import Validator
from update import Updater

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Translation Linter')
        self.geometry('760x340')
        self.updater = Updater()
        
        self.create_widgets()
        self.updater.check_for_rules_update()

    def create_widgets(self):
        # File selection buttons
        self.validate_btn = tk.Button(self, text='Validate', command=self.validate_text)
        self.validate_btn.place(x=20, y=20, width=100, height=30)

        # Clear input button
        self.clear_btn = tk.Button(self, text='Clear', command=self.clear_input)
        self.clear_btn.place(x=20, y=70, width=100, height=30)

        # Update rules button
        self.update_rules_btn = tk.Button(self, text='Update Rules', command=self.updater.update_rules)
        self.update_rules_btn.place(x=20, y=120, width=100, height=30)

        # Exit button
        self.update_check_btn = tk.Button(self, text='Exit', command=sys.exit)
        self.update_check_btn.place(x=20, y=170, width=100, height=30)

        # Text box
        self.text_box = tk.Text(self, height=200, width=600)
        self.text_box.place(x=140, y=20, width=600, height=300)

    def clear_input(self):
        self.text_box.delete('1.0', tk.END)

    def validate_text(self):
        validator = Validator(self.text_box.get('1.0', tk.END))
        self.report = validator.validate()
        del validator
        self.clear_input()
        self.text_box.insert(tk.END, self.report)


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
