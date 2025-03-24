# Translation Linter

## Description

Translation Linter is a Python application that helps you validate and check translated Word documents (.docx) against a set of predefined rules. It uses PyQt5 for the GUI, python-docx for handling Word documents, and jsonschema for validating the rules.

## Features

- Load and validate translations in Word documents against custom rules.
- Update rules from a remote repository.
- Check for application updates.
- Generate a report of errors found in the document.

Compilation: `pyinstaller --onefile --add-data "rules.json;." --windowed  main.py`

TODO:

1. Update inform rule to exclude 'information'
