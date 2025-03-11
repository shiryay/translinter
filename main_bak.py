import sys
import json
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog, QMessageBox
from PyQt5.QtCore import QThread, pyqtSignal
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

class Updater(QThread):
    update_available = pyqtSignal(bool)

    def __init__(self, current_version, repo_url):
        super().__init__()
        self.current_version = current_version
        self.repo_url = repo_url

    def run(self):
        response = requests.get(f"{self.repo_url}/releases/latest")
        latest_version = response.json()['tag_name']
        if latest_version != self.current_version:
            self.update_available.emit(True)
        else:
            self.update_available.emit(False)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.rules_manager = RulesManager('rules.json')

    def initUI(self):
        self.setWindowTitle('Translation Linter')
        self.setGeometry(100, 100, 400, 200)

        self.select_button = QPushButton('Select File', self)
        self.select_button.setGeometry(50, 50, 100, 30)
        self.select_button.clicked.connect(self.select_file)

        self.save_button = QPushButton('Save File', self)
        self.save_button.setGeometry(200, 50, 100, 30)
        self.save_button.clicked.connect(self.save_file)

        self.update_rules_button = QPushButton('Update Rules', self)
        self.update_rules_button.setGeometry(50, 100, 100, 30)
        self.update_rules_button.clicked.connect(self.update_rules)

        self.check_updates_button = QPushButton('Check for Updates', self)
        self.check_updates_button.setGeometry(200, 100, 150, 30)
        self.check_updates_button.clicked.connect(self.check_for_updates)

    def select_file(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Word File", "", "Word Files (*.docx)", options=options)
        if file_path:
            self.file_path = file_path
            self.check_file()

    def save_file(self):
        options = QFileDialog.Options()
        save_path, _ = QFileDialog.getSaveFileName(self, "Save Word File", "", "Word Files (*.docx)", options=options)
        if save_path:
            # Implement saving logic here
            pass

    def update_rules(self):
        url = 'https://raw.githubusercontent.com/your-repo/rules.json'
        self.rules_manager.update_rules(url)
        QMessageBox.information(self, 'Update', 'Rules updated successfully!')

    def check_for_updates(self):
        current_version = '1.0.0'
        repo_url = 'https://api.github.com/repos/your-repo'
        self.updater = Updater(current_version, repo_url)
        self.updater.update_available.connect(self.handle_update_check)
        self.updater.start()

    def handle_update_check(self, update_available):
        if update_available:
            QMessageBox.information(self, 'Update', 'A new version is available!')
        else:
            QMessageBox.information(self, 'Update', 'You are using the latest version.')

    def check_file(self):
        checker = FileChecker(self.rules_manager.rules)
        errors = checker.check_file(self.file_path)
        if errors:
            QMessageBox.warning(self, 'Errors Found', '\n'.join(errors))
        else:
            QMessageBox.information(self, 'No Errors', 'No errors found in the file.')

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

'''
Make sure to place your rules.json file in the same directory as main.py or adjust the path accordingly. Replace 'https://raw.githubusercontent.com/your-repo/rules.json' and 'https://api.github.com/repos/your-repo' with the actual URLs of your GitHub repository.
"Compilation": pyinstaller --onefile --windowed src/main.py
'''