from ressurser.delt import SqlKobling
from ressurser.pc.logg_inn import loggInn


class lever_utstyr:
    def __init__(self):
        a = loggInn()
        a.show()

class laan_utstyr:
    def __init__(self):
        print("Lån ustyr")


class innstilinger:
    def __init__(self):
        print("Innstilinger")


class tilgjengelig_utstyr:
    def __init__(self):
        print("Tilgjengelig Utstyr")


class rapporter_feil:
    def __init__(self):
        print("Rapporter feil")


class administrasjon:
    def __init__(self):
        print("Administrasjon")