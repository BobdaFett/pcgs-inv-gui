if __name__ == "__main__":
    import sys
    print("Please run the program from the main.py file.")
    sys.exit()

from .Coin import Coin

import json
import os
import logging

class CoinCollection:
    ''' A dictionary wrapper class. Keeps track of all the coins in a collection.
        Coins are hashed into the dictionary using their PCGS number. '''
    def __init__(self):
        # Initialize a list to hold all of the Coin objects
        self.collection: dict[str, Coin] = {}
        self.total = 0

    def __iter__(self):
        ''' Returns an iterator to the underlying dictionary. '''
        return iter(self.collection.values())
    
    def __len__(self) -> int:
        ''' Returns the length of the underlying dictionary. '''
        return self.collection.__len__()
    
    def __getitem__(self, key) -> Coin:
        ''' Returns the Coin object with the corresponding PCGS number. '''
        return self.collection[key]
    
    def __delitem__(self, key):
        ''' Deletes the Coin object with the corresponding PCGS number. '''
        coin = self[key]
        self.total -= coin.total_price
        del self.collection[key]
    
    def read_save_file(self, working_directory="", file_name="collection.json") -> bool:
        ''' Reads a saved JSON file into the collection. 
            Returns a boolean indicating if the saved.json file could be read. '''
        try:
            if working_directory == "":
                working_directory = os.path.realpath(".")
            with open(working_directory + "\\src\\config\\" + file_name, "r") as file:
                logging.info("Save file found. Reading...")
                # Read the file.
                json_obj = json.load(file)
                for coin_dict in json_obj['collection'].values():
                    self.add_coin(Coin(coin_dict))
                logging.info("Save file read successfully.")
                return True
        except FileNotFoundError:
            logging.info("Save file does not exist. Continuing without saved data.")
            return False

    def create_save_file(self, working_directory="", file_name="collection.json"):
        ''' Creates a file that can be used in the read_file() method. '''
        logging.info("Creating save file...")
        if working_directory == "":
            working_directory = os.path.realpath(".")
        path = working_directory + "\\src\\config\\"
        if os.path.exists(path) is False:
            os.mkdir(path)
        with open(working_directory + "\\src\\config\\" + file_name, "w") as file:
            file.write(self.toJson())
        logging.info("Save file created successfully.")

    def dump_csv(self, file_path="collection.csv"):
        ''' Dumps the collection into a CSV file. '''
        with open(file_path, "w") as file:
            logging.info("Creating CSV file...")
            # Set up file headers.
            file.write("Series,Year,Mint,Denomination,Variety,Grade,Designation,Est. Price,PCGS #\n")
            # Serialize and write objects to the file.
            for coin in self:
                file.write(coin.serialize_csv())
            # Set up the footer.
            file.write(",,,,,,Total,${0},".format(self.total))
        print("CSV created at " + file_path)

    def add_coin(self, coin: Coin):
        ''' Adds a coin into the collection. '''
        logging.info("Adding coin with number {0} to collection...".format(coin.PCGSNo))
        self.collection[coin.PCGSNo] = coin
        self.total += coin.total_price * coin.Quantity

    def toJson(self):
        ''' Serializes the collection into a JSON object. '''
        logging.info("Serializing collection to JSON...")
        return json.dumps(self, indent=4, default=lambda o: o.__dict__)