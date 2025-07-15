#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_action, Htparam, Bediener, Queasy

def prepare_eg_actionbl(user_init:string):

    prepare_cache ([Htparam, Bediener, Queasy])

    engid = 0
    groupid = 0
    maintask_data = []
    t_eg_action_data = []
    eg_action = htparam = bediener = queasy = None

    t_eg_action = maintask = None

    t_eg_action_data, T_eg_action = create_model_like(Eg_action, {"rec_id":int})
    maintask_data, Maintask = create_model("Maintask", {"main_nr":int, "main_nm":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, maintask_data, t_eg_action_data, eg_action, htparam, bediener, queasy
        nonlocal user_init


        nonlocal t_eg_action, maintask
        nonlocal t_eg_action_data, maintask_data

        return {"engid": engid, "groupid": groupid, "maintask": maintask_data, "t-eg-action": t_eg_action_data}

    def define_engineering():

        nonlocal engid, groupid, maintask_data, t_eg_action_data, eg_action, htparam, bediener, queasy
        nonlocal user_init


        nonlocal t_eg_action, maintask
        nonlocal t_eg_action_data, maintask_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, maintask_data, t_eg_action_data, eg_action, htparam, bediener, queasy
        nonlocal user_init


        nonlocal t_eg_action, maintask
        nonlocal t_eg_action_data, maintask_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def create_main_nr():

        nonlocal engid, groupid, maintask_data, t_eg_action_data, eg_action, htparam, bediener, queasy
        nonlocal user_init


        nonlocal t_eg_action, maintask
        nonlocal t_eg_action_data, maintask_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        maintask_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 133)).order_by(Qbuff._recid).all():
            maintask = Maintask()
            maintask_data.append(maintask)

            maintask.main_nr = qbuff.number1
            maintask.main_nm = qbuff.char1


    define_group()
    define_engineering()
    create_main_nr()

    for eg_action in db_session.query(Eg_action).order_by(Eg_action._recid).all():
        t_eg_action = T_eg_action()
        t_eg_action_data.append(t_eg_action)

        buffer_copy(eg_action, t_eg_action)
        t_eg_action.rec_id = eg_action._recid

    return generate_output()