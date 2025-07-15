#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import H_artikel, Htparam

def ts_hbline_select_item2bl(art_list_artnr:int, dept:int):

    prepare_cache ([H_artikel, Htparam])

    param_172 = ""
    t_h_artikel_data = []
    i:int = 0
    h_artikel = htparam = None

    t_h_artikel = None

    t_h_artikel_data, T_h_artikel = create_model("T_h_artikel", {"bezaendern":bool, "epreis1":Decimal, "departement":int, "aenderwunsch":bool, "bondruckernr":[int,4], "betriebsnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal param_172, t_h_artikel_data, i, h_artikel, htparam
        nonlocal art_list_artnr, dept


        nonlocal t_h_artikel
        nonlocal t_h_artikel_data

        return {"param_172": param_172, "t-h-artikel": t_h_artikel_data}

    h_artikel = get_cache (H_artikel, {"artnr": [(eq, art_list_artnr)],"departement": [(eq, dept)]})
    t_h_artikel = T_h_artikel()
    t_h_artikel_data.append(t_h_artikel)

    t_h_artikel.bezaendern = h_artikel.bezaendern
    t_h_artikel.epreis1 =  to_decimal(h_artikel.epreis1)
    t_h_artikel.departement = h_artikel.departement
    t_h_artikel.aenderwunsch = h_artikel.aenderwunsch
    t_h_artikel.betriebsnr = h_artikel.betriebsnr


    for i in range(1,4 + 1) :
        t_h_artikel.bondruckernr[i - 1] = h_artikel.bondruckernr[i - 1]
        i = i + 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 172)]})
    param_172 = htparam.fchar

    return generate_output()