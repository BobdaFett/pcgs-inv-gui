from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem

import requests
import json

class PCGSClient:
    ''' A client that handles all PCGS Public API requests. '''
    def __init__(self, api_key: str):
        self.API_URL = "https://api.pcgs.com/publicapi"
        self.API_KEY = api_key

    def request_facts_by_grade(self, pcgs: int, grade: int, plus_grade: bool=False) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON serialized value. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByGrade/?PCGSNo={0}&GradeNo={1}&PlusGrade={2}".format(pcgs, grade, plus_grade)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        result.raise_for_status()
        return result.json()

    def request_facts_by_barcode(self, barcode: int, service: str) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON serialized value. 
            Note that the service argument only accepts PCGS or NGC. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByBarcode/?barcode={0}&gradingService={1}".format(barcode, service)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        result.raise_for_status()
        return result.json()

    def request_facts_by_cert(self, cert_number: int) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON serialized value. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByCertNo/{0}".format(cert_number)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        result.raise_for_status()
        return result.json()


class Coin:
    def __init__(self, obj: dict):
        self.json_obj = obj
        self.pcgs_no = obj['PCGSNo']
        self.year = obj['Year']
        self.denomination = obj['Denomination']
        self.mint_mark = obj['MintMark']
        self.grade = obj['Grade']
        self.price = obj['PriceGuideValue']
        self.fact_link = obj['CoinFactsLink']
        self.maj_var = obj['MajorVariety']
        self.min_var = obj['MinorVariety']
        self.die_var = obj['DieVariety']
        self.series_name = obj['SeriesName']
        self.category = obj['Category']
        self.designation = obj['Designation']

    def serialize(self) -> str:
        return json.dumps(self.json_obj)  # TODO Change to have only required information.

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
        
        return widget


class CoinCollection:
    def __init__(self):
        # Initialize a list to hold all of the Coin objects
        self.collection: list[Coin] = []

    def read_file(self, file_path: str):
        with open(file_path, "r") as file:
            # Read the file.
            obj_str = file.read()

    def dump_json(self, file_path="saved.txt"):
        with open(file_path, "wa") as file:
            # Serialize and write objects to the file.
            for coin in self.collection:
                file.write(coin.serialize())

    def add_coin(self, coin: Coin):
        self.collection.append(coin)

    def list(self):
        return self.collection