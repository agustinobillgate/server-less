from functions.additional_functions import *
import decimal
import re
from models import Res_line, Queasy, Htparam

def mobileweb_check_flagbl(rsv_number:int, rsvline_number:int, case_type:int):
    res_status = ""
    key_maked = 0
    key_max = 0
    key_avail = 0
    key_qty = 0
    key_string = ""
    payment_flag = ""
    mess_str = ""
    loop:int = 0
    tmp_char:str = ""
    res_line = queasy = htparam = None

    rline = res_sharer = None

    Rline = Res_line
    Res_sharer = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal res_status, key_maked, key_max, key_avail, key_qty, key_string, payment_flag, mess_str, loop, tmp_char, res_line, queasy, htparam
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

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == rsv_number) &  (Res_line.reslinnr == rsvline_number)).first()

        if res_line:

            if case_type == 1:

                if res_line.resstatus == 6 and res_line.active_flag == 1:
                    res_status = "1 - Reservation Already Check_In!"
                else:
                    res_status = "0 - Reservation Not Check_In Yet!"

            elif case_type == 2:
                for loop in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :
                    tmp_char = entry(loop - 1, res_line.zimmer_wunsch, ";")

                    if re.match(".*PREAUTHCC.*",tmp_char):
                        payment_flag = "1 - Reservation Already Paid!"
                        break
                    else:
                        payment_flag = "0 - Reservation Not Paid Yet!"
            mess_str = "0 - Checking flag success."
        else:
            mess_str = "3 - Reservation not found! Please check parameter!"

            return generate_output()

    elif case_type == 3:

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 216) &  (Queasy.number1 == 8) &  (Queasy.number2 == 3)).first()

        if queasy:
            key_max = queasy.number3

        if key_max == 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 927)).first()

            if htparam:
                key_max = htparam.finteger

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == rsv_number) &  (Res_line.reslinnr == rsvline_number)).first()

        if res_line:

            res_sharer = db_session.query(Res_sharer).filter(
                    (Res_sharer.resnr == res_line.resnr) &  (Res_sharer.reslinnr != res_line.reslinnr) &  (Res_sharer.resstatus == 11) &  (Res_sharer.zinr == res_line.zinr)).first()

            if res_sharer:

                for rline in db_session.query(Rline).filter(
                        (Rline.resnr == res_line.resnr) &  (Rline.resstatus == 11) &  (Rline.zinr == res_line.zinr)).all():
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