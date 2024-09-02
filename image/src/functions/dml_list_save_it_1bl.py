from functions.additional_functions import *
import decimal
from datetime import date
from models import Dml_art, Queasy, Dml_artdep

def dml_list_save_it_1bl(curr_dept:int, cbuff_artnr:int, cbuff_qty:decimal, selected_date:date, user_init:str, cbuff_price:decimal, cbuff_lief_nr:int, cbuff_approved:bool, cbuff_remark:str):
    dml_art = queasy = dml_artdep = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_art, queasy, dml_artdep


        return {}


    if curr_dept == 0:

        dml_art = db_session.query(Dml_art).filter(
                (Dml_art.artnr == cbuff_artnr) &  (Dml_art.datum == selected_date)).first()

        if not dml_art:
            dml_art = Dml_art()
            db_session.add(dml_art)

            dml_art.artnr = cbuff_artnr
            dml_art.datum = selected_date
            dml_art.userinit = user_init


        dml_art.anzahl = cbuff_qty
        dml_art.einzelpreis = cbuff_price
        dml_art.userinit = entry(0, dml_art.userinit, ";")
        dml_art.chginit = user_init

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 202) &  (Queasy.number1 == 0) &  (Queasy.number2 == cbuff_artnr) &  (Queasy.date1 == selected_date)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 202
            queasy.number1 = 0
            queasy.number2 = cbuff_artnr
            queasy.date1 = selected_date
            queasy.char1 = cbuff_remark


        else:

            queasy = db_session.query(Queasy).first()
            queasy.char1 = cbuff_remark

            queasy = db_session.query(Queasy).first()


        if cbuff_lief_nr > 0:
            dml_art.userinit = dml_art.userinit +\
                ";" + to_string(cbuff_lief_nr)

        if cbuff_approved:
            dml_art.chginit = dml_art.chginit + "!"

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 254) &  (Queasy.number1 == 0) &  (Queasy.date1 == dml_art.datum) &  (Queasy.logi1) &  (Queasy.logi2 == False)).first()

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 254
                queasy.number1 = 0
                queasy.date1 = dml_art.datum
                queasy.logi1 = True
                queasy.logi2 = False

        dml_art = db_session.query(Dml_art).first()
    else:

        dml_artdep = db_session.query(Dml_artdep).filter(
                (Dml_artdep.artnr == cbuff_artnr) &  (Dml_artdep.datum == selected_date) &  (Dml_artdep.departement == curr_dept)).first()

        if not dml_artdep:
            dml_artdep = Dml_artdep()
            db_session.add(dml_artdep)

            dml_artdep.artnr = cbuff_artnr
            dml_artdep.datum = selected_date
            dml_artdep.departement = curr_dept
            dml_artdep.userinit = user_init


        dml_artdep.anzahl = cbuff_qty
        dml_artdep.einzelpreis = cbuff_price
        dml_artdep.userinit = entry(0, dml_artdep.userinit, ";")
        dml_artdep.chginit = user_init

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 202) &  (Queasy.number1 == curr_dept) &  (Queasy.number2 == cbuff_artnr) &  (Queasy.date1 == selected_date)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 202
            queasy.number1 = curr_dept
            queasy.number2 = cbuff_artnr
            queasy.date1 = selected_date
            queasy.char1 = cbuff_remark


        else:

            queasy = db_session.query(Queasy).first()
            queasy.char1 = cbuff_remark

            queasy = db_session.query(Queasy).first()


        if cbuff_lief_nr > 0:
            dml_artdep.userinit = dml_artdep.userinit +\
                ";" + to_string(cbuff_lief_nr)

        if cbuff_approved:
            dml_artdep.chginit = dml_artdep.chginit + "!"

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 254) &  (Queasy.number1 == dml_artdep.departement) &  (Queasy.date1 == dml_artdep.datum) &  (Queasy.logi1) &  (Queasy.logi2 == False)).first()

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 254
                queasy.number1 = dml_artdep.departement
                queasy.date1 = dml_artdep.datum
                queasy.logi1 = True
                queasy.logi2 = False

        dml_artdep = db_session.query(Dml_artdep).first()

    return generate_output()