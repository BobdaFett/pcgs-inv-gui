# Required for use with Qt
from PySide6.QtWidgets import *
from PySide6.QtGui import QIntValidator
from PySide6.QtCore import QSize

import sys
import requests
import config

auth = "bearer " + config.api_key
api_url = "https://api.pcgs.com/publicapi/"

headers = {'authorization': auth}

# Our current test coin.
# PCGSNo = 4906
# GradeNo = 3
# PlusGrade = false

# Should output a CSV file. PowerBI/Python integration?
# PCGS Number, name, grade, price
# API request requirements are manual inputs, everything else is automatic.

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Testing")
        self.pcgs_input = QLineEdit()
        self.pcgs_input.setPlaceholderText("PCGS Number...")
        self.grade_input = QLineEdit()
        self.grade_input.setPlaceholderText("Grade Number...")
        self.test_button = QPushButton("Add Coin...")
        self.test_button.clicked.connect(self.ok_click)

        self.new_button = QPushButton("New...")
        self.edit_button = QPushButton("Edit...")
        self.del_button = QPushButton("Delete")
        self.export_button = QPushButton("Export to CSV")

        self.tree = QTreeWidget()
        self.tree.setColumnCount(4)
        self.tree.setHeaderLabels(["PCGS #", "Name", "Grade", "Est. Value"])

        validator = QIntValidator()
        self.pcgs_input.setValidator(validator)
        self.grade_input.setValidator(validator)

        layout = QGridLayout()
        layout.addWidget(self.tree, 0, 0, 1, 5)
        layout.addWidget(self.new_button, 1, 0)
        layout.addWidget(self.edit_button, 1, 1)
        layout.addWidget(self.del_button, 1, 2)
        layout.addWidget(self.export_button, 1, 4)

        self.setMinimumSize(QSize(450, 250))

        self.setLayout(layout)
    
    def hi(self):
        print("Hello world!")

    def ok_click(self):
        # Requests and saves the information from the API.
        pcgs = int(self.pcgs_input.text())
        grade = int(self.grade_input.text())

        # Use our utility function in order to send the request to the API.
        response = self.request_facts_by_grade(pcgs, grade)

        # Save this information somewhere. Not sure where yet.
        self.output_csv(response)


    def request_facts_by_grade(self, pcgs: int, grade: int):
        # Build the request url.
        request_url = api_url + "coindetail/GetCoinFactsByGrade?PCGSNo=" + pcgs.__str__() + "&GradeNo=" + grade.__str__() + "&PlusGrade=false"
        print("Sending request for coin facts for coin number " + pcgs.__str__() + "...")
        
        # Send the request to the server and wait for a response.
        response = requests.get(request_url, headers=headers)
        print("Response received.")

        # Add a check here to ensure there are no errors. This will most likely become its own function.
        return response.json()

    def output_csv(self, data: dict):
        # Creates a CSV file and overwrites any that were previously created.
        csv = open("csvTest.csv", "w")
        print("Writing file...")

        # Output all required data from the current list of coins we have.
        # Not really sure how or where these are stored for right now. To be continued...
        csv.write("PCGS #,Name,Grade,Est. Value\n")
        csv.write(data["PCGSNo"].__str__() + "," + data["Name"].__str__() + "," + data["Grade"].__str__() + "," + data["PriceGuideValue"].__str__() + "\n")

        Modal(parent=self, text="File written successfully.", title="Success")

class Modal(QDialog):
    def __init__(self, parent=None, text="", title="Alert"):
        super(Modal, self).__init__(parent)
        self.setWindowTitle(title)
        self.label = QLabel(text)
        self.button = QPushButton("OK")
        self.button.clicked.connect(self.button_clicked)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)

        self.setLayout(layout)
        self.exec()

    def button_clicked(self):
        self.close()


if __name__ == "__main__":
    app = QApplication()

    form = Form()
    form.show()

    sys.exit(app.exec())
