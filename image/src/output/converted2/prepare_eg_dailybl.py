#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_cost, Eg_resources, Eg_budget, Htparam, Bediener

def prepare_eg_dailybl(user_init:string):

    prepare_cache ([Htparam, Bediener])

    engid = 0
    groupid = 0
    t_eg_resources_list = []
    t_eg_cost_list = []
    t_eg_budget_list = []
    eg_cost = eg_resources = eg_budget = htparam = bediener = None

    t_eg_cost = t_eg_resources = t_eg_budget = None

    t_eg_cost_list, T_eg_cost = create_model_like(Eg_cost, {"rec_id":int})
    t_eg_resources_list, T_eg_resources = create_model_like(Eg_resources, {"rec_id":int})
    t_eg_budget_list, T_eg_budget = create_model_like(Eg_budget)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal engid, groupid, t_eg_resources_list, t_eg_cost_list, t_eg_budget_list, eg_cost, eg_resources, eg_budget, htparam, bediener
        nonlocal user_init


        nonlocal t_eg_cost, t_eg_resources, t_eg_budget
        nonlocal t_eg_cost_list, t_eg_resources_list, t_eg_budget_list

        return {"engid": engid, "groupid": groupid, "t-eg-resources": t_eg_resources_list, "t-eg-cost": t_eg_cost_list, "t-eg-budget": t_eg_budget_list}

    def define_engineering():

        nonlocal engid, groupid, t_eg_resources_list, t_eg_cost_list, t_eg_budget_list, eg_cost, eg_resources, eg_budget, htparam, bediener
        nonlocal user_init


        nonlocal t_eg_cost, t_eg_resources, t_eg_budget
        nonlocal t_eg_cost_list, t_eg_resources_list, t_eg_budget_list

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1200)],"feldtyp": [(eq, 1)]})

        if htparam:
            engid = htparam.finteger


        else:
            engid = 0


    def define_group():

        nonlocal engid, groupid, t_eg_resources_list, t_eg_cost_list, t_eg_budget_list, eg_cost, eg_resources, eg_budget, htparam, bediener
        nonlocal user_init


        nonlocal t_eg_cost, t_eg_resources, t_eg_budget
        nonlocal t_eg_cost_list, t_eg_resources_list, t_eg_budget_list

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            groupid = bediener.user_group

    define_group()
    define_engineering()

    for eg_resources in db_session.query(Eg_resources).order_by(Eg_resources._recid).all():
        t_eg_resources = T_eg_resources()
        t_eg_resources_list.append(t_eg_resources)

        buffer_copy(eg_resources, t_eg_resources)
        t_eg_resources.rec_id = eg_resources._recid

    for eg_cost in db_session.query(Eg_cost).order_by(Eg_cost._recid).all():
        t_eg_cost = T_eg_cost()
        t_eg_cost_list.append(t_eg_cost)

        buffer_copy(eg_cost, t_eg_cost)

    for eg_budget in db_session.query(Eg_budget).order_by(Eg_budget._recid).all():
        t_eg_budget = T_eg_budget()
        t_eg_budget_list.append(t_eg_budget)

        buffer_copy(eg_budget, t_eg_budget)

    return generate_output()