from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Htparam, Bediener

def prepare_eg_rephistorymovebl(user_init:str):
    ci_date = None
    engid = 0
    groupid = 0
    t_queasy133_list = []
    queasy = htparam = bediener = None

    t_queasy133 = None

    t_queasy133_list, T_queasy133 = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, engid, groupid, t_queasy133_list, queasy, htparam, bediener


        nonlocal t_queasy133
        nonlocal t_queasy133_list
        return {"ci_date": ci_date, "engid": engid, "groupid": groupid, "t-queasy133": t_queasy133_list}

    def define_engineering():

        nonlocal ci_date, engid, groupid, t_queasy133_list, queasy, htparam, bediener


        nonlocal t_queasy133
        nonlocal t_queasy133_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal ci_date, engid, groupid, t_queasy133_list, queasy, htparam, bediener


        nonlocal t_queasy133
        nonlocal t_queasy133_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    define_group()
    define_engineering()

    for queasy in db_session.query(Queasy).filter(
            (Queasy.KEY == 133)).all():
        t_queasy133 = T_queasy133()
        t_queasy133_list.append(t_queasy133)

        buffer_copy(queasy, t_queasy133)

    return generate_output()