from json import load as jload

class Data:
    def __init__(self, filename:str):
        self.file = filename

    @property
    def json_read(self):
        with open(f"data/{self.file}.json", "r", encoding='utf8') as f:
            return jload(f)
