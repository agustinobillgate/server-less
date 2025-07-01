#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_cost

def eg_daily_refresh_browsebl():
    t_eg_cost_list = []
    eg_cost = None

    t_eg_cost = None

    t_eg_cost_list, T_eg_cost = create_model_like(Eg_cost, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_eg_cost_list, eg_cost


        nonlocal t_eg_cost
        nonlocal t_eg_cost_list

        return {"t-eg-cost": t_eg_cost_list}


    t_eg_cost_list.clear()

    for eg_cost in db_session.query(Eg_cost).order_by(Eg_cost._recid).all():
        t_eg_cost = T_eg_cost()
        t_eg_cost_list.append(t_eg_cost)

        buffer_copy(eg_cost, t_eg_cost)

    return generate_output()