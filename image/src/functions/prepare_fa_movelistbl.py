from functions.additional_functions import *
import decimal
from datetime import date
from models import Mathis, Fa_grup, Htparam

def prepare_fa_movelistbl(bill_date:date):
    fdate = None
    tdate = None
    t_fa_grup_list = []
    t_mathis_list = []
    mathis = fa_grup = htparam = None

    t_mathis = t_fa_grup = None

    t_mathis_list, T_mathis = create_model_like(Mathis)
    t_fa_grup_list, T_fa_grup = create_model_like(Fa_grup)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fdate, tdate, t_fa_grup_list, t_mathis_list, mathis, fa_grup, htparam


        nonlocal t_mathis, t_fa_grup
        nonlocal t_mathis_list, t_fa_grup_list
        return {"fdate": fdate, "tdate": tdate, "t-fa-grup": t_fa_grup_list, "t-mathis": t_mathis_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()

    if htparam:
        bill_date = htparam.fdate
    fdate = date_mdy(get_month(bill_date) , 1, get_year(bill_date))
    tdate = fdate - 1

    for mathis in db_session.query(Mathis).all():
        t_mathis = T_mathis()
        t_mathis_list.append(t_mathis)

        buffer_copy(mathis, t_mathis)

    for fa_grup in db_session.query(Fa_grup).all():
        t_fa_grup = T_fa_grup()
        t_fa_grup_list.append(t_fa_grup)

        buffer_copy(fa_grup, t_fa_grup)

    return generate_output()