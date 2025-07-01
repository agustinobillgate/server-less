#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_bestand, L_artikel

op_list_list, Op_list = create_model_like(L_op, {"bezeich":string, "username":string, "onhand":Decimal, "acct_bez":string, "masseinheit":string})

def s_storerequest_check_qtybl(pvilanguage:int, op_list_list:[Op_list]):

    prepare_cache ([L_bestand, L_artikel])

    its_ok = True
    msg_str = ""
    lvcarea:string = "s-storerequest"
    l_op = l_bestand = l_artikel = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, lvcarea, l_op, l_bestand, l_artikel
        nonlocal pvilanguage


        nonlocal op_list

        return {"its_ok": its_ok, "msg_str": msg_str}

    def check_qty():

        nonlocal its_ok, msg_str, lvcarea, l_op, l_bestand, l_artikel
        nonlocal pvilanguage


        nonlocal op_list

        curr_oh:Decimal = to_decimal("0.0")

        for op_list in query(op_list_list):
            curr_oh =  to_decimal("0")

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, op_list.artnr)],"lager_nr": [(eq, op_list.lager_nr)]})

            if l_bestand:
                curr_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)

            if curr_oh < op_list.anzahl:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, op_list.artnr)]})
                msg_str = msg_str + chr_unicode(2) + translateExtended ("Wrong quantity: ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr_unicode(10) + translateExtended ("Inputted quantity =", lvcarea, "") + " " + to_string(op_list.anzahl) + translateExtended (" - Stock onhand =", lvcarea, "") + " " + to_string(curr_oh) + chr_unicode(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
                its_ok = False

                return

    check_qty()

    return generate_output()