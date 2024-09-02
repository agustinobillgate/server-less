from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Mathis, Fa_artikel, Htparam, Fa_op, Counters

def fa_move_move_itbl(location_str:str, qty:int, user_init:str, artnr:int):
    anz1 = 0
    anz2 = 0
    mathis = fa_artikel = htparam = fa_op = counters = None

    fabuff = mabuff = None

    Fabuff = Fa_artikel
    Mabuff = Mathis

    db_session = local_storage.db_session

    def generate_output():
        nonlocal anz1, anz2, mathis, fa_artikel, htparam, fa_op, counters
        nonlocal fabuff, mabuff


        nonlocal fabuff, mabuff
        return {"anz1": anz1, "anz2": anz2}

    def move_it():

        nonlocal anz1, anz2, mathis, fa_artikel, htparam, fa_op, counters
        nonlocal fabuff, mabuff


        nonlocal fabuff, mabuff

        found:bool = False
        billdate:date = None
        Fabuff = Fa_artikel
        Mabuff = Mathis

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 474)).first()
        billdate = htparam.fdate

        for mabuff in db_session.query(Mabuff).filter(
                (Mabuff.name == mathis.name) &  (func.lower(Mabuff.location) != mathis.location) &  (Mabuff.asset == mathis.asset) &  (func.lower(Mabuff.location) == (location_str).lower())).all():

            fabuff = db_session.query(Fabuff).filter(
                    (Fabuff.nr == mabuff.nr)).first()

            if fabuff.katnr == fa_artikel.katnr and fabuff.gnr == fa_artikel.gnr and fabuff.subgrp == fa_artikel.subgrp and fabuff.anz_depn == fa_artikel.anz_dep and fabuff.loeschflag == 0 and fabuff._recid != fa_artikel._recid:
                found = True
                break

        if found:
            fa_op = Fa_op()
            db_session.add(fa_op)

            fa_op.nr = mathis.nr
            fa_op.opart = 2
            fa_op.datum = billdate
            fa_op.zeit = get_current_time_in_seconds()
            fa_op.anzahl = qty
            fa_op.einzelpreis = fa_artikel.book_wert / fa_artikel.anzahl
            fa_op.warenwert = fa_op.einzelpreis * qty
            fa_op.id = user_init
            fa_op.docu_nr = mathis.name + ";;" +\
                    mathis.location + ";;" +\
                    location_str + ";;" +\
                    "YES" + ";;" +\
                    to_string(get_year(get_current_date())) + to_string(get_month(get_current_date()) , "99") +\
                    to_string(get_day(get_current_date()) , "99") + ";;"

            fa_op = db_session.query(Fa_op).first()


            fabuff = db_session.query(Fabuff).first()

            fa_artikel = db_session.query(Fa_artikel).first()

            if fa_artikel.anzahl == qty:
                fabuff.warenwert = fabuff.warenwert + fa_artikel.warenwert
                fabuff.book_wert = fabuff.book_wert + fa_artikel.book_wert
                fabuff.depn_wert = fabuff.depn_wert + fa_artikel.depn_wert
                fabuff.anzahl = fabuff.anzahl + qty
                fabuff.anz100 = fabuff.anzahl + qty
                fabuff.cid = user_init
                fabuff.changed = get_current_date()
                fa_artikel.loeschflag = 1
                fa_artikel.deleted = get_current_date()


            else:
                fabuff.warenwert = fabuff.warenwert +\
                        fa_artikel.warenwert * qty / fa_artikel.anzahl
                fabuff.book_wert = fabuff.book_wert +\
                        fa_artikel.book_wert * qty / fa_artikel.anzahl
                fabuff.depn_wert = fabuff.depn_wert +\
                        fa_artikel.depn_wert * qty / fa_artikel.anzahl
                fabuff.anzahl = fabuff.anzahl + qty
                fabuff.anz100 = fabuff.anzahl + qty


                fa_artikel.warenwert = fa_artikel.warenwert *\
                        (1 - qty / fa_artikel.anzahl)
                fa_artikel.book_wert = fa_artikel.book_wert *\
                        (1 - qty / fa_artikel.anzahl)
                fa_artikel.depn_wert = fa_artikel.depn_wert *\
                        (1 - qty / fa_artikel.anzahl)
                fa_artikel.anzahl = fa_artikel.anzahl - qty
                fa_artikel.anz100 = fa_artikel.anzahl - qty

                fa_artikel = db_session.query(Fa_artikel).first()
            anz1 = 11
            anz2 = 22


        else:
            fa_op = Fa_op()
            db_session.add(fa_op)

            fa_op.nr = mathis.nr
            fa_op.opart = 2
            fa_op.datum = billdate
            fa_op.zeit = get_current_time_in_seconds()
            fa_op.anzahl = qty
            fa_op.einzelpreis = fa_artikel.book_wert / fa_artikel.anzahl
            fa_op.warenwert = fa_op.einzelpreis * qty
            fa_op.id = user_init
            fa_op.docu_nr = mathis.name + ";;" +\
                    mathis.location + ";;" +\
                    location_str + ";;" +\
                    "NO" + ";;" +\
                    to_string(get_year(get_current_date())) + to_string(get_month(get_current_date()) , "99") +\
                    to_string(get_day(get_current_date()) , "99") + ";;"

            fa_op = db_session.query(Fa_op).first()


            if fa_artikel.anzahl == qty:

                mathis = db_session.query(Mathis).first()
                mathis.location = location_str

                mathis = db_session.query(Mathis).first()
            else:

                counters = db_session.query(Counters).filter(
                        (Counters.counter_no == 17)).first()
                counters.counter = counters.counter + 1

                counters = db_session.query(Counters).first()
                mabuff = Mabuff()
                db_session.add(mabuff)

                buffer_copy(mathis, mabuff,except_fields=["mathis.nr"])
                mabuff.nr = counters.counter
                mabuff.location = location_str

                mabuff = db_session.query(Mabuff).first()
                fabuff = Fabuff()
                db_session.add(fabuff)

                buffer_copy(fa_artikel, fabuff,except_fields=["fa_artikel.nr"])
                fabuff.nr = counters.counter
                fabuff.anzahl = qty
                fabuff.anz100 = qty
                fabuff.warenwert = fa_artikel.warenwert * qty / fa_artikel.anzahl
                fabuff.book_wert = fa_artikel.book_wert * qty / fa_artikel.anzahl
                fabuff.depn_wert = fa_artikel.depn_wert * qty / fa_artikel.anzahl

                fabuff = db_session.query(Fabuff).first()

                fa_artikel = db_session.query(Fa_artikel).first()
                fa_artikel.warenwert = fa_artikel.warenwert *\
                        (1 - qty / fa_artikel.anzahl)
                fa_artikel.book_wert = fa_artikel.book_wert *\
                        (1 - qty / fa_artikel.anzahl)
                fa_artikel.depn_wert = fa_artikel.depn_wert *\
                        (1 - qty / fa_artikel.anzahl)
                fa_artikel.anzahl = fa_artikel.anzahl - qty
                fa_artikel.anz100 = fa_artikel.anzahl - qty
                fa_artikel.cid = user_init
                fa_artikel.changed = get_current_date()

                fa_artikel = db_session.query(Fa_artikel).first()


    mathis = db_session.query(Mathis).filter(
            (Mathis.nr == artnr)).first()

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.nr == artnr)).first()
    move_it()

    return generate_output()