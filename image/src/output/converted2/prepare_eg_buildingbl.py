#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Htparam, Bediener

def prepare_eg_buildingbl(user_init:string):

    prepare_cache ([Htparam, Bediener])

    groupid = 0
    engid = 0
    t_queasy_list = []
    queasy = htparam = bediener = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, t_queasy_list, queasy, htparam, bediener
        nonlocal user_init


        nonlocal t_queasy
        nonlocal t_queasy_list

        return {"groupid": groupid, "engid": engid, "t-queasy": t_queasy_list}

    def define_engineering():

        nonlocal groupid, engid, t_queasy_list, queasy, htparam, bediener
        nonlocal user_init


        nonlocal t_queasy
        nonlocal t_queasy_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal groupid, engid, t_queasy_list, queasy, htparam, bediener
        nonlocal user_init


        nonlocal t_queasy
        nonlocal t_queasy_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group

    define_group()
    define_engineering()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 135)).order_by(Queasy.number1).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    return generate_output()