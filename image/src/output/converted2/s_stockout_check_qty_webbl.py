#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_bestand, L_artikel

op_list_list, Op_list = create_model_like(L_op, {"fibu":string, "a_bezeich":string, "a_lief_einheit":Decimal, "a_traubensort":string})

def s_stockout_check_qty_webbl(op_list_list:[Op_list], pvilanguage:int):

    prepare_cache ([L_bestand, L_artikel])

    msg_str = ""
    its_ok = True
    lvcarea:string = "s-stockout"
    l_op = l_bestand = l_artikel = None

    op_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, its_ok, lvcarea, l_op, l_bestand, l_artikel
        nonlocal pvilanguage


        nonlocal op_list

        return {"msg_str": msg_str, "its_ok": its_ok}

    def check_qty():

        nonlocal msg_str, its_ok, lvcarea, l_op, l_bestand, l_artikel
        nonlocal pvilanguage


        nonlocal op_list

        curr_oh:Decimal = to_decimal("0.0")
        out_oh:Decimal = to_decimal("0.0")
        curr_artnr:int = 0
        count_artnr:int = 0

        for op_list in query(op_list_list, sort_by=[("artnr",False)]):

            l_bestand = get_cache (L_bestand, {"artnr": [(eq, op_list.artnr)],"lager_nr": [(eq, op_list.lager_nr)]})

            if curr_artnr == 0 or (curr_artnr != op_list.artnr):
                curr_oh =  to_decimal(l_bestand.anz_anf_best) + to_decimal(l_bestand.anz_eingang) - to_decimal(l_bestand.anz_ausgang)
                count_artnr = 0


            count_artnr = count_artnr + 1

            if curr_oh < op_list.anzahl and curr_oh > 0:

                l_artikel = get_cache (L_artikel, {"artnr": [(eq, op_list.artnr)]})

                if count_artnr == 1:
                    msg_str = msg_str + chr_unicode(2) + translateExtended ("Wrong quantity: ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr_unicode(10) + translateExtended ("Inputted quantity =", lvcarea, "") + " " + to_string(op_list.anzahl) + translateExtended (" - Stock onhand =", lvcarea, "") + " " + to_string(curr_oh) + chr_unicode(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
                else:
                    msg_str = msg_str + chr_unicode(2) + translateExtended ("The same article has been found : ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr_unicode(10) + translateExtended ("Inputted quantity =", lvcarea, "") + " " + to_string(op_list.anzahl) + translateExtended (" - Stock onhand =", lvcarea, "") + " " + to_string(curr_oh) + chr_unicode(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
                its_ok = False

                return
            out_oh =  to_decimal(op_list.anzahl)
            curr_oh =  to_decimal(curr_oh) - to_decimal(out_oh)
            curr_artnr = op_list.artnr

    check_qty()

    return generate_output()