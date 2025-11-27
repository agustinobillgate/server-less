#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd 24/7/2025
# gitlab: 772
# Rd, 27/11/2025, with_for_update added
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Queasy
from sqlalchemy import func

def rsvpurpose_admin_btn_delbl(pvilanguage:int, number1:int):
    msg_str = ""
    success_flag = False
    search_str:string = "segm_pur"
    lvcarea:string = "rsvpurpose-admin"
    res_line = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, search_str, lvcarea, res_line, queasy
        nonlocal pvilanguage, number1

        return {"msg_str": msg_str, "success_flag": success_flag}

    search_str = "segm_pur" + to_string(number1) + ";"

    # Rd, 24/7/2025
    # res_line = db_session.query(Res_line).filter(
    #          (Res_line.active_flag <= 1) & (get_index(Res_line.zimmer_wunsch, search_str) > 0)).first()
    sql_query = text("""
           SELECT *
            FROM res_line
            WHERE active_flag <= 1
            AND res_line.zimmer_wunsch ILIKE :search_str
            LIMIT 1;
        """)
    res_line = db_session.execute(sql_query, {"search_str": search_str}).fetchone()

    if res_line:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Reservation exists, deleting not possible.", lvcarea, "")
    else:

        # queasy = get_cache (Queasy, {"key": [(eq, 143)],"number1": [(eq, number1)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 143) &
                 (Queasy.number1 == number1)).with_for_update().first()

        if queasy:
            db_session.delete(queasy)
            success_flag = True

    return generate_output()