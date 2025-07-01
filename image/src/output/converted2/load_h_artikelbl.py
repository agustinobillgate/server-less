#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel

def load_h_artikelbl(case_type:int, dept:int, arttype:int):
    t_h_artikel_list = []
    h_artikel = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_artikel_list, h_artikel
        nonlocal case_type, dept, arttype


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        return {"t-h-artikel": t_h_artikel_list}

    if case_type == 1:

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept) & (H_artikel.artart == arttype) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():
            t_h_artikel = T_h_artikel()
            t_h_artikel_list.append(t_h_artikel)

            buffer_copy(h_artikel, t_h_artikel)


    elif case_type == 2:

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept) & ((H_artikel.artart == 2) | (H_artikel.artart == 7)) & (H_artikel.activeflag)).order_by(H_artikel._recid).all():
            t_h_artikel = T_h_artikel()
            t_h_artikel_list.append(t_h_artikel)

            buffer_copy(h_artikel, t_h_artikel)


    elif case_type == 3:

        for h_artikel in db_session.query(H_artikel).filter(
                 (H_artikel.departement == dept)).order_by(H_artikel._recid).all():
            t_h_artikel = T_h_artikel()
            t_h_artikel_list.append(t_h_artikel)

            buffer_copy(h_artikel, t_h_artikel)


    return generate_output()