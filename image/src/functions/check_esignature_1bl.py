from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guestbook, Queasy

def check_esignature_1bl(case_type:int, user_init:str, docu_nr:str, flag_type:str):
    found_flag = False
    esign_list_list = []
    esign_print_list = []
    guestbook = queasy = None

    esign_list = esign_print = None

    esign_list_list, Esign_list = create_model("Esign_list", {"sign_nr":int, "sign_name":str, "sign_img":bytes, "sign_use_for":str, "sign_position":str, "sign_userinit":str, "sign_id":int, "sign_select":bool, "sign_pass":str, "sign_pr":bool, "sign_po":bool})
    esign_print_list, Esign_print = create_model("Esign_print", {"sign_nr":int, "sign_name":str, "sign_img":bytes, "sign_date":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal found_flag, esign_list_list, esign_print_list, guestbook, queasy


        nonlocal esign_list, esign_print
        nonlocal esign_list_list, esign_print_list
        return {"found_flag": found_flag, "esign-list": esign_list_list, "esign-print": esign_print_list}


    if case_type == 1:

        if flag_type.lower()  == "PR":

            guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr >= -271150) &  (Guestbook.gastnr <= -271080) &  (func.lower(Guestbook.userinit) == (user_init).lower()) &  (Guestbook.reserve_logic[0])).first()

            if guestbook:
                found_flag = True
                esign_list = Esign_list()
                esign_list_list.append(esign_list)

                esign_list.sign_nr = to_int(entry(0, guestbook.infostr, "|"))
                esign_list.sign_name = entry(1, guestbook.infostr, "|")
                esign_list.sign_img = guestbook.imagefile
                esign_list.sign_use_for = entry(2, guestbook.infostr, "|")
                esign_list.sign_position = entry(3, guestbook.infostr, "|")
                esign_list.sign_userinit = guestbook.userinit
                esign_list.sign_id = guestbook.gastnr
                esign_list.sign_pass = guestbook.reserve_char[0]
                esign_list.sign_pr = guestbook.reserve_logic[0]
                esign_list.sign_po = guestbook.reserve_logic[1]


            else:
                found_flag = False

        elif flag_type.lower()  == "PO":

            guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr >= -271150) &  (Guestbook.gastnr <= -271080) &  (func.lower(Guestbook.userinit) == (user_init).lower()) &  (Guestbook.reserve_logic[1])).first()

            if guestbook:
                found_flag = True
                esign_list = Esign_list()
                esign_list_list.append(esign_list)

                esign_list.sign_nr = to_int(entry(0, guestbook.infostr, "|"))
                esign_list.sign_name = entry(1, guestbook.infostr, "|")
                esign_list.sign_img = guestbook.imagefile
                esign_list.sign_use_for = entry(2, guestbook.infostr, "|")
                esign_list.sign_position = entry(3, guestbook.infostr, "|")
                esign_list.sign_userinit = guestbook.userinit
                esign_list.sign_id = guestbook.gastnr
                esign_list.sign_pass = guestbook.reserve_char[0]
                esign_list.sign_pr = guestbook.reserve_logic[0]
                esign_list.sign_po = guestbook.reserve_logic[1]


            else:
                found_flag = False

    elif case_type == 2:

        if flag_type.lower()  == "PR":

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 227) &  (func.lower(Queasy.char1) == (docu_nr).lower())).all():

                guestbook = db_session.query(Guestbook).filter(
                        (Guestbook.gastnr == queasy.number2) &  (Guestbook.reserve_logic[0])).first()

                if guestbook:
                    esign_print = Esign_print()
                    esign_print_list.append(esign_print)

                    esign_print.sign_nr = queasy.number1
                    esign_print.sign_name = entry(1, guestbook.infostr, "|")
                    esign_print.sign_img = guestbook.imagefile
                    esign_print.sign_date = entry(1, queasy.char3, "|")

        elif flag_type.lower()  == "PO":

            for queasy in db_session.query(Queasy).filter(
                    (Queasy.key == 245) &  (func.lower(Queasy.char1) == (docu_nr).lower())).all():

                guestbook = db_session.query(Guestbook).filter(
                        (Guestbook.gastnr == queasy.number2) &  (Guestbook.reserve_logic[1])).first()

                if guestbook:
                    esign_print = Esign_print()
                    esign_print_list.append(esign_print)

                    esign_print.sign_nr = queasy.number1
                    esign_print.sign_name = entry(1, guestbook.infostr, "|")
                    esign_print.sign_img = guestbook.imagefile
                    esign_print.sign_date = entry(1, queasy.char3, "|")

    return generate_output()