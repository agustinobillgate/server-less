from functions.additional_functions import *
import decimal
from datetime import date
from models import H_artikel, H_compli

def ldry_compli_p_artnrbl(artnr:int, c_list_dept:int, c_list_rechnr:int, c_list_datum:date):
    flag = 0
    t_bez = ""
    h_artikel = h_compli = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, t_bez, h_artikel, h_compli


        return {"flag": flag, "t_bez": t_bez}


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == artnr) &  (H_artikel.departement == c_list_dept)).first()

    if not h_artikel:
        flag = 1

        return generate_output()
    flag = 2
    t_bez = h_artikel.bezeich

    for h_compli in db_session.query(H_compli).filter(
            (H_compli.datum == c_list_datum) &  (H_compli.c_list_dept == H_compli.departement) &  (H_compli.c_list_rechnr == H_compli.rechnr)).all():
        h_compli.p_artnr = artnr

    return generate_output()