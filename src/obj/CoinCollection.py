from Coin import Coin

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
                file.write(coin.serialize_json())

    def add_coin(self, coin: Coin):
        ''' Adds a coin into the collection. '''
        self.collection[coin.pcgs_no] = coin