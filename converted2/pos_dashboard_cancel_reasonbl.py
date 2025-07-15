from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def pos_dashboard_cancel_reasonbl(od_cancel_list:[Od_cancel_list], user_init:str, cancel_str:str):
    cancel_id:str = ""
    queasy = None

    od_cancel_list = None

    od_cancel_list_list, Od_cancel_list = create_model("Od_cancel_list", {"nr":int, "table_nr":int, "order_nr":int, "bezeich":str, "qty":int, "sp_req":str, "confirm":bool, "remarks":str, "order_date":str, "art_nr":int, "posted":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cancel_id, queasy


        nonlocal od_cancel_list
        nonlocal od_cancel_list_list
        return {}


    cancel_id = user_init

    for od_cancel_list in query(od_cancel_list_list, filters=(lambda od_cancel_list :od_cancel_list.confirm == False and od_cancel_list.posted == False)):

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 225) &  (func.lower(Queasy.char1) == "orderbill_line") &  (Queasy.number2 == od_cancel_list.table_nr) &  (Queasy.number1 == od_cancel_list.order_nr) &  (Queasy.number3 == od_cancel_list.nr) &  (entry(2, Queasy.char2, "|Queasy.") == od_cancel_list.order_date) &  (Queasy.logi2 == False) &  (Queasy.logi3 == False)).first()

        if queasy:

            queasy = db_session.query(Queasy).first()

            if num_entries(queasy.char3) >= 8:
                queasy.char3 = queasy.char3 + "|" + cancel_str + "|" + to_string(get_current_time_in_seconds(), "HH:MM:SS") + "|" + cancel_id
            else:
                queasy.char3 = queasy.char3 + "|||" + cancel_str + "|" + to_string(get_current_time_in_seconds(), "HH:MM:SS") + "|" + cancel_id

            queasy = db_session.query(Queasy).first()


    return generate_output()