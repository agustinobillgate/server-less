from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_resources, Htparam, Bediener, Queasy

def prepare_eg_resourcesbl(user_init:str):
    engid = 0
    groupid = 0
    t_eg_resources_list = []
    eg_resources = htparam = bediener = queasy = None

    typeres = t_eg_resources = qbuff = None

    typeres_list, Typeres = create_model("Typeres", {"type":int, "fldres":str})
    t_eg_resources_list, T_eg_resources = create_model_like(Eg_resources, {"rec_id":int})

    Qbuff = Queasy

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, t_eg_resources_list, eg_resources, htparam, bediener, queasy
        nonlocal qbuff


        nonlocal typeres, t_eg_resources, qbuff
        nonlocal typeres_list, t_eg_resources_list
        return {"engid": engid, "groupid": groupid, "t-eg-resources": t_eg_resources_list}

    def define_engineering():

        nonlocal engid, groupid, t_eg_resources_list, eg_resources, htparam, bediener, queasy
        nonlocal qbuff


        nonlocal typeres, t_eg_resources, qbuff
        nonlocal typeres_list, t_eg_resources_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal engid, groupid, t_eg_resources_list, eg_resources, htparam, bediener, queasy
        nonlocal qbuff


        nonlocal typeres, t_eg_resources, qbuff
        nonlocal typeres_list, t_eg_resources_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    def create_type():

        nonlocal engid, groupid, t_eg_resources_list, eg_resources, htparam, bediener, queasy
        nonlocal qbuff


        nonlocal typeres, t_eg_resources, qbuff
        nonlocal typeres_list, t_eg_resources_list


        Qbuff = Queasy
        typeres_list.clear()

        for qbuff in db_session.query(Qbuff).filter(
                (Qbuff.key == 136)).all():
            typeres = Typeres()
            typeres_list.append(typeres)

            typeres.TYPE = qbuff.number1
            typeres.fldres = qbuff.char1

    define_group()
    define_engineering()
    create_type()

    for eg_resources in db_session.query(Eg_resources).all():
        t_eg_resources = T_eg_resources()
        t_eg_resources_list.append(t_eg_resources)

        buffer_copy(eg_resources, t_eg_resources)
        t_eg_resources.rec_id = eg_resources._recid

    return generate_output()