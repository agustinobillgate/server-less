#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Artikel

def ts_disc1_cal_amountbl(menu_artnr:int, menu_departement:int):

    prepare_cache ([H_artikel, Artikel])

    t_h_artikel_data = []
    t_artikel_data = []
    h_artikel = artikel = None

    t_h_artikel = t_artikel = None

    t_h_artikel_data, T_h_artikel = create_model("T_h_artikel", {"mwst":int, "service":int, "artnr":int, "bezeich":string, "service_code":int, "mwst_code":int})
    t_artikel_data, T_artikel = create_model("T_artikel", {"umsatzart":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_artikel_data, t_artikel_data, h_artikel, artikel
        nonlocal menu_artnr, menu_departement


        nonlocal t_h_artikel, t_artikel
        nonlocal t_h_artikel_data, t_artikel_data

        return {"t-h-artikel": t_h_artikel_data, "t-artikel": t_artikel_data}


    h_artikel = get_cache (H_artikel, {"artnr": [(eq, menu_artnr)],"departement": [(eq, menu_departement)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})
    t_h_artikel = T_h_artikel()
    t_h_artikel_data.append(t_h_artikel)

    t_h_artikel.mwst = h_artikel.mwst_code
    t_h_artikel.service = h_artikel.service_code
    t_h_artikel.artnr = h_artikel.artnr
    t_h_artikel.bezeich = h_artikel.bezeich
    t_h_artikel.service_code = h_artikel.service_code
    t_h_artikel.mwst_code = h_artikel.mwst_code


    t_artikel = T_artikel()
    t_artikel_data.append(t_artikel)

    t_artikel.umsatzart = artikel.umsatzart

    return generate_output()