from functions.additional_functions import *
import decimal
from models import H_artikel, Htparam

def ts_hbline_select_item2bl(art_list_artnr:int, dept:int):
    param_172 = ""
    t_h_artikel_list = []
    i:int = 0
    h_artikel = htparam = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model("T_h_artikel", {"bezaendern":bool, "epreis1":decimal, "departement":int, "aenderwunsch":bool, "bondruckernr":[int], "betriebsnr":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal param_172, t_h_artikel_list, i, h_artikel, htparam


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list
        return {"param_172": param_172, "t-h-artikel": t_h_artikel_list}

    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == art_list_artnr) &  (H_artikel.departement == dept)).first()
    t_h_artikel = T_h_artikel()
    t_h_artikel_list.append(t_h_artikel)

    t_h_artikel.bezaendern = h_artikel.bezaendern
    t_h_artikel.epreis1 = h_artikel.epreis1
    t_h_artikel.departement = h_artikel.departement
    t_h_artikel.aenderwunsch = h_artikel.aenderwunsch
    t_h_artikel.betriebsnr = h_artikel.betriebsnr


    for i in range(1,4 + 1) :
        t_h_artikel.bondruckernr[i - 1] = h_artikel.bondruckernr[i - 1]
        i = i + 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 172)).first()
    param_172 = htparam.fchar

    return generate_output()