#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel

def read_h_artikelbl(case_type:int, artno:int, dept:int, aname:string, artart:int, betriebsno:int, actflag:bool):
    t_artikel_data = []
    h_artikel = None

    t_artikel = None

    t_artikel_data, T_artikel = create_model_like(H_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_data, h_artikel
        nonlocal case_type, artno, dept, aname, artart, betriebsno, actflag


        nonlocal t_artikel
        nonlocal t_artikel_data

        return {"t-artikel": t_artikel_data}

    def cr_artikel():

        nonlocal t_artikel_data, h_artikel
        nonlocal case_type, artno, dept, aname, artart, betriebsno, actflag


        nonlocal t_artikel
        nonlocal t_artikel_data


        t_artikel = T_artikel()
        t_artikel_data.append(t_artikel)

        buffer_copy(h_artikel, t_artikel)


    if case_type == 1:

        if artno != 0:

            h_artikel = get_cache (H_artikel, {"artnr": [(eq, artno)],"departement": [(eq, dept)]})

        elif aname != "":

            h_artikel = get_cache (H_artikel, {"bezeich": [(eq, aname)],"departement": [(eq, dept)]})

        if h_artikel:
            cr_artikel()
    elif case_type == 2:

        h_artikel = get_cache (H_artikel, {"departement": [(eq, dept)],"bezeich": [(eq, aname)],"artnr": [(ne, artno)]})

        if h_artikel:
            cr_artikel()

    return generate_output()