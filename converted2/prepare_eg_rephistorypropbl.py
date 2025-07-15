#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Eg_property, Htparam, Bediener

def prepare_eg_rephistorypropbl(user_init:string):

    prepare_cache ([Htparam, Bediener])

    ci_date = None
    engid = 0
    groupid = 0
    q_133_data = []
    t_eg_property_data = []
    queasy = eg_property = htparam = bediener = None

    q_133 = t_eg_property = None

    q_133_data, Q_133 = create_model_like(Queasy)
    t_eg_property_data, T_eg_property = create_model_like(Eg_property)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, engid, groupid, q_133_data, t_eg_property_data, queasy, eg_property, htparam, bediener
        nonlocal user_init


        nonlocal q_133, t_eg_property
        nonlocal q_133_data, t_eg_property_data

        return {"ci_date": ci_date, "engid": engid, "groupid": groupid, "q-133": q_133_data, "t-eg-property": t_eg_property_data}

    def define_engineering():

        nonlocal ci_date, engid, groupid, q_133_data, t_eg_property_data, queasy, eg_property, htparam, bediener
        nonlocal user_init


        nonlocal q_133, t_eg_property
        nonlocal q_133_data, t_eg_property_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal ci_date, engid, groupid, q_133_data, t_eg_property_data, queasy, eg_property, htparam, bediener
        nonlocal user_init


        nonlocal q_133, t_eg_property
        nonlocal q_133_data, t_eg_property_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    define_group()
    define_engineering()

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 133)).order_by(Queasy._recid).all():
        q_133 = Q_133()
        q_133_data.append(q_133)

        buffer_copy(queasy, q_133)

    for eg_property in db_session.query(Eg_property).order_by(Eg_property._recid).all():
        t_eg_property = T_eg_property()
        t_eg_property_data.append(t_eg_property)

        buffer_copy(eg_property, t_eg_property)

    return generate_output()