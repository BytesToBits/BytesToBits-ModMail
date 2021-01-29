from yaml import load as yload, FullLoader
class Data:
    def __init__(self, filename:str):
        self.file = filename

    def yaml_read(self):
        with open(f"data/{self.file}.yml", "r", encoding='utf8') as f:
            return yload(f, Loader=FullLoader)
