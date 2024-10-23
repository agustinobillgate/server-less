from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

q245_list, Q245 = create_model("Q245", {"key":int, "docu_nr":str, "user_init":str, "app_id":str, "app_no":int, "sign_id":int})

def chg_po_btn_stop_signbl(docu_nr:str, q245_list:[Q245]):
    queasy = None

    q245 = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal docu_nr, q245_list


        nonlocal q245
        nonlocal q245_list
        return {}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 245) & (func.lower(Queasy.char1) == (docu_nr).lower())).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    for q245 in query(q245_list):

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == q245.key) & (Queasy.char1 == q245.docu_nr) & (Queasy.number1 == q245.app_no)).first()

        if not queasy:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = q245.key
            queasy.char1 = q245.docu_nr
            queasy.char2 = q245.user_init
            queasy.char3 = q245.app_id
            queasy.number1 = q245.app_no
            queasy.number2 = q245.sign_id

        if queasy:
            queasy.char2 = q245.user_init
            queasy.char3 = q245.app_id
            queasy.number1 = q245.app_no
            queasy.number2 = q245.sign_id

    return generate_output()