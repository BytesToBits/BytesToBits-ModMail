from yaml import load as yload, FullLoader
class Data:
    def __init__(self, filename:str):
        self.file = filename

<<<<<<< Updated upstream
    @property
    def json_read(self):
        with open(f"data/{self.file}.json", "r", encoding='utf8') as f:
            return jload(f)
=======
    def yaml_read(self):
        with open(f"data/{self.file}.yml", "r") as f:
            return yload(f, Loader=FullLoader)
>>>>>>> Stashed changes
