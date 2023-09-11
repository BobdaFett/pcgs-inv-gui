import requests
import logging

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
        logging.debug("PCGSClient initialized.")
        # TODO Find out if there's a way to test the api before using it. Allows raising errors.
        # if self.test_api() is False:
        #     logging.critical("API key is invalid.")
        #     raise Exception("API key is invalid.")

    def request_facts_by_grade(self, pcgs: int, grade: int, plus_grade: bool=False) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON deserialized value. '''
        logging.debug("Sending request to PCGS API using ID {0} and grade {1}.".format(pcgs, grade))
        request_url = self.API_URL + "/coindetail/GetCoinFactsByGrade/?PCGSNo={0}&GradeNo={1}&PlusGrade={2}".format(pcgs, grade, plus_grade)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        # Check the result for any errors.
        return self.error_check(result)

    def request_facts_by_barcode(self, barcode: int, service: str) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON deserialized value. 
            Note that the service argument only accepts PCGS or NGC. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByBarcode/?barcode={0}&gradingService={1}".format(barcode, service)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        return self.error_check(result)

    def request_facts_by_cert(self, cert_number: int) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON deserialized value. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByCertNo/{0}".format(cert_number)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        return self.error_check(result)

    def error_check(self, response: requests.Response):
        ''' Checks the result for any errors. '''
        response.raise_for_status()
        result = response.json()
        if result["ServerMessage"] == "No data found":
            logging.error("Coin not found in PCGS database.")
            raise PCGSClient.CoinNotFoundException("Coin not found in PCGS database.")
        elif result["ServerMessage"] == "A server error occurred":
            logging.error("An API error occurred.")
            raise PCGSClient.PCGSApiException("An API error occurred.")
        else:
            return result