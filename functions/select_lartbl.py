#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def select_lartbl(lief_nr:int, t_zwkum:int):

    prepare_cache ([L_artikel])

    t_l_artikel_data = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_data, T_l_artikel = create_model("T_l_artikel", {"artnr":int, "bezeich":string, "masseinheit":string, "ek_aktuell":Decimal, "ek_letzter":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_data, l_artikel
        nonlocal lief_nr, t_zwkum


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data

        return {"t-l-artikel": t_l_artikel_data}

    if lief_nr > 0:

        for l_artikel in db_session.query(L_artikel).filter(
                 ((L_artikel.lief_nr1 == lief_nr) | (L_artikel.lief_nr2 == lief_nr) | (L_artikel.lief_nr3 == lief_nr))).order_by(L_artikel.bezeich).all():
            t_l_artikel = T_l_artikel()
            t_l_artikel_data.append(t_l_artikel)

            t_l_artikel.artnr = l_artikel.artnr
            t_l_artikel.bezeich = l_artikel.bezeich
            t_l_artikel.masseinheit = l_artikel.masseinheit
            t_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
            t_l_artikel.ek_letzter =  to_decimal(l_artikel.ek_letzter)

    else:

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.zwkum == t_zwkum)).order_by(L_artikel.bezeich).all():
            t_l_artikel = T_l_artikel()
            t_l_artikel_data.append(t_l_artikel)

            t_l_artikel.artnr = l_artikel.artnr
            t_l_artikel.bezeich = l_artikel.bezeich
            t_l_artikel.masseinheit = l_artikel.masseinheit
            t_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
            t_l_artikel.ek_letzter =  to_decimal(l_artikel.ek_letzter)

    return generate_output()