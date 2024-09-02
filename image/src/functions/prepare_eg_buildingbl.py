from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Htparam, Bediener

def prepare_eg_buildingbl(user_init:str):
    groupid = 0
    engid = 0
    t_queasy_list = []
    queasy = htparam = bediener = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model_like(Queasy, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal groupid, engid, t_queasy_list, queasy, htparam, bediener


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"groupid": groupid, "engid": engid, "t-queasy": t_queasy_list}

    def define_engineering():

        nonlocal groupid, engid, t_queasy_list, queasy, htparam, bediener


        nonlocal t_queasy
        nonlocal t_queasy_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal groupid, engid, t_queasy_list, queasy, htparam, bediener


        nonlocal t_queasy
        nonlocal t_queasy_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group


    define_group()
    define_engineering()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 135)).all():
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)
        t_queasy.rec_id = queasy._recid

    return generate_output()