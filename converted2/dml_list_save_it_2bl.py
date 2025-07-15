#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy, Dml_artdep, Dml_art, Queasy

def dml_list_save_it_2bl(curr_dept:int, cbuff_artnr:int, cbuff_qty:Decimal, selected_date:date, user_init:string, cbuff_price:Decimal, cbuff_lief_nr:int, cbuff_approved:bool, cbuff_remark:string, curr_select:string, dml_no:string, counter:int):

    prepare_cache ([Dml_art, Queasy])

    reslin_queasy = dml_artdep = dml_art = queasy = None

    breslin = bdml_artdep = None

    Breslin = create_buffer("Breslin",Reslin_queasy)
    Bdml_artdep = create_buffer("Bdml_artdep",Dml_artdep)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal reslin_queasy, dml_artdep, dml_art, queasy
        nonlocal curr_dept, cbuff_artnr, cbuff_qty, selected_date, user_init, cbuff_price, cbuff_lief_nr, cbuff_approved, cbuff_remark, curr_select, dml_no, counter
        nonlocal breslin, bdml_artdep


        nonlocal breslin, bdml_artdep

        return {}


    if curr_dept == 0:

        dml_art = db_session.query(Dml_art).filter(
                 (Dml_art.artnr == cbuff_artnr) & (Dml_art.datum == selected_date) & (entry(1, Dml_art.chginit, ";") == (dml_no).lower())).first()

        if not dml_art:
            dml_art = Dml_art()
            db_session.add(dml_art)

            dml_art.artnr = cbuff_artnr
            dml_art.datum = selected_date
            dml_art.userinit = user_init
            dml_art.chginit = user_init + ";" + dml_no


        dml_art.anzahl =  to_decimal(cbuff_qty)
        dml_art.einzelpreis =  to_decimal(cbuff_price)
        dml_art.userinit = entry(0, dml_art.userinit, ";")

        if num_entries(dml_art.chginit, ";") > 1:
            dml_art.chginit = entry(0, dml_art.chginit, ";", user_init)

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

            if num_entries(dml_art.chginit, ";") > 1:
                dml_art.chginit = entry(0, dml_art.chginit, ";", entry(0, dml_art.chginit, ";") + "!")
            else:
                dml_art.chginit = dml_art.chginit + "!"

            queasy = get_cache (Queasy, {"key": [(eq, 254)],"number1": [(eq, 0)],"date1": [(eq, dml_art.datum)],"logi1": [(eq, True)],"number3": [(eq, 0)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 254
                queasy.number1 = 0
                queasy.date1 = dml_art.datum
                queasy.logi1 = True
                queasy.logi2 = False
                queasy.number3 = 0


        pass
    else:

        if curr_select.lower()  == ("new").lower() :

            if counter > 1:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("DML").lower()) & (to_int(entry(0, Reslin_queasy.char1, ";")) == cbuff_artnr) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (Reslin_queasy.number2 == counter)).first()

                if not reslin_queasy:
                    reslin_queasy = Reslin_queasy()
                    db_session.add(reslin_queasy)

                    reslin_queasy.key = "DML"
                    reslin_queasy.char1 = to_string(cbuff_artnr) + ";" + to_string(curr_dept) + ";" + cbuff_remark
                    reslin_queasy.char2 = user_init
                    reslin_queasy.char3 = user_init + ";" + dml_no
                    reslin_queasy.deci2 =  to_decimal(cbuff_qty)
                    reslin_queasy.number2 = counter
                    reslin_queasy.deci1 =  to_decimal(cbuff_price)
                    reslin_queasy.date1 = selected_date

                    if cbuff_lief_nr > 0:
                        reslin_queasy.char2 = reslin_queasy.char2 + ";" + to_string(cbuff_lief_nr)

                    if cbuff_approved:

                        if num_entries(reslin_queasy.char3, ";") > 1:
                            replace_str((entry(0, reslin_queasy.char3, ";")) , "", "!")
                        else:
                            reslin_queasy.char3 = reslin_queasy.char3 + "!"

                        queasy = get_cache (Queasy, {"key": [(eq, 254)],"number1": [(eq, to_int(entry(1, reslin_queasy.char1, ";")))],"date1": [(eq, reslin_queasy.date1)],"logi1": [(eq, True)],"number3": [(eq, counter)]})

                        if not queasy:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 254
                            queasy.number1 = to_int(entry(1, reslin_queasy.char1, ";"))
                            queasy.date1 = reslin_queasy.date1
                            queasy.logi1 = True
                            queasy.logi2 = False
                            queasy.number3 = counter


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
                    dml_artdep.chginit = user_init + ";" + dml_no

                    queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, curr_dept)],"number2": [(eq, cbuff_artnr)],"date1": [(eq, selected_date)]})

                    if not queasy:
                        queasy = Queasy()
                        db_session.add(queasy)

                        queasy.key = 202
                        queasy.number1 = curr_dept
                        queasy.number2 = cbuff_artnr
                        queasy.number3 = counter
                        queasy.date1 = selected_date
                        queasy.char1 = cbuff_remark


                    else:
                        pass
                        queasy.char1 = cbuff_remark


                        pass
                        pass

                    if cbuff_lief_nr > 0:
                        dml_artdep.userinit = dml_artdep.userinit + ";" + to_string(cbuff_lief_nr)

                    if cbuff_approved:

                        if num_entries(dml_artdep.chginit, ";") > 1:
                            dml_artdep.chginit = entry(0, dml_artdep.chginit, ";", entry(0, dml_artdep.chginit, ";") + "!")
                        else:
                            dml_artdep.chginit = dml_artdep.chginit + "!"

                        queasy = get_cache (Queasy, {"key": [(eq, 254)],"number1": [(eq, dml_artdep.departement)],"date1": [(eq, dml_artdep.datum)],"logi1": [(eq, True)],"number3": [(eq, 0)]})

                        if not queasy:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 254
                            queasy.number1 = dml_artdep.departement
                            queasy.date1 = dml_artdep.datum
                            queasy.logi1 = True
                            queasy.logi2 = False
                            queasy.number3 = 0


                    pass
        else:

            breslin = db_session.query(Breslin).filter(
                     (Breslin.key == ("DML").lower()) & (entry(1, Breslin.char3, ";") == (dml_no).lower())).first()

            if breslin:

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("DML").lower()) & (to_int(entry(0, Reslin_queasy.char1, ";")) == cbuff_artnr) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (entry(1, Reslin_queasy.char3, ";") == (dml_no).lower())).first()

                if reslin_queasy:

                    if cbuff_qty > 0:
                        reslin_queasy.deci2 =  to_decimal(cbuff_qty)
                        reslin_queasy.deci1 =  to_decimal(cbuff_price)
                        reslin_queasy.char2 = entry(0, reslin_queasy.char2, ";")
                        reslin_queasy.char3 = entry(0, reslin_queasy.char3, ";", user_init)

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
                            reslin_queasy.char2 = reslin_queasy.char2 + ";" + to_string(cbuff_lief_nr)

                        if cbuff_approved:

                            if num_entries(reslin_queasy.char3, ";") > 1:
                                reslin_queasy.char3 = entry(0, reslin_queasy.char3, ";", entry(0, reslin_queasy.char3, ";") + "!")
                            else:
                                reslin_queasy.char3 = reslin_queasy.char3 + "!"

                            queasy = get_cache (Queasy, {"key": [(eq, 254)],"number1": [(eq, to_int(entry(1, reslin_queasy.char1, ";")))],"date1": [(eq, reslin_queasy.date1)],"logi1": [(eq, True)],"number3": [(eq, counter)]})

                            if not queasy:
                                queasy = Queasy()
                                db_session.add(queasy)

                                queasy.key = 254
                                queasy.number1 = to_int(entry(1, reslin_queasy.char1, ";"))
                                queasy.date1 = reslin_queasy.date1
                                queasy.logi1 = True
                                queasy.logi2 = False
                                queasy.number3 = reslin_queasy.number2


                        pass
                        pass
                    else:
                        db_session.delete(reslin_queasy)
                        pass
                else:
                    reslin_queasy = Reslin_queasy()
                    db_session.add(reslin_queasy)

                    reslin_queasy.key = "DML"
                    reslin_queasy.char1 = to_string(cbuff_artnr) + ";" + to_string(curr_dept) + ";" + cbuff_remark
                    reslin_queasy.char2 = user_init
                    reslin_queasy.char3 = user_init + ";" + dml_no
                    reslin_queasy.deci2 =  to_decimal(cbuff_qty)
                    reslin_queasy.number2 = counter
                    reslin_queasy.deci1 =  to_decimal(cbuff_price)
                    reslin_queasy.date1 = selected_date

                    if cbuff_lief_nr > 0:
                        reslin_queasy.char2 = reslin_queasy.char2 + ";" + to_string(cbuff_lief_nr)

                    if cbuff_approved:

                        if num_entries(reslin_queasy.char3, ";") > 1:
                            reslin_queasy.char3 = entry(0, reslin_queasy.char3, ";", entry(0, reslin_queasy.char3, ";") + "!")
                        else:
                            reslin_queasy.char3 = reslin_queasy.char3 + "!"

                        queasy = get_cache (Queasy, {"key": [(eq, 254)],"number1": [(eq, to_int(entry(1, reslin_queasy.char1, ";")))],"date1": [(eq, reslin_queasy.date1)],"logi1": [(eq, True)],"number3": [(eq, counter)]})

                        if not queasy:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 254
                            queasy.number1 = to_int(entry(1, reslin_queasy.char1, ";"))
                            queasy.date1 = reslin_queasy.date1
                            queasy.logi1 = True
                            queasy.logi2 = False
                            queasy.number3 = counter


            else:

                dml_artdep = get_cache (Dml_artdep, {"artnr": [(eq, cbuff_artnr)],"datum": [(eq, selected_date)],"departement": [(eq, curr_dept)]})

                if dml_artdep:

                    if cbuff_qty > 0:
                        dml_artdep.anzahl =  to_decimal(cbuff_qty)
                        dml_artdep.einzelpreis =  to_decimal(cbuff_price)
                        dml_artdep.userinit = entry(0, dml_artdep.userinit, ";")
                        dml_artdep.chginit = entry(0, dml_artdep.chginit, ";", user_init)

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
                            dml_artdep.userinit = dml_artdep.userinit + ";" + to_string(cbuff_lief_nr)

                        if cbuff_approved:

                            if num_entries(dml_artdep.chginit, ";") > 1:
                                dml_artdep.chginit = entry(0, dml_artdep.chginit, ";", entry(0, dml_artdep.chginit, ";") + "!")
                            else:
                                dml_artdep.chginit = dml_artdep.chginit + "!"

                            queasy = get_cache (Queasy, {"key": [(eq, 254)],"number1": [(eq, dml_artdep.departement)],"date1": [(eq, dml_artdep.datum)],"logi1": [(eq, True)],"number3": [(eq, 0)]})

                            if not queasy:
                                queasy = Queasy()
                                db_session.add(queasy)

                                queasy.key = 254
                                queasy.number1 = dml_artdep.departement
                                queasy.date1 = dml_artdep.datum
                                queasy.logi1 = True
                                queasy.logi2 = False
                                queasy.number3 = 0


                        pass
                        pass
                    else:
                        db_session.delete(dml_artdep)
                        pass
                else:
                    dml_artdep = Dml_artdep()
                    db_session.add(dml_artdep)

                    dml_artdep.artnr = cbuff_artnr
                    dml_artdep.datum = selected_date
                    dml_artdep.departement = curr_dept
                    dml_artdep.userinit = user_init
                    dml_artdep.chginit = user_init + ";" + dml_no
                    dml_artdep.anzahl =  to_decimal(cbuff_qty)
                    dml_artdep.einzelpreis =  to_decimal(cbuff_price)

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
                        dml_artdep.userinit = dml_artdep.userinit + ";" + to_string(cbuff_lief_nr)

                    if cbuff_approved:

                        if num_entries(dml_artdep.chginit, ";") > 1:
                            dml_artdep.chginit = entry(0, dml_artdep.chginit, ";", entry(0, dml_artdep.chginit, ";") + "!")
                        else:
                            dml_artdep.chginit = dml_artdep.chginit + "!"

                        queasy = get_cache (Queasy, {"key": [(eq, 254)],"number1": [(eq, dml_artdep.departement)],"date1": [(eq, dml_artdep.datum)],"logi1": [(eq, True)],"number3": [(eq, 0)]})

                        if not queasy:
                            queasy = Queasy()
                            db_session.add(queasy)

                            queasy.key = 254
                            queasy.number1 = dml_artdep.departement
                            queasy.date1 = dml_artdep.datum
                            queasy.logi1 = True
                            queasy.logi2 = False
                            queasy.number3 = 0

    return generate_output()