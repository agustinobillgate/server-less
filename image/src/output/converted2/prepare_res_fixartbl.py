#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fixleist, Res_line, Guest_pr, Htparam, Hoteldpt, Waehrung

def prepare_res_fixartbl(pvilanguage:int, resnr:int, reslinnr:int):

    prepare_cache ([Res_line, Guest_pr, Htparam, Hoteldpt, Waehrung])

    f_tittle = ""
    contcode = ""
    billdate = None
    foreign_rate = False
    double_currency = False
    price_decimal = 0
    exchg_rate = 1
    curr_local = ""
    curr_foreign = ""
    flag = False
    t_fixleist_list = []
    lvcarea:string = "res-fixart"
    ct:string = ""
    fixleist = res_line = guest_pr = htparam = hoteldpt = waehrung = None

    t_fixleist = None

    t_fixleist_list, T_fixleist = create_model_like(Fixleist, {"depart":string, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_tittle, contcode, billdate, foreign_rate, double_currency, price_decimal, exchg_rate, curr_local, curr_foreign, flag, t_fixleist_list, lvcarea, ct, fixleist, res_line, guest_pr, htparam, hoteldpt, waehrung
        nonlocal pvilanguage, resnr, reslinnr


        nonlocal t_fixleist
        nonlocal t_fixleist_list

        return {"f_tittle": f_tittle, "contcode": contcode, "billdate": billdate, "foreign_rate": foreign_rate, "double_currency": double_currency, "price_decimal": price_decimal, "exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "flag": flag, "t-fixleist": t_fixleist_list}

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
    f_tittle = res_line.name + " - " + translateExtended ("Check-In", lvcarea, "") + " " + to_string(res_line.ankunft) + "; " + translateExtended ("Check-Out", lvcarea, "") + " " + to_string(res_line.abreise)
    contcode = ""

    guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, res_line.gastnr)]})

    if guest_pr:
        contcode = guest_pr.code
        ct = res_line.zimmer_wunsch

        if matches(ct,r"*$CODE$*"):
            ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
            contcode = substring(ct, 0, get_index(ct, ";") - 1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate

    for fixleist in db_session.query(Fixleist).filter(
             (Fixleist.resnr == resnr) & (Fixleist.reslinnr == reslinnr)).order_by(Fixleist.departement, Fixleist.artnr).all():
        t_fixleist = T_fixleist()
        t_fixleist_list.append(t_fixleist)

        buffer_copy(fixleist, t_fixleist)
        t_fixleist.rec_id = fixleist._recid

        hoteldpt = get_cache (Hoteldpt, {"num": [(eq, fixleist.departement)]})
        t_fixleist.depart = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    double_currency = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    curr_local = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
    curr_foreign = htparam.fchar

    if res_line.adrflag:
        flag = True

    return generate_output()