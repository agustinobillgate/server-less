#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def mk_po_load_l_artikelbl(icase:int, lief_nr:int, a_artnr:int, a_bezeich:string):

    prepare_cache ([L_artikel])

    t_l_artikel_list = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"rec_id":int, "artnr":int, "bezeich":string, "betriebsnr":int, "ek_aktuell":Decimal, "ek_letzter":Decimal, "traubensort":string, "lief_einheit":Decimal, "lief_nr1":int, "lief_nr2":int, "lief_nr3":int, "jahrgang":int, "alkoholgrad":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_list, l_artikel
        nonlocal icase, lief_nr, a_artnr, a_bezeich


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list

        return {"t-l-artikel": t_l_artikel_list}

    def create_t_l_artikel():

        nonlocal t_l_artikel_list, l_artikel
        nonlocal icase, lief_nr, a_artnr, a_bezeich


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list


        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.rec_id = l_artikel._recid
        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.betriebsnr = l_artikel.betriebsnr
        t_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
        t_l_artikel.ek_letzter =  to_decimal(l_artikel.ek_letzter)
        t_l_artikel.traubensort = l_artikel.traubensorte
        t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        t_l_artikel.lief_nr1 = l_artikel.lief_nr1
        t_l_artikel.lief_nr2 = l_artikel.lief_nr2
        t_l_artikel.lief_nr3 = l_artikel.lief_nr3
        t_l_artikel.jahrgang = l_artikel.jahrgang
        t_l_artikel.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)


    if icase == 1:

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= a_artnr) & ((L_artikel.lief_nr1 == lief_nr) | (L_artikel.lief_nr2 == lief_nr) | (L_artikel.lief_nr3 == lief_nr))).order_by(L_artikel.artnr).all():
            create_t_l_artikel()


    elif icase == 2:

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.bezeich >= (a_bezeich).lower()) & ((L_artikel.lief_nr1 == lief_nr) | (L_artikel.lief_nr2 == lief_nr) | (L_artikel.lief_nr3 == lief_nr))).order_by(L_artikel.bezeich).all():
            create_t_l_artikel()


    return generate_output()