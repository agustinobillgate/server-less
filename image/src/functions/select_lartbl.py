from functions.additional_functions import *
import decimal
from models import L_artikel

def select_lartbl(lief_nr:int, t_zwkum:int):
    t_l_artikel_list = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"artnr":int, "bezeich":str, "masseinheit":str, "ek_aktuell":decimal, "ek_letzter":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_list, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list
        return {"t-l-artikel": t_l_artikel_list}

    if lief_nr > 0:

        for l_artikel in db_session.query(L_artikel).filter(
                ((L_artikel.lief_nr1 == lief_nr) |  (L_artikel.lief_nr2 == lief_nr) |  (L_artikel.lief_nr3 == lief_nr))).all():
            t_l_artikel = T_l_artikel()
            t_l_artikel_list.append(t_l_artikel)

            t_l_artikel.artnr = l_artikel.artnr
            t_l_artikel.bezeich = l_artikel.bezeich
            t_l_artikel.masseinheit = l_artikel.masseinheit
            t_l_artikel.ek_aktuell = l_artikel.ek_aktuell
            t_l_artikel.ek_letzter = l_artikel.ek_letzter

    else:

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.zwkum == t_zwkum)).all():
            t_l_artikel = T_l_artikel()
            t_l_artikel_list.append(t_l_artikel)

            t_l_artikel.artnr = l_artikel.artnr
            t_l_artikel.bezeich = l_artikel.bezeich
            t_l_artikel.masseinheit = l_artikel.masseinheit
            t_l_artikel.ek_aktuell = l_artikel.ek_aktuell
            t_l_artikel.ek_letzter = l_artikel.ek_letzter

    return generate_output()