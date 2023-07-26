if __name__ == "__main__":
    import sys
    print("Please run the program from the main.py file.")
    sys.exit()

from PySide6.QtWidgets import QDialog, QPushButton, QTreeWidget, QGridLayout, QLabel, QFileDialog
from PySide6.QtCore import QSize
from dotenv import load_dotenv
from obj.Coin import Coin
from obj.CoinCollection import CoinCollection
from obj.PCGSClient import PCGSClient
from .DeleteWindow import DeleteWindow
from .RequestWindow import RequestWindow
from .EditWindow import EditWindow

import os

load_dotenv()
PCGS_CERT = os.getenv("PCGS_CERT")

class Form(QDialog):
    def __init__(self, parent=None):
        super(Form, self).__init__(parent)
        self.setWindowTitle("Testing")

        self.client = PCGSClient(PCGS_CERT)
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
        self.tree.setHeaderLabels(["Series", "Year", "Mint", "Denomination", "Variety", "Grade", "Designation", "Est. Price", "PCGS #", "Quantity"])
        self.tree.setColumnWidth(0, 300)
        self.tree.setColumnWidth(4, 175)
        self.tree.setColumnWidth(8, 75)
        self.tree.setColumnWidth(9, 75)
        self.tree.setSelectionMode(QTreeWidget.SelectionMode.SingleSelection)
        self.tree.setSortingEnabled(True)

        if self.collection.read_save_file():
            # Initialize the QTreeWidget list.
            for coin in self.collection:
                coin.to_widget(self.tree)

        layout = QGridLayout()
        layout.addWidget(self.tree, 0, 0, 1, 5)
        layout.addWidget(self.new_button, 1, 0)
        layout.addWidget(self.edit_button, 1, 1)
        layout.addWidget(self.del_button, 1, 2)
        layout.addWidget(self.total_label, 1, 3)
        layout.addWidget(self.export_button, 1, 4)

        self.setMinimumSize(QSize(1250, 500))

        self.setLayout(layout)

    def __del__(self):
        # Allow normal deletion, with the addition of a save pass.
        self.collection.create_save_file()

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
                self.total += new_coin.PriceGuideValue
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
        # This will run every time.
        sel_coin.PriceGuideValue = float(window.price.text())
        sel_coin.Quantity = int(window.quantity.text())
        sel_coin.paid_for = int(window.paid_for.text())
        sel_coin.notes = window.notes.toPlainText()
        sel_item.setText(7, "${0}".format(window.price.text()))
        sel_item.setText(9, window.quantity.text())

    def del_click(self):
        ''' Asks for confirmation that the user will delete a coin, then acts on that info. '''
        sel_item = self.tree.selectedItems()[0]
        sel_coin = self.collection[sel_item.text(8)]
        window = DeleteWindow(sel_coin.Name, self)
        window.exec()
        if window.result() == 1:
            print("User accepted the verification request, deleting coin.")
            # Update the total price.
            self.total -= sel_coin.total_price
            self.total_label.setText("Total Value = $" + self.total.__str__())
            # Update the tree.
            self.tree.invisibleRootItem().removeChild(sel_item)
            # Delete the item from the collection.
            del self.collection[sel_coin.PCGSNo]
        else:
            print("User denied the verification request.")

    def export_click(self):
        ''' Will show a window that allows the user to export a CSV file to their PC. '''
        file_path = QFileDialog.getSaveFileName(self, 'Save As...', filter='Comma separated values (*.csv)')[0]  # must access the first index of a (str, str)
        if file_path != "":
            self.collection.dump_csv(file_path)
        else:
            print("User denied the file selection dialog.")