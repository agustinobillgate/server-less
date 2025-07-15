#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Arrangement

def read_arrangementbl(case_type:int, argtno:int, argtstr:string):
    t_arrangement_data = []
    arrangement = None

    t_arrangement = None

    t_arrangement_data, T_arrangement = create_model_like(Arrangement)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_arrangement_data, arrangement
        nonlocal case_type, argtno, argtstr


        nonlocal t_arrangement
        nonlocal t_arrangement_data

        return {"t-arrangement": t_arrangement_data}

    def assign_it():

        nonlocal t_arrangement_data, arrangement
        nonlocal case_type, argtno, argtstr


        nonlocal t_arrangement
        nonlocal t_arrangement_data


        t_arrangement = T_arrangement()
        t_arrangement_data.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)


    if case_type == 1:

        arrangement = get_cache (Arrangement, {"argtnr": [(eq, argtno)]})

        if arrangement:
            assign_it()
    elif case_type == 2:

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, argtstr)]})

        if arrangement:
            assign_it()
    elif case_type == 3:

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, argtstr)],"argtnr": [(ne, argtno)]})

        if arrangement:
            assign_it()
    elif case_type == 4:

        for arrangement in db_session.query(Arrangement).order_by(Arrangement._recid).all():
            assign_it()
    elif case_type == 5:

        for arrangement in db_session.query(Arrangement).filter(
                 (Arrangement.segmentcode != argtno)).order_by(Arrangement._recid).all():
            assign_it()

    return generate_output()