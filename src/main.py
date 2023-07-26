from PySide6.QtWidgets import QApplication
from dotenv import load_dotenv

import sys
import webbrowser
import os

app = QApplication()

load_dotenv()
try:
    os.getenv("PCGS_CERT")
except KeyError:
    open_browser = input("API Key was not detected.\nWould you like to visit the PCGS Public API webpage for extra instructions? (Y/n) ")
    if open_browser.lower() == "y":
        webbrowser.open("https://www.pcgs.com/publicapi/", 0)
    api_key_input = input("After logging in, your API key can be found by clicking the link inside the \"Documentation\" area on the right.\nPlease paste your API key here: ")
    with open("src/config/.env", "w") as file:
        file.write("PCGS_CERT = \'" + api_key_input + "\'")

from windows.MainWindow import Form

form = Form()
form.show()

sys.exit(app.exec())
