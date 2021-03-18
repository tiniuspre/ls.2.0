import logging
from datetime import *
import mysql.connector


logging.basicConfig(filename='logg.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s\n', datefmt='%d-%b-%y %H:%M:%S', level='DEBUG')

# Debug Level:
# 0 : Viser ingenting
# 1 : Viser uforventete feil.
# 2 : Viser forventede feil.
# 3 : Viser bare tilkoblingsfeil


class HentFraSql:
    def __init__(self, debug_level=1, host_til_db="localhost", bruker="root", passord="*", database_db="datab"):
        self._Debug = debug_level
        try:
            self._db = mysql.connector.connect(host=f"{host_til_db}", user=f"{bruker}", password=f"{passord}", database=f"{database_db}")
            self._cursor = self._db.cursor()
            logging.info("Koblet til database")

        except Exception as Feil:
            logging.error(f"Feil ved tilkobling av DB, Feil = {Feil} (Brukernavn = {bruker}, passord = {passord}, host = {host_til_db}, lisens = {database_db})")
            if self.Debug > 3 or self.Debug == 1:
                raise Exception(f"Tilkoblingsfeil til DB: {Feil}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.commit()
        self.close()

    @property
    def connection(self):
        return self._db

    @property
    def Debug(self):
        return self._Debug

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        logging.info("Lagrer til DB")
        self.connection.commit()

    def close(self, commit=True):
        try:
            logging.info("Lukker tilkobling til DB")
            if commit:
                self.commit()
            self.connection.close()
        except Exception as Feil:
            logging.error(f"Feil ved lukking av DB, feil = {Feil}")
            if self.Debug == 1:
                raise Exception(Feil)

    def execute(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
            logging.info(f"Executer SQL = {sql}, parametere = {params}")
            self.commit()
        except Exception as Feil:
            logging.error(f"Feil ved executing av sql = {Feil}, parametere = {params}")
            if self.Debug == 1:
                raise Exception(f"Feil ved executing av sql = {Feil}, parametere = {params}")

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        try:
            self.cursor.execute(sql, params or ())
            return self.fetchall()
        except Exception as Feil:
            logging.error(f"Feil ved query, Feil = {Feil}, SQL = {sql}, parametere = {params}")
            if self.Debug == 1:
                raise Exception(f"Feil ved query, Feil = {Feil}, SQL = {sql}, parametere = {params}")

    @staticmethod
    def sorter(curr):
        hva = []
        for hvem in curr:
            bruker_info = []
            for info in hvem:
                bruker_info.append(info)
            hva.append(bruker_info)

        return hva

    def hent_utstyr(self, tabell="tilgjengelig_utstyr"):
        self.cursor.execute(f"SELECT * FROM {tabell}")
        return self.sorter(self.cursor)

    def legg_til_utstyr(self, navn, kvantitet, klasse="alle", kode=None):
        if kvantitet is not int:
            raise Exception("Kvantitet må være integer")
        if kvantitet <= 0:
            raise Exception("Kvantitet må være >= 1")
        if kvantitet is None:
            for tabell_navn in ["tilgjengelig_utstyr", "total_ustyr"]:
                self.cursor.execute(f"INSERT INTO {tabell_navn} (navn, kvantitet, datoLagtTil, klasse, kode) VALUES ('{str(navn.lower())}','{str(kvantitet)}','{str(datetime.now().strftime('%Y-%m-%d'))}', '{str(klasse)}', '{str(kode)}')")
                self.commit()

    def lag_tabell(self, tabell_navn=None, argumenter=None):
        try:
            if tabell_navn is None and self.Debug == 2:
                logging.error(f'Tabell ikke laget navn = {tabell_navn}')
                raise NameError(f'{tabell_navn}')
            else:
                self.cursor.execute(f'CREATE TABLE {tabell_navn}({argumenter})')
                self.commit()
                logging.info(f'Tabell laget navn = {tabell_navn}')
        except mysql.connector.errors.ProgrammingError as Feil:
            logging.warning(f'Tabell finnes, navn = {tabell_navn}, FEIL = {Feil}')

    def fjern_utstyr(self, navn_utsyr, loning=False, antall=0):
        if antall == 0:
            raise Exception(f"Antall kan ikke være {antall}")
        if not loning:
            self.cursor.execute(f"DELETE FROM tilgjengelig_utstyr WHERE navn = '{navn_utsyr}'")
            self.commit()
            logging.info(f"Fjernet {navn_utsyr}")
        if loning:
            self.cursor.execute(f"UPDATE FROM tilgjengelig_utstyr SET ")
            self.commit()

    def hent_brukere(self, navn_="alle", klasse_="alle", rettighet_="alle"):
        if klasse_.lower() == "alle" or "*":
            klasse_ = "*"
        if rettighet_.lower() == "alle" and navn_.lower() == "alle":
            self.cursor.execute(f"SELECT {klasse_} FROM brukere")
            return self.sorter(self.cursor)
        if navn_.lower() != "alle":
            self.cursor.execute(f"SELECT {klasse_} FROM brukere WHERE navn = '{navn_}' ")
            return self.sorter(self.cursor)

    def legg_til_bruker(self, navn_=None, epost_=None, telefon_nr_=None, klasse_=None, pin_=None, rettigheter_=None):
        feil = False
        try:
            bruker_info = [navn_, epost_, klasse_, pin_, rettigheter_]
            for info in bruker_info:
                if info is None:
                    feil = True
                    break
            if feil:
                logging.info("Ufulstendig fylt inn når bruker lagt til.")
                if self.Debug == 1:
                    print("Fyll ut info til bruker")
                    raise Exception("Fyll ut info til bruker")
                return
            else:
                dato = datetime.now().strftime('%Y-%m-%d')
                self.cursor.execute(f"INSERT INTO brukere (navn,epost,telefonNr,klasse,pin,rettigheter,datoLagtTil) VALUES ('{navn_.lower()}','{epost_.lower()}','{telefon_nr_.lower()}','{klasse_.lower()}','{pin_.lower()}','{rettigheter_.lower()}','{dato}')")
                self.commit()
                logging.info(f"Bruker {navn_} er lagt til")
        except Exception as Feil:
            print(Feil)
            logging.error(f"Feil inlegging av bruker feil = {Feil}")

    def legg_til_klasse(self, klasse_0=None, klasse_1=None, klasse_2=None, klasse_3=None, klasse_4=None):
        data_i_klasser = self.query("SELECT * FROM klasser limit 1")
        if not data_i_klasser:
            self.cursor.execute("INSERT INTO klasser (klasse0, klasse1, klasse2, klasse3, klasse4) VALUES (NULL, NULL, NULL, NULL, NULL)")
            self.commit()
        #  print(self.cursor)
        #  for i in self.cursor:
        #      if i == None:
        #          print("AAA")
        #  klasserListe = [klasse_0, klasse_1, klasse_2, klasse_3, klasse_4]


class testKobling():
    def test(self, host=f"localhost", user=f"root", password=f"128bwn", database=f"datab"):
        try:
            mysql.connector.connect(host=f"{host}", user=f"{user}", password=f"{password}", database=f"{database}")
            return "Kobling fungerer"
        except mysql.connector.errors.InterfaceError as Feil:
            return "Kobling Feilet"



HentFraSql = HentFraSql(debug_level=2)

HentFraSql.lag_tabell(tabell_navn="brukere", argumenter='navn VARCHAR(255), epost VARCHAR(255), telefonNr VARCHAR(255), klasse VARCHAR(255), pin VARCHAR(255), rettigheter VARCHAR(255), datoLagtTil VARCHAR(255)')
HentFraSql.lag_tabell(tabell_navn="lont_utstyr", argumenter=' hvem VARCHAR(255), epost VARCHAR(255), telefonNr VARCHAR(255), klasse VARCHAR(255), hvaLont VARCHAR(255), datoLont VARCHAR(255), dagerLont VARCHAR(255), tilbakeLont VARCHAR(255), dagerSidenVarsling VARCHAR(255)')
HentFraSql.lag_tabell(tabell_navn="total_ustyr", argumenter='navn VARCHAR(255), kvantitet VARCHAR(255), datoLagtTil VARCHAR(255), klasse VARCHAR(255), kode VARCHAR(255)')
HentFraSql.lag_tabell(tabell_navn="tilgjengelig_utstyr", argumenter='navn VARCHAR(255), kvantitet VARCHAR(255), datoLagtTil VARCHAR(255), klasse VARCHAR(255), kode VARCHAR(255)')
HentFraSql.lag_tabell(tabell_navn="klasser", argumenter="klasse0 VARCHAR(255), klasse1 VARCHAR(255), klasse2 VARCHAR(255), klasse3 VARCHAR(255), klasse4 VARCHAR(255)")

#  HentFraSql.legg_til_bruker(navn_="test", epost_="test@epost.no", telefon_nr_="12345678", klasse_="VG2", pin_="4321", rettigheter_="bruker")

