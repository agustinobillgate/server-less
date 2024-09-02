from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_artikel

def read_l_artikelbl(case_type:int, zwkum:int, artno:int, s_artnr:int, s_bezeich:str):
    t_l_artikel_list = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_list, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list
        return {"t-l-artikel": t_l_artikel_list}

    def cr_l_artikel():

        nonlocal t_l_artikel_list, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list


        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)

    if case_type == 1:

        l_artikel = db_session.query(L_artikel).first()

        if l_artikel:
            cr_l_artikel()
    elif case_type == 2:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.zwkum == zwkum) &  (L_artikel.artnr == artno)).first()

        if l_artikel:

            l_artikel = db_session.query(L_artikel).first()

            if l_artikel:
                cr_l_artikel()
    elif case_type == 3:

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.artnr >= s_artnr)).all():
            cr_l_artikel()
    elif case_type == 4:

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.bezeich.op("~")(s_bezeich))).all():
            cr_l_artikel()
    elif case_type == 5:

        for l_artikel in db_session.query(L_artikel).filter(
                (func.lower(L_artikel.bezeich) >= (s_bezeich).lower())).all():
            cr_l_artikel()
    elif case_type == 6:

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == artno)).first()

        if l_artikel:
            cr_l_artikel()
    elif case_type == 7:

        for l_artikel in db_session.query(L_artikel).all():
            cr_l_artikel()

    return generate_output()