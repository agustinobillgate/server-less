from functions.additional_functions import *
import decimal
from models import L_artikel, Htparam

def mk_rezept_sort_articlebl(case_type:int, fbart_only:bool):
    t_l_artikel_list = []
    food_endkum:int = 0
    bev_endkum:int = 0
    mat_endkum:int = 0
    l_artikel = htparam = None

    t_l_artikel = None

    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_list, food_endkum, bev_endkum, mat_endkum, l_artikel, htparam
        nonlocal case_type, fbart_only


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list
        return {"t-l-artikel": t_l_artikel_list}

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 257)).first()
    food_endkum = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 258)).first()
    bev_endkum = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 268)).first()
    mat_endkum = htparam.finteger

    if case_type == 1:

        if fbart_only:

            for l_artikel in db_session.query(L_artikel).filter(
                     (L_artikel.endkum == food_endkum) | (L_artikel.endkum == bev_endkum)).order_by(L_artikel._recid).all():
                t_l_artikel = T_l_artikel()
                t_l_artikel_list.append(t_l_artikel)

                buffer_copy(l_artikel, t_l_artikel)
        else:

            for l_artikel in db_session.query(L_artikel).order_by(L_artikel._recid).all():
                t_l_artikel = T_l_artikel()
                t_l_artikel_list.append(t_l_artikel)

                buffer_copy(l_artikel, t_l_artikel)

    return generate_output()