from functions.additional_functions import *
import decimal
from datetime import date
from models import H_artikel, H_compli

def hcompli_list_p_artnrbl(c_list_p_artnr:int, c_list_bezeich:str, artnr:int, c_list_dept:int, c_list_datum:date, c_list_rechnr:int):
    avail_h_artikel = False
    h_artikel = h_compli = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_h_artikel, h_artikel, h_compli


        return {"avail_h_artikel": avail_h_artikel}


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel.artnr == c_list_p_artnr) &  (H_artikel.departement == c_list_dept)).first()

    if not h_artikel:
        avail_h_artikel = False

        return generate_output()
    c_list_p_artnr = h_artikel.artnr
    c_list_bezeich = h_artikel.bezeich
    avail_h_artikel = True

    for h_compli in db_session.query(H_compli).filter(
            (H_compli.datum == c_list_datum) &  (H_compli.c_list_dept == H_compli.departement) &  (H_compli.c_list_rechnr == H_compli.rechnr) &  (H_compli.betriebsnr == 0)).all():
        h_compli.p_artnr = c_list_p_artnr

    return generate_output()