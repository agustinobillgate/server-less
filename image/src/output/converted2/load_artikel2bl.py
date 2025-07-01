#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Artikel

def load_artikel2bl(case_type:int, int1:int, int2:int, int3:int, int4:int, int5:int, char1:string):
    t_artikel_list = []
    artikel = None

    t_artikel = None

    t_artikel_list, T_artikel = create_model_like(Artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_artikel_list, artikel
        nonlocal case_type, int1, int2, int3, int4, int5, char1


        nonlocal t_artikel
        nonlocal t_artikel_list

        return {"t-artikel": t_artikel_list}

    if case_type == 1:

        for artikel in db_session.query(Artikel).filter(
                 ((Artikel.artart == int1) | (Artikel.artart == int2)) & (Artikel.artnr >= int3) & (Artikel.artnr <= int4) & (Artikel.departement == int5)).order_by((to_string(Artikel.artart) + to_string(Artikel.artnr, "9999"))).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)
    elif case_type == 2:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == int1) & (Artikel.artart == int2) & (Artikel.activeflag)).order_by(Artikel._recid).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)
    elif case_type == 3:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == int1) & (Artikel.artart == int2) & (Artikel.artnr >= int3) & (Artikel.activeflag)).order_by(Artikel._recid).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)
    elif case_type == 4:

        for artikel in db_session.query(Artikel).filter(
                 (Artikel.departement == int1) & (Artikel.artart == int2) & (Artikel.bezeich >= (char1).lower()) & (Artikel.activeflag)).order_by(Artikel._recid).all():
            t_artikel = T_artikel()
            t_artikel_list.append(t_artikel)

            buffer_copy(artikel, t_artikel)

    return generate_output()