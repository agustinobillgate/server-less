#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_rezept

def read_h_rezeptbl(case_type:int, int1:int, int2:int, int3:int, char1:string, date1:date):
    t_h_rezept_data = []
    h_rezept = None

    t_h_rezept = None

    t_h_rezept_data, T_h_rezept = create_model_like(H_rezept)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_rezept_data, h_rezept
        nonlocal case_type, int1, int2, int3, char1, date1


        nonlocal t_h_rezept
        nonlocal t_h_rezept_data

        return {"t-h-rezept": t_h_rezept_data}

    def assign_it():

        nonlocal t_h_rezept_data, h_rezept
        nonlocal case_type, int1, int2, int3, char1, date1


        nonlocal t_h_rezept
        nonlocal t_h_rezept_data


        t_h_rezept = T_h_rezept()
        t_h_rezept_data.append(t_h_rezept)

        buffer_copy(h_rezept, t_h_rezept)


    if case_type == 1:

        h_rezept = get_cache (H_rezept, {"artnrrezept": [(eq, int1)]})

        if h_rezept:
            assign_it()
    elif case_type == 2:

        for h_rezept in db_session.query(H_rezept).order_by(H_rezept._recid).all():
            assign_it()

    return generate_output()