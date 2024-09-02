from functions.additional_functions import *
import decimal
from datetime import date
from models import Queasy, Htparam

def prepare_parent_child_rcodebl():
    ci_date = None
    tb1_list = []
    tb2_list = []
    in_percent:bool = False
    queasy = htparam = None

    tb1 = tb2 = qbuff = None

    tb1_list, Tb1 = create_model_like(Queasy, {"parent_code":str, "percent_amt":str, "adjust_value":decimal})
    tb2_list, Tb2 = create_model_like(Tb1)
    qbuff_list, Qbuff = create_model("Qbuff", {"char3":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, tb1_list, tb2_list, in_percent, queasy, htparam


        nonlocal tb1, tb2, qbuff
        nonlocal tb1_list, tb2_list, qbuff_list
        return {"ci_date": ci_date, "tb1": tb1_list, "tb2": tb2_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (not Queasy.logi2) &  (num_entries(Queasy.char3, ";") > 2)).all():
        qbuff = Qbuff()
        qbuff_list.append(qbuff)

        qbuff.char3 = queasy.char3

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (not Queasy.logi2)).all():

        if num_entries(queasy.char3, ";") > 2:
            tb2 = Tb2()
            tb2_list.append(tb2)

            buffer_copy(queasy, tb2)
            tb2.parent_code = entry(1, queasy.char3, ";")
            in_percent = substring(entry(2, queasy.char3, ";") , 0, 1) == "%"
            tb2.adjust_value = decimal.Decimal(substring(entry(2, queasy.char3, ";") , 1)) / 100

            if in_percent:
                tb2.percent_amt = "%"
        else:

            qbuff = query(qbuff_list, filters=(lambda qbuff :entry(1, qbuff.char3, ";") == queasy.char1), first=True)

            if qbuff:
                tb1 = Tb1()
                tb1_list.append(tb1)

                buffer_copy(queasy, tb1)

    return generate_output()