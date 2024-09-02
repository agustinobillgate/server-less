from functions.additional_functions import *
import decimal
from datetime import date
from models import Bediener, Salesbud, Htparam

def prepare_salesbudbl():
    bill_date = None
    from_date = None
    t_bediener_list = []
    t_salesbud_list = []
    bediener = salesbud = htparam = None

    t_bediener = t_salesbud = None

    t_bediener_list, T_bediener = create_model_like(Bediener)
    t_salesbud_list, T_salesbud = create_model_like(Salesbud, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bill_date, from_date, t_bediener_list, t_salesbud_list, bediener, salesbud, htparam


        nonlocal t_bediener, t_salesbud
        nonlocal t_bediener_list, t_salesbud_list
        return {"bill_date": bill_date, "from_date": from_date, "t-bediener": t_bediener_list, "t-salesbud": t_salesbud_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate
    from_date = date_mdy(get_month(bill_date) , 1, get_year(bill_date))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 547)).first()

    for bediener in db_session.query(Bediener).filter(
            (Bediener.user_group == htparam.finteger)).all():
        t_bediener = T_bediener()
        t_bediener_list.append(t_bediener)

        buffer_copy(bediener, t_bediener)

    for salesbud in db_session.query(Salesbud).all():
        t_salesbud = T_salesbud()
        t_salesbud_list.append(t_salesbud)

        buffer_copy(salesbud, t_salesbud)
        t_salesbud.rec_id = salesbud._recid

    return generate_output()