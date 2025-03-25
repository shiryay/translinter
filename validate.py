import os
import json
import re
from tkinter import messagebox


class Validator:

    def __init__(self, text: str):
        self.rules_file = "rules.json"
        self.report = []
        self.processed_text = text
        self.load_rules()

    def __del__(self):
        self.unload_rules()

    def validate(self) -> str:
        self.check_end_tag()
        self.check_wf_tags()
        self.check_dates_format()
        self.check_stop_phrases()
        if self.report:
            return '\n'.join(self.report)
        else:
            return "Everything seems OK"

    def check_end_tag(self) -> None:
        if not self.processed_text.strip().endswith("-end of document-"):
            self.report.append("No end tag found!")

    def check_wf_tags(self) -> None:
        pattern = re.compile(r"<}\d+{>")
        if (
            pattern.search(self.processed_text)
            or "{0>" in self.processed_text
            or "<0}" in self.processed_text
        ):
            self.report.append("WF tag found!")

    def check_dates_format(self) -> None:
        pattern = re.compile(r"\b(\d|\d\d)([\./-])(\d|\d\d)([\./-])(\d\d\d\d|\d\d)\b")
        list_of_dates = re.findall(pattern, self.processed_text)
        for d in list_of_dates:
            if d[1] != "/" or d[3] != "/" or int(d[0]) > 12:
                self.report.append("Seems like a suspicious date: " + "".join(d))

    def check_stop_phrases(self) -> None:
        # rule is a tuple of (regex, usage_tip)
        for rule in self.rules['rules']:
            pattern = rule['bug']
            results = re.findall(pattern, self.processed_text, re.IGNORECASE)
            if len(results) == 0:
                continue
            elif len(results) == 1:
                count_word = 'instance'
            else:
                count_word = 'instances'
            self.report.append(f"Found {len(results)} {count_word}:")
            self.report.append(rule['tip'])
            self.report.append("---------------")
            for result in results:
                report_line = f"\t{result}"
                self.report.append(report_line)
            self.report.append("\n")

    def load_rules(self) -> None:
        if os.path.exists(self.rules_file):
            with open(self.rules_file, "r") as rules_file:
                self.rules = json.load(rules_file)
        else:
            print("No rules file found! Click 'Update Rules' to download the rules file.")

    def unload_rules(self) -> None:
        self.rules = {}

