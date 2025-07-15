#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_bestand, Htparam

def dml_stockin_ret_qtybl(s_artnr:int, curr_lager:int, qty:Decimal):

    prepare_cache ([Htparam])

    rest = to_decimal("0.0")
    fl_code = 0
    htparam_paramgruppe = 0
    htparam_flogical = False
    l_bestand = htparam = None

    l_oh = None

    L_oh = create_buffer("L_oh",L_bestand)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rest, fl_code, htparam_paramgruppe, htparam_flogical, l_bestand, htparam
        nonlocal s_artnr, curr_lager, qty
        nonlocal l_oh


        nonlocal l_oh

        return {"rest": rest, "fl_code": fl_code, "htparam_paramgruppe": htparam_paramgruppe, "htparam_flogical": htparam_flogical}


    if qty < 0:

        l_oh = db_session.query(L_oh).filter(
                 (L_oh.artnr == s_artnr) & (L_oh.lager_nr == curr_lager)).first()

        if l_oh and (anz_anf_best + anz_eingang - anz_ausgang + qty) < 0:
            rest = ( to_decimal(anz_anf_best) + to_decimal(anz_eingang) - to_decimal(anz_ausgang) + to_decimal(qty))
            fl_code = 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 402)]})
    htparam_paramgruppe = htparam.paramgruppe
    htparam_flogical = htparam.flogical

    return generate_output()