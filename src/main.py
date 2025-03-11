import tkinter as tk
from tkinter import filedialog, messagebox
import threading
import json
import requests
import docx
import os

class FileChecker:
    def __init__(self, rules):
        self.rules = rules

    def check_file(self, file_path):
        doc = docx.Document(file_path)
        errors = []
        for rule in self.rules:
            for paragraph in doc.paragraphs:
                if rule['keyword'] in paragraph.text:
                    errors.append(f"Error: {rule['message']} in paragraph: {paragraph.text}")
        return errors

class RulesManager:
    def __init__(self, rules_path):
        self.rules_path = rules_path
        self.rules = self.load_rules()

    def load_rules(self):
        with open(self.rules_path, 'r') as file:
            return json.load(file)

    def update_rules(self, url):
        response = requests.get(url)
        with open(self.rules_path, 'w') as file:
            file.write(response.text)
        self.rules = self.load_rules()

class Updater(threading.Thread):
    def __init__(self, current_version, repo_url, callback):
        super().__init__()
        self.current_version = current_version
        self.repo_url = repo_url
        self.callback = callback

    def run(self):
        try:
            response = requests.get(f"{self.repo_url}/releases/latest")
            latest_version = response.json()['tag_name']
            self.callback(latest_version != self.current_version)
        except Exception as e:
            print(f"Update check failed: {e}")
            self.callback(False)

class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Translation Linter')
        self.geometry('400x200')
        self.rules_manager = RulesManager('rules.json')
        self.file_path = None
        
        self.create_widgets()

    def create_widgets(self):
        # File selection buttons
        self.select_btn = tk.Button(self, text='Select File', command=self.select_file)
        self.select_btn.place(x=50, y=50, width=100, height=30)

        self.save_btn = tk.Button(self, text='Save File', command=self.save_file)
        self.save_btn.place(x=200, y=50, width=100, height=30)

        # Update buttons
        self.update_rules_btn = tk.Button(self, text='Update Rules', command=self.update_rules)
        self.update_rules_btn.place(x=50, y=100, width=100, height=30)

        self.update_check_btn = tk.Button(self, text='Check for Updates', command=self.check_for_updates)
        self.update_check_btn.place(x=200, y=100, width=150, height=30)

    def select_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
        if file_path:
            self.file_path = file_path
            self.check_file()

    def save_file(self):
        save_path = filedialog.asksaveasfilename(
            defaultextension=".docx",
            filetypes=[("Word Files", "*.docx")]
        )
        if save_path:
            # Add your save logic here
            pass

    def update_rules(self):
        def update_task():
            try:
                self.rules_manager.update_rules('https://raw.githubusercontent.com/your-repo/rules.json')
                self.after(0, lambda: messagebox.showinfo("Success", "Rules updated successfully!"))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", f"Rule update failed: {str(e)}"))
        
        threading.Thread(target=update_task, daemon=True).start()

    def check_for_updates(self):
        def update_callback(available):
            message = "New version available!" if available else "You're up to date!"
            self.after(0, lambda: messagebox.showinfo("Update Check", message))
        
        Updater('1.0.0', 'https://api.github.com/repos/your-repo', update_callback).start()

    def check_file(self):
        def check_task():
            try:
                checker = FileChecker(self.rules_manager.rules)
                errors = checker.check_file(self.file_path)
                message = '\n'.join(errors) if errors else 'No errors found'
                msg_type = messagebox.showwarning if errors else messagebox.showinfo
                self.after(0, lambda: msg_type("Check Results", message))
            except Exception as e:
                self.after(0, lambda: messagebox.showerror("Error", f"File check failed: {str(e)}"))
        
        threading.Thread(target=check_task, daemon=True).start()

if __name__ == '__main__':
    app = MainWindow()
    app.mainloop()

'''
Make sure to place your rules.json file in the same directory as main.py or adjust the path accordingly. Replace 'https://raw.githubusercontent.com/your-repo/rules.json' and 'https://api.github.com/repos/your-repo' with the actual URLs of your GitHub repository.
"Compilation": pyinstaller --onefile --windowed src/main.py
'''