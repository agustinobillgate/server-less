#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history

def confirm_signature_1bl(app_id:string, app_no:int, docu_nr:string, user_init:string, sign_id:int, confirmsign_flag:bool, flag_type:string):

    prepare_cache ([Bediener, Res_history])

    queasy = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy, bediener, res_history
        nonlocal app_id, app_no, docu_nr, user_init, sign_id, confirmsign_flag, flag_type

        return {}


    if confirmsign_flag :

        if flag_type.lower()  == ("PR").lower() :

            queasy = get_cache (Queasy, {"key": [(eq, 227)],"char1": [(eq, docu_nr)],"number1": [(eq, app_no)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 227
                queasy.char1 = docu_nr
                queasy.char2 = user_init
                queasy.char3 = app_id
                queasy.number1 = app_no
                queasy.number2 = sign_id

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Using E-Signature For PR: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
                res_history.action = "E-Signature"


                pass
                pass
                pass

            if queasy:
                queasy.char2 = user_init
                queasy.char3 = app_id
                queasy.number1 = app_no
                queasy.number2 = sign_id

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Change E-Signature For PR: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
                res_history.action = "E-Signature"


                pass
                pass
                pass

        if flag_type.lower()  == ("PO").lower() :

            queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, docu_nr)],"number1": [(eq, app_no)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 245
                queasy.char1 = docu_nr
                queasy.char2 = user_init
                queasy.char3 = app_id
                queasy.number1 = app_no
                queasy.number2 = sign_id

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Using E-Signature For PO: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
                res_history.action = "E-Signature"


                pass
                pass
                pass

            if queasy:
                queasy.char2 = user_init
                queasy.char3 = app_id
                queasy.number1 = app_no
                queasy.number2 = sign_id

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Change E-Signature For PO: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
                res_history.action = "E-Signature"


                pass
                pass
                pass

    elif confirmsign_flag == False:

        if flag_type.lower()  == ("PR").lower() :

            queasy = get_cache (Queasy, {"key": [(eq, 227)],"char1": [(eq, docu_nr)],"number1": [(eq, app_no)]})

            if queasy:
                db_session.delete(queasy)

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Cancel E-Signature For PR: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
                res_history.action = "E-Signature"


                pass
                pass
                pass

        if flag_type.lower()  == ("PO").lower() :

            queasy = get_cache (Queasy, {"key": [(eq, 245)],"char1": [(eq, docu_nr)],"number1": [(eq, app_no)]})

            if queasy:
                db_session.delete(queasy)

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.aenderung = "Cancel E-Signature For PO: " + docu_nr + "|Approve No: " + to_string(app_no) + "|" + app_id
                res_history.action = "E-Signature"


                pass
                pass
                pass

    return generate_output()