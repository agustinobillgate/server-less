from functions.additional_functions import *
import decimal
from models import H_artikel, Artikel

def ts_disc1_cal_amountbl(menu_artnr:int, menu_departement:int):
    t_h_artikel_list = []
    t_artikel_list = []
    h_artikel = artikel = None

    t_h_artikel = t_artikel = None

    t_h_artikel_list, T_h_artikel = create_model("T_h_artikel", {"mwst":int, "service":int, "artnr":int, "bezeich":str, "service_code":int, "mwst_code":int})
    t_artikel_list, T_artikel = create_model("T_artikel", {"umsatzart":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_h_artikel_list, t_artikel_list, h_artikel, artikel


        nonlocal t_h_artikel, t_artikel
        nonlocal t_h_artikel_list, t_artikel_list
        return {"t-h-artikel": t_h_artikel_list, "t-artikel": t_artikel_list}


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == menu_artnr) &  (H_artikel.departement == menu_departement)).first()

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == h_Artikel.artnrfront) &  (Artikel.departement == h_Artikel.departement)).first()
    t_h_artikel = T_h_artikel()
    t_h_artikel_list.append(t_h_artikel)

    t_h_artikel.mwst = h_artikel.mwst_code
    t_h_artikel.service = h_artikel.service_code
    t_h_artikel.artnr = h_artikel.artnr
    t_h_artikel.bezeich = h_artikel.bezeich
    t_h_artikel.service_code = h_artikel.service_code
    t_h_artikel.mwst_code = h_artikel.mwst_code


    t_artikel = T_artikel()
    t_artikel_list.append(t_artikel)

    t_artikel.umsatzart = artikel.umsatzart

    return generate_output()