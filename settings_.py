import json

class Settings:

    def __init__(self):
        json_file = open("set_file.json")
        dectionary = json.load(json_file)
        self.record_path = dectionary['record_path']
        self.lesson_path = dectionary['lesson_path']



