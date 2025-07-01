#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Queasy, Htparam

def mobileweb_check_flagbl(rsv_number:int, rsvline_number:int, case_type:int):

    prepare_cache ([Res_line, Queasy, Htparam])

    res_status = ""
    key_maked = 0
    key_max = 0
    key_avail = 0
    key_qty = 0
    key_string = ""
    payment_flag = ""
    mess_str = ""
    loop:int = 0
    tmp_char:string = ""
    res_line = queasy = htparam = None

    rline = res_sharer = None

    Rline = create_buffer("Rline",Res_line)
    Res_sharer = create_buffer("Res_sharer",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_status, key_maked, key_max, key_avail, key_qty, key_string, payment_flag, mess_str, loop, tmp_char, res_line, queasy, htparam
        nonlocal rsv_number, rsvline_number, case_type
        nonlocal rline, res_sharer


        nonlocal rline, res_sharer

        return {"res_status": res_status, "key_maked": key_maked, "key_max": key_max, "key_avail": key_avail, "key_qty": key_qty, "key_string": key_string, "payment_flag": payment_flag, "mess_str": mess_str}


    if rsv_number == None:
        rsv_number = 0

    if rsvline_number == None:
        rsvline_number = 0

    if case_type == None:
        case_type = 0

    if (rsv_number == 0 or rsvline_number == 0):
        mess_str = "1 - Wrong value parameters for rsvNumber and revlineNumber!"

        return generate_output()

    if (case_type < 1 or case_type > 3):
        mess_str = "2 - Wrong value parameters for caseType!"

        return generate_output()

    if case_type != 3:

        res_line = get_cache (Res_line, {"resnr": [(eq, rsv_number)],"reslinnr": [(eq, rsvline_number)]})

        if res_line:

            if case_type == 1:

                if res_line.resstatus == 6 and res_line.active_flag == 1:
                    res_status = "1 - Reservation Already Check-In!"
                else:
                    res_status = "0 - Reservation Not Check-In Yet!"

            elif case_type == 2:
                for loop in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                    tmp_char = entry(loop - 1, res_line.zimmer_wunsch, ";")

                    if matches(tmp_char,r"*PREAUTHCC*"):
                        payment_flag = "1 - Reservation Already Paid!"
                        break
                    else:
                        payment_flag = "0 - Reservation Not Paid Yet!"
            mess_str = "0 - Checking flag success."
        else:
            mess_str = "3 - Reservation not found! Please check parameter!"

            return generate_output()

    elif case_type == 3:

        queasy = get_cache (Queasy, {"key": [(eq, 216)],"number1": [(eq, 8)],"number2": [(eq, 3)]})

        if queasy:
            key_max = queasy.number3

        if key_max == 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 927)]})

            if htparam:
                key_max = htparam.finteger

        res_line = get_cache (Res_line, {"resnr": [(eq, rsv_number)],"reslinnr": [(eq, rsvline_number)]})

        if res_line:

            res_sharer = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(ne, res_line.reslinnr)],"resstatus": [(eq, 11)],"zinr": [(eq, res_line.zinr)]})

            if res_sharer:

                for rline in db_session.query(Rline).filter(
                         (Rline.resnr == res_line.resnr) & (Rline.resstatus == 11) & (Rline.zinr == res_line.zinr)).order_by(Rline._recid).all():
                    key_qty = key_qty + rline.erwach + rline.kind1 + rline.gratis
                    key_maked = key_maked + rline.betrieb_gast
            key_maked = key_maked + res_line.betrieb_gast
            key_qty = key_qty + res_line.erwach + res_line.kind1 + res_line.gratis
            key_avail = key_max - key_maked

            if key_maked >= key_max:
                mess_str = "4 - Maximum given key reached, please goto front desk!"

                return generate_output()

            if key_maked > 0:
                key_string = res_line.zinr + "|" + to_string(res_line.resnr) + "|" + to_string(res_line.reslinnr) + "|" + to_string(key_qty) + "|DUPKEY"
            else:
                key_string = res_line.zinr + "|" + to_string(res_line.resnr) + "|" + to_string(res_line.reslinnr) + "|" + to_string(key_qty) + "|MAINKEY"
            mess_str = "0 - Checking flag success."
        else:
            mess_str = "3 - Reservation not found! Please check parameter!"

            return generate_output()

    return generate_output()