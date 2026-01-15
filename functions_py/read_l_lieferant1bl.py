# using conversion tools version: 1.0.0.117
"""_yusufwijasena_13/01/2026

        remark: - optimize query for l_lieferant
"""
from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import L_lieferant


def read_l_lieferant1bl(case_type: int, char1: string, int1: int):
    t_l_lieferant_data = []
    l_lieferant = None

    t_l_lieferant = None

    t_l_lieferant_data, T_l_lieferant = create_model_like(L_lieferant)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_lieferant_data, l_lieferant
        nonlocal case_type, char1, int1
        nonlocal t_l_lieferant
        nonlocal t_l_lieferant_data

        return {"t-l-lieferant": t_l_lieferant_data}

    if case_type == 1:

        query_l_lierant_1 = (
            db_session.query(L_lieferant)
            .filter(
                (L_lieferant.firma >= (char1).lower())
            )
            .order_by(L_lieferant.firma)
        )

        for l_lieferant in query_l_lierant_1.yield_per(100):
            t_l_lieferant = T_l_lieferant()
            t_l_lieferant_data.append(t_l_lieferant)

            buffer_copy(l_lieferant, t_l_lieferant)
    elif case_type == 2:

        query_l_lierant_2 = (
            db_session.query(L_lieferant)
            .filter(
                (matches(L_lieferant.firma, ("*" + char1 + "*")))
            )
            .order_by(L_lieferant.firma)
        )
        for l_lieferant in query_l_lierant_2:
            t_l_lieferant = T_l_lieferant()
            t_l_lieferant_data.append(t_l_lieferant)

            buffer_copy(l_lieferant, t_l_lieferant)

    return generate_output()
