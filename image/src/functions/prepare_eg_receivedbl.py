from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_resources, Eg_budget, Htparam, Bediener

def prepare_eg_receivedbl(user_init:str):
    engid = 0
    groupid = 0
    t_eg_resources_list = []
    t_eg_budget_list = []
    eg_resources = eg_budget = htparam = bediener = None

    t_eg_resources = t_eg_budget = None

    t_eg_resources_list, T_eg_resources = create_model_like(Eg_resources)
    t_eg_budget_list, T_eg_budget = create_model_like(Eg_budget)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, t_eg_resources_list, t_eg_budget_list, eg_resources, eg_budget, htparam, bediener


        nonlocal t_eg_resources, t_eg_budget
        nonlocal t_eg_resources_list, t_eg_budget_list
        return {"engid": engid, "groupid": groupid, "t-eg-resources": t_eg_resources_list, "t-eg-budget": t_eg_budget_list}

    def define_engineering():

        nonlocal engid, groupid, t_eg_resources_list, t_eg_budget_list, eg_resources, eg_budget, htparam, bediener


        nonlocal t_eg_resources, t_eg_budget
        nonlocal t_eg_resources_list, t_eg_budget_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal engid, groupid, t_eg_resources_list, t_eg_budget_list, eg_resources, eg_budget, htparam, bediener


        nonlocal t_eg_resources, t_eg_budget
        nonlocal t_eg_resources_list, t_eg_budget_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group

    define_group()
    define_engineering()

    for eg_resources in db_session.query(Eg_resources).all():
        t_eg_resources = T_eg_resources()
        t_eg_resources_list.append(t_eg_resources)

        buffer_copy(eg_resources, t_eg_resources)

    for eg_budget in db_session.query(Eg_budget).all():
        t_eg_budget = T_eg_budget()
        t_eg_budget_list.append(t_eg_budget)

        buffer_copy(eg_budget, t_eg_budget)

    return generate_output()