#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Hoteldpt, Waehrung

def prepare_ktrans_reportbl(min_dept:int, max_dept:int):

    prepare_cache ([Htparam, Hoteldpt, Waehrung])

    billdate = None
    from_date = None
    to_date = None
    long_digit = False
    min_art = 9999
    max_art = 0
    from_art = 0
    to_art = 9999
    from_dept = 1
    to_dept = 99
    depname1 = ""
    depname2 = ""
    double_currency = False
    exchg_rate = 1
    t_hoteldpt_data = []
    htparam = hoteldpt = waehrung = None

    t_hoteldpt = None

    t_hoteldpt_data, T_hoteldpt = create_model("T_hoteldpt", {"num":int, "depart":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal billdate, from_date, to_date, long_digit, min_art, max_art, from_art, to_art, from_dept, to_dept, depname1, depname2, double_currency, exchg_rate, t_hoteldpt_data, htparam, hoteldpt, waehrung
        nonlocal min_dept, max_dept


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_data

        return {"billdate": billdate, "from_date": from_date, "to_date": to_date, "long_digit": long_digit, "min_art": min_art, "max_art": max_art, "from_art": from_art, "to_art": to_art, "from_dept": from_dept, "to_dept": to_dept, "depname1": depname1, "depname2": depname2, "double_currency": double_currency, "exchg_rate": exchg_rate, "t-hoteldpt": t_hoteldpt_data}

    def select_dept():

        nonlocal billdate, from_date, to_date, long_digit, min_art, max_art, from_art, to_art, from_dept, to_dept, depname1, depname2, double_currency, exchg_rate, t_hoteldpt_data, htparam, hoteldpt, waehrung
        nonlocal min_dept, max_dept


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_data

        ldry:int = 0
        dstore:int = 0

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1081)]})
        ldry = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1082)]})
        dstore = htparam.finteger
        min_dept = 1

        for hoteldpt in db_session.query(Hoteldpt).filter(
                 (Hoteldpt.num >= 1) & (Hoteldpt.num != ldry) & (Hoteldpt.num != dstore)).order_by(Hoteldpt.num).all():

            if max_dept < hoteldpt.num:
                max_dept = hoteldpt.num


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    billdate = htparam.fdate
    from_date = htparam.fdate - timedelta(days=1)
    to_date = htparam.fdate - timedelta(days=1)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical
    select_dept()
    min_art = 0
    max_art = 99999
    from_art = min_art
    to_art = max_art
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

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        else:
            exchg_rate =  to_decimal("1")

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num
        t_hoteldpt.depart = hoteldpt.depart

    return generate_output()