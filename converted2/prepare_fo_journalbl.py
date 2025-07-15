#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Htparam

def prepare_fo_journalbl(from_dept:int, to_dept:int):

    prepare_cache ([Htparam])

    from_date = None
    to_date = None
    long_digit = False
    depname1 = ""
    depname2 = ""
    t_hoteldpt_data = []
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal from_date, to_date, long_digit, depname1, depname2, t_hoteldpt_data, hoteldpt, htparam
        nonlocal from_dept, to_dept


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_data

        return {"from_date": from_date, "to_date": to_date, "long_digit": long_digit, "depname1": depname1, "depname2": depname2, "t-hoteldpt": t_hoteldpt_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    from_date = htparam.fdate
    to_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, from_dept)]})
    depname1 = hoteldpt.depart

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, to_dept)]})
    depname2 = hoteldpt.depart

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()