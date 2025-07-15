#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Htparam, Bediener

def prepare_egsourcebl(user_init:string):

    prepare_cache ([Htparam, Bediener])

    engid = 0
    groupid = 0
    fl_code = 0
    t_queasy_data = []
    queasy = htparam = bediener = None

    t_queasy = None

    t_queasy_data, T_queasy = create_model_like(Queasy, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, fl_code, t_queasy_data, queasy, htparam, bediener
        nonlocal user_init


        nonlocal t_queasy
        nonlocal t_queasy_data

        return {"engid": engid, "groupid": groupid, "fl_code": fl_code, "t-queasy": t_queasy_data}

    def define_engineering():

        nonlocal engid, groupid, fl_code, t_queasy_data, queasy, htparam, bediener
        nonlocal user_init


        nonlocal t_queasy
        nonlocal t_queasy_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


            fl_code = 1


    def define_group():

        nonlocal engid, groupid, fl_code, t_queasy_data, queasy, htparam, bediener
        nonlocal user_init


        nonlocal t_queasy
        nonlocal t_queasy_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group

    define_group()
    define_engineering()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 130)).order_by(Queasy.number1).all():
        t_queasy = T_queasy()
        t_queasy_data.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    return generate_output()