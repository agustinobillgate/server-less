from functions.additional_functions import *
import decimal
from models import L_op, L_bestand, L_artikel

def s_transform_check_qtybl(op_list:[Op_list], pvilanguage:int):
    its_ok = False
    msg_str = ""
    curr_oh:decimal = 0
    lvcarea:str = "s_transform"
    l_op = l_bestand = l_artikel = None

    op_list = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, curr_oh, lvcarea, l_op, l_bestand, l_artikel


        nonlocal op_list
        nonlocal op_list_list
        return {"its_ok": its_ok, "msg_str": msg_str}

    for op_list in query(op_list_list):

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == op_list.artnr) &  (L_bestand.lager_nr == op_list.lager_nr)).first()
        curr_oh = anz_anf_best + anz_eingang - anz_ausgang

        if curr_oh < op_list.anzahl:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == op_list.artnr)).first()
            msg_str = msg_str + chr(2) + translateExtended ("Wrong quantity: ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr(10) + translateExtended ("Inputted quantity  == ", lvcarea, "") + " " + to_string(op_list.anzahl) + translateExtended (" - Stock onhand  == ", lvcarea, "") + " " + to_string(curr_oh) + chr(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
            its_ok = False

            return generate_output()