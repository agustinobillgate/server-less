from functions.additional_functions import *
import decimal
from datetime import date
from functions.htplogic import htplogic
from functions.htpdate import htpdate
from models import Bediener, Htparam, Waehrung

def prepare_fo_daysalebl():
    exchg_rate = 0
    curr_local = ""
    curr_foreign = ""
    from_date = None
    h_art_coupon = 0
    p_240 = False
    p_110 = None
    bline_list_list = []
    bediener = htparam = waehrung = None

    bline_list = usr1 = None

    bline_list_list, Bline_list = create_model("Bline_list", {"flag":int, "userinit":str, "selected":bool, "name":str, "bl_recid":int})

    Usr1 = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal exchg_rate, curr_local, curr_foreign, from_date, h_art_coupon, p_240, p_110, bline_list_list, bediener, htparam, waehrung
        nonlocal usr1


        nonlocal bline_list, usr1
        nonlocal bline_list_list
        return {"exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "from_date": from_date, "h_art_coupon": h_art_coupon, "p_240": p_240, "p_110": p_110, "bline-list": bline_list_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit
    else:
        exchg_rate = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    curr_local = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    curr_foreign = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    from_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1001)).first()
    h_art_coupon = htparam.finteger

    for usr1 in db_session.query(Usr1).filter(
            (Usr1.username != "")).all():
        bline_list = Bline_list()
        bline_list_list.append(bline_list)

        bline_list.userinit = usr1.userinit
        bline_list.name = usr1.username
        bline_list.bl_recid = usr1._recid
        bline_list.selected = True

        if substring(usr1.permissions, 7, 1) >= "2":
            bline_list.flag = 1
    p_240 = get_output(htplogic(240))
    p_110 = get_output(htpdate(110))

    return generate_output()