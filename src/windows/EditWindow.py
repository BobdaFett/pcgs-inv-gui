from PySide6.QtWidgets import QDialog, QLineEdit, QPushButton, QGridLayout, QLabel, QHBoxLayout
from PySide6.QtGui import QIntValidator, QDesktopServices
from obj.Coin import Coin

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
            QLabel("Mint Mark:"),
            QLabel("Denomination:"),
            QLabel("Grade:"),
            QLabel("Est. Price:"),
            QLabel("Major Variety:"),
            QLabel("Minor Variety:"),
            QLabel("Die Variety:"),
            QLabel("Series:"),
            QLabel("Category:"),
            QLabel("Designation:"),
            QLabel("Quantity:"),
            QLabel("Paid For:")
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
        self.quantity       = QLineEdit()
        self.paid_for       = QLineEdit()
        self.fact_link      = QPushButton(text="PCGS Website")
        
        self.price.setText(display.price.__str__())
        self.quantity.setText(display.quantity.__str__())
        self.paid_for.setText(display.paid_for.__str__())

        self.fact_link.clicked.connect(self.link_clicked)

        ''' Create small layout structures for the price and "paid for" inputs. '''
        price_layout = QHBoxLayout()
        price_layout.addWidget(QLabel("$"))
        price_layout.addWidget(self.price)

        paid_layout = QHBoxLayout()
        paid_layout.addWidget(QLabel("$"))
        paid_layout.addWidget(self.paid_for)

        ''' Add all the widgets to the layout for the window. '''
        layout = QGridLayout()
        for (i, label) in enumerate(self.headers):
            layout.addWidget(label, i, 0)
        layout.addWidget(self.pcgs_no, 0, 1)
        layout.addWidget(self.year, 1, 1)
        layout.addWidget(self.mint_mark, 2, 1)
        layout.addWidget(self.denomination, 3, 1)
        layout.addWidget(self.grade, 4, 1)
        layout.addLayout(price_layout, 5, 1)
        layout.addWidget(self.maj_var, 6, 1)
        layout.addWidget(self.min_var, 7, 1)
        layout.addWidget(self.die_var, 8, 1)
        layout.addWidget(self.series, 9, 1)
        layout.addWidget(self.category, 10, 1)
        layout.addWidget(self.designation, 11, 1)
        layout.addWidget(self.quantity, 12, 1)
        layout.addLayout(paid_layout, 13, 1)
        layout.addWidget(self.fact_link, 14, 0, 1, 2)

        ''' Enable text validation for the corresponding input boxes. '''
        validator = QIntValidator()
        self.price.setValidator(validator)
        self.quantity.setValidator(validator)
        self.paid_for.setValidator(validator)

        layout.setColumnMinimumWidth(0, 150)

        self.setLayout(layout)

        self.setMinimumWidth(300)

    def link_clicked(self):
        ''' Utility function to handle clicking on the website button. '''
        QDesktopServices.openUrl(self.selected_coin.fact_link)