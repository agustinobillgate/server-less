from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_artikel

def s_stockins_load_l_artikelbl(icase:int, a_artnr:int, a_bezeich:str):
    t_l_artikel_list = []
    l_artikel = None

    t_l_artikel = None

    t_l_artikel_list, T_l_artikel = create_model("T_l_artikel", {"artnr":int, "bezeich":str, "ek_aktuell":decimal, "t_description":str, "lief_einheit":decimal, "betriebsnr":int, "vk_preis":decimal, "alkoholgrad":decimal, "rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_l_artikel_list, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list
        return {"t-l-artikel": t_l_artikel_list}

    def create_t_l_artikel():

        nonlocal t_l_artikel_list, l_artikel


        nonlocal t_l_artikel
        nonlocal t_l_artikel_list


        t_l_artikel = T_l_artikel()
        t_l_artikel_list.append(t_l_artikel)

        t_l_artikel.artnr = l_artikel.artnr
        t_l_artikel.bezeich = l_artikel.bezeich
        t_l_artikel.ek_aktuell = l_artikel.ek_aktuell
        t_l_artikel.t_description = trim(l_artikel.bezeich) + " - " +\
                l_artikel.traubensort + " [" +\
                to_string(l_artikel.lief_einheit) + " " +\
                l_artikel.masseinheit + "]"
        t_l_artikel.lief_einheit = l_artikel.lief_einheit
        t_l_artikel.betriebsnr = l_artikel.betriebsnr
        t_l_artikel.vk_preis = l_artikel.vk_preis
        t_l_artikel.alkoholgrad = l_artikel.alkoholgrad
        t_l_artikel.rec_id = l_artikel._recid

    if icase == 1:

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.artnr >= a_artnr)).all():
            create_t_l_artikel()


    elif icase == 2:

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.bezeich matches a_bezeich)).all():
            create_t_l_artikel()


    elif icase == 3:

        for l_artikel in db_session.query(L_artikel).filter(
                (func.lower(L_artikel.bezeich) >= (a_bezeich).lower())).all():
            create_t_l_artikel()


    return generate_output()