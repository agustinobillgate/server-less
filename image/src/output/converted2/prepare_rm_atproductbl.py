#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpint import htpint
from models import Bediener, Htparam

def prepare_rm_atproductbl():

    prepare_cache ([Htparam])

    ci_date = None
    to_date = None
    fdate = None
    tdate = None
    p_143 = False
    t_bediener_list = []
    bediener = htparam = None

    t_bediener = None

    t_bediener_list, T_bediener = create_model_like(Bediener)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, to_date, fdate, tdate, p_143, t_bediener_list, bediener, htparam


        nonlocal t_bediener
        nonlocal t_bediener_list

        return {"ci_date": ci_date, "to_date": to_date, "fdate": fdate, "tdate": tdate, "p_143": p_143, "t-bediener": t_bediener_list}

    def create_sales_combo():

        nonlocal ci_date, to_date, fdate, tdate, p_143, t_bediener_list, bediener, htparam


        nonlocal t_bediener
        nonlocal t_bediener_list

        sales_grp:int = 0
        sales_grp = get_output(htpint(547))

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.user_group == sales_grp)).order_by(Bediener.userinit).all():
            t_bediener = T_bediener()
            t_bediener_list.append(t_bediener)

            buffer_copy(bediener, t_bediener)

    ci_date = get_output(htpdate(87))
    to_date = ci_date - timedelta(days=1)
    fdate = to_date
    tdate = to_date

    htparam = get_cache (Htparam, {"paramnr": [(eq, 143)]})
    p_143 = htparam.flogical
    create_sales_combo()

    return generate_output()