from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from sqlalchemy import func
from models import Eg_resources, Eg_budget, Eg_cost, Htparam, Bediener

def prepare_eg_costbl(user_init:str):
    engid = 0
    groupid = 0
    ci_date = None
    t_eg_resources_list = []
    t_eg_budget_list = []
    t_eg_cost_list = []
    eg_resources = eg_budget = eg_cost = htparam = bediener = None

    t_eg_resources = t_eg_budget = t_eg_cost = None

    t_eg_resources_list, T_eg_resources = create_model_like(Eg_resources, {"rec_id":int})
    t_eg_budget_list, T_eg_budget = create_model_like(Eg_budget)
    t_eg_cost_list, T_eg_cost = create_model_like(Eg_cost)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, ci_date, t_eg_resources_list, t_eg_budget_list, t_eg_cost_list, eg_resources, eg_budget, eg_cost, htparam, bediener


        nonlocal t_eg_resources, t_eg_budget, t_eg_cost
        nonlocal t_eg_resources_list, t_eg_budget_list, t_eg_cost_list
        return {"engid": engid, "groupid": groupid, "ci_date": ci_date, "t-eg-resources": t_eg_resources_list, "t-eg-budget": t_eg_budget_list, "t-eg-cost": t_eg_cost_list}

    def define_engineering():

        nonlocal engid, groupid, ci_date, t_eg_resources_list, t_eg_budget_list, t_eg_cost_list, eg_resources, eg_budget, eg_cost, htparam, bediener


        nonlocal t_eg_resources, t_eg_budget, t_eg_cost
        nonlocal t_eg_resources_list, t_eg_budget_list, t_eg_cost_list

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 1200) &  (Htparam.feldtyp == 1)).first()

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0

    def define_group():

        nonlocal engid, groupid, ci_date, t_eg_resources_list, t_eg_budget_list, t_eg_cost_list, eg_resources, eg_budget, eg_cost, htparam, bediener


        nonlocal t_eg_resources, t_eg_budget, t_eg_cost
        nonlocal t_eg_resources_list, t_eg_budget_list, t_eg_cost_list

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            groupid = bediener.user_group


    ci_date = get_output(htpdate(87))
    define_group()
    define_engineering()

    for eg_resources in db_session.query(Eg_resources).all():
        t_eg_resources = T_eg_resources()
        t_eg_resources_list.append(t_eg_resources)

        buffer_copy(eg_resources, t_eg_resources)
        t_eg_resources.rec_id = eg_resources._recid

    for eg_budget in db_session.query(Eg_budget).all():
        t_eg_budget = T_eg_budget()
        t_eg_budget_list.append(t_eg_budget)

        buffer_copy(eg_budget, t_eg_budget)

    for eg_cost in db_session.query(Eg_cost).all():
        t_eg_cost = T_eg_cost()
        t_eg_cost_list.append(t_eg_cost)

        buffer_copy(eg_cost, t_eg_cost)

    return generate_output()