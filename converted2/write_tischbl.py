#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Tisch

t_tisch_data, T_tisch = create_model_like(Tisch)

def write_tischbl(i_case:int, inp_dept:int, inp_tisch:int, t_tisch_data:[T_tisch]):
    tisch = None

    t_tisch = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tisch
        nonlocal i_case, inp_dept, inp_tisch


        nonlocal t_tisch

        return {}

    t_tisch = query(t_tisch_data, first=True)

    if not t_tisch:

        return generate_output()

    if i_case == 1:

        for t_tisch in query(t_tisch_data):

            tisch = get_cache (Tisch, {"departement": [(eq, t_tisch.departement)],"tischnr": [(eq, t_tisch.tischnr)]})

            if not tisch:
                tisch = Tisch()
                db_session.add(tisch)

                buffer_copy(t_tisch, tisch)
    elif i_case == 2:

        tisch = get_cache (Tisch, {"departement": [(eq, inp_dept)],"tischnr": [(eq, inp_tisch)]})

        if tisch:
            pass
            buffer_copy(t_tisch, tisch)
            pass
    elif i_case == 3:

        tisch = get_cache (Tisch, {"departement": [(eq, inp_dept)],"tischnr": [(eq, inp_tisch)]})

        if tisch:
            pass
            db_session.delete(tisch)
            pass

    return generate_output()