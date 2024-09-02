from functions.additional_functions import *
import decimal
from models import L_artikel

def s_stockiss_l_artikelbl(s_artnr:int):
    temp_l_artikel1_list = []
    l_artikel = None

    temp_l_artikel1 = None

    temp_l_artikel1_list, Temp_l_artikel1 = create_model("Temp_l_artikel1", {"fibukonto":str, "bezeich":str, "ek_aktuell":decimal, "artnr":int, "traubensort":str, "lief_einheit":decimal, "masseinheit":str, "betriebsnr":int, "alkoholgrad":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_l_artikel1_list, l_artikel


        nonlocal temp_l_artikel1
        nonlocal temp_l_artikel1_list
        return {"temp-l-artikel1": temp_l_artikel1_list}

    l_artikel = db_session.query(L_artikel).filter(
            (L_artikel.artnr == s_artnr)).first()

    if l_artikel:
        temp_l_artikel1 = Temp_l_artikel1()
        temp_l_artikel1_list.append(temp_l_artikel1)

        temp_l_artikel1.fibukonto = l_artikel.fibukonto
        temp_l_artikel1.bezeich = l_artikel.bezeich
        temp_l_artikel1.ek_aktuell = l_artikel.ek_aktuell
        temp_l_artikel1.artnr = l_artikel.artnr
        temp_l_artikel1.traubensort = l_artikel.traubensorte
        temp_l_artikel1.lief_einheit = l_artikel.lief_einheit
        temp_l_artikel1.masseinheit = l_artikel.masseinheit
        temp_l_artikel1.betriebsnr = l_artikel.betriebsnr
        temp_l_artikel1.alkoholgrad = l_artikel.alkoholgrad

    return generate_output()