#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, L_bestand

def po_retour_return_qty_1bl(transdate:date, closedate:date, s_artnr:int, curr_lager:int, qty:Decimal, content:int):

    prepare_cache ([L_bestand])

    err_code = 0
    t_queasy_list = []
    qty1:Decimal = to_decimal("0.0")
    queasy = l_bestand = None

    t_queasy = l_oh = None

    t_queasy_list, T_queasy = create_model_like(Queasy)

    L_oh = create_buffer("L_oh",L_bestand)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, t_queasy_list, qty1, queasy, l_bestand
        nonlocal transdate, closedate, s_artnr, curr_lager, qty, content
        nonlocal l_oh


        nonlocal t_queasy, l_oh
        nonlocal t_queasy_list

        return {"err_code": err_code, "t-queasy": t_queasy_list}

    if transdate <= closedate:
        qty1 =  to_decimal(qty) * to_decimal(content)

        l_oh = get_cache (L_bestand, {"artnr": [(eq, s_artnr)],"lager_nr": [(eq, curr_lager)]})

        if l_oh:

            if (l_oh.anz_anf_best + l_oh.anz_eingang - l_oh.anz_ausgang) < qty1:
                err_code = 1

                return generate_output()

    queasy = get_cache (Queasy, {"key": [(eq, 20)],"number1": [(eq, s_artnr)]})

    if queasy:
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        buffer_copy(queasy, t_queasy)

    return generate_output()