#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_bestand, L_op

def s_transform_return_s_artnrbl(s_artnr:int, curr_lager:int, avail_out_list:bool, transdate:date, mat_closedate:date, closedate:date, req_flag:bool, lscheinnr:string):

    prepare_cache ([L_artikel, L_bestand])

    l_artikel_artnr = 0
    stock_oh = to_decimal("0.0")
    description = ""
    price = to_decimal("0.0")
    l_op_lscheinnr = ""
    err_flag = 0
    l_artikel = l_bestand = l_op = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_artikel_artnr, stock_oh, description, price, l_op_lscheinnr, err_flag, l_artikel, l_bestand, l_op
        nonlocal s_artnr, curr_lager, avail_out_list, transdate, mat_closedate, closedate, req_flag, lscheinnr

        return {"l_artikel_artnr": l_artikel_artnr, "stock_oh": stock_oh, "description": description, "price": price, "l_op_lscheinnr": l_op_lscheinnr, "err_flag": err_flag}


    l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_artnr)]})

    if not l_artikel:
        err_flag = 1

        return generate_output()
    l_artikel_artnr = l_artikel.artnr

    if l_artikel.betriebsnr == 0:

        l_bestand = get_cache (L_bestand, {"lager_nr": [(eq, curr_lager)],"artnr": [(eq, s_artnr)]})

        if not l_bestand:
            err_flag = 2

            return generate_output()
        else:

            if avail_out_list:
                err_flag = 3

                return generate_output()

            if l_artikel.endkum < 3:

                if transdate > closedate:
                    err_flag = 4

                    return generate_output()

            if l_artikel.endkum == 3:

                if transdate > mat_closedate:
                    err_flag = 5

                    return generate_output()

            if req_flag:

                l_op = db_session.query(L_op).filter(
                         (L_op.artnr == s_artnr) & (L_op.datum == transdate) & ((L_op.op_art == 3) | (L_op.op_art == 4)) & (substring(L_op.lscheinnr, 3, (length(L_op.lscheinnr) - 3)) == substring(lscheinnr, 3, (length(lscheinnr) - 3)))).first()

                if l_op:
                    err_flag = 6
            stock_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
            description = l_artikel.bezeich + " - " + l_artikel.masseinheit
            price =  to_decimal(l_artikel.vk_preis)
            err_flag = 7

            return generate_output()
    else:
        description = l_artikel.bezeich + " - " + l_artikel.masseinheit
        price =  to_decimal("0")
        stock_oh =  to_decimal("0")
        err_flag = 8

        return generate_output()

    return generate_output()