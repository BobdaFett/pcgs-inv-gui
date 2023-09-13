import requests
import logging


class PCGSClient:
    class CoinNotFoundException(Exception):
        """ Raised when the coin is not found in the PCGS database. """
        pass

    class PCGSApiException(Exception):
        """ Raised when the PCGS API returns an unidentified error. """
        pass

    class APIKeyInvalidException(Exception):
        """ Raised when the PCGS API returns a code 401 (unauthorized) """
        pass

    def __init__(self, api_key):
        self.API_URL = "https://api.pcgs.com/publicapi"
        self.API_KEY = api_key
        logging.debug("PCGSClient initialized.")
        # TODO Find out if there's a way to test the api before using it. Allows raising errors.

    def request_facts_by_grade(self, pcgs: int, grade: int, plus_grade: bool = False) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON deserialized value. '''
        logging.debug("Sending request to PCGS API using ID {0} and grade {1}.".format(pcgs, grade))
        request_url = self.API_URL + "/coindetail/GetCoinFactsByGrade/?PCGSNo={0}&GradeNo={1}&PlusGrade={2}".format(
            pcgs, grade, plus_grade)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        # Check the result for any errors.
        return self.error_check(result)

    def request_facts_by_barcode(self, barcode: int, service: str) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON deserialized value. 
            Note that the service argument only accepts PCGS or NGC. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByBarcode/?barcode={0}&gradingService={1}".format(barcode,
                                                                                                                service)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        return self.error_check(result)

    def request_facts_by_cert(self, cert_number: int) -> dict:
        ''' Handles sending a request to the PCGS Public API. Returns a JSON deserialized value. '''
        request_url = self.API_URL + "/coindetail/GetCoinFactsByCertNo/{0}".format(cert_number)
        result = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        return self.error_check(result)

    def error_check(self, response: requests.Response):
        ''' Checks the result for any errors. '''
        try:
            response.raise_for_status()
        except requests.HTTPError as e:
            if e.response.status_code == 401:
                raise self.APIKeyInvalidException("API key is invalid. Please reconfigure your API key.")
        result = response.json()
        if result["ServerMessage"] == "No data found":
            logging.error("Coin not found in PCGS database.")
            raise PCGSClient.CoinNotFoundException("Coin not found in PCGS database.")
        elif result["ServerMessage"] == "A server error occurred":
            logging.error("An API error occurred.")
            raise PCGSClient.PCGSApiException("An API error occurred.")
        else:
            return result

    def test_key(self):
        """ Send a request for an invalid coin. This is very fast, and will allow the program to tell if the
            API key is functional or not by simply checking the HTTP status code. Should the key be valid,
            this will return with a code 200 regardless of whether the coin is real or not. Should the key
            be invalid, the requests package will throw an HTTPError stating that there was an HTTP code
            401 (unauthorized). This should be handled externally to this file. """
        request_url = self.API_URL + "/coindetail/GetCoinFactsByGrade/?PCGSNo=1&GradeNo=1&PlusGrade=False"
        response = requests.get(request_url, headers={'authorization': 'bearer ' + self.API_KEY})
        response.raise_for_status()
