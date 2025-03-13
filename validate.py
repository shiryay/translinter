#! python3
# -*-coding: utf-8-*-

import docx
import os
import json
import re
import sys
import win32com.client
from tkinter import messagebox


class Validator:

    def __init__(self, file_name: str):
        self.rules_file = "rules.json"
        self.load_rules()
        self.processed_file = file_name
        self.report_file = os.path.dirname(file_name) + "\\" + "report.txt" 
        self.word = None
        self.doc = None
        self.processed_text = ''
        self.open_doc()
        self.grab_text()


    def open_doc(self) -> object:
        try:
            self.word = win32com.client.Dispatch("Word.Application")
            self.word.visible = False
            wb = self.word.Documents.Open(self.processed_file)
            self.doc = self.word.ActiveDocument
        except FileNotFoundError:
            messagebox.showerror("Error", "File was not found...")
        except:
             messagebox.showerror("Error", "Something went wrong :-(")

    def validate(self) -> None:
        self.write_header_to_report()

        # checks within MS Word
        self.check_language()
        self.check_page_size()
        self.check_page_break()
        self.check_section_break()

        # done outside word to avoid VBA dependencies
        self.check_end_tag()
        self.check_wf_tags()
        self.check_dates_format()
        self.check_stop_phrases()

        # clean up
        self.doc.Close()
        self.unload_rules()

        # show report
        self.show_report()

    def write_header_to_report(self):
        self.write_to_report(f"Checking {self.doc.Name}")
        line = "-" * 79
        self.write_to_report(f"{line}\n")

    def grab_text(self) -> str:
        self.processed_text = self.doc.Content.Text
        # return str(self.doc.Range().Text)

    def write_to_report(self, report_line: str) -> None:
        with open(self.report_file, "a", encoding="utf16") as f:
            f.write(report_line)
            f.write("\n")

    def show_report(self) -> None:
        if os.path.exists(self.report_file):
            os.startfile(self.report_file)
        else:
            self.write_to_report("Everything seems OK")
            self.show_report()

    def check_language(self) -> None:
        self.doc.LanguageDetected = False
        # self.doc.DetectLanguage()

        for para in self.doc.Paragraphs:
            if para.Range.LanguageID != 1033:
                self.write_to_report("The document is not in US English!")
                break

    def check_page_size(self) -> None:
        if self.doc.PageSetup.PaperSize != 2:
            self.write_to_report("Wrong paper size!")

    def check_end_tag(self) -> None:
        if not self.processed_text.strip().endswith("-end of document-"):
            self.write_to_report("No end tag found!")

    def check_page_break(self) -> None:
        if self.is_found("^m"):
            self.write_to_report("Page break found!")

    def check_section_break(self) -> None:
        if self.is_found("^b"):
            self.write_to_report("Section break found!")

    def check_wf_tags(self) -> None:
        pattern = re.compile(r"<}\d+{>")
        if (
            pattern.search(self.processed_text)
            or "{0>" in self.processed_text
            or "<0}" in self.processed_text
        ):
            self.write_to_report("WF tag found!")

    def check_dates_format(self) -> None:
        pattern = re.compile(r"\b(\d|\d\d)([\./-])(\d|\d\d)([\./-])(\d\d\d\d|\d\d)\b")
        list_of_dates = re.findall(pattern, self.processed_text)
        for d in list_of_dates:
            if d[1] != "/" or d[3] != "/" or int(d[0]) > 12:
                self.write_to_report("Seems like a suspicious date: " + "".join(d))

    def check_stop_phrases(self) -> None:
        # rule is a tuple of (regex, usage_tip)
        for rule in self.rules['rules']:
            pattern = rule['bug']
            results = re.findall(pattern, self.processed_text, re.IGNORECASE)
            for result in results:
                report_line = f"{result} - {rule['tip']}"
                self.write_to_report(report_line)

    def is_found(self, target: str) -> bool:
        self.word.Selection.Find.ClearFormatting()
        fnd = self.word.Selection.Find
        fnd.Text = target
        fnd.replacement.Text = ""
        fnd.Forward = True
        fnd.Wrap = 1
        fnd.Format = False
        fnd.MatchCase = False
        fnd.MatchWholeWord = False
        fnd.MatchWildcards = False
        fnd.MatchSoundsLike = False
        fnd.MatchAllWordForms = False
        fnd.Execute()
        return fnd.Found

    def load_rules(self) -> None:
        if os.path.exists(self.rules_file):
            with open(self.rules_file, "r") as rules_file:
                self.rules = json.load(rules_file)
        else:
            print("No rules file found! Click 'Update Rules' to download the rules file.")

    def unload_rules(self) -> None:
        self.rules = []
