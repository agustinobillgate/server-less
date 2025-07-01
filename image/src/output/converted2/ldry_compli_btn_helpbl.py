#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, H_compli

def ldry_compli_btn_helpbl(billart:int, c_list_dept:int, c_list_datum:date, c_list_rechnr:int):

    prepare_cache ([H_artikel, H_compli])

    t_bezeich = ""
    h_artikel = h_compli = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_bezeich, h_artikel, h_compli
        nonlocal billart, c_list_dept, c_list_datum, c_list_rechnr

        return {"t_bezeich": t_bezeich}


    h_artikel = get_cache (H_artikel, {"artnr": [(eq, billart)],"departement": [(eq, c_list_dept)]})
    t_bezeich = h_artikel.bezeich

    for h_compli in db_session.query(H_compli).filter(
             (H_compli.datum == c_list_datum) & (c_list_dept == H_compli.departement) & (c_list_rechnr == H_compli.rechnr)).order_by(H_compli._recid).all():
        h_compli.p_artnr = billart

    return generate_output()