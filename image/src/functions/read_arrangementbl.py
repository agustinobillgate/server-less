from functions.additional_functions import *
import decimal
from models import Arrangement

def read_arrangementbl(case_type:int, argtno:int, argtstr:str):
    t_arrangement_list = []
    arrangement = None

    t_arrangement = None

    t_arrangement_list, T_arrangement = create_model_like(Arrangement)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_arrangement_list, arrangement


        nonlocal t_arrangement
        nonlocal t_arrangement_list
        return {"t-arrangement": t_arrangement_list}

    def assign_it():

        nonlocal t_arrangement_list, arrangement


        nonlocal t_arrangement
        nonlocal t_arrangement_list


        t_arrangement = T_arrangement()
        t_arrangement_list.append(t_arrangement)

        buffer_copy(arrangement, t_arrangement)

    if case_type == 1:

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement.argtnr == argtno)).first()

        if arrangement:
            assign_it()
    elif case_type == 2:

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == argtstr)).first()

        if arrangement:
            assign_it()
    elif case_type == 3:

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == argtstr) &  (Arrangement.argtnr != argtno)).first()

        if arrangement:
            assign_it()
    elif case_type == 4:

        for arrangement in db_session.query(Arrangement).all():
            assign_it()
    elif case_type == 5:

        for arrangement in db_session.query(Arrangement).filter(
                (Arrangement.segmentcode != argtno)).all():
            assign_it()

    return generate_output()