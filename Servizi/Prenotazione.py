import datetime


class Prenotazione:
    def __init__(self):
        self.data: datetime.datetime = datetime.datetime(1970, 1, 1, 0, 0)
        self.durata: datetime.timedelta = datetime.timedelta(hours=0, minutes=0)
