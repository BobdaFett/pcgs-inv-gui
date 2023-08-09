from PySide6.QtWidgets import QApplication
from dotenv import load_dotenv

import sys
import webbrowser
import os
import datetime

app = QApplication()

path = os.path.realpath(".") + "\\src\\config\\"

try:
    if load_dotenv(path + ".env") is False:
        print(".env did not load.")
        raise Exception
    if os.getenv('PCGS_CERT') is None:
        print("Couldn't find PCGS cert.")
        raise Exception
except Exception:
    # Display a dialog window to ask for user input.
    from windows.KeyEnterWindow import *
    window = KeyEnterWindow()
    window.exec()

    # Get the information from the window.
    api_key = window.key_input.text()

    # Write the key into the .env file.
    if os.path.exists(path) is False:
            os.mkdir(path)
    with open(path + ".env", "w") as file:
        file.write("PCGS_CERT = \'" + api_key + "\'")

from windows.MainWindow import Form

form = Form()
form.show()

sys.exit(app.exec())
