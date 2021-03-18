from configparser import *
import ast


class ConfKlasse:
    def __init__(self):
        self.config = ConfigParser()

    def skriv(self, navn):
        with open(f'{navn}.ini', 'w') as configfile:
            self.config.write(configfile)

    def skriv_innlogging(self, host=None, port=None, brukernavn=None, passord=None, fil_navn="info", valg_fil=None):
        if valg_fil is None:
            valg_fil = ["host", "port", "username", "password"]
        self.config['INFO'] = {
            "valg": f"{valg_fil}",
            "host": f"{host}",
            "port": f"{port}",
            "username": f"{brukernavn}",
            "password": f"{passord}"
        }
        self.skriv(fil_navn)


    def hent_info(self, filnavn, header=None, hva_hente=None, hent_alt=False):
        self.config.read(filnavn)
        if hent_alt:
            info = self.hent_info(filnavn="info.ini", header="INFO", hva_hente="valg")
            print(info)
            liste = []
            for hva in info:
                print(hva)
                liste.append(self.hent_info(filnavn="info.ini", header="INFO", hva_hente=f"{hva}"))
            return liste

        if hva_hente == "valg":
            return ast.literal_eval(self.config.get(f"{header}", f"{hva_hente}"))
        else:
            return self.config.get(f"{header}", f"{hva_hente}")


"""
CF = ConfKlasse()

CF.skriv_innlogging(host="192.168.0.1", port="22", brukernavn="root", passord="1234")
info = CF.hent_info(filnavn="info.ini", header="INFO", hent_alt=True)
print(info)

"""
