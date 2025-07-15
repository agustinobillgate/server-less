#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Htparam, Bediener

def prepare_eg_rephistorymovebl(user_init:string):

    prepare_cache ([Htparam, Bediener])

    ci_date = None
    engid = 0
    groupid = 0
    t_queasy133_data = []
    queasy = htparam = bediener = None

    t_queasy133 = None

    t_queasy133_data, T_queasy133 = create_model_like(Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, engid, groupid, t_queasy133_data, queasy, htparam, bediener
        nonlocal user_init


        nonlocal t_queasy133
        nonlocal t_queasy133_data

        return {"ci_date": ci_date, "engid": engid, "groupid": groupid, "t-queasy133": t_queasy133_data}

    def define_engineering():

        nonlocal ci_date, engid, groupid, t_queasy133_data, queasy, htparam, bediener
        nonlocal user_init


        nonlocal t_queasy133
        nonlocal t_queasy133_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal ci_date, engid, groupid, t_queasy133_data, queasy, htparam, bediener
        nonlocal user_init


        nonlocal t_queasy133
        nonlocal t_queasy133_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    define_group()
    define_engineering()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 133)).order_by(Queasy._recid).all():
        t_queasy133 = T_queasy133()
        t_queasy133_data.append(t_queasy133)

        buffer_copy(queasy, t_queasy133)

    return generate_output()