from PySide6.QtWidgets import QApplication
from dotenv import load_dotenv

import sys
import os
import logging

app = QApplication()

path = os.path.realpath(".") + "\\config\\"

try:
    if load_dotenv(path + ".env") is False:
        raise FileNotFoundError
    if os.getenv('PCGS_CERT') is None:
        raise FileNotFoundError
except FileNotFoundError:
    # Display a dialog window to ask for user input.
    from windows.KeyEnterWindow import *
    window = KeyEnterWindow()
    window.exec()

    while True:
        if window.result() == 1:  # If the user accepted the dialog...
            # Get the information from the window.
            api_key = window.key_input.text()
            if window.key_input.text() != "":
                # Create folder for .env, if it doesn't exist already.
                if os.path.exists(path) is False:
                    os.mkdir(path)
                # Create the .env file and open in write mode.
                try:
                    file = open(path + ".env", "x")
                except FileExistsError:
                    file = open(path + ".env", "w")
                file.write("PCGS_CERT = \'" + api_key + "\'")
                # Make the newly created file hidden. I would rather not have the user be able to edit this.
                import subprocess
                subprocess.check_call(["attrib", "+H", path + ".env"])
            else:
                # API key was not found. Do not write and allow the user to try again.
                logging.debug("User accepted dialog but API key was not found. Retrying...")
                window.exec()
        else:  # if the user denied adding their API key...
            sys.exit(0)

# Set up the logger.
logging.basicConfig(filename=path + "log.txt",
                    level=logging.DEBUG,
                    filemode="w",
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%m/%d/%y %H:%M:%S %p")

from windows.MainWindow import Form

form = Form()
form.show()

sys.exit(app.exec())
