from functions.additional_functions import *
import decimal
from models import Artikel, Kellne1, Kellner

def rwaiter_admin_copy_waiterbl(r_kellner:int, dept2:int, dept:int, crart2:int):
    artikel = kellne1 = kellner = None

    toart1 = toart2 = waiter1 = waiter2 = None

    Toart1 = Artikel
    Toart2 = Artikel
    Waiter1 = Kellne1
    Waiter2 = Kellner

    db_session = local_storage.db_session

    def generate_output():
        nonlocal artikel, kellne1, kellner
        nonlocal toart1, toart2, waiter1, waiter2


        nonlocal toart1, toart2, waiter1, waiter2
        return {}


    kellner = db_session.query(Kellner).filter(
            (Kellner._recid == r_kellner)).first()

    toart2 = db_session.query(Toart2).filter(
            (Toart2.artnr == kellner.kumsatz_nr) &  (Toart2.departement == dept2)).first()

    if not toart2:

        toart1 = db_session.query(Toart1).filter(
                (Toart1.artnr == kellner.kumsatz_nr) &  (Toart1.departement == dept)).first()
        buffer_copy(toart1, toart2,except_fields=["departement"])
        toart2.departement = dept2

    toart2 = db_session.query(Toart2).filter(
            (Toart2.artnr == kellner.kzahl_nr) &  (Toart2.departement == dept2)).first()

    if not toart2:
        toart2 = Toart2()
        db_session.add(toart2)


        toart1 = db_session.query(Toart1).filter(
                (Toart1.artnr == kellner.kzahl_nr) &  (Toart1.departement == dept)).first()
        buffer_copy(toart1, toart2,except_fields=["departement"])
        toart2.departement = dept2

    waiter2 = db_session.query(Waiter2).filter(
            (Waiter2.departement == dept2) &  (Waiter2.kumsatz_nr == kellner.kumsatz_nr)).first()

    if waiter2:

        waiter2 = db_session.query(Waiter2).first()
        buffer_copy(kellner, waiter2,except_fields=["kcredit_nr","departement"])
        waiter2.kcredit_nr = crart2
        waiter2.departement = dept2


    else:

        kellner = db_session.query(Kellner).filter(
                (Kellner._recid == r_kellner)).first()
        waiter2 = Waiter2()
        db_session.add(waiter2)

        buffer_copy(kellner, waiter2,except_fields=["kcredit_nr","departement"])
        waiter2.kcredit_nr = crart2
        waiter2.departement = dept2

    waiter2 = db_session.query(Waiter2).first()


    waiter1 = db_session.query(Waiter1).filter(
            (Waiter1.kellner_nr == kellner_nr) &  (Waiter1.departement == dept2)).first()

    if not waiter1:
        waiter1 = Waiter1()
        db_session.add(waiter1)

        buffer_copy(kellner, waiter1,except_fields=["departement"])
        waiter1.departement = dept2


    return generate_output()