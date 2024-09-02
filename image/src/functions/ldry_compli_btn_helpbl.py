from functions.additional_functions import *
import decimal
from datetime import date
from models import H_artikel, H_compli

def ldry_compli_btn_helpbl(billart:int, c_list_dept:int, c_list_datum:date, c_list_rechnr:int):
    t_bezeich = ""
    h_artikel = h_compli = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bezeich, h_artikel, h_compli


        return {"t_bezeich": t_bezeich}


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == billart) &  (H_artikel.departement == c_list_dept)).first()
    t_bezeich = h_artikel.bezeich

    for h_compli in db_session.query(H_compli).filter(
            (H_compli.datum == c_list_datum) &  (H_compli.c_list_dept == H_compli.departement) &  (H_compli.c_list_rechnr == H_compli.rechnr)).all():
        h_compli.p_artnr = billart

    return generate_output()