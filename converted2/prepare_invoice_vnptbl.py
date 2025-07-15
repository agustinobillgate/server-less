#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Hoteldpt, Htparam

def prepare_invoice_vnptbl():

    prepare_cache ([Htparam])

    cidate = None
    from_dept = 0
    to_dept = 0
    depname1 = ""
    depname2 = ""
    t_hoteldpt_data = []
    min_dept:int = 99
    max_dept:int = 0
    hoteldpt = htparam = None

    t_hoteldpt = None

    t_hoteldpt_data, T_hoteldpt = create_model_like(Hoteldpt)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cidate, from_dept, to_dept, depname1, depname2, t_hoteldpt_data, min_dept, max_dept, hoteldpt, htparam


        nonlocal t_hoteldpt
        nonlocal t_hoteldpt_data

        return {"cidate": cidate, "from_dept": from_dept, "to_dept": to_dept, "depname1": depname1, "depname2": depname2, "t-hoteldpt": t_hoteldpt_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})

    if htparam:
        cidate = htparam.fdate

    for hoteldpt in db_session.query(Hoteldpt).filter(
             (Hoteldpt.num >= 0)).order_by(Hoteldpt.num).all():

        if min_dept > hoteldpt.num:
            min_dept = hoteldpt.num

        if max_dept < hoteldpt.num:
            max_dept = hoteldpt.num
    from_dept = min_dept
    to_dept = max_dept

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, from_dept)]})
    depname1 = hoteldpt.depart

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, to_dept)]})
    depname2 = hoteldpt.depart

    for hoteldpt in db_session.query(Hoteldpt).order_by(Hoteldpt._recid).all():
        t_hoteldpt = T_hoteldpt()
        t_hoteldpt_data.append(t_hoteldpt)

        buffer_copy(hoteldpt, t_hoteldpt)

    return generate_output()