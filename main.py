import requests

auth = "bearer QLtcuEs-j2rivJqYUHYO9vYa5vL_5nCNef9n3IGiE81o05UKBnBQkPuBiPHG-dTLPvpWz2Pn_cr54ZY2XNUnk2SCtFlRbWcHvsndHKaiTWJmdQaXRabo_Rhw9c4lUkr9ZuziXAWMwzNKUTR8r_3k2M6_E0d6UP9X7OrgA9xRhjkJucU9iVYGDPpQxi_QrNhEFxsw1Q2oF-isNujwN3UDhXTZEM1oZtfBMamH8vHPUbF6YUNFvlQYk5UcGo_Jxkw1KmjN2IOG_wkStbUgbXPLWH_PfW9zt6ZYce9A3aQfV-5DWmlV"
api_url = "https://api.pcgs.com/publicapi/"

headers = {'authorization': auth}

# PCGSNo = 4906
# GradeNo = 3
# PlusGrade = false

# Should output a CSV file. PowerBI/Python integration?
# PCGS Number, name, price
# API requests are manual inputs, everything else is automatic.


def request_facts_by_grade(pcgs, grade, plus_grade):
    # Build the request url.
    request_url = api_url + "coindetail/GetCoinFactsByGrade?PCGSNo=" + pcgs.__str__() + "&GradeNo=" + grade.__str__() + "&PlusGrade=" + plus_grade.__str__()
    print("Sending request for coin facts for coin number " + pcgs.__str__() + "...")
    # Send the request to the server and wait for a response.
    response = requests.get(request_url, headers=headers)
    print("Response received.")
    # Add a check here to ensure there are no errors. This will most likely become its own function.
    return response.json()

def output_csv(data):
    # Creates a CSV file and overwrites any that were previously created.
    csv = open("csvTest.csv", "w")
    # Output all required data from the current list of coins we have.
    # Not really sure where these are stored for right now. To be continued...
    csv.write(data["PCGSNo"].__str__() + "," + data["Name"].__str__() + "," + data["PriceGuideValue"].__str__())

if __name__ == "__main__":
    data = request_facts_by_grade(4906, 3, False)
    output_csv(data)