from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guestbook, Bediener, Res_history

def esign_setup_1bl(case_type:int, user_init:str, esign_list:[Esign_list]):
    booknr:int = 0
    guestbook = bediener = res_history = None

    esign_list = gbook = None

    esign_list_list, Esign_list = create_model("Esign_list", {"sign_nr":int, "sign_name":str, "sign_img":bytes, "sign_use_for":str, "sign_position":str, "sign_userinit":str, "sign_id":int, "sign_select":bool, "sign_pass":str, "sign_pr":bool, "sign_po":bool})

    Gbook = Guestbook

    db_session = local_storage.db_session

    def generate_output():
        nonlocal booknr, guestbook, bediener, res_history
        nonlocal gbook


        nonlocal esign_list, gbook
        nonlocal esign_list_list
        return {}

    if case_type == 0:

        for guestbook in db_session.query(Guestbook).filter(
                (Guestbook.gastnr >= -271150) &  (Guestbook.gastnr <= -271080)).all():
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

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "VIEWING DATA E_Signature"
        res_history.action = "E_Signature Setup"

        bediener = db_session.query(Bediener).first()

        res_history = db_session.query(Res_history).first()

    elif case_type == 1:

        for esign_list in query(esign_list_list):

            guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr == esign_list.sign_id)).first()

            if guestbook:

                guestbook = db_session.query(Guestbook).first()
                guestbook.infostr = to_string(esign_list.sign_nr) + "|" +\
                        esign_list.sign_name + "|" +\
                        esign_list.sign_use_for + "|" +\
                        esign_list.sign_position
                guestbook.imagefile = esign_list.sign_img
                guestbook.userinit = esign_list.sign_userinit
                guestbook.reserve_char[0] = esign_list.sign_pass
                guestbook.reserve_logic[0] = esign_list.sign_pr
                guestbook.reserve_logic[1] = esign_list.sign_po

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "MODIFY E_Sign: ID Name " + esign_list.sign_name
                res_history.action = "E_Signature Setup"

                guestbook = db_session.query(Guestbook).first()

                bediener = db_session.query(Bediener).first()

                res_history = db_session.query(Res_history).first()

            else:

                gbook = db_session.query(Gbook).filter(
                        (Gbook.gastnr >= -271150) &  (Gbook.gastnr <= -271080)).first()

                if gbook:

                    for guestbook in db_session.query(Guestbook).filter(
                            (Guestbook.gastnr >= -271150) &  (Guestbook.gastnr <= -271080)).all():
                        booknr = guestbook.gastnr - 1
                        break
                else:
                    booknr = - 271080

                guestbook = Guestbook()
                db_session.add(guestbook)

                guestbook.gastnr = booknr
                guestbook.reserve_int[0] = esign_list.sign_nr
                guestbook.infostr = to_string(esign_list.sign_nr) + "|" +\
                        esign_list.sign_name + "|" +\
                        esign_list.sign_use_for + "|" +\
                        esign_list.sign_position
                guestbook.imagefile = esign_list.sign_img
                guestbook.userinit = esign_list.sign_userinit
                guestbook.reserve_char[0] = esign_list.sign_pass
                guestbook.reserve_logic[0] = esign_list.sign_pr
                guestbook.reserve_logic[1] = esign_list.sign_po
                esign_list.sign_id = booknr

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "ADD E_Sign: ID Name " + esign_list.sign_name
                res_history.action = "E_Signature Setup"

                guestbook = db_session.query(Guestbook).first()

                bediener = db_session.query(Bediener).first()

                res_history = db_session.query(Res_history).first()


    elif case_type == 2:

        esign_list = query(esign_list_list, filters=(lambda esign_list :esign_list.sign_select), first=True)

        if esign_list:

            guestbook = db_session.query(Guestbook).filter(
                    (Guestbook.gastnr == esign_list.sign_id)).first()

            if guestbook:

                guestbook = db_session.query(Guestbook).first()
                db_session.delete(guestbook)

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "DELETE E_Sign: ID Name " + esign_list.sign_name
                res_history.action = "E_Signature Setup"

                bediener = db_session.query(Bediener).first()

                res_history = db_session.query(Res_history).first()


    return generate_output()