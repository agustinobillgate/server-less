from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_action, Htparam, Bediener, Queasy

def prepare_eg_actionbl(user_init:str):
    engid = 0
    groupid = 0
    maintask_list = []
    t_eg_action_list = []
    eg_action = htparam = bediener = queasy = None

    t_eg_action = maintask = qbuff = None

    t_eg_action_list, T_eg_action = create_model_like(Eg_action, {"rec_id":int})
    maintask_list, Maintask = create_model("Maintask", {"main_nr":int, "main_nm":str})

    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, maintask_list, t_eg_action_list, eg_action, htparam, bediener, queasy
        nonlocal qbuff


        nonlocal t_eg_action, maintask, qbuff
        nonlocal t_eg_action_list, maintask_list
        return {"engid": engid, "groupid": groupid, "maintask": maintask_list, "t-eg-action": t_eg_action_list}

    def define_engineering():

        nonlocal engid, groupid, maintask_list, t_eg_action_list, eg_action, htparam, bediener, queasy
        nonlocal qbuff


        nonlocal t_eg_action, maintask, qbuff
        nonlocal t_eg_action_list, maintask_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal engid, groupid, maintask_list, t_eg_action_list, eg_action, htparam, bediener, queasy
        nonlocal qbuff


        nonlocal t_eg_action, maintask, qbuff
        nonlocal t_eg_action_list, maintask_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def create_main_nr():

        nonlocal engid, groupid, maintask_list, t_eg_action_list, eg_action, htparam, bediener, queasy
        nonlocal qbuff


        nonlocal t_eg_action, maintask, qbuff
        nonlocal t_eg_action_list, maintask_list


        Qbuff = Queasy
        maintask_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 133)).all():
            maintask = Maintask()
            maintask_list.append(maintask)

            maintask.main_nr = qbuff.number1
            maintask.main_nm = qbuff.char1

    define_group()
    define_engineering()
    create_main_nr()

    for eg_action in db_session.query(Eg_action).all():
        t_eg_action = T_eg_action()
        t_eg_action_list.append(t_eg_action)

        buffer_copy(eg_action, t_eg_action)
        t_eg_action.rec_id = eg_action._recid

    return generate_output()