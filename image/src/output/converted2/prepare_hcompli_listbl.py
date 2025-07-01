#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Htparam, Queasy, Waehrung

def prepare_hcompli_listbl():

    prepare_cache ([Hoteldpt, Htparam, Waehrung])

    from_dept = 1
    to_dept = 99
    billdate = None
    avail_queasy = False
    min_dept = 99
    max_dept = 0
    depname1 = ""
    depname2 = ""
    double_currency = False
    exchg_rate = 1
    foreign_nr = 0
    min_art = 9999
    max_art = 0
    from_art = 0
    to_art = 0
    t_hoteldpt_list = []
    ldry:int = 0
    dstore:int = 0
    hoteldpt = htparam = queasy = waehrung = None

    t_hoteldpt = None

    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int, "depart":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_dept, to_dept, billdate, avail_queasy, min_dept, max_dept, depname1, depname2, double_currency, exchg_rate, foreign_nr, min_art, max_art, from_art, to_art, t_hoteldpt_list, ldry, dstore, hoteldpt, htparam, queasy, waehrung


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        return {"from_dept": from_dept, "to_dept": to_dept, "billdate": billdate, "avail_queasy": avail_queasy, "min_dept": min_dept, "max_dept": max_dept, "depname1": depname1, "depname2": depname2, "double_currency": double_currency, "exchg_rate": exchg_rate, "foreign_nr": foreign_nr, "min_art": min_art, "max_art": max_art, "from_art": from_art, "to_art": to_art, "t-hoteldpt": t_hoteldpt_list}

    def select_dept():

        nonlocal from_dept, to_dept, billdate, avail_queasy, min_dept, max_dept, depname1, depname2, double_currency, exchg_rate, foreign_nr, min_art, max_art, from_art, to_art, t_hoteldpt_list, ldry, dstore, hoteldpt, htparam, queasy, waehrung


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
        ldry = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})
        dstore = htparam.finteger
        min_dept = 999
        max_dept = 1

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= 1) & (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            if min_dept > hoteldpt.num:
                min_dept = hoteldpt.num

            if max_dept < hoteldpt.num:
                max_dept = hoteldpt.num


    hoteldpt = get_cache (Hoteldpt, {"num": [(gt, 0)]})

    if not hoteldpt:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate
    select_dept()
    min_art = 0
    max_art = 99999
    from_art = min_art
    to_art = max_art

    queasy = get_cache (Queasy, {"key": [(eq, 105)]})

    if queasy:
        avail_queasy = True
    from_dept = min_dept
    to_dept = max_dept

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, from_dept)]})
    depname1 = hoteldpt.depart

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, to_dept)]})
    depname2 = hoteldpt.depart

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})

    if htparam.flogical:
        double_currency = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    if htparam.fchar != "":

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            foreign_nr = waehrung.waehrungsnr
        else:
            exchg_rate =  to_decimal("1")

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num
        t_hoteldpt.depart = hoteldpt.depart

    return generate_output()