from PySide6.QtWidgets import QTreeWidget, QTreeWidgetItem
from collections.abc import Sequence

import requests
import json

class PCGSClient:
    ''' A client that handles all PCGS Public API requests. '''
    def __init__(self, api_key: str):
        self.API_URL = "https://api.pcgs.com/publicapi"
        self.API_KEY = api_key
        # TODO Find out if there's a way to test the api before using it. Allows raising errors.

    def request_facts_by_grade(self, pcgs: int, grade: int, plus_grade: bool=False) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON deserialized value. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByGrade/?PCGSNo={0}&GradeNo={1}&PlusGrade={2}".format(pcgs, grade, plus_grade)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        result.raise_for_status()
        return result.json()

    def request_facts_by_barcode(self, barcode: int, service: str) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON deserialized value. 
            Note that the service argument only accepts PCGS or NGC. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByBarcode/?barcode={0}&gradingService={1}".format(barcode, service)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        result.raise_for_status()
        return result.json()

    def request_facts_by_cert(self, cert_number: int) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON deserialized value. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByCertNo/{0}".format(cert_number)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        result.raise_for_status()
        return result.json()


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
        self.collection: dict[str, Coin] = {}
        self.current_index = 0
        super().__init__()

    def __iter__(self):
        return iter(self.collection.values())
    
    # def __next__(self) -> Coin:
    #     try:
    #         result = self.collection[self.current_index]
    #     except IndexError:
    #         raise StopIteration
    #     self.current_index += 1
    #     return result
    
    def __len__(self) -> int:
        return self.collection.__len__()
    
    def __getitem__(self, key) -> Coin:
        return self.collection[key]
    
    def read_file(self, file_path: str):
        ''' Reads a saved file into the collection. '''
        with open(file_path, "r") as file:
            # Read the file.
            obj_str = file.read()

    def dump_json(self, file_path="saved.txt"):
        ''' Creates a file that can be used in the read_file() method. '''
        with open(file_path, "wa") as file:
            # Serialize and write objects to the file.
            for coin in self.collection.values():
                file.write(coin.serialize())

    def add_coin(self, coin: Coin):
        ''' Adds a coin into the collection. '''
        self.collection[coin.pcgs_no] = coin