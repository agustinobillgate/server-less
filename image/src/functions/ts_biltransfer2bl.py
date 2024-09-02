from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def ts_biltransfer2bl(mc_str:str):
    do_it = False
    t_queasy_list = []
    queasy = None

    t_queasy = None

    t_queasy_list, T_queasy = create_model("T_queasy", {"char3":str, "char1":str, "number3":int, "deci3":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal do_it, t_queasy_list, queasy


        nonlocal t_queasy
        nonlocal t_queasy_list
        return {"do_it": do_it, "t-queasy": t_queasy_list}

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 105) &  (Queasy.number2 == 0) &  (Queasy.deci2 == 0) &  (func.lower(Queasy.char2) == (mc_str).lower()) &  (Queasy.logi2 == False)).first()
    do_it = None != queasy

    if queasy:
        t_queasy = T_queasy()
        t_queasy_list.append(t_queasy)

        t_queasy.char3 = queasy.char3
        t_queasy.char1 = queasy.char1
        t_queasy.number3 = queasy.number3
        t_queasy.deci3 = queasy.deci3

    return generate_output()