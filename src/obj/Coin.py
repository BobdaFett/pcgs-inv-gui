from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

import json

class Coin:
    def __init__(self, obj: dict, quantity=1):
        self.json_obj           = obj
        self.pcgs_no            = obj['PCGSNo']
        self.name               = obj['Name']
        self.year               = obj['Year']
        self.denomination       = obj['Denomination']
        self.mint_mark          = obj['MintMark']
        self.grade              = obj['Grade']
        self.price              = obj['PriceGuideValue']
        self.fact_link          = obj['CoinFactsLink']
        self.maj_var            = obj['MajorVariety']
        self.min_var            = obj['MinorVariety']
        self.die_var            = obj['DieVariety']
        self.series_name        = obj['SeriesName']
        self.category           = obj['Category']
        self.designation        = obj['Designation']
        self.quantity           = quantity
        self.total_price        = quantity * self.price
        self.paid_for           = 0

    def serialize_json(self) -> str:
        return json.dumps(self.json_obj)  # TODO Change to have only required information.
    
    def serialize_csv(self) -> str:
        return "{0},{1},{2},{3},{4},{5},{6},{7}\n".format(self.series_name, self.year, self.mint_mark, self.denomination, self.maj_var,
                                                                          self.grade, self.designation, self.price, self.pcgs_no)

    def to_widget(self, parent: QTreeWidget) -> QTreeWidgetItem:
        widget = QTreeWidgetItem(parent)
        widget.setText(0, self.series_name)
        widget.setText(1, self.year.__str__())
        widget.setText(2, self.mint_mark)
        widget.setText(3, self.denomination)
        widget.setText(4, self.maj_var)
        widget.setText(5, self.grade)
        widget.setText(6, self.designation)
        widget.setText(7, self.price.__str__())
        widget.setText(8, self.pcgs_no.__str__())
        widget.setText(9, self.quantity.__str__())
        
        return widget
