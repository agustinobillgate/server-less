from functions.additional_functions import *
import decimal
from functions.htpchar import htpchar
from functions.htplogic import htplogic
from models import Htparam, H_artikel

def prepare_ts_cash1bl(dept:int):
    c_param870 = ""
    double_currency = False
    voucher_found = False
    htparam = h_artikel = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal c_param870, double_currency, voucher_found, htparam, h_artikel


        return {"c_param870": c_param870, "double_currency": double_currency, "voucher_found": voucher_found}

    c_param870 = get_output(htpchar(870))
    double_currency = get_output(htplogic(240))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1001)).first()

    if htparam.finteger > 0:

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnr == htparam.finteger) &  (H_artikel.departement == dept)).first()
        voucher_found = None != h_artikel

    return generate_output()