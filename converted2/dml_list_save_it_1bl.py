#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Dml_art, Queasy, Dml_artdep

def dml_list_save_it_1bl(curr_dept:int, cbuff_artnr:int, cbuff_qty:Decimal, selected_date:date, user_init:string, cbuff_price:Decimal, cbuff_lief_nr:int, cbuff_approved:bool, cbuff_remark:string):

    prepare_cache ([Dml_art, Queasy, Dml_artdep])

    dml_art = queasy = dml_artdep = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal dml_art, queasy, dml_artdep
        nonlocal curr_dept, cbuff_artnr, cbuff_qty, selected_date, user_init, cbuff_price, cbuff_lief_nr, cbuff_approved, cbuff_remark

        return {}


    if curr_dept == 0:

        dml_art = get_cache (Dml_art, {"artnr": [(eq, cbuff_artnr)],"datum": [(eq, selected_date)]})

        if not dml_art:
            dml_art = Dml_art()
            db_session.add(dml_art)

            dml_art.artnr = cbuff_artnr
            dml_art.datum = selected_date
            dml_art.userinit = user_init


        dml_art.anzahl =  to_decimal(cbuff_qty)
        dml_art.einzelpreis =  to_decimal(cbuff_price)
        dml_art.userinit = entry(0, dml_art.userinit, ";")
        dml_art.chginit = user_init

        queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, 0)],"number2": [(eq, cbuff_artnr)],"date1": [(eq, selected_date)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 202
            queasy.number1 = 0
            queasy.number2 = cbuff_artnr
            queasy.date1 = selected_date
            queasy.char1 = cbuff_remark


        else:
            pass
            queasy.char1 = cbuff_remark


            pass
            pass

        if cbuff_lief_nr > 0:
            dml_art.userinit = dml_art.userinit +\
                ";" + to_string(cbuff_lief_nr)

        if cbuff_approved:
            dml_art.chginit = dml_art.chginit + "!"

            queasy = get_cache (Queasy, {"key": [(eq, 254)],"number1": [(eq, 0)],"date1": [(eq, dml_art.datum)],"logi1": [(eq, True)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 254
                queasy.number1 = 0
                queasy.date1 = dml_art.datum
                queasy.logi1 = True
                queasy.logi2 = False


        pass
    else:

        dml_artdep = get_cache (Dml_artdep, {"artnr": [(eq, cbuff_artnr)],"datum": [(eq, selected_date)],"departement": [(eq, curr_dept)]})

        if not dml_artdep:
            dml_artdep = Dml_artdep()
            db_session.add(dml_artdep)

            dml_artdep.artnr = cbuff_artnr
            dml_artdep.datum = selected_date
            dml_artdep.departement = curr_dept
            dml_artdep.userinit = user_init


        dml_artdep.anzahl =  to_decimal(cbuff_qty)
        dml_artdep.einzelpreis =  to_decimal(cbuff_price)
        dml_artdep.userinit = entry(0, dml_artdep.userinit, ";")
        dml_artdep.chginit = user_init

        queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, curr_dept)],"number2": [(eq, cbuff_artnr)],"date1": [(eq, selected_date)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 202
            queasy.number1 = curr_dept
            queasy.number2 = cbuff_artnr
            queasy.date1 = selected_date
            queasy.char1 = cbuff_remark


        else:
            pass
            queasy.char1 = cbuff_remark


            pass
            pass

        if cbuff_lief_nr > 0:
            dml_artdep.userinit = dml_artdep.userinit +\
                ";" + to_string(cbuff_lief_nr)

        if cbuff_approved:
            dml_artdep.chginit = dml_artdep.chginit + "!"

            queasy = get_cache (Queasy, {"key": [(eq, 254)],"number1": [(eq, dml_artdep.departement)],"date1": [(eq, dml_artdep.datum)],"logi1": [(eq, True)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 254
                queasy.number1 = dml_artdep.departement
                queasy.date1 = dml_artdep.datum
                queasy.logi1 = True
                queasy.logi2 = False


        pass

    return generate_output()