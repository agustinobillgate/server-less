#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Guest, Guest_pr, Bediener, Res_history, Waehrung

def ratecode_adm_prcode_2bl(curr_select:string, prcode:string, bezeich:string, segmentcode:string, minstay:int, maxstay:int, minadvance:int, maxadvance:int, frdate:date, todate:date, user_init:string, foreign_rate:bool, local_flag:bool, drate_flag:bool, gastnr:int, local_nr:int, foreign_nr:int, rcode_element:string):

    prepare_cache ([Queasy, Guest, Guest_pr, Bediener, Res_history, Waehrung])

    tb1_list = []
    queasy_number1:int = 0
    ct:string = ""
    queasy = guest = guest_pr = bediener = res_history = waehrung = None

    tb1 = bqueasy = None

    tb1_list, Tb1 = create_model_like(Queasy, {"waehrungsnr":int, "wabkurz":string, "active_flag":bool})

    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tb1_list, queasy_number1, ct, queasy, guest, guest_pr, bediener, res_history, waehrung
        nonlocal curr_select, prcode, bezeich, segmentcode, minstay, maxstay, minadvance, maxadvance, frdate, todate, user_init, foreign_rate, local_flag, drate_flag, gastnr, local_nr, foreign_nr, rcode_element
        nonlocal bqueasy


        nonlocal tb1, bqueasy
        nonlocal tb1_list

        return {"tb1": tb1_list}

    if curr_select.lower()  == ("add").lower() :
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 2
        queasy.char1 = prcode
        queasy.char2 = bezeich
        queasy.char3 = segmentcode
        queasy.number2 = minstay
        queasy.deci2 =  to_decimal(maxstay)
        queasy.number3 = minadvance
        queasy.deci3 =  to_decimal(maxadvance)
        queasy.date1 = frdate
        queasy.date2 = todate
        queasy.logi1 = local_flag
        queasy.logi2 = drate_flag

        if (not foreign_rate) or queasy.logi1:
            queasy.number1 = local_nr
        else:
            queasy.number1 = foreign_nr
        queasy_number1 = queasy.number1


        pass
        pass

        bqueasy = get_cache (Queasy, {"key": [(eq, 289)],"char1": [(eq, prcode)]})

        if not bqueasy:
            bqueasy = Queasy()
            db_session.add(bqueasy)

            bqueasy.key = 289
            bqueasy.char1 = prcode
            bqueasy.char2 = rcode_element

        if gastnr == 0:

            guest = db_session.query(Guest).order_by(Guest._recid.desc()).first()

            if guest and guest.gastnr > 0:
                gastnr = guest.gastnr + 1
            else:
                gastnr = 1
            guest = Guest()
            db_session.add(guest)

            guest.gastnr = gastnr
            guest.name = prcode
            guest.karteityp = 9
            guest.anlage_datum = get_current_date()
            guest.char1 = user_init


            pass
        guest_pr = Guest_pr()
        db_session.add(guest_pr)

        guest_pr.gastnr = gastnr
        guest_pr.code = prcode

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Add Contract Rate, Code: " + prcode + " segmentcode: " + segmentcode + " Description: " + bezeich


            res_history.action = "RateCode"
            pass
            pass
    else:

        queasy = get_cache (Queasy, {"key": [(eq, 2)],"char1": [(eq, prcode)]})

        if queasy:
            pass
            queasy.char2 = bezeich
            queasy.logi1 = local_flag
            queasy.number2 = minstay
            queasy.deci2 =  to_decimal(maxstay)
            queasy.number3 = minadvance
            queasy.deci3 =  to_decimal(maxadvance)
            queasy.date1 = frdate
            queasy.date2 = todate

            if not matches(queasy.char3,r"*;*"):
                queasy.char3 = segmentcode + ";"


            else:
                ct = entry(0, queasy.char3, ";") + ";"
                queasy.char3 = segmentcode + ";" + substring(queasy.char3, length(ct) + 1 - 1)

            if (not foreign_rate) or queasy.logi1:
                queasy.number1 = local_nr
            else:
                queasy.number1 = foreign_nr
            queasy_number1 = queasy.number1


            pass
            pass

        bqueasy = get_cache (Queasy, {"key": [(eq, 289)],"char1": [(eq, prcode)]})

        if bqueasy:
            pass
            bqueasy.char2 = rcode_element
            pass
            pass
        else:
            bqueasy = Queasy()
            db_session.add(bqueasy)

            bqueasy.key = 289
            bqueasy.char1 = prcode
            bqueasy.char2 = rcode_element

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Modify Contract Rate, Code: " + prcode + " segmentcode: " + segmentcode + " Description: " + bezeich


            res_history.action = "RateCode"
            pass
            pass
    tb1 = Tb1()
    tb1_list.append(tb1)

    buffer_copy(queasy, tb1)

    if queasy_number1 != None:

        waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, queasy_number1)]})

        if waehrung:
            tb1.waehrungsnr = waehrung.waehrungsnr
            tb1.wabkurz = waehrung.wabkurz

    return generate_output()