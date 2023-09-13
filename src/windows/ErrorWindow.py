import logging

if __name__ == "__main__":
    import sys

    print("Please run the program from the main.py file.")
    sys.exit()

from PySide6.QtWidgets import QDialog, QPushButton, QGridLayout, QLabel
from requests import HTTPError


class ErrorWindow(QDialog):
    def __init__(self, e, parent=None):
        super(ErrorWindow, self).__init__(parent)
        self.setWindowTitle("Error")
        self.error = e

        # Match and simplify the HTTPError.
        if isinstance(self.error, HTTPError):
            self.error = "HTTP error: {0} - {1}".format(self.error.response.status_code, self.error.response.reason)
            if self.error.response.status_code == 401:
                import sys
                import os
                logging.critical("API key is invalid. Deleting .env file for reconfig upon restart...")
                path = os.path.realpath(".")
                if os.path.exists(path + "\\config\\.env"):
                    os.remove(path + "\\config\\.env")
                    logging.debug(".env file deleted successfully. Shutting down...")
                else:
                    logging.error(".env file does not exist. Shutting down...")
                sys.exit(401)

        # Display the error in a QLabel.
        self.error_label = QLabel(self.error.__str__())
        self.close_button = QPushButton("Close")
        self.close_button.clicked.connect(self.close)

        # Set up the layout.
        layout = QGridLayout()
        layout.addWidget(self.error_label, 0, 0)
        layout.addWidget(self.close_button, 1, 0)
        self.setLayout(layout)
