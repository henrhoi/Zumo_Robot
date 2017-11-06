

#Arbitratoren bestemmer hvilke motobs som skal utføres. Motobs gir beskjed til motors hva de skal gjøre
class Motob:

    def __init__(self):
        self.motors = [] #En liste av motorer som sine handlinger vil avgjøres av motob
        self.value = 0 #a holder of the most recent motor recommendation sent to the motob


    def update(self):
        #Motta en motor recommendation, load til value, og operationalize det
        pass

    def operationalize(self):
        #Convert en motor recommendation til en eller flere motor settings, som er sendt til de korresponderene motorene
        pass

