#using conversion tools version: 1.0.0.118

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy, Dml_artdep, Paramtext, Dml_art, Queasy

def dml_list_save_it_3bl(curr_dept:int, cbuff_artnr:int, cbuff_qty:Decimal, selected_date:date, user_init:string, cbuff_price:Decimal, cbuff_lief_nr:int, cbuff_approved:bool, cbuff_remark:string, curr_select:string, dml_no:string, counter:int):

    prepare_cache ([Paramtext, Dml_art, Queasy])

    curr_time:string = ""
    htl_name:string = ""
    reslin_queasy = dml_artdep = paramtext = dml_art = queasy = None

    breslin = bdml_artdep = None

    Breslin = create_buffer("Breslin",Reslin_queasy)
    Bdml_artdep = create_buffer("Bdml_artdep",Dml_artdep)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_time, htl_name, reslin_queasy, dml_artdep, paramtext, dml_art, queasy
        nonlocal curr_dept, cbuff_artnr, cbuff_qty, selected_date, user_init, cbuff_price, cbuff_lief_nr, cbuff_approved, cbuff_remark, curr_select, dml_no, counter
        nonlocal breslin, bdml_artdep


        nonlocal breslin, bdml_artdep

        return {}

    curr_time = to_string(get_current_time_in_seconds(), "HH:MM")
    curr_time = replace_str(curr_time, ":", "")

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

    if paramtext:
        htl_name = paramtext.ptexte

    if OPSYS.lower()  == ("UNIX").lower() :

        if SEARCH ("/usr1/vhp/tmpLOG/") == None:
            UNIX SILENT VALUE ("mkdir " + "/usr1/vhp/tmpLOG/")

        if curr_select.lower()  == ("new").lower() :
            OUTPUT STREAM s1 TO VALUE ("/usr1/vhp/tmpLOG/DML-LIST- " + htl_name + "-" + to_string(get_day(get_current_date())) + to_string(get_month(get_current_date()) , "99") + to_string(get_year(get_current_date())) + curr_time + to_string(curr_dept, "99") + "-New" + ".txt") APPEND UNBUFFERED

            if cbuff_approved:
                OUTPUT STREAM s2 TO VALUE ("/usr1/vhp/tmpLOG/DML-LIST- " + htl_name + "-" + to_string(get_day(get_current_date())) + to_string(get_month(get_current_date()) , "99") + to_string(get_year(get_current_date())) + curr_time + to_string(curr_dept, "99") + "-Approved" + ".txt") APPEND UNBUFFERED
        else:
            OUTPUT STREAM s1 TO VALUE ("/usr1/vhp/tmpLOG/DML-LIST- " + htl_name + "-" + to_string(get_day(get_current_date())) + to_string(get_month(get_current_date()) , "99") + to_string(get_year(get_current_date())) + curr_time + to_string(curr_dept, "99") + "-Modify" + ".txt") APPEND UNBUFFERED

            if cbuff_approved:
                OUTPUT STREAM s2 TO VALUE ("/usr1/vhp/tmpLOG/DML-LIST- " + htl_name + "-" + to_string(get_day(get_current_date())) + to_string(get_month(get_current_date()) , "99") + to_string(get_year(get_current_date())) + curr_time + to_string(curr_dept, "99") + "-Approved" + ".txt") APPEND UNBUFFERED
    else:

        if SEARCH ("C:\\e1-vhp\\tmpLOG\\") == None:
            UNIX SILENT VALUE ("mkdir " + "C:\\e1-vhp\\tmpLOG\\")

        if curr_select.lower()  == ("new").lower() :
            OUTPUT STREAM s1 TO VALUE ("C:\\e1-vhp\\tmpLOG\\DML-LIST- " + htl_name + "-" + to_string(get_day(get_current_date())) + to_string(get_month(get_current_date()) , "99") + to_string(get_year(get_current_date())) + curr_time + to_string(curr_dept, "99") + "-New" + ".txt") APPEND UNBUFFERED

            if cbuff_approved:
                OUTPUT STREAM s2 TO VALUE ("C:\\e1-vhp\\tmpLOG\\DML-LIST- " + htl_name + "-" + to_string(get_day(get_current_date())) + to_string(get_month(get_current_date()) , "99") + to_string(get_year(get_current_date())) + curr_time + to_string(curr_dept, "99") + "-Approved" + ".txt") APPEND UNBUFFERED
        else:
            OUTPUT STREAM s1 TO VALUE ("C:\\e1-vhp\\tmpLOG\\DML-LIST- " + htl_name + "-" + to_string(get_day(get_current_date())) + to_string(get_month(get_current_date()) , "99") + to_string(get_year(get_current_date())) + curr_time + to_string(curr_dept, "99") + "-Modify" + ".txt") APPEND UNBUFFERED

            if cbuff_approved:
                OUTPUT STREAM s2 TO VALUE ("C:\\e1-vhp\\tmpLOG\\DML-LIST- " + htl_name + "-" + to_string(get_day(get_current_date())) + to_string(get_month(get_current_date()) , "99") + to_string(get_year(get_current_date())) + curr_time + to_string(curr_dept, "99") + "-Approved" + ".txt") APPEND UNBUFFERED

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
        dml_art.chginit = user_init + ";" + dml_no

        queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, 0)],"number2": [(eq, cbuff_artnr)],"number3": [(eq, counter)],"date1": [(eq, selected_date)]})

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 202
            queasy.number1 = 0
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
            dml_art.userinit = dml_art.userinit +\
                ";" + to_string(cbuff_lief_nr)

        if cbuff_approved:

            if num_entries(dml_art.chginit, ";") > 1:
                dml_art.chginit = entry(0, dml_art.chginit, ";", entry(0, dml_art.chginit, ";") + "!")
            else:
                dml_art.chginit = dml_art.chginit + "!"

            if entry(0, dml_art.chginit, ";") != "":
                else:
                    IF entry(0, dml_art.chginit, ";") != "" and curr_select == "new"THEN PUT STREAM s1 UNFORMATTED to_string(get_current_date()) ";" to_string(get_current_time_in_seconds(), "HH:MM:SS") ";" selected_date ";" curr_dept ";" cbuff_artnr ";" entry(0, dml_art.chginit, ";") ";" curr_select SKIP
                else:
                else:

                    if curr_select.lower()  == ("new").lower() :
                        else:
                        pass
                    pass
                else:

                    if curr_select.lower()  == ("new").lower() :

                        if counter > 1:

                            reslin_queasy = db_session.query(Reslin_queasy).filter(
                                     (Reslin_queasy.key == ("DML").lower()) & (to_int(entry(0, Reslin_queasy.char1, ";")) == cbuff_artnr) & (Reslin_queasy.date1 == selected_date) & (to_int(entry(1, Reslin_queasy.char1, ";")) == curr_dept) & (Reslin_queasy.number2 == counter)).first()

                            if not reslin_queasy and cbuff_qty != 0:
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

                                    if curr_select.lower()  == ("new").lower() :
                                        pass
                                else:

                                    if curr_select.lower()  == ("new").lower() :
                                        else:
                                        pass

                                    queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, curr_dept)],"number2": [(eq, cbuff_artnr)],"number3": [(eq, counter)],"date1": [(eq, selected_date)]})

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
                            else:

                                dml_artdep = get_cache (Dml_artdep, {"artnr": [(eq, cbuff_artnr)],"datum": [(eq, selected_date)],"departement": [(eq, curr_dept)]})

                                if not dml_artdep and cbuff_qty != 0:
                                    dml_artdep = Dml_artdep()
                                    db_session.add(dml_artdep)

                                    dml_artdep.artnr = cbuff_artnr
                                    dml_artdep.datum = selected_date
                                    dml_artdep.departement = curr_dept
                                    dml_artdep.userinit = user_init
                                    dml_artdep.anzahl =  to_decimal(cbuff_qty)
                                    dml_artdep.einzelpreis =  to_decimal(cbuff_price)
                                    dml_artdep.chginit = user_init + ";" + dml_no

                                    queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, curr_dept)],"number2": [(eq, cbuff_artnr)],"number3": [(eq, counter)],"date1": [(eq, selected_date)]})

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

                                        if curr_select.lower()  == ("new").lower() :
                                            pass
                                    else:

                                        if curr_select.lower()  == ("new").lower() :
                                            else:
                                        pass
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
                                            reslin_queasy.char3 = user_init + ";" + dml_no

                                            queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, curr_dept)],"number2": [(eq, cbuff_artnr)],"number3": [(eq, counter)],"date1": [(eq, selected_date)]})

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
                                                reslin_queasy.char2 = reslin_queasy.char2 + ";" + to_string(cbuff_lief_nr)

                                            if cbuff_approved:

                                                if num_entries(reslin_queasy.char3, ";") > 1:
                                                    reslin_queasy.char3 = entry(0, reslin_queasy.char3, ";", entry(0, reslin_queasy.char3, ";") + "!")
                                                else:
                                                    reslin_queasy.char3 = reslin_queasy.char3 + "!"

                                                if curr_select.lower()  == ("new").lower() :
                                                    pass
                                            else:

                                                if curr_select.lower()  == ("new").lower() :
                                                    else:
                                                    pass
                                                pass
                                            else:
                                                db_session.delete(reslin_queasy)
                                                pass
                                        else:

                                            if cbuff_qty > 0:
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

                                                    if curr_select.lower()  == ("new").lower() :
                                                        pass
                                                else:

                                                    if curr_select.lower()  == ("new").lower() :
                                                        else:
                                                        pass

                                                    queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, curr_dept)],"number2": [(eq, cbuff_artnr)],"number3": [(eq, counter)],"date1": [(eq, selected_date)]})

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
                                        else:

                                            dml_artdep = get_cache (Dml_artdep, {"artnr": [(eq, cbuff_artnr)],"datum": [(eq, selected_date)],"departement": [(eq, curr_dept)]})

                                            if dml_artdep:

                                                if cbuff_qty > 0:
                                                    dml_artdep.anzahl =  to_decimal(cbuff_qty)
                                                    dml_artdep.einzelpreis =  to_decimal(cbuff_price)
                                                    dml_artdep.userinit = entry(0, dml_artdep.userinit, ";")
                                                    dml_artdep.chginit = user_init + ";" + dml_no

                                                    queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, curr_dept)],"number2": [(eq, cbuff_artnr)],"number3": [(eq, counter)],"date1": [(eq, selected_date)]})

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

                                                        if num_entries(dml_artdep.chginit, ";") > 1:
                                                            else:

                                                                if num_entries(dml_artdep.chginit, ";") > 1 and curr_select.lower()  == ("new").lower() :

                                                                    elif curr_select.lower()  == ("new").lower() :
                                                                    else:

                                                                        if curr_select.lower()  == ("new").lower() :
                                                                            else:
                                                                            pass
                                                                        pass
                                                                    else:
                                                                        db_session.delete(dml_artdep)
                                                                        pass
                                                                else:

                                                                    if cbuff_qty > 0:
                                                                        dml_artdep = Dml_artdep()
                                                                        db_session.add(dml_artdep)

                                                                        dml_artdep.artnr = cbuff_artnr
                                                                        dml_artdep.datum = selected_date
                                                                        dml_artdep.departement = curr_dept
                                                                        dml_artdep.userinit = user_init
                                                                        dml_artdep.chginit = user_init + ";" + dml_no
                                                                        dml_artdep.anzahl =  to_decimal(cbuff_qty)
                                                                        dml_artdep.einzelpreis =  to_decimal(cbuff_price)

                                                                        queasy = get_cache (Queasy, {"key": [(eq, 202)],"number1": [(eq, curr_dept)],"number2": [(eq, cbuff_artnr)],"number3": [(eq, counter)],"date1": [(eq, selected_date)]})

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

                                                                            if curr_select.lower()  == ("new").lower() :
                                                                                pass
                                                                        else:

                                                                            if curr_select.lower()  == ("new").lower() :
                                                                                else:
                                                                                pass
                                                        OUTPUT STREAM s1 CLOSE
                                                        OUTPUT STREAM s2 CLOSE

    return generate_output()