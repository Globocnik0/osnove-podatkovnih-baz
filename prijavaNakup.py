import auth
from baze import *
from simulacijaPodatkov import *
import psycopg2, psycopg2.extensions, psycopg2.extras
from tabulate import tabulate

psycopg2.extensions.register_type(psycopg2.extensions.UNICODE)

import csv


conn = psycopg2.connect(dbname = auth.db, host = auth.host, user = auth.user, password = auth.password)
cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

def registracijaUporabnika(podatki): #podatki so [emso, ime, rojstvo, naslov, mail, geslo]
    cur.execute(""" SELECT mail from uporabnik where mail = %s """, [podatki[4]])
    mailObstaja = cur.fetchall()
    if mailObstaja:
        return False

    cur.execute(""" SELECT emso from uporabnik where emso = %s """,[podatki[0]])
    emsoObstaja = cur.fetchall()
    if emsoObstaja:
        return False

    print('registriran')
    cur.execute("""INSERT INTO uporabnik(emso, ime, rojstvo, naslov, mail, geslo) values (%s, %s, %s, %s, %s, %s)""", podatki)
    conn.commit()
    return True
        

def nakupKarte(podatki): #[emso, vpostaja, ipostaja, vrsta Karte, cena]
    
    emso = podatki[0]
    vpostaja = podatki[1]
    ipostaja = podatki[2]
    vrsta = podatki[3]
    cena = podatki[4]
    cur.execute("""SELECT velja FROM vozovnica WHERE id = {} """.format(vrsta))
    velja = cur.fetchall()[0][0]
    cur.execute(""" INSERT INTO kupljeneKarte (uporabnik, vrstakarte, datum_nakupa, datumveljavnosti, vstopnaPostaja, iztopnaPostaja, cena)
                    values(%s, %s, (SELECT CURRENT_DATE), (SELECT (SELECT CURRENT_DATE + INTERVAL '%s day')::TIMESTAMP::DATE), %s,%s,%s)
                    """, [emso, vrsta, velja, vpostaja, ipostaja, cena])
    conn.commit()

# nakupKarte(["1835012", 1])
#registracijaUporabnika(["000", "Kranj", "2022-02-02", "asdasdasd", "mailZaBednike", "123123123"] )

def prijava(uporabniskoIme, geslo):
    cur.execute(""" SELECT mail from uporabnik where mail = %s """, [uporabniskoIme])
    mailObstaja = cur.fetchall()
    
    if mailObstaja == []:
        return False

    
    cur.execute(""" SELECT geslo from uporabnik where mail = %s """, [uporabniskoIme])
    g = cur.fetchall()
    if g[0][0] == geslo:
        return True
    else: 
        return False

def dobiEmso(mail):
    cur.execute("""SELECT emso FROM uporabnik WHERE mail = %s """, [mail])
    podatki = cur.fetchall()
    return podatki[0][0]

def informacijeUporabnika(emso):
    cur.execute("""SELECT ime, rojstvo, naslov, mail FROM uporabnik WHERE emso = %s """, [emso])
    podatki = cur.fetchall()
    return podatki[0]

def informacijeUporabnikaNakupi(emso):
    cur.execute("""SELECT opis, datum_nakupa, datumveljavnosti, vstopnapostaja, iztopnapostaja, kk.velja FROM kupljenekarte kk
                    JOIN vozovnica v on v.id = kk.vrstakarte
                    WHERE kk.uporabnik = %s""", [emso])
    podatki = cur.fetchall()
    return podatki #vrne opis karte, datum nakupa, datumveljavnosti, vstopnapostaja, iztopnapostaja, velja(boolean)


#podatki = ["8", "Alex", "08-08-2022", "Britof", "abcd@mail", "123123"]
#print(registracijaUporabnika(podatki))
#print(informacijeUporabnika("0000"))
#print(dobiEmso("nekej@asd"))
#podatkiNakupKarte = ["8", None, None, 1, 102] #[emso, vpostaja, ipostaja, vrsta Karte, cena]
#nakupKarte(podatkiNakupKarte)
#rint(informacijeUporabnikaNakupi("8"))
