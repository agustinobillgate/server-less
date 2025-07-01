#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def ins_po_load_l_artikelbl(s_artnr:int):

    prepare_cache ([L_artikel])

    t_l_artikel_list = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "bezeich":string, "ek_aktuell":Decimal, "ek_letzter":Decimal, "traubensort":string, "lief_einheit":Decimal, "lief_nr1":int, "lief_nr2":int, "lief_nr3":int, "jahrgang":int, "alkoholgrad":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_list, l_artikel
        nonlocal s_artnr


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list

        return {"t-l-artikel": t_l_artikel_list}

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})
    t_l_artikel = T_l_artikel()
    t_l_artikel_list.append(t_l_artikel)

    t_l_artikel.rec_id = l_artikel._recid
    t_l_artikel.artnr = l_artikel.artnr
    t_l_artikel.bezeich = l_artikel.bezeich
    t_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
    t_l_artikel.ek_letzter =  to_decimal(l_artikel.ek_letzter)
    t_l_artikel.traubensort = l_artikel.traubensorte
    t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
    t_l_artikel.lief_nr1 = l_artikel.lief_nr1
    t_l_artikel.lief_nr2 = l_artikel.lief_nr2
    t_l_artikel.lief_nr3 = l_artikel.lief_nr3
    t_l_artikel.jahrgang = l_artikel.jahrgang
    t_l_artikel.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)

    return generate_output()