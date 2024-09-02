from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy, Bediener, Res_history

def confirm_signature_1bl(app_id:str, app_no:int, docu_nr:str, user_init:str, sign_id:int, confirmsign_flag:bool, flag_type:str):
    queasy = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy, bediener, res_history


        return {}


    if confirmsign_flag :

        if flag_type.lower()  == "PR":

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 227) &  (func.lower(Queasy.char1) == (docu_nr).lower()) &  (Queasy.number1 == app_no)).first()

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 227
                queasy.char1 = docu_nr
                queasy.char2 = user_init
                queasy.char3 = app_id
                queasy.number1 = app_no
                queasy.number2 = sign_id

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Using E_Signature For PR: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
                res_history.action = "E_Signature"

                bediener = db_session.query(Bediener).first()

                res_history = db_session.query(Res_history).first()


            if queasy:
                queasy.char2 = user_init
                queasy.char3 = app_id
                queasy.number1 = app_no
                queasy.number2 = sign_id

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Change E_Signature For PR: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
                res_history.action = "E_Signature"

                bediener = db_session.query(Bediener).first()

                res_history = db_session.query(Res_history).first()


    if flag_type.lower()  == "PO":

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 245) &  (func.lower(Queasy.char1) == (docu_nr).lower()) &  (Queasy.number1 == app_no)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 245
            queasy.char1 = docu_nr
            queasy.char2 = user_init
            queasy.char3 = app_id
            queasy.number1 = app_no
            queasy.number2 = sign_id

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Using E_Signature For PO: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
            res_history.action = "E_Signature"

            bediener = db_session.query(Bediener).first()

            res_history = db_session.query(Res_history).first()


        if queasy:
            queasy.char2 = user_init
            queasy.char3 = app_id
            queasy.number1 = app_no
            queasy.number2 = sign_id

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Change E_Signature For PO: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
            res_history.action = "E_Signature"

            bediener = db_session.query(Bediener).first()

            res_history = db_session.query(Res_history).first()


    elif confirmsign_flag == False:

        if flag_type.lower()  == "PR":

            queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 227) &  (func.lower(Queasy.char1) == (docu_nr).lower()) &  (Queasy.number1 == app_no)).first()

            if queasy:
                db_session.delete(queasy)

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Cancel E_Signature For PR: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
                res_history.action = "E_Signature"

                bediener = db_session.query(Bediener).first()

                res_history = db_session.query(Res_history).first()


    if flag_type.lower()  == "PO":

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 245) &  (func.lower(Queasy.char1) == (docu_nr).lower()) &  (Queasy.number1 == app_no)).first()

        if queasy:
            db_session.delete(queasy)

            bediener = db_session.query(Bediener).filter(
                    (func.lower(Bediener.userinit) == (user_init).lower())).first()
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Cancel E_Signature For PO: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
            res_history.action = "E_Signature"

            bediener = db_session.query(Bediener).first()

            res_history = db_session.query(Res_history).first()


    return generate_output()