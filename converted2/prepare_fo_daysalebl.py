#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htplogic import htplogic
from functions.htpdate import htpdate
from models import Bediener, Htparam, Waehrung

def prepare_fo_daysalebl():

    prepare_cache ([Bediener, Htparam, Waehrung])

    exchg_rate = to_decimal("0.0")
    curr_local = ""
    curr_foreign = ""
    from_date = None
    h_art_coupon = 0
    p_240 = False
    p_110 = None
    bline_list_data = []
    bediener = htparam = waehrung = None

    bline_list = usr1 = None

    bline_list_data, Bline_list = create_model("Bline_list", {"flag":int, "userinit":string, "selected":bool, "name":string, "bl_recid":int})

    Usr1 = create_buffer("Usr1",Bediener)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal exchg_rate, curr_local, curr_foreign, from_date, h_art_coupon, p_240, p_110, bline_list_data, bediener, htparam, waehrung
        nonlocal usr1


        nonlocal bline_list, usr1
        nonlocal bline_list_data

        return {"exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "from_date": from_date, "h_art_coupon": h_art_coupon, "p_240": p_240, "p_110": p_110, "bline-list": bline_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    curr_local = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
    curr_foreign = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1001)]})
    h_art_coupon = htparam.finteger

    for usr1 in db_session.query(Usr1).filter(
             (Usr1.username != "")).order_by(Usr1.username).all():
        bline_list = Bline_list()
        bline_list_data.append(bline_list)

        bline_list.userinit = usr1.userinit
        bline_list.name = usr1.username
        bline_list.bl_recid = usr1._recid
        bline_list.selected = True

        if substring(usr1.permissions, 7, 1) >= ("2").lower() :
            bline_list.flag = 1
    p_240 = get_output(htplogic(240))
    p_110 = get_output(htpdate(110))

    return generate_output()