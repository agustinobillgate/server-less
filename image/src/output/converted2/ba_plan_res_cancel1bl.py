#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Bk_veran, Guest, Htparam, Bill, Bk_raum

def ba_plan_res_cancel1bl(pvilanguage:int, t_resnr:int, t_reslinnr:int):

    prepare_cache ([Bk_reser, Bk_veran, Guest, Htparam, Bk_raum])

    msg_str1 = ""
    msg_str2 = ""
    msg_str3 = ""
    ci_date:date = None
    lvcarea:string = "ba-plan"
    bk_reser = bk_veran = guest = htparam = bill = bk_raum = None

    bk_resline = resline = mainres = gast = None

    Bk_resline = create_buffer("Bk_resline",Bk_reser)
    Resline = create_buffer("Resline",Bk_reser)
    Mainres = create_buffer("Mainres",Bk_veran)
    Gast = create_buffer("Gast",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str1, msg_str2, msg_str3, ci_date, lvcarea, bk_reser, bk_veran, guest, htparam, bill, bk_raum
        nonlocal pvilanguage, t_resnr, t_reslinnr
        nonlocal bk_resline, resline, mainres, gast


        nonlocal bk_resline, resline, mainres, gast

        return {"msg_str1": msg_str1, "msg_str2": msg_str2, "msg_str3": msg_str3}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    resline = get_cache (Bk_reser, {"veran_nr": [(eq, t_resnr)],"veran_resnr": [(eq, t_reslinnr)]})

    if resline:

        if (resline.datum == ci_date) and (resline.resstatus == 1):
            msg_str1 = translateExtended ("Can not cancel today's guaranted reservation.", lvcarea, "")

            return generate_output()

        mainres = get_cache (Bk_veran, {"veran_nr": [(eq, resline.veran_nr)]})

        if (mainres.deposit_payment[0] + mainres.deposit_payment[1] + mainres.deposit_payment[2] + mainres.deposit_payment[3] + mainres.deposit_payment[4] + mainres.deposit_payment[5] + mainres.deposit_payment[6] + mainres.deposit_payment[7] + mainres.deposit_payment[8]) > 0:

            bk_resline = get_cache (Bk_reser, {"veran_nr": [(eq, mainres.veran_nr)],"veran_resnr": [(ne, t_reslinnr)],"resstatus": [(eq, 1)]})

            if not bk_resline:
                msg_str1 = translateExtended ("Deposit exists, cancel reservation not possible.", lvcarea, "")

                return generate_output()
        else:

            bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, mainres.veran_nr)],"veran_resnr": [(eq, t_reslinnr)],"resstatus": [(le, 3)]})

            if not bk_reser:
                msg_str1 = translateExtended ("Deposit exists, cancel reservation not possible.", lvcarea, "")

                return generate_output()

        if mainres.rechnr > 0:

            bk_resline = get_cache (Bk_reser, {"veran_nr": [(eq, mainres.veran_nr)],"veran_resnr": [(ne, t_reslinnr)],"resstatus": [(le, 2)]})

            if not bk_resline:

                bill = get_cache (Bill, {"rechnr": [(eq, mainres.rechnr)],"flag": [(eq, 0)]})

                if bill:
                    msg_str1 = translateExtended ("Bill exists, cancel reservation not possible.", lvcarea, "")

                    return generate_output()

        gast = get_cache (Guest, {"gastnr": [(eq, mainres.gastnr)]})

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, resline.raum)]})
        msg_str2 = "&Q" + translateExtended ("Do you really want to cancel reservation of", lvcarea, "") + chr_unicode(10) + gast.name + translateExtended (" - Room:", lvcarea, "") + " " + bk_raum.bezeich + chr_unicode(10) + translateExtended ("Date:", lvcarea, "") + " " + to_string(resline.datum) + " - " + to_string(resline.bis_datum) + translateExtended (" Time:", lvcarea, "") + " " + to_string(resline.von_zeit, "99:99") + " - " + to_string(resline.bis_zeit, "99:99") + "?"
        msg_str3 = "&Q" + translateExtended ("Do you want to cancel all reservation of this reservation number ", lvcarea, "") + chr_unicode(10) + translateExtended ("ResNr:", lvcarea, "") + " " + to_string(resline.veran_nr) + "?"

    return generate_output()