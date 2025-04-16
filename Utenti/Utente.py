from typing import override


class Utente:
    def __init__(self, nome: str, cognome: str, username: str, password: str):
        self._nome: str = ""
        self._cognome: str = ""
        self._password: str = ""
        self._username: str = ""
        self.nome: str = nome
        self.cognome: str = cognome
        self.username: str = username
        self.password: str = password

        self._amministratore = False
        

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, nome: str):
        if nome == "":
            raise ValueError("Il nome non può essere vuoto")
        self._nome = nome

    @property
    def cognome(self):
        return self._cognome

    @cognome.setter
    def cognome(self, cognome: str):
        if cognome == "":
            raise ValueError("Il cognome non può essere vuoto")
        self._cognome = cognome

    @property
    def username(self):
        return self._username

    @username.setter
    def username(self, username: str):
        if username == "":
            raise ValueError("Lo username non può essere vuoto")
        if self._username != "":
            raise ValueError("Lo username non può essere modificato")
        self._username = username

    @property
    def password(self):
        return self._password

    @password.setter
    def password(self, password: str):
        if password == "":
            raise ValueError("La password non può essere vuota")
        if self._password == password:
            raise ValueError("La password è uguale a quella attuale")
        self._password = password

    @property
    def amministratore(self):
        return self._amministratore

    @amministratore.setter
    def amministratore(self, amministratore: bool):
        self._amministratore = amministratore

    @override
    def __str__(self):
        return self.username
