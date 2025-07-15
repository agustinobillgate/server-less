#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_resources, Htparam, Bediener, Queasy

def prepare_eg_resourcesbl(user_init:string):

    prepare_cache ([Htparam, Bediener, Queasy])

    engid = 0
    groupid = 0
    t_eg_resources_data = []
    eg_resources = htparam = bediener = queasy = None

    typeres = t_eg_resources = None

    typeres_data, Typeres = create_model("Typeres", {"type":int, "fldres":string})
    t_eg_resources_data, T_eg_resources = create_model_like(Eg_resources, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, t_eg_resources_data, eg_resources, htparam, bediener, queasy
        nonlocal user_init


        nonlocal typeres, t_eg_resources
        nonlocal typeres_data, t_eg_resources_data

        return {"engid": engid, "groupid": groupid, "t-eg-resources": t_eg_resources_data}

    def define_engineering():

        nonlocal engid, groupid, t_eg_resources_data, eg_resources, htparam, bediener, queasy
        nonlocal user_init


        nonlocal typeres, t_eg_resources
        nonlocal typeres_data, t_eg_resources_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, t_eg_resources_data, eg_resources, htparam, bediener, queasy
        nonlocal user_init


        nonlocal typeres, t_eg_resources
        nonlocal typeres_data, t_eg_resources_data

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group


    def create_type():

        nonlocal engid, groupid, t_eg_resources_data, eg_resources, htparam, bediener, queasy
        nonlocal user_init


        nonlocal typeres, t_eg_resources
        nonlocal typeres_data, t_eg_resources_data

        qbuff = None
        Qbuff =  create_buffer("Qbuff",Queasy)
        typeres_data.clear()

        for qbuff in db_session.query(Qbuff).filter(
                 (Qbuff.key == 136)).order_by(Qbuff._recid).all():
            typeres = Typeres()
            typeres_data.append(typeres)

            typeres.type = qbuff.number1
            typeres.fldres = qbuff.char1


    define_group()
    define_engineering()
    create_type()

    for eg_resources in db_session.query(Eg_resources).order_by(Eg_resources._recid).all():
        t_eg_resources = T_eg_resources()
        t_eg_resources_data.append(t_eg_resources)

        buffer_copy(eg_resources, t_eg_resources)
        t_eg_resources.rec_id = eg_resources._recid

    return generate_output()