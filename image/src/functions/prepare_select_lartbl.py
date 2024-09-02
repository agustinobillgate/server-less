from functions.additional_functions import *
import decimal
from models import L_untergrup, L_artikel

def prepare_select_lartbl(lief_nr:int):
    t_l_untergrup_list = []
    t_l_artikel_list = []
    l_untergrup = l_artikel = None

    t_l_artikel = t_l_untergrup = None

    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"artnr":int, "bezeich":str, "masseinheit":str, "ek_aktuell":decimal, "ek_letzter":decimal})
    t_l_untergrup_list, T_l_untergrup = create_model("T_l_untergrup", {"zwkum":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_untergrup_list, t_l_artikel_list, l_untergrup, l_artikel


        nonlocal t_l_artikel, t_l_untergrup
        nonlocal t_l_artikel_list, t_l_untergrup_list
        return {"t-l-untergrup": t_l_untergrup_list, "t-l-artikel": t_l_artikel_list}


    for l_untergrup in db_session.query(L_untergrup).all():
        t_l_untergrup = T_l_untergrup()
        t_l_untergrup_list.append(t_l_untergrup)

        t_l_untergrup.zwkum = l_untergrup.zwkum
        t_l_untergrup.bezeich = l_untergrup.bezeich

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

        t_l_untergrup = query(t_l_untergrup_list, first=True)

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.zwkum == t_l_untergrup.zwkum)).all():
            t_l_artikel = T_l_artikel()
            t_l_artikel_list.append(t_l_artikel)

            t_l_artikel.artnr = l_artikel.artnr
            t_l_artikel.bezeich = l_artikel.bezeich
            t_l_artikel.masseinheit = l_artikel.masseinheit
            t_l_artikel.ek_aktuell = l_artikel.ek_aktuell
            t_l_artikel.ek_letzter = l_artikel.ek_letzter

    return generate_output()