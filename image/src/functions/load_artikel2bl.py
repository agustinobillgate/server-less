from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Artikel

def load_artikel2bl(case_type:int, int1:int, int2:int, int3:int, int4:int, int5:int, char1:str):
    t_artikel_list = []
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, artikel


        nonlocal t_artikel
        nonlocal t_artikel_list
        return {"t-artikel": t_artikel_list}

    if case_type == 1:

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == int1) |  (Artikel.artart == int2)) &  (Artikel.artnr >= int3) &  (Artikel.artnr <= int4) &  (Artikel.departement == int5)).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)
    elif case_type == 2:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == int1) &  (Artikel.artart == int2) &  (Artikel.activeflag)).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)
    elif case_type == 3:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == int1) &  (Artikel.artart == int2) &  (Artikel.artnr >= int3) &  (Artikel.activeflag)).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)
    elif case_type == 4:

        for artikel in db_session.query(Artikel).filter(
                (Artikel.departement == int1) &  (Artikel.artart == int2) &  (func.lower(Artikel.bezeich) >= (char1).lower()) &  (Artikel.activeflag)).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)

    return generate_output()