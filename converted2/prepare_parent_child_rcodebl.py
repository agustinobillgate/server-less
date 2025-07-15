#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam

def prepare_parent_child_rcodebl():

    prepare_cache ([Htparam])

    ci_date = None
    tb1_data = []
    tb2_data = []
    in_percent:bool = False
    queasy = htparam = None

    tb1 = tb2 = qbuff = None

    tb1_data, Tb1 = create_model_like(Queasy, {"parent_code":string, "percent_amt":string, "adjust_value":Decimal})
    tb2_data, Tb2 = create_model_like(Tb1)
    qbuff_data, Qbuff = create_model("Qbuff", {"char3":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, tb1_data, tb2_data, in_percent, queasy, htparam


        nonlocal tb1, tb2, qbuff
        nonlocal tb1_data, tb2_data, qbuff_data

        return {"ci_date": ci_date, "tb1": tb1_data, "tb2": tb2_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2) & not_ (Queasy.logi2) & (num_entries(Queasy.char3, ";") > 2)).order_by(Queasy._recid).all():
        qbuff = Qbuff()
        qbuff_data.append(qbuff)

        qbuff.char3 = queasy.char3

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 2) & not_ (Queasy.logi2)).order_by(Queasy._recid).all():

        if num_entries(queasy.char3, ";") > 2:
            tb2 = Tb2()
            tb2_data.append(tb2)

            buffer_copy(queasy, tb2)
            tb2.parent_code = entry(1, queasy.char3, ";")
            in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
            tb2.adjust_value = to_decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100

            if in_percent:
                tb2.percent_amt = "%"
        else:

            qbuff = query(qbuff_data, filters=(lambda qbuff: entry(1, qbuff.char3, ";") == queasy.char1), first=True)

            if qbuff:
                tb1 = Tb1()
                tb1_data.append(tb1)

                buffer_copy(queasy, tb1)

    return generate_output()