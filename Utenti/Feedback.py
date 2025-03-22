import datetime


class Feedback:
    def __init__(self):
        self.contenuto: str = ""
        self.data: datetime.datetime = datetime.datetime(1970,1,1,0,0)