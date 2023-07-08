import requests
from tkinter import *

# The authorization key should be concealed somewhere. Not quite sure how to go about doing this.
auth = "bearer QLtcuEs-j2rivJqYUHYO9vYa5vL_5nCNef9n3IGiE81o05UKBnBQkPuBiPHG-dTLPvpWz2Pn_cr54ZY2XNUnk2SCtFlRbWcHvsndHKaiTWJmdQaXRabo_Rhw9c4lUkr9ZuziXAWMwzNKUTR8r_3k2M6_E0d6UP9X7OrgA9xRhjkJucU9iVYGDPpQxi_QrNhEFxsw1Q2oF-isNujwN3UDhXTZEM1oZtfBMamH8vHPUbF6YUNFvlQYk5UcGo_Jxkw1KmjN2IOG_wkStbUgbXPLWH_PfW9zt6ZYce9A3aQfV-5DWmlV"
api_url = "https://api.pcgs.com/publicapi/"

headers = {'authorization': auth}

# Our current test coin.
# PCGSNo = 4906
# GradeNo = 3
# PlusGrade = false

# Should output a CSV file. PowerBI/Python integration?
# PCGS Number, name, price
# API request requirements are manual inputs, everything else is automatic.

def ok_click(event):
    # Requests and saves the information from the API.
    print("OK button was clicked")
    pcgs = int(pcgs_input.get())
    grade = int(grade_input.get())
    plus = plus_grade.get()

    # Use our utility function in order to send the request to the API.
    response = request_facts_by_grade(pcgs, grade, plus)

    # Save this information somewhere. Not sure where yet.
    output_csv(response)


def csv_click(event):
    # This should open a new window to choose a path for a file with .csv file extension.
    # This is very much a later issue.
    print("Import CSV was clicked")


def request_facts_by_grade(pcgs: int, grade: int, plus_grade: bool):
    # Build the request url.
    request_url = api_url + "coindetail/GetCoinFactsByGrade?PCGSNo=" + pcgs.__str__() + "&GradeNo=" + grade.__str__() + "&PlusGrade=" + plus_grade.__str__()
    print("Sending request for coin facts for coin number " + pcgs.__str__() + "...")
    
    # Send the request to the server and wait for a response.
    response = requests.get(request_url, headers=headers)
    print("Response received.")

    # Add a check here to ensure there are no errors. This will most likely become its own function.
    return response.json()


def output_csv(data: dict):
    # Creates a CSV file and overwrites any that were previously created.
    csv = open("csvTest.csv", "w")

    # Output all required data from the current list of coins we have.
    # Not really sure how or where these are stored for right now. To be continued...
    csv.write(data["PCGSNo"].__str__() + "," + data["Name"].__str__() + "," + data["PriceGuideValue"].__str__())

    print("File written successfully.")


# Create the window. We want these to be public (even though it makes me cringe)
# TODO Move this into a class. This shouldn't be attached to the file here.

window = Tk()
window.title("Coin Search")

plus_grade = BooleanVar()

pcgs_input = Entry()
grade_input = Entry()
plus_input = Checkbutton(offvalue=False, onvalue=True, variable=plus_grade)

pcgs_label = Label(text="PCGS Number:", padx=15)
grade_label = Label(text="Coin Grade:", padx=15)
plus_label = Label(text="Plus Grade:", padx=15)

ok_button = Button(text="OK", padx=5, pady=5)
ok_button.bind("<Button-1>", ok_click)

pcgs_input.grid(row=0, column=1, pady=5)
grade_input.grid(row=1, column=1, pady=5)
plus_input.grid(row=2, column=1, pady=5)
pcgs_label.grid(row=0, column=0, pady=5)
grade_label.grid(row=1, column=0, pady=5)
plus_label.grid(row=2, column=0, pady=5)
ok_button.grid(row=3, columnspan=2, column=0, pady=10)

window.mainloop()
