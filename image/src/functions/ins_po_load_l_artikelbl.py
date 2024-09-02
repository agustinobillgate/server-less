from functions.additional_functions import *
import decimal
from models import L_artikel

def ins_po_load_l_artikelbl(s_artnr:int):
    t_l_artikel_list = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "bezeich":str, "ek_aktuell":decimal, "ek_letzter":decimal, "traubensort":str, "lief_einheit":decimal, "lief_nr1":int, "lief_nr2":int, "lief_nr3":int, "jahrgang":int, "alkoholgrad":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_list, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list
        return {"t-l-artikel": t_l_artikel_list}

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()
    t_l_artikel = T_l_artikel()
    t_l_artikel_list.append(t_l_artikel)

    t_l_artikel.rec_id = l_artikel._recid
    t_l_artikel.artnr = l_artikel.artnr
    t_l_artikel.bezeich = l_artikel.bezeich
    t_l_artikel.ek_aktuell = l_artikel.ek_aktuell
    t_l_artikel.ek_letzter = l_artikel.ek_letzter
    t_l_artikel.traubensort = l_artikel.traubensorte
    t_l_artikel.lief_einheit = l_artikel.lief_einheit
    t_l_artikel.lief_nr1 = l_artikel.lief_nr1
    t_l_artikel.lief_nr2 = l_artikel.lief_nr2
    t_l_artikel.lief_nr3 = l_artikel.lief_nr3
    t_l_artikel.jahrgang = l_artikel.jahrgang
    t_l_artikel.alkoholgrad = l_artikel.alkoholgrad

    return generate_output()