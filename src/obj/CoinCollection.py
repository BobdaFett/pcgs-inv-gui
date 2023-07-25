from .Coin import Coin

class CoinCollection:
    ''' A dictionary wrapper class. Keeps track of all the coins in a collection.
        Coins are hashed into the dictionary using their PCGS number. As such,
        the key to access them is that number.'''
    def __init__(self):
        # Initialize a list to hold all of the Coin objects
        self.collection: dict[str, Coin] = {}
        self.current_index = 0
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
    
    # TODO Finish this function.
    def read_file(self, file_path: str):
        ''' Reads a saved JSON file into the collection. '''
        with open(file_path, "r") as file:
            # Read the file.
            obj_str = file.read()

    def dump_json(self, file_path="saved.txt"):
        ''' Creates a file that can be used in the read_file() method. '''
        with open(file_path, "w") as file:
            # Serialize and write objects to the file.
            for coin in self:
                file.write(coin.serialize_json())

    def dump_csv(self, file_path="collection.csv"):
        with open(file_path, "w") as file:
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
        self.collection[coin.pcgs_no] = coin
        self.total += coin.total_price * coin.quantity
