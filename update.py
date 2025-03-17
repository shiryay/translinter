import difflib

import requests

from tkinter import messagebox


class Updater:

    def __init__(self):

        self.rules_file = 'rules.json'
        self.rules_url = 'https://raw.githubusercontent.com/shiryay/rulesrepo/refs/heads/main/rules.json'
        self.version_url = "https://raw.githubusercontent.com/shiryay/rulesrepo/refs/heads/main/version.txt"

    def check_for_rules_update(self):

        try:
            # Get GitHub content
            response = requests.get(self.rules_url)
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
            response = requests.get(self.rules_url)
            with open(self.rules_file, 'w') as file:
                file.write(response.text)
            messagebox.showinfo("Success", "Rules updated successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Rule update failed: {str(e)}")

    def newer_version_found(self) -> bool:
        # compare versions in version.txt
        from packaging import version

        try:
            # Read GitHub version
            response = requests.get(self.version_url)
            github_version = response.text.strip()

            # Read local version
            with open('version.txt', 'r') as f:
                local_version = f.read().strip()

            return version.parse(github_version) > version.parse(local_version)

        except Exception as e:
            messagebox.showerror("Error", f"Version check failed: {str(e)}")
            return False

    def check_for_sw_update(self):
        if self.newer_version_found():
            messagebox.showinfo("Attention!", "New software version available!")

    def update_prog(self):
        # run upd.exe
        import subprocess

        try:
            subprocess.run(['upd.exe'], check=True)
        except subprocess.CalledProcessError as e:
            messagebox.showerror("Error", f"Update failed: {str(e)}")
        except FileNotFoundError:
            messagebox.showerror("Error", "Update file not found")
