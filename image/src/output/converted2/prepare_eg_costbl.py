#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Eg_resources, Eg_budget, Eg_cost, Htparam, Bediener

def prepare_eg_costbl(user_init:string):

    prepare_cache ([Htparam, Bediener])

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
        nonlocal user_init


        nonlocal t_eg_resources, t_eg_budget, t_eg_cost
        nonlocal t_eg_resources_list, t_eg_budget_list, t_eg_cost_list

        return {"engid": engid, "groupid": groupid, "ci_date": ci_date, "t-eg-resources": t_eg_resources_list, "t-eg-budget": t_eg_budget_list, "t-eg-cost": t_eg_cost_list}

    def define_engineering():

        nonlocal engid, groupid, ci_date, t_eg_resources_list, t_eg_budget_list, t_eg_cost_list, eg_resources, eg_budget, eg_cost, htparam, bediener
        nonlocal user_init


        nonlocal t_eg_resources, t_eg_budget, t_eg_cost
        nonlocal t_eg_resources_list, t_eg_budget_list, t_eg_cost_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, ci_date, t_eg_resources_list, t_eg_budget_list, t_eg_cost_list, eg_resources, eg_budget, eg_cost, htparam, bediener
        nonlocal user_init


        nonlocal t_eg_resources, t_eg_budget, t_eg_cost
        nonlocal t_eg_resources_list, t_eg_budget_list, t_eg_cost_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group

    ci_date = get_output(htpdate(87))
    define_group()
    define_engineering()

    for eg_resources in db_session.query(Eg_resources).order_by(Eg_resources._recid).all():
        t_eg_resources = T_eg_resources()
        t_eg_resources_list.append(t_eg_resources)

        buffer_copy(eg_resources, t_eg_resources)
        t_eg_resources.rec_id = eg_resources._recid

    for eg_budget in db_session.query(Eg_budget).order_by(Eg_budget._recid).all():
        t_eg_budget = T_eg_budget()
        t_eg_budget_list.append(t_eg_budget)

        buffer_copy(eg_budget, t_eg_budget)

    for eg_cost in db_session.query(Eg_cost).order_by(Eg_cost._recid).all():
        t_eg_cost = T_eg_cost()
        t_eg_cost_list.append(t_eg_cost)

        buffer_copy(eg_cost, t_eg_cost)

    return generate_output()