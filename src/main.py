from PySide6.QtWidgets import QApplication
from windows.MainWindow import Form
from dotenv import dotenv_values

import sys
import webbrowser

app = QApplication()

config = dotenv_values()
try:
    config["PCGS_CERT"]
except KeyError:
    open_browser = input("API Key was not detected.\nWould you like to visit the PCGS Public API webpage for extra instructions? (Y/n) ")
    if open_browser.lower() == "y":
        webbrowser.open("https://api.pcgs.com/publicapi/", 0)
    api_key_input = input("Please paste your API key here: ")
    with open(".env", "w") as file:
        file.write("PCGS_CERT = \'" + api_key_input + "\'")

form = Form()
form.show()

sys.exit(app.exec())
