#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_artikel

def s_stockiss_l_artikelbl(s_artnr:int):

    prepare_cache ([L_artikel])

    temp_l_artikel1_data = []
    l_artikel = None

    temp_l_artikel1 = None

    temp_l_artikel1_data, Temp_l_artikel1 = create_model("Temp_l_artikel1", {"fibukonto":string, "bezeich":string, "ek_aktuell":Decimal, "artnr":int, "traubensort":string, "lief_einheit":Decimal, "masseinheit":string, "betriebsnr":int, "alkoholgrad":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_l_artikel1_data, l_artikel
        nonlocal s_artnr


        nonlocal temp_l_artikel1
        nonlocal temp_l_artikel1_data

        return {"temp-l-artikel1": temp_l_artikel1_data}

    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    if l_artikel:
        temp_l_artikel1 = Temp_l_artikel1()
        temp_l_artikel1_data.append(temp_l_artikel1)

        temp_l_artikel1.fibukonto = l_artikel.fibukonto
        temp_l_artikel1.bezeich = l_artikel.bezeich
        temp_l_artikel1.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
        temp_l_artikel1.artnr = l_artikel.artnr
        temp_l_artikel1.traubensort = l_artikel.traubensorte
        temp_l_artikel1.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        temp_l_artikel1.masseinheit = l_artikel.masseinheit
        temp_l_artikel1.betriebsnr = l_artikel.betriebsnr
        temp_l_artikel1.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)

    return generate_output()