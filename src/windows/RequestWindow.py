if __name__ == "__main__":
    import sys
    print("Please run the program from the main.py file.")
    sys.exit()

from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout
from PySide6.QtGui import QIntValidator

class RequestWindow(QDialog):
    ''' A window that follows the general form for a PCGS API request. '''
    def __init__(self, window_title: str, parent=None, pcgs="", grade=""):
        super(RequestWindow, self).__init__(parent)
        self.setWindowTitle(window_title)

        self.pcgs_input         = QLineEdit()
        self.grade_input        = QLineEdit()
        self.quantity_input     = QLineEdit()
        self.ok_button          = QPushButton("OK")
        self.cancel_button      = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.pcgs_input.setPlaceholderText("PCGS Number...")
        self.pcgs_input.setText(pcgs)
        self.grade_input.setPlaceholderText("Grade Number...")
        self.grade_input.setText(grade)

        layout = QGridLayout()
        layout.addWidget(self.pcgs_input, 0, 0, 1, 2)
        layout.addWidget(self.grade_input, 1, 0, 1, 2)
        layout.addWidget(self.ok_button, 2, 0)
        layout.addWidget(self.cancel_button, 2, 1)

        validator = QIntValidator()
        self.pcgs_input.setValidator(validator)

        self.setLayout(layout)