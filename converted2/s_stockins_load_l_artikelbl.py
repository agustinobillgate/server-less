#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import L_artikel

def s_stockins_load_l_artikelbl(icase:int, a_artnr:int, a_bezeich:string):

    prepare_cache ([L_artikel])

    t_l_artikel_data = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_data, T_l_artikel = create_model("T_l_artikel", {"artnr":int, "bezeich":string, "ek_aktuell":Decimal, "t_description":string, "lief_einheit":Decimal, "betriebsnr":int, "vk_preis":Decimal, "alkoholgrad":Decimal, "rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_data, l_artikel
        nonlocal icase, a_artnr, a_bezeich


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data

        return {"t-l-artikel": t_l_artikel_data}

    def create_t_l_artikel():

        nonlocal t_l_artikel_data, l_artikel
        nonlocal icase, a_artnr, a_bezeich


        nonlocal t_l_artikel
        nonlocal t_l_artikel_data


        t_l_artikel = T_l_artikel()
        t_l_artikel_data.append(t_l_artikel)

        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
        t_l_artikel.t_description = trim(l_artikel.bezeich) + " - " +\
                l_artikel.traubensorte + " [" +\
                to_string(l_artikel.lief_einheit) + " " +\
                l_artikel.masseinheit + "]"
        t_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        t_l_artikel.betriebsnr = l_artikel.betriebsnr
        t_l_artikel.vk_preis =  to_decimal(l_artikel.vk_preis)
        t_l_artikel.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)
        t_l_artikel.rec_id = l_artikel._recid


    if icase == 1:

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= a_artnr)).order_by(L_artikel._recid).all():
            create_t_l_artikel()


    elif icase == 2:

        for l_artikel in db_session.query(L_artikel).filter(
                 (matches(L_artikel.bezeich,a_bezeich))).order_by(L_artikel._recid).all():
            create_t_l_artikel()


    elif icase == 3:

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.bezeich >= (a_bezeich).lower())).order_by(L_artikel._recid).all():
            create_t_l_artikel()


    return generate_output()