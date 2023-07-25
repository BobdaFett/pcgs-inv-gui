import requests

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
