from functions.additional_functions import *
import decimal
from models import L_op, L_bestand, L_artikel, L_lager

def s_transform_check_bestandbl(op_list:[Op_list], pvilanguage:int):
    its_ok = False
    msg_str = ""
    curr_store:str = ""
    lvcarea:str = "s_transform"
    l_op = l_bestand = l_artikel = l_lager = None

    op_list = b_bestand = None

    op_list_list, Op_list = create_model_like(L_op, {"bezeich":str, "username":str})

    B_bestand = L_bestand

    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, msg_str, curr_store, lvcarea, l_op, l_bestand, l_artikel, l_lager
        nonlocal b_bestand


        nonlocal op_list, b_bestand
        nonlocal op_list_list
        return {"its_ok": its_ok, "msg_str": msg_str}

    for op_list in query(op_list_list):

        l_bestand = db_session.query(L_bestand).filter(
                (L_bestand.artnr == op_list.artnr) &  (L_bestand.lager_nr == op_list.lager_nr)).first()

        if not l_bestand:

            l_artikel = db_session.query(L_artikel).filter(
                    (L_artikel.artnr == op_list.artnr)).first()

            l_lager = db_session.query(L_lager).filter(
                    (L_lager.lager_nr == op_list.lager_nr)).first()

            b_bestand = db_session.query(B_bestand).filter(
                    (B_bestand.artnr == op_list.artnr) &  (B_bestand.lager_nr != 0)).first()

            if b_bestand:

                l_lager = db_session.query(L_lager).filter(
                        (L_lager.lager_nr == op_list.lager_nr)).first()

                if l_lager:
                    curr_store = l_lager.bezeich
            msg_str = msg_str + chr(2) + translateExtended ("Wrong Store: ", lvcarea, "") + to_string(l_artikel.artnr) + " - " + l_artikel.bezeich + chr(10) + translateExtended ("Inputted Store  == ", lvcarea, "") + " " + to_string(l_lager.bezeich) + translateExtended (" - Artikel Store  == ", lvcarea, "") + " " + to_string(curr_store) + chr(10) + translateExtended ("POSTING NOT POSSIBLE", lvcarea, "")
            its_ok = False

            return generate_output()