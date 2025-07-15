#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import L_artikel

def s_stockin_load_temp_l_artikelbl(icase:int, a_artnr:int, a_bezeich:string):

    prepare_cache ([L_artikel])

    temp_l_artikel_data = []
    l_artikel = None

    temp_l_artikel = None

    temp_l_artikel_data, Temp_l_artikel = create_model("Temp_l_artikel", {"bezeich":string, "ek_aktuell":Decimal, "artnr":int, "traubensort":string, "lief_einheit":Decimal, "masseinheit":string, "betriebsnr":int, "alkoholgrad":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal temp_l_artikel_data, l_artikel
        nonlocal icase, a_artnr, a_bezeich


        nonlocal temp_l_artikel
        nonlocal temp_l_artikel_data

        return {"temp-l-artikel": temp_l_artikel_data}

    def create_temp_l_artikel():

        nonlocal temp_l_artikel_data, l_artikel
        nonlocal icase, a_artnr, a_bezeich


        nonlocal temp_l_artikel
        nonlocal temp_l_artikel_data


        temp_l_artikel = Temp_l_artikel()
        temp_l_artikel_data.append(temp_l_artikel)

        temp_l_artikel.bezeich = l_artikel.bezeich
        temp_l_artikel.ek_aktuell =  to_decimal(l_artikel.ek_aktuell)
        temp_l_artikel.artnr = l_artikel.artnr
        temp_l_artikel.traubensort = l_artikel.traubensorte
        temp_l_artikel.lief_einheit =  to_decimal(l_artikel.lief_einheit)
        temp_l_artikel.masseinheit = l_artikel.masseinheit
        temp_l_artikel.betriebsnr = l_artikel.betriebsnr
        temp_l_artikel.alkoholgrad =  to_decimal(l_artikel.alkoholgrad)


    if icase == 1:

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.artnr >= a_artnr)).order_by(L_artikel._recid).all():
            create_temp_l_artikel()


    elif icase == 2:

        for l_artikel in db_session.query(L_artikel).filter(
                 (matches(L_artikel.bezeich,a_bezeich))).order_by(L_artikel._recid).all():
            create_temp_l_artikel()


    elif icase == 3:

        for l_artikel in db_session.query(L_artikel).filter(
                 (L_artikel.bezeich >= (a_bezeich).lower())).order_by(L_artikel._recid).all():
            create_temp_l_artikel()


    return generate_output()