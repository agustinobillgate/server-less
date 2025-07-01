#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import L_lieferant

def read_l_lieferant1bl(case_type:int, char1:string, int1:int):
    t_l_lieferant_list = []
    l_lieferant = None

    t_l_lieferant = None

    t_l_lieferant_list, T_l_lieferant = create_model_like(L_lieferant)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_lieferant_list, l_lieferant
        nonlocal case_type, char1, int1


        nonlocal t_l_lieferant
        nonlocal t_l_lieferant_list

        return {"t-l-lieferant": t_l_lieferant_list}

    if case_type == 1:

        for l_lieferant in db_session.query(L_lieferant).filter(
                 (L_lieferant.firma >= (char1).lower())).order_by(L_lieferant.firma).all():
            t_l_lieferant = T_l_lieferant()
            t_l_lieferant_list.append(t_l_lieferant)

            buffer_copy(l_lieferant, t_l_lieferant)
    elif case_type == 2:

        for l_lieferant in db_session.query(L_lieferant).filter(
                 (matches(L_lieferant.firma,("*" + char1 + "*")))).order_by(L_lieferant.firma).all():
            t_l_lieferant = T_l_lieferant()
            t_l_lieferant_list.append(t_l_lieferant)

            buffer_copy(l_lieferant, t_l_lieferant)

    return generate_output()