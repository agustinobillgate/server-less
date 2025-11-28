#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, 
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_reser, Bk_veran, Guest, Htparam, Bill

def ba_plan_res_checkout1bl(pvilanguage:int, t_resnr:int, t_reslinnr:int):

    prepare_cache ([Bk_reser, Bk_veran, Guest, Htparam, Bill])

    mainres_recid = 0
    msg_str1 = ""
    msg_str2 = ""
    msg_str3 = ""
    ci_date:date = None
    lvcarea:string = "ba-plan"
    bk_reser = bk_veran = guest = htparam = bill = None

    resline = bk_resline = mainres = gast = None

    Resline = create_buffer("Resline",Bk_reser)
    Bk_resline = create_buffer("Bk_resline",Bk_reser)
    Mainres = create_buffer("Mainres",Bk_veran)
    Gast = create_buffer("Gast",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainres_recid, msg_str1, msg_str2, msg_str3, ci_date, lvcarea, bk_reser, bk_veran, guest, htparam, bill
        nonlocal pvilanguage, t_resnr, t_reslinnr
        nonlocal resline, bk_resline, mainres, gast


        nonlocal resline, bk_resline, mainres, gast

        return {"mainres_recid": mainres_recid, "msg_str1": msg_str1, "msg_str2": msg_str2, "msg_str3": msg_str3}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    resline = get_cache (Bk_reser, {"veran_nr": [(eq, t_resnr)],"veran_resnr": [(eq, t_reslinnr)]})

    if resline:

        if resline.datum > ci_date:
            msg_str1 = translateExtended ("This a banquet reservation for coming day(s), closing not possible.", lvcarea, "")

            return generate_output()

        bk_resline = get_cache (Bk_reser, {"veran_nr": [(eq, resline.veran_nr)],"resstatus": [(le, 2)],"datum": [(gt, ci_date)]})

        if bk_resline:
            msg_str1 = translateExtended ("Active banquet reservation later than TODAY exists.", lvcarea, "")

            return generate_output()

        mainres = get_cache (Bk_veran, {"veran_nr": [(eq, resline.veran_nr)]})

        if mainres.rechnr == 0:
            msg_str2 = "&W" + translateExtended ("Banquet Bill does not exist.", lvcarea, "")
        else:

            bill = get_cache (Bill, {"rechnr": [(eq, mainres.rechnr)]})

            if bill.saldo != 0:
                msg_str1 = translateExtended ("Banquet Bill not balanced.", lvcarea, "")

                return generate_output()

            if bill.gesamtumsatz == 0:
                msg_str2 = "&W" + translateExtended ("Banquet Bill has ZERO sales.", lvcarea, "")

        gast = get_cache (Guest, {"gastnr": [(eq, mainres.gastnr)]})
        msg_str3 = "&Q" + translateExtended ("Do you really want to close the banquet reservation of", lvcarea, "") + chr_unicode(10) + gast.name + translateExtended (" - ResNo:", lvcarea, "") + " " + to_string(resline.veran_nr) + " ?"
        mainres_recid = mainres._recid

    return generate_output()