#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, H_compli

def hcompli_list_p_artnrbl(c_list_p_artnr:int, c_list_bezeich:string, artnr:int, c_list_dept:int, c_list_datum:date, c_list_rechnr:int):

    prepare_cache ([H_artikel, H_compli])

    avail_h_artikel = False
    h_artikel = h_compli = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_h_artikel, h_artikel, h_compli
        nonlocal c_list_p_artnr, c_list_bezeich, artnr, c_list_dept, c_list_datum, c_list_rechnr

        return {"c_list_p_artnr": c_list_p_artnr, "c_list_bezeich": c_list_bezeich, "avail_h_artikel": avail_h_artikel}


    h_artikel = get_cache (H_artikel, {"artnr": [(eq, c_list_p_artnr)],"departement": [(eq, c_list_dept)]})

    if not h_artikel:
        avail_h_artikel = False

        return generate_output()
    c_list_p_artnr = h_artikel.artnr
    c_list_bezeich = h_artikel.bezeich
    avail_h_artikel = True

    for h_compli in db_session.query(H_compli).filter(
             (H_compli.datum == c_list_datum) & (c_list_dept == H_compli.departement) & (c_list_rechnr == H_compli.rechnr) & (H_compli.betriebsnr == 0)).order_by(H_compli._recid).all():
        h_compli.p_artnr = c_list_p_artnr

    return generate_output()