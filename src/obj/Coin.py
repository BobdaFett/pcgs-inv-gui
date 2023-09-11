from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

import json

class Coin:
    def __init__(self, obj: dict, quantity=1):
        self.PCGSNo             = obj['PCGSNo']
        self.Name               = obj['Name']
        self.Year               = obj['Year']
        self.Denomination       = obj['Denomination']
        self.MintMark           = obj['MintMark']
        self.Grade              = obj['Grade']
        self.PriceGuideValue    = obj['PriceGuideValue']
        self.CoinFactsLink      = obj['CoinFactsLink']
        self.MajorVariety       = obj['MajorVariety']
        self.MinorVariety       = obj['MinorVariety']
        self.DieVariety         = obj['DieVariety']
        self.SeriesName         = obj['SeriesName']
        self.Category           = obj['Category']
        self.Designation        = obj['Designation']
        self.CertNo             = obj['CertNo']
        self.Quantity           = quantity
        self.total_price        = quantity * self.PriceGuideValue
        self.paid_for           = 0
        self.notes: str         = ""

        try:
            self.Quantity = obj['Quantity']
            self.total_price = obj['total_price']
            self.paid_for = obj['paid_for']
            self.notes = obj['notes']
        except Exception:
            print("New coin created - no user data found. Continuing using defaults.")

    def serialize_csv(self) -> str:
        ''' Serializes the object into a CSV format. '''
        formatted_notes = self.notes.replace('\n', ' ')
        return "{0},{1},{2},{3},{4},{5},{6},{7},{8},{9}\n".format(self.SeriesName, self.Year, self.MintMark, self.Denomination, self.MajorVariety,
                                                              self.Grade, self.Designation, self.PriceGuideValue, self.PCGSNo, self.Quantity, formatted_notes)

    def to_widget(self, parent: QTreeWidget) -> QTreeWidgetItem:
        ''' Creates a QTreeWidgetItem from the object. '''
        widget = QTreeWidgetItem(parent)
        widget.setText(0, self.SeriesName)
        widget.setText(1, self.Year.__str__())
        widget.setText(2, self.MintMark)
        widget.setText(3, self.Denomination)
        widget.setText(4, self.MajorVariety)
        widget.setText(5, self.Grade)
        widget.setText(6, self.Designation)
        widget.setText(7, "${0}".format(self.PriceGuideValue))
        widget.setText(8, self.PCGSNo.__str__())
        widget.setText(9, self.Quantity.__str__())
        
        return widget

    def toJson(self):
        ''' Serializes the object into a JSON object. '''
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)
