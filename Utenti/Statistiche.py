import matplotlib.pyplot as plt

class Statistiche:
    def __init__(self):
        self.report = ""
        self.tabella_mesi = ["Gen", "Feb", "Mar", "Apr", "Mag", "Giu", "Lug", "Ago", "Set", "Ott", "Nov", "Dic"]
        self.tabella_numero_clienti = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


    def mostraGrafico(self,tabella_mesi,tabella_numero_clienti):
        # Creazione della figura e dell'asse
        fig, ax = plt.subplots(figsize=(7, 5))

        # Creazione del grafico a barre
        ax.bar(tabella_mesi, tabella_numero_clienti, color="skyblue")

        # Aggiungere titoli e etichette
        ax.set_title("Numero di clienti per mese")
        ax.set_xlabel("Mesi")
        ax.set_ylabel("Numero di clienti")

        # Mostrare il grafico
        plt.show()


        


