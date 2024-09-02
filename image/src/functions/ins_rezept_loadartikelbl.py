from functions.additional_functions import *
import decimal
from models import L_artikel

def ins_rezept_loadartikelbl(sorttype:int, int1:int, int2:int, chr1:str):
    t_l_artikel_list = []
    a_bezeich:str = ""
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_list, T_l_artikel = create_model_like(L_artikel)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_list, a_bezeich, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list
        return {"t-l-artikel": t_l_artikel_list}

    def create_art():

        nonlocal t_l_artikel_list, a_bezeich, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list


        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        buffer_copy(l_artikel, t_l_artikel)


    a_bezeich = chr1

    if sorttype == 1:

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.artnr >= int1) &  (L_artikel.artnr <= int2)).all():
            create_art()
    else:

        if substring(a_bezeich, len(a_bezeich) - 1, 1) != "*":
            a_bezeich = a_bezeich + "*"

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.bezeich.op("~")(a_bezeich))).all():
            create_art()

    return generate_output()