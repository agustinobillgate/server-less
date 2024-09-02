from functions.additional_functions import *
import decimal
from models import L_artikel

def s_stockout_load_l_artikelbl(s_artnr:int):
    temp_l_artikel_list = []
    l_artikel = None

    temp_l_artikel = None

    temp_l_artikel_list, Temp_l_artikel = create_model("Temp_l_artikel", {"artnr":int, "bezeich":str, "betriebsnr":int, "endkum":int, "masseinheit":str, "vk_preis":decimal, "inhalt":decimal, "lief_einheit":decimal, "traubensort":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_l_artikel_list, l_artikel


        nonlocal temp_l_artikel
        nonlocal temp_l_artikel_list
        return {"temp-l-artikel": temp_l_artikel_list}

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    if not l_artikel:

        return generate_output()
    temp_l_artikel = Temp_l_artikel()
    temp_l_artikel_list.append(temp_l_artikel)

    temp_l_artikel.artnr = l_artikel.artnr
    temp_l_artikel.bezeich = l_artikel.bezeich
    temp_l_artikel.betriebsnr = l_artikel.betriebsnr
    temp_l_artikel.endkum = l_artikel.endkum
    temp_l_artikel.masseinheit = l_artikel.masseinheit
    temp_l_artikel.vk_preis = l_artikel.vk_preis
    temp_l_artikel.inhalt = l_artikel.inhalt
    temp_l_artikel.lief_einheit = l_artikel.lief_einheit
    temp_l_artikel.traubensort = l_artikel.traubensorte

    return generate_output()