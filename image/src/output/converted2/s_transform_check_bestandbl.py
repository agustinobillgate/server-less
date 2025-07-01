#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_op, L_bestand, L_artikel, L_lager

op_list_list, Op_list = create_model_like(L_op, {"bezeich":string, "username":string})

def s_transform_check_bestandbl(op_list_list:[Op_list], pvilanguage:int):

    prepare_cache ([L_artikel, L_lager])

    its_ok = True
    msg_str = ""
    curr_store:string = ""
    lvcarea:string = "s-transform"
    l_op = l_bestand = l_artikel = l_lager = None

    op_list = b_bestand = None

    B_bestand = create_buffer("B_bestand",L_bestand)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, curr_store, lvcarea, l_op, l_bestand, l_artikel, l_lager
        nonlocal pvilanguage
        nonlocal b_bestand


        nonlocal op_list, b_bestand

        return {"its_ok": its_ok, "msg_str": msg_str}

    for op_list in query(op_list_list):

        l_bestand = get_cache (L_bestand, {"artnr": [(eq, op_list.artnr)],"lager_nr": [(eq, op_list.lager_nr)]})

        if not l_bestand:

            l_artikel = get_cache (L_artikel, {"artnr": [(eq, op_list.artnr)]})

            l_lager = get_cache (L_lager, {"lager_nr": [(eq, op_list.lager_nr)]})

            b_bestand = db_session.query(B_bestand).filter(
                     (B_bestand.artnr == op_list.artnr) & (B_bestand.lager_nr != 0)).first()

            if b_bestand:

                l_lager = get_cache (L_lager, {"lager_nr": [(eq, op_list.lager_nr)]})

                if l_lager:
                    curr_store = l_lager.bezeich
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Wrong Store: ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr_unicode(10) + translateExtended ("Inputted Store =", lvcarea, "") + " " + to_string(l_lager.bezeich) + translateExtended (" - Artikel Store =", lvcarea, "") + " " + to_string(curr_store) + chr_unicode(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
            its_ok = False

            return generate_output()

    return generate_output()