#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

q245_data, Q245 = create_model("Q245", {"key":int, "docu_nr":string, "user_init":string, "app_id":string, "app_no":int, "sign_id":int})

def chg_po_btn_stop_signbl(docu_nr:string, q245_data:[Q245]):
    queasy = None

    q245 = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal docu_nr, q245_data


        nonlocal q245

        return {}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 245) & (Queasy.char1 == (docu_nr).lower())).order_by(Queasy._recid).all():
        db_session.delete(queasy)

    for q245 in query(q245_data):

        queasy = get_cache (Queasy, {"key": [(eq, q245.key)],"char1": [(eq, q245.docu_nr)],"number1": [(eq, q245.app_no)]})

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