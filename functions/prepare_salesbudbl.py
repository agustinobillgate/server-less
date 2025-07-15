#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bediener, Salesbud, Htparam

def prepare_salesbudbl():

    prepare_cache ([Htparam])

    bill_date = None
    from_date = None
    t_bediener_data = []
    t_salesbud_data = []
    bediener = salesbud = htparam = None

    t_bediener = t_salesbud = None

    t_bediener_data, T_bediener = create_model_like(Bediener)
    t_salesbud_data, T_salesbud = create_model_like(Salesbud, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, from_date, t_bediener_data, t_salesbud_data, bediener, salesbud, htparam


        nonlocal t_bediener, t_salesbud
        nonlocal t_bediener_data, t_salesbud_data

        return {"bill_date": bill_date, "from_date": from_date, "t-bediener": t_bediener_data, "t-salesbud": t_salesbud_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate
    from_date = date_mdy(get_month(bill_date) , 1, get_year(bill_date))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 547)]})

    for bediener in db_session.query(Bediener).filter(
             (Bediener.user_group == htparam.finteger)).order_by(Bediener.username).all():
        t_bediener = T_bediener()
        t_bediener_data.append(t_bediener)

        buffer_copy(bediener, t_bediener)

    for salesbud in db_session.query(Salesbud).order_by(Salesbud._recid).all():
        t_salesbud = T_salesbud()
        t_salesbud_data.append(t_salesbud)

        buffer_copy(salesbud, t_salesbud)
        t_salesbud.rec_id = salesbud._recid

    return generate_output()