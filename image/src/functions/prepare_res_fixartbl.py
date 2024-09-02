from functions.additional_functions import *
import decimal
from datetime import date
import re
from models import Fixleist, Res_line, Guest_pr, Htparam, Hoteldpt, Waehrung

def prepare_res_fixartbl(pvilanguage:int, resnr:int, reslinnr:int):
    f_tittle = ""
    contcode = ""
    billdate = None
    foreign_rate = False
    double_currency = False
    price_decimal = 0
    exchg_rate = 0
    curr_local = ""
    curr_foreign = ""
    flag = False
    t_fixleist_list = []
    lvcarea:str = "res_fixart"
    ct:str = ""
    fixleist = res_line = guest_pr = htparam = hoteldpt = waehrung = None

    t_fixleist = None

    t_fixleist_list, T_fixleist = create_model_like(Fixleist, {"depart":str, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_tittle, contcode, billdate, foreign_rate, double_currency, price_decimal, exchg_rate, curr_local, curr_foreign, flag, t_fixleist_list, lvcarea, ct, fixleist, res_line, guest_pr, htparam, hoteldpt, waehrung


        nonlocal t_fixleist
        nonlocal t_fixleist_list
        return {"f_tittle": f_tittle, "contcode": contcode, "billdate": billdate, "foreign_rate": foreign_rate, "double_currency": double_currency, "price_decimal": price_decimal, "exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "flag": flag, "t-fixleist": t_fixleist_list}

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()
    f_tittle = res_line.name + " - " + translateExtended ("Check_In", lvcarea, "") + " " + to_string(res_line.ankunft) + "; " + translateExtended ("Check_Out", lvcarea, "") + " " + to_string(res_line.abreise)
    contcode = ""

    guest_pr = db_session.query(Guest_pr).filter(
            (Guest_pr.gastnr == res_line.gastnr)).first()

    if guest_pr:
        contcode = guest_pr.CODE
        ct = res_line.zimmer_wunsch

        if re.match(".*\$CODE\$.*",ct):
            ct = substring(ct,0 + get_index(ct, "$CODE$") + 6)
            contcode = substring(ct, 0,1 + get_index(ct, ";") - 1)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    billdate = htparam.fdate

    for fixleist in db_session.query(Fixleist).filter(
            (Fixleist.resnr == resnr) &  (Fixleist.reslinnr == reslinnr)).all():
        t_fixleist = T_fixleist()
        t_fixleist_list.append(t_fixleist)

        buffer_copy(fixleist, t_fixleist)
        t_fixleist.rec_id = fixleist._recid

        hoteldpt = db_session.query(Hoteldpt).filter(
                (Hoteldpt.num == fixleist.departement)).first()
        t_fixleist.depart = hoteldpt.depart

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    waehrung = db_session.query(Waehrung).filter(
            (Waehrungsnr == res_line.betriebsnr)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    curr_local = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    curr_foreign = fchar

    if res_line.adrflag:
        flag = True

    return generate_output()