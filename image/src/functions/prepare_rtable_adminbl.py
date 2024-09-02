from functions.additional_functions import *
import decimal
from models import Tisch, Hoteldpt

def prepare_rtable_adminbl(dept:int):
    h_depart = ""
    t_tisch_list = []
    tisch = hoteldpt = None

    t_tisch = None

    t_tisch_list, T_tisch = create_model_like(Tisch)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_depart, t_tisch_list, tisch, hoteldpt


        nonlocal t_tisch
        nonlocal t_tisch_list
        return {"h_depart": h_depart, "t-tisch": t_tisch_list}

    hoteldpt = db_session.query(Hoteldpt).filter(
            (Hoteldpt.num == dept)).first()
    h_depart = hoteldpt.depart

    for tisch in db_session.query(Tisch).filter(
            (Tisch.departement == dept)).all():
        t_tisch = T_tisch()
        t_tisch_list.append(t_tisch)

        buffer_copy(tisch, t_tisch)

    return generate_output()