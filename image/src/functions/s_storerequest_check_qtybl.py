from functions.additional_functions import *
import decimal
from models import L_op, L_bestand, L_artikel

def s_storerequest_check_qtybl(pvilanguage:int, op_list:[Op_list]):
    its_ok = False
    msg_str = ""
    lvcarea:str = "s_storerequest"
    l_op = l_bestand = l_artikel = None

    op_list = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str, "onhand":decimal, "acct_bez":str, "masseinheit":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, lvcarea, l_op, l_bestand, l_artikel


        nonlocal op_list
        nonlocal op_list_list
        return {"its_ok": its_ok, "msg_str": msg_str}

    def check_qty():

        nonlocal its_ok, msg_str, lvcarea, l_op, l_bestand, l_artikel


        nonlocal op_list
        nonlocal op_list_list

        curr_oh:decimal = 0

        for op_list in query(op_list_list):
            curr_oh = 0

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.artnr == op_list.artnr) &  (L_bestand.lager_nr == op_list.lager_nr)).first()

            if l_bestand:
                curr_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang

            if curr_oh < op_list.anzahl:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == op_list.artnr)).first()
                msg_str = msg_str + chr(2) + translateExtended ("Wrong quantity: ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr(10) + translateExtended ("Inputted quantity  == ", lvcarea, "") + " " + to_string(op_list.anzahl) + translateExtended (" - Stock onhand  == ", lvcarea, "") + " " + to_string(curr_oh) + chr(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
                its_ok = False

                return


    check_qty()

    return generate_output()