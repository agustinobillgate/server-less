from functions.additional_functions import *
import decimal
from models import Queasy

def prepare_select_segmpurbl():
    pur_list_list = []
    queasy = None

    pur_list = None

    pur_list_list, Pur_list = create_model("Pur_list", {"number1":int, "char1":str, "char3":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal pur_list_list, queasy


        nonlocal pur_list
        nonlocal pur_list_list
        return {"pur-list": pur_list_list}

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 143)).all():
        pur_list = Pur_list()
        pur_list_list.append(pur_list)

        pur_list.number1 = queasy.number1
        pur_list.char1 = queasy.char1
        pur_list.char3 = queasy.char3

    return generate_output()