#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, H_compli

def ldry_compli_p_artnrbl(artnr:int, c_list_dept:int, c_list_rechnr:int, c_list_datum:date):

    prepare_cache ([H_artikel, H_compli])

    flag = 0
    t_bez = ""
    h_artikel = h_compli = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, t_bez, h_artikel, h_compli
        nonlocal artnr, c_list_dept, c_list_rechnr, c_list_datum

        return {"flag": flag, "t_bez": t_bez}


    h_artikel = get_cache (H_artikel, {"artnr": [(eq, artnr)],"departement": [(eq, c_list_dept)]})

    if not h_artikel:
        flag = 1

        return generate_output()
    flag = 2
    t_bez = h_artikel.bezeich

    for h_compli in db_session.query(H_compli).filter(
             (H_compli.datum == c_list_datum) & (c_list_dept == H_compli.departement) & (c_list_rechnr == H_compli.rechnr)).order_by(H_compli._recid).all():
        h_compli.p_artnr = artnr

    return generate_output()