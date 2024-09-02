from functions.additional_functions import *
import decimal
from datetime import date
from models import Bk_reser, Bk_veran, Guest, Htparam, Bill

def ba_plan_res_checkout1bl(pvilanguage:int, t_resnr:int, t_reslinnr:int):
    mainres_recid = 0
    msg_str1 = ""
    msg_str2 = ""
    msg_str3 = ""
    ci_date:date = None
    lvcarea:str = "ba_plan"
    bk_reser = bk_veran = guest = htparam = bill = None

    resline = bk_resline = mainres = gast = None

    Resline = Bk_reser
    Bk_resline = Bk_reser
    Mainres = Bk_veran
    Gast = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mainres_recid, msg_str1, msg_str2, msg_str3, ci_date, lvcarea, bk_reser, bk_veran, guest, htparam, bill
        nonlocal resline, bk_resline, mainres, gast


        nonlocal resline, bk_resline, mainres, gast
        return {"mainres_recid": mainres_recid, "msg_str1": msg_str1, "msg_str2": msg_str2, "msg_str3": msg_str3}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    resline = db_session.query(Resline).filter(
            (Resline.veran_nr == t_resnr) &  (Resline.veran_resnr == t_reslinnr)).first()

    if resline:

        if resline.datum > ci_date:
            msg_str1 = translateExtended ("This a banquet reservation for  lvcarea, "")

            return generate_output()

        bk_resline = db_session.query(Bk_resline).filter(
                (Bk_resline.veran_nr == resline.veran_nr) &  (Bk_resline.resstatus <= 2) &  (Bk_resline.datum > ci_date)).first()

        if bk_resline:
            msg_str1 = translateExtended ("Active banquet reservation later than  return

        mainres = db_session.query(Mainres).filter(
                (Mainres.veran_nr == resline.veran_nr)).first()

        if mainres.rechnr == 0:
            msg_str2 = "&W" + translateExtended ("Banquet Bill does not exist.", lvcarea, "")
        else:

            bill = db_session.query(Bill).filter(
                    (Bill.rechnr == mainres.rechnr)).first()

            if bill.saldo != 0:
                msg_str1 = translateExtended ("Banquet Bill not balanced.", lvcarea, "")

                return generate_output()

            if bill.gesamtumsatz == 0:
                msg_str2 = "&W" + translateExtended ("Banquet Bill has ZERO sales.", lvcarea, "")

        gast = db_session.query(Gast).filter(
                (Gast.gastnr == mainres.gastnr)).first()
        msg_str3 = "&Q" + translateExtended ("Do you really want to close the banquet  + chr(10) + gast.name + translateExtended (" - ResNo:", lvcarea, "") + " " + to_string(resline.veran_nr) + " ?"
        mainres_recid = mainres._recid

    return generate_output()