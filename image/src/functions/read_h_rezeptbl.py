from functions.additional_functions import *
import decimal
from datetime import date
from models import H_rezept

def read_h_rezeptbl(case_type:int, int1:int, int2:int, int3:int, char1:str, date1:date):
    t_h_rezept_list = []
    h_rezept = None

    t_h_rezept = None

    t_h_rezept_list, T_h_rezept = create_model_like(H_rezept)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_rezept_list, h_rezept


        nonlocal t_h_rezept
        nonlocal t_h_rezept_list
        return {"t-h-rezept": t_h_rezept_list}

    def assign_it():

        nonlocal t_h_rezept_list, h_rezept


        nonlocal t_h_rezept
        nonlocal t_h_rezept_list


        t_h_rezept = T_h_rezept()
        t_h_rezept_list.append(t_h_rezept)

        buffer_copy(h_rezept, t_h_rezept)

    if case_type == 1:

        h_rezept = db_session.query(H_rezept).filter(
                (H_rezept.artnrrezept == int1)).first()

        if h_rezept:
            assign_it()
    elif case_type == 2:

        for h_rezept in db_session.query(H_rezept).all():
            assign_it()

    return generate_output()