import difflib
import requests
from tkinter import messagebox

class Updater:
    def __init__(self):
        self.rules_file = 'rules.json'
        self.github_raw_url = 'https://raw.githubusercontent.com/shiryay/translinter/refs/heads/master/rules.json'

    def check_for_rules_update(self):
        try:
            # Get GitHub content
            response = requests.get(self.github_raw_url)
            github_content = response.text.splitlines()

            # Read local file
            with open(self.rules_file, 'r') as file:
                local_content = file.read().splitlines()

            # Generate diff
            diff = difflib.unified_diff(
                github_content,
                local_content,
                fromfile='GitHub Version',
                tofile='Local Version',
                lineterm=''
            )
            if len('\n'.join(diff)) > 0:
                messagebox.showinfo("Attention!", "Rules update available!")
        except Exception as e:
            messagebox.showerror("Error", f"Rule update checking failed: {str(e)}")

    def update_rules(self):
        try:
            response = requests.get(self.github_raw_url)
            with open(self.rules_file, 'w') as file:
                file.write(response.text)
            messagebox.showinfo("Success", "Rules updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Rule update failed: {str(e)}")
