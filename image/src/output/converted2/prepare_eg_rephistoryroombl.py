#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimmer, Htparam, Bediener

def prepare_eg_rephistoryroombl(user_init:string):

    prepare_cache ([Htparam, Bediener])

    ci_date = None
    engid = 0
    groupid = 0
    t_zimmer_list = []
    zimmer = htparam = bediener = None

    t_zimmer = None

    t_zimmer_list, T_zimmer = create_model_like(Zimmer)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, engid, groupid, t_zimmer_list, zimmer, htparam, bediener
        nonlocal user_init


        nonlocal t_zimmer
        nonlocal t_zimmer_list

        return {"ci_date": ci_date, "engid": engid, "groupid": groupid, "t-zimmer": t_zimmer_list}

    def define_engineering():

        nonlocal ci_date, engid, groupid, t_zimmer_list, zimmer, htparam, bediener
        nonlocal user_init


        nonlocal t_zimmer
        nonlocal t_zimmer_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal ci_date, engid, groupid, t_zimmer_list, zimmer, htparam, bediener
        nonlocal user_init


        nonlocal t_zimmer
        nonlocal t_zimmer_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    define_group()
    define_engineering()

    for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
        t_zimmer = T_zimmer()
        t_zimmer_list.append(t_zimmer)

        buffer_copy(zimmer, t_zimmer)

    return generate_output()