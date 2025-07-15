#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Tisch, Hoteldpt

def prepare_rtable_adminbl(dept:int):

    prepare_cache ([Hoteldpt])

    h_depart = ""
    t_tisch_data = []
    tisch = hoteldpt = None

    t_tisch = None

    t_tisch_data, T_tisch = create_model_like(Tisch)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_depart, t_tisch_data, tisch, hoteldpt
        nonlocal dept


        nonlocal t_tisch
        nonlocal t_tisch_data

        return {"h_depart": h_depart, "t-tisch": t_tisch_data}

    hoteldpt = get_cache (Hoteldpt, {"num": [(eq, dept)]})
    h_depart = hoteldpt.depart

    for tisch in db_session.query(Tisch).filter(
             (Tisch.departement == dept)).order_by(Tisch.tischnr).all():
        t_tisch = T_tisch()
        t_tisch_data.append(t_tisch)

        buffer_copy(tisch, t_tisch)

    return generate_output()