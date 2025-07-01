#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, Hoteldpt, Kellner

def prepare_rest_daymercurebl():

    prepare_cache ([Htparam, Waehrung, Hoteldpt, Kellner])

    exchg_rate = to_decimal("0.0")
    curr_local = ""
    curr_foreign = ""
    from_date = None
    h_art_coupon = 0
    t_hoteldpt_list = []
    t_kellner_list = []
    htparam = waehrung = hoteldpt = kellner = None

    t_kellner = t_hoteldpt = None

    t_kellner_list, T_kellner = create_model("T_kellner", {"kellnername":string, "kellner_nr":int, "departement":int, "rec_id":int})
    t_hoteldpt_list, T_hoteldpt = create_model("T_hoteldpt", {"num":int, "depart":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal exchg_rate, curr_local, curr_foreign, from_date, h_art_coupon, t_hoteldpt_list, t_kellner_list, htparam, waehrung, hoteldpt, kellner


        nonlocal t_kellner, t_hoteldpt
        nonlocal t_kellner_list, t_hoteldpt_list

        return {"exchg_rate": exchg_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "from_date": from_date, "h_art_coupon": h_art_coupon, "t-hoteldpt": t_hoteldpt_list, "t-kellner": t_kellner_list}


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

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num > 0)).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_list.append(t_hoteldpt)

        t_hoteldpt.num = hoteldpt.num
        t_hoteldpt.depart = hoteldpt.depart

    for kellner in db_session.query(Kellner).order_by(Kellner._recid).all():
        t_kellner = T_kellner()
        t_kellner_list.append(t_kellner)

        t_kellner.kellnername = kellner.kellnername
        t_kellner.kellner_nr = kellner.kellner_nr
        t_kellner.departement = kellner.departement
        t_kellner.rec_id = kellner._recid

    return generate_output()