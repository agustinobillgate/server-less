from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_artikel

def s_stockiss_load_l_artikelbl(icase:int, a_artnr:int, a_bezeich:str):
    temp_l_artikel_list = []
    l_artikel = None

    temp_l_artikel = None

    temp_l_artikel_list, Temp_l_artikel = create_model("Temp_l_artikel", {"fibukonto":str, "bezeich":str, "ek_aktuell":decimal, "artnr":int, "traubensort":str, "lief_einheit":decimal, "masseinheit":str, "betriebsnr":int, "alkoholgrad":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_l_artikel_list, l_artikel


        nonlocal temp_l_artikel
        nonlocal temp_l_artikel_list
        return {"temp-l-artikel": temp_l_artikel_list}

    def create_temp_l_artikel():

        nonlocal temp_l_artikel_list, l_artikel


        nonlocal temp_l_artikel
        nonlocal temp_l_artikel_list


        temp_l_artikel = Temp_l_artikel()
        temp_l_artikel_list.append(temp_l_artikel)

        temp_l_artikel.fibukonto = l_artikel.fibukonto
        temp_l_artikel.bezeich = l_artikel.bezeich
        temp_l_artikel.ek_aktuell = l_artikel.ek_aktuell
        temp_l_artikel.artnr = l_artikel.artnr
        temp_l_artikel.traubensort = l_artikel.traubensorte
        temp_l_artikel.lief_einheit = l_artikel.lief_einheit
        temp_l_artikel.masseinheit = l_artikel.masseinheit
        temp_l_artikel.betriebsnr = l_artikel.betriebsnr
        temp_l_artikel.alkoholgrad = l_artikel.alkoholgrad

    if icase == 1:

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.artnr >= a_artnr)).all():
            create_temp_l_artikel()


    elif icase == 2:

        for l_artikel in db_session.query(L_artikel).filter(
                (L_artikel.bezeich matches a_bezeich)).all():
            create_temp_l_artikel()


    elif icase == 3:

        for l_artikel in db_session.query(L_artikel).filter(
                (func.lower(L_artikel.bezeich) >= (a_bezeich).lower())).all():
            create_temp_l_artikel()


    return generate_output()