from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def pos_dashboard_cancel_orderbl(menu_list:[Menu_list], curr_dept:int, order_no:int, tischnr:int, session_param:str):
    mess_str = ""
    queasy = None

    menu_list = None

    menu_list_list, Menu_list = create_model("Menu_list", {"rec_id":int, "description":str, "qty":int, "price":decimal, "special_request":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_str, queasy


        nonlocal menu_list
        nonlocal menu_list_list
        return {"mess_str": mess_str}

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 225) &  (Queasy.number1 == curr_dept) &  (func.lower(Queasy.char1) == "orderbill") &  (Queasy.logi1) &  (Queasy.number3 == order_no) &  (func.lower(Queasy.char3) == (session_param).lower())).first()

    if queasy:
        queasy.logi3 = True
        mess_str = "Cancel Order Success!"
    else:
        mess_str = "No Orderbill Found!"

        return generate_output()