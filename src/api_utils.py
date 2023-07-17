import requests
import config

API_URL = "https://api.pcgs.com/publicapi"

def request_facts_by_grade(pcgs: int, grade: int, plus_grade: bool=False) -> dict:
    ''' Handles sending a request to the PCGS Public API. Returns a JSON serialized value. '''
    request_url = API_URL + "/coindetail/GetCoinFactsByGrade/?PCGSNo={0}&GradeNo={1}&PlusGrade={2}".format(pcgs, grade, plus_grade)
    result = requests.get(request_url, headers={'authorization': 'bearer ' + config.PCGS_CERT})
    result.raise_for_status()
    return result.json()

def request_facts_by_barcode(barcode: int, service: str) -> dict:
    ''' Handles sending a request to the PCGS Public API. Returns a JSON serialized value. 
        Note that the service argument only accepts PCGS or NGC. '''
    request_url = API_URL + "/coindetail/GetCoinFactsByBarcode/?barcode={0}&gradingService={1}".format(barcode, service)
    result = requests.get(request_url, headers={'authorization': 'bearer ' + config.PCGS_CERT})
    result.raise_for_status()
    return result.json()

def request_facts_by_cert(cert_number: int) -> dict:
    ''' Handles sending a request to the PCGS Public API. Returns a JSON serialized value. '''
    request_url = API_URL + "/coindetail/GetCoinFactsByCertNo/{0}".format(cert_number)
    result = requests.get(request_url, headers={'authorization': 'bearer ' + config.PCGS_CERT})
    result.raise_for_status()
    return result.json()