from PySide6.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QTreeWidget, QTreeWidgetItem, QGridLayout, QLabel, QFileDialog, QVBoxLayout
from PySide6.QtCore import QSize
from api_utils import *

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
        self.total_label = QLabel("Total Value = $" + self.total.__str__())

        self.new_button.clicked.connect(self.new_click)
        self.edit_button.clicked.connect(self.edit_click)
        self.del_button.clicked.connect(self.del_click)
        self.export_button.clicked.connect(self.export_click)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabels(["Series", "Year", "Mint", "Denomination", "Variety", "Grade", "Designation", "Est. Price", "PCGS #"])
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(4, 175)
        self.tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.tree.setSortingEnabled(True)

        layout = QGridLayout()
        layout.addWidget(self.tree, 0, 0, 1, 5)
        layout.addWidget(self.new_button, 1, 0)
        layout.addWidget(self.edit_button, 1, 1)
        layout.addWidget(self.del_button, 1, 2)
        layout.addWidget(self.total_label, 1, 3)
        layout.addWidget(self.export_button, 1, 4)

        self.setMinimumSize(QSize(1200, 250))

        self.setLayout(layout)

    def new_click(self):
        ''' Displays a modal window that requests the required info for a PCGS request. '''
        print("New clicked")
        window = RequestWindow("New Coin")
        window.exec()
        # Check that the user accepted the dialog before taking any actions.
        if window.result() == 1:
            try:
                print("User accepted dialog, making request.")
                pcgs = int(window.pcgs_input.text())
                grade = int(window.grade_input.text())
                coin_facts = self.client.request_facts_by_grade(pcgs, grade)
                new_coin = Coin(coin_facts)
                self.collection.add_coin(new_coin)
                new_coin.to_widget(self.tree)
                self.total += new_coin.price
                self.total_label.setText("Total Value = $" + self.total.__str__())
            except KeyError:
                # TODO Make a nice error window for this, which will allow the user to try again.
                print("Error: PCGS number does not match anything on record.")

    def edit_click(self):
        ''' Displays a window allowing the user to enter new information for the selected coin. '''
        sel_item = self.tree.selectedItems()[0]  # Gets the selected QTreeWidgetItem. There can only ever be one selected.
        sel_coin = self.collection[sel_item.text(8)]  # Gets the selected coin. This feels overcomplicated.
        window = EditWindow(sel_coin, self)
        window.exec()
        # Reinitialize the selected object. Simply take the (possibly) new values and change the QTreeWidgetItem.
        # This will run every time because it's fast.
        print("Updating coin...")

    def del_click(self):
        ''' Asks for confirmation that the user will delete a coin, then acts on that info. '''
        print("Delete clicked")

    def export_click(self):
        ''' Will show a window that allows the user to export a CSV file to their PC. '''
        file_path = QFileDialog.getSaveFileName(self, 'Save As...', filter='Comma separated values (*.csv)')[0]  # must access the first index of a (str, str)
        if file_path != "":
            with open(file_path, 'w') as file:
                # Set up the file's headers. These would be equivalent to the first line on an Excel sheet.
                file.write("Series,Year,Mint,Denomination,Variety,Grade,Designation,Est. Price,PCGS #\n")
                # Write the contents of every coin in the collection.
                for coin in self.collection:
                    file.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(coin.series_name, coin.year, coin.mint_mark, coin.denomination, coin.maj_var,
                                                                          coin.grade, coin.designation, coin.price, coin.pcgs_no))
                # Print the total. This should be specific to the CSV file.
                file.write(",,,,,,Total,{0},".format(self.total))
            print("File successfully saved at \"{0}\"".format(file_path))
        else:
            print("User denied the file selection dialog.")


class RequestWindow(QDialog):
    ''' A window that follows the general form for a PCGS API request.
        NOTE: You must use the QDialog.exec() method to show this in order for the
            QDialog.result() method to work. '''
    def __init__(self, window_title: str, parent=None, pcgs="", grade=""):
        super(RequestWindow, self).__init__(parent)
        self.setWindowTitle(window_title)

        self.pcgs_input = QLineEdit()
        self.grade_input = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")

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

        self.setLayout(layout)


class EditWindow(QDialog):
    def __init__(self, display: Coin, parent=None):
        super(EditWindow, self).__init__(parent)
        self.setWindowTitle("Editing {0}".format(display.name))
        self.selected_coin = display
        
        ''' Should show all of the coin's optional information.
            Eventually I may create an optional "Notes" section.
            These labels are the base labels - they only store the headers.
            They won't need to be changed at all, so we'll store them in a list for ease
            of organization. '''
        self.headers = [
            QLabel("PCGS Number:"),
            QLabel("Year:"),
            QLabel("Denomination:"),
            QLabel("Mint Mark:"),
            QLabel("Grade:"),
            QLabel("Est. Price:"),
            QLabel("Major Variety:"),
            QLabel("Minor Variety:"),
            QLabel("Die Variety:"),
            QLabel("Category:"),
            QLabel("Designation:")
        ]

        ''' Labels that store the information of the currently displayed coin. 
            This makes visual organization and formatting much easier. '''
        self.pcgs_no        = QLabel(display.pcgs_no.__str__())
        self.year           = QLabel(display.year.__str__())
        self.denomination   = QLabel(display.denomination)
        self.mint_mark      = QLabel(display.mint_mark)
        self.grade          = QLabel(display.grade)
        self.price          = QLineEdit()
        self.maj_var        = QLabel(display.maj_var)
        self.min_var        = QLabel(display.min_var)
        self.die_var        = QLabel(display.die_var)
        self.series         = QLabel(display.series_name)
        self.category       = QLabel(display.category)
        self.designation    = QLabel(display.designation)
        self.fact_link      = QPushButton(text="PCGS Website")
        
        self.price.setText(display.price)

        layout = QGridLayout()
        # Add the "header" labels.
        for (i, label) in enumerate(self.headers):
            layout.addWidget(label, i, 0)
        # Add the info labels.
        layout.addWidget(self.pcgs_no, 0, 1)
        layout.addWidget(self.year, 1, 1)
        layout.addWidget(self.denomination, 2, 1)
        layout.addWidget(self.mint_mark, 3, 1)
        layout.addWidget(self.grade, 4, 1)
        layout.addWidget(self.price, 5, 1)
        layout.addWidget(self.maj_var, 6, 1)
        layout.addWidget(self.min_var, 7, 1)
        layout.addWidget(self.die_var, 8, 1)
        layout.addWidget(self.series, 9, 1)
        layout.addWidget(self.category, 10, 1)
        layout.addWidget(self.designation, 11, 1)
        layout.addWidget(self.fact_link, 12, 0, 1, 2)

        layout.setColumnMinimumWidth(0, 100)

        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication()

    form = Form()
    form.show()

    import sys
    sys.exit(app.exec())
