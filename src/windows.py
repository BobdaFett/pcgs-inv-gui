from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QGridLayout, QLabel
from PySide6.QtCore import QSize
from api_utils import *

import json
import config

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Testing")

        self.client = PCGSClient(config.PCGS_CERT)
        self.collection = CoinCollection()

        self.new_button = QPushButton("New...")
        self.edit_button = QPushButton("Edit...")
        self.del_button = QPushButton("Delete")
        self.export_button = QPushButton("Export to CSV")
        self.total = 0
        self.total_label = QLabel("Total = $" + self.total.__str__())

        self.new_button.clicked.connect(self.new_click)
        self.edit_button.clicked.connect(self.edit_click)
        self.del_button.clicked.connect(self.del_click)
        self.export_button.clicked.connect(self.export_click)

        self.tree = QTreeWidget()
        self.tree.setColumnCount(4)
        self.tree.setHeaderLabels(["Series", "Year", "Mint", "Denomination", "Variety", "Grade", "Designation", "Est. Price", "PCGS #"])

        layout = QGridLayout()
        layout.addWidget(self.tree, 0, 0, 1, 5)
        layout.addWidget(self.new_button, 1, 0)
        layout.addWidget(self.edit_button, 1, 1)
        layout.addWidget(self.del_button, 1, 2)
        layout.addWidget(self.total_label, 1, 3)
        layout.addWidget(self.export_button, 1, 4)

        self.setMinimumSize(QSize(450, 250))

        self.setLayout(layout)

    def new_click(self):
        ''' Displays a modal window that requests the required info for a PCGS request. '''
        print("New clicked")
        window = RequestWindow("New Coin")
        window.exec()
        # Check that the user accepted the dialog before taking any actions.
        if window.result() == 1:
            print("User accepted dialog, making request.")
            pcgs = int(window.pcgs_input.text())
            grade = int(window.grade_input.text())
            coin_facts = self.client.request_facts_by_grade(pcgs, grade)
            new_coin = Coin(coin_facts)
            self.collection.add_coin(new_coin)
            new_coin.to_widget(self.tree)
            self.total += new_coin.price
            self.total_label.setText("Total = $" + self.total.__str__())

    def edit_click(self):
        ''' Displays a window allowing the user to enter new information for the selected coin. '''
        print("Edit clicked")
        window = RequestWindow("Edit Coin")
        window.exec()
        # Check that the user accepted the dialog before taking any actions.
        if window.result() == 1:
            print("User accepted dialog, making request.")

    def del_click(self):
        ''' Asks for confirmation that the user will delete a coin, then acts on that info. '''
        print("Delete clicked")

    def export_click(self):
        ''' Will show a window that allows the user to export a CSV file to their PC, OneDrive, or Google Drive (when I can get them working) '''
        print("Export clicked")


class RequestWindow(QDialog):
    ''' A window that follows the general form for a PCGS API request.
        NOTE: You must use the QDialog.exec() method to show this in order for the QDialog.result() method to work. '''
    def __init__(self, window_title: str, parent=None):
        super(RequestWindow, self).__init__(parent)
        self.setWindowTitle(window_title)

        self.pcgs_input = QLineEdit()
        self.grade_input = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)

        self.pcgs_input.setPlaceholderText("PCGS Number...")
        self.grade_input.setPlaceholderText("Grade Number...")

        layout = QGridLayout()
        layout.addWidget(self.pcgs_input, 0, 0, 1, 2)
        layout.addWidget(self.grade_input, 1, 0, 1, 2)
        layout.addWidget(self.ok_button, 2, 0)
        layout.addWidget(self.cancel_button, 2, 1)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication()

    form = Form()
    form.show()

    with open("file.txt", "w") as file:
        file.write("Hello")

    import sys
    sys.exit(app.exec())
