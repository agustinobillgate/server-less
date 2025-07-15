#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Prmarket

def read_prmarketbl(case_type:int, prno:int, bezeich:string):
    t_prmarket_data = []
    prmarket = None

    t_prmarket = None

    t_prmarket_data, T_prmarket = create_model_like(Prmarket)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_prmarket_data, prmarket
        nonlocal case_type, prno, bezeich


        nonlocal t_prmarket
        nonlocal t_prmarket_data

        return {"t-prmarket": t_prmarket_data}

    if case_type == 1:

        prmarket = get_cache (Prmarket, {"nr": [(eq, prno)]})
    elif case_type == 2:

        prmarket = get_cache (Prmarket, {"bezeich": [(eq, bezeich)]})
    elif case_type == 3:

        prmarket = get_cache (Prmarket, {"bezeich": [(eq, bezeich)],"_recid": [(ne, prno)]})

    if prmarket:
        t_prmarket = T_prmarket()
        t_prmarket_data.append(t_prmarket)

        buffer_copy(prmarket, t_prmarket)

    return generate_output()