#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_bestand, L_artikel

op_list_list, Op_list = create_model_like(L_op, {"bezeich":string, "username":string})

def s_transform_check_qtybl(op_list_list:[Op_list], pvilanguage:int):

    prepare_cache ([L_artikel])

    its_ok = True
    msg_str = ""
    curr_oh:Decimal = to_decimal("0.0")
    lvcarea:string = "s-transform"
    l_op = l_bestand = l_artikel = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, curr_oh, lvcarea, l_op, l_bestand, l_artikel
        nonlocal pvilanguage


        nonlocal op_list

        return {"its_ok": its_ok, "msg_str": msg_str}

    for op_list in query(op_list_list):

        l_bestand = get_cache (L_bestand, {"artnr": [(eq, op_list.artnr)],"lager_nr": [(eq, op_list.lager_nr)]})
        curr_oh =  to_decimal(anz_anf_best) + to_decimal(anz_eingang) - to_decimal(anz_ausgang)

        if curr_oh < op_list.anzahl:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, op_list.artnr)]})
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Wrong quantity: ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr_unicode(10) + translateExtended ("Inputted quantity =", lvcarea, "") + " " + to_string(op_list.anzahl) + translateExtended (" - Stock onhand =", lvcarea, "") + " " + to_string(curr_oh) + chr_unicode(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
            its_ok = False

            return generate_output()

    return generate_output()