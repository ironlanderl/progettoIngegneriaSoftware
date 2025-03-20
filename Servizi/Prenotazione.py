import datetime


class Prenotazione():
    def __init__(self):
        self.data = datetime.datetime(1970,0,0,0,0)
        self.durata = datetime.timedelta(hours = 0,minutes = 0)
