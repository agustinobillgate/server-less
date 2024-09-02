from functions.additional_functions import *
import decimal
from models import L_op, L_bestand, L_artikel

def s_stockout_check_qtybl(op_list:[Op_list], pvilanguage:int):
    msg_str = ""
    its_ok = False
    lvcarea:str = "s_stockout"
    l_op = l_bestand = l_artikel = None

    op_list = None

    op_list_list, Op_list = create_model_like(L_op, {"fibu":str, "a_bezeich":str, "a_lief_einheit":decimal, "a_traubensort":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, its_ok, lvcarea, l_op, l_bestand, l_artikel


        nonlocal op_list
        nonlocal op_list_list
        return {"msg_str": msg_str, "its_ok": its_ok}

    def check_qty():

        nonlocal msg_str, its_ok, lvcarea, l_op, l_bestand, l_artikel


        nonlocal op_list
        nonlocal op_list_list

        curr_oh:decimal = 0
        out_oh:decimal = 0
        curr_artnr:int = 0
        count_artnr:int = 0

        for op_list in query(op_list_list):

            l_bestand = db_session.query(L_bestand).filter(
                    (L_bestand.artnr == op_list.artnr) &  (L_bestand.lager_nr == op_list.lager_nr)).first()

            if curr_artnr == 0 or (curr_artnr != op_list.artnr):
                curr_oh = l_bestand.anz_anf_best + l_bestand.anz_eingang - l_bestand.anz_ausgang
                count_artnr = 0


            count_artnr = count_artnr + 1

            if curr_oh < op_list.anzahl:

                l_artikel = db_session.query(L_artikel).filter(
                        (L_artikel.artnr == op_list.artnr)).first()

                if count_artnr == 1:
                    msg_str = msg_str + chr(2) + translateExtended ("Wrong quantity: ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr(10) + translateExtended ("Inputted quantity  == ", lvcarea, "") + " " + to_string(op_list.anzahl) + translateExtended (" - Stock onhand  == ", lvcarea, "") + " " + to_string(curr_oh) + chr(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
                else:
                    msg_str = msg_str + chr(2) + translateExtended ("The same article has been found : ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr(10) + translateExtended ("Inputted quantity  == ", lvcarea, "") + " " + to_string(op_list.anzahl) + translateExtended (" - Stock onhand  == ", lvcarea, "") + " " + to_string(curr_oh) + chr(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
                its_ok = False

                return
            out_oh = op_list.anzahl
            curr_oh = curr_oh - out_oh
            curr_artnr = op_list.artnr


    check_qty()

    return generate_output()