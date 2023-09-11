import requests

class PCGSClient:
    class CoinNotFoundException(Exception):
        """ Raised when the coin is not found in the PCGS database. """
        pass
    class PCGSApiException(Exception):
        """ Raised when the PCGS API returns an unidentified error. """
        pass

    ''' A client that handles all PCGS Public API requests. '''
    def __init__(self, api_key):
        self.API_URL = "https://api.pcgs.com/publicapi"
        self.API_KEY = api_key
        # TODO Find out if there's a way to test the api before using it. Allows raising errors.

    def request_facts_by_grade(self, pcgs: int, grade: int, plus_grade: bool=False) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON deserialized value. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByGrade/?PCGSNo={0}&GradeNo={1}&PlusGrade={2}".format(pcgs, grade, plus_grade)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        # Check the result for any errors.
        result.raise_for_status()
        result_json = result.json()
        if result_json["ServerMessage"] == "No data found":
            raise PCGSClient.CoinNotFoundException("Coin not found with given PCGS number and grade.")
        elif result_json["ServerMessage"] == "A server error occurred":
            raise PCGSClient.PCGSApiException("An API error occurred.")
        else:
            return result_json

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
    