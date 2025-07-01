#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand, Htparam

def dml_issue_return_qtybl(qty:Decimal, s_artnr:int, curr_lager:int):

    prepare_cache ([Htparam])

    rest = to_decimal("0.0")
    err_code = 0
    l_bestand = htparam = None

    l_oh = None

    L_oh = create_buffer("L_oh",L_bestand)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest, err_code, l_bestand, htparam
        nonlocal qty, s_artnr, curr_lager
        nonlocal l_oh


        nonlocal l_oh

        return {"rest": rest, "err_code": err_code}


    if qty < 0:

        l_oh = db_session.query(L_oh).filter(
                 (L_oh.artnr == s_artnr) & (L_oh.lager_nr == curr_lager)).first()

        if l_oh and (anz_anf_best + anz_eingang - anz_ausgang + qty) < 0:
            err_code = 1
            rest = ( to_decimal(anz_anf_best) + to_decimal(anz_eingang) - to_decimal(anz_ausgang) + to_decimal(qty))

            return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 402)]})

    if htparam.paramgruppe == 15:
        err_code = 2

        return generate_output()

    if not htparam.flogical:
        err_code = 3

        return generate_output()

    return generate_output()