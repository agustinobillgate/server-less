from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Eg_property, Htparam, Bediener

def prepare_eg_rephistorypropbl(user_init:str):
    ci_date = None
    engid = 0
    groupid = 0
    q_133_list = []
    t_eg_property_list = []
    queasy = eg_property = htparam = bediener = None

    q_133 = t_eg_property = None

    q_133_list, Q_133 = create_model_like(Queasy)
    t_eg_property_list, T_eg_property = create_model_like(Eg_property)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, engid, groupid, q_133_list, t_eg_property_list, queasy, eg_property, htparam, bediener


        nonlocal q_133, t_eg_property
        nonlocal q_133_list, t_eg_property_list
        return {"ci_date": ci_date, "engid": engid, "groupid": groupid, "q-133": q_133_list, "t-eg-property": t_eg_property_list}

    def define_engineering():

        nonlocal ci_date, engid, groupid, q_133_list, t_eg_property_list, queasy, eg_property, htparam, bediener


        nonlocal q_133, t_eg_property
        nonlocal q_133_list, t_eg_property_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal ci_date, engid, groupid, q_133_list, t_eg_property_list, queasy, eg_property, htparam, bediener


        nonlocal q_133, t_eg_property
        nonlocal q_133_list, t_eg_property_list

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
            (Queasy.key == 133)).all():
        q_133 = Q_133()
        q_133_list.append(q_133)

        buffer_copy(queasy, q_133)

    for eg_property in db_session.query(Eg_property).all():
        t_eg_property = T_eg_property()
        t_eg_property_list.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    return generate_output()