if __name__ == "__main__":
    import sys

    print("Please run the program from the main.py file.")
    sys.exit()

from PySide6.QtWidgets import QDialog, QPushButton, QLineEdit, QGridLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QDesktopServices

import PySide6.QtCore as QtCore  # AlignmentFlags


def open_website():
    ''' Unfortunately, there's no single sign on component that I'm aware of from PCGS.
        I would love to grab the API key from an OAuth handshake, however this isn't possible at the moment. '''
    QDesktopServices.openUrl("https://www.pcgs.com/publicapi")


class KeyEnterWindow(QDialog):
    def __init__(self, parent=None):
        super(KeyEnterWindow, self).__init__(parent)
        self.setWindowTitle("API Key Input")

        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.accept)
        self.website_button = QPushButton("Website")
        self.website_button.clicked.connect(open_website)

        self.description = QLabel(
            '''An existing API key was not found.
Before using this application, you must get your public API key from the PCGS website.
Click the "Website" button to be redirected to the PCGS website.
Be sure to click the "Documentation" link in the top right after you sign in.''')
        self.description.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.key_label = QLabel("API Key:")
        self.key_input = QLineEdit()
        self.key_input.setPlaceholderText("Paste key here...")

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.website_button)

        layout = QGridLayout()
        layout.addWidget(self.key_label, 0, 0)
        layout.addWidget(self.key_input, 0, 1)
        layout.addWidget(self.description, 1, 0, 1, 2)
        layout.addLayout(button_layout, 2, 0, 1, 2)

        self.setLayout(layout)
