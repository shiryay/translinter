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
        self.updater = Updater(parent_window=self)
        
        self.create_widgets()
        self.updater.check_for_rules_update()
        self.updater.check_for_sw_update()

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

        # Update program button
        self.update_prog_btn = tk.Button(self, text='Update Linter', command=self.updater.update_prog)
        self.update_prog_btn.place(x=20, y=170, width=100, height=30)

        # Suggest Rule button
        self.update_check_btn = tk.Button(self, text='Suggest Rule', command=self.suggest_rule)
        self.update_check_btn.place(x=20, y=220, width=100, height=30)

        # Exit button
        self.update_check_btn = tk.Button(self, text='Exit', command=sys.exit)
        self.update_check_btn.place(x=20, y=270, width=100, height=30)

        # Text box
        self.text_box = tk.Text(self, height=200, width=600)
        self.text_box.place(x=140, y=20, width=600, height=300)

    def clear_input(self):
        self.text_box.delete('1.0', tk.END)

    def validate_text(self):
        text_to_check = self.text_box.get('1.0', tk.END)

        if not text_to_check:
            self.text_box.insert(tk.END, "No text to validate!")
            return

        validator = Validator(text_to_check)
        self.report = validator.validate()
        del validator
        self.clear_input()
        self.text_box.insert(tk.END, self.report)

    def suggest_rule(self):
        from tkinter import simpledialog, messagebox
        import telegram
        from datetime import datetime
        import socket
        
        try:
            bot = telegram.Bot(token='7252379080:AAEwoD--Ptjs5c3VkMVb45z_G90747o7rNQ')
            suggestion = simpledialog.askstring("Suggest Rule", "Please describe your rule suggestion:", parent=self)
            
            if suggestion:
                # Add PC identifier to the message
                pc_name = socket.gethostname()
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                message = f"New rule suggestion from {pc_name} at {timestamp}:\n{suggestion}"
                
                bot.send_message(chat_id='1461312271', text=message)
                messagebox.showinfo("Success", "Thank you! Your suggestion has been sent.", parent=self)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to send suggestion: {str(e)}", parent=self)


if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()
