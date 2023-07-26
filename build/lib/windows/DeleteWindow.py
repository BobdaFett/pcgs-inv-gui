if __name__ == "__main__":
    import sys
    print("Please run the program from the main.py file.")
    sys.exit()
    
from PySide6.QtWidgets import QDialog, QPushButton, QLabel, QGridLayout

class DeleteWindow(QDialog):
    def __init__(self, name: str, parent=None):
        super(DeleteWindow, self).__init__(parent)
        self.label              = QLabel("Are you sure you want to delete \"{0}?\"".format(name))
        self.ok_button          = QPushButton(text="Yep, delete it.")
        self.cancel_button      = QPushButton(text="No")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        layout = QGridLayout()
        layout.addWidget(self.label, 0, 0, 1, 2)
        layout.addWidget(self.ok_button, 1, 0)
        layout.addWidget(self.cancel_button, 1, 1)

        self.setLayout(layout)
