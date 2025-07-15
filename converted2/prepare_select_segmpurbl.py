#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def prepare_select_segmpurbl():

    prepare_cache ([Queasy])

    pur_list_data = []
    queasy = None

    pur_list = None

    pur_list_data, Pur_list = create_model("Pur_list", {"number1":int, "char1":string, "char3":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal pur_list_data, queasy


        nonlocal pur_list
        nonlocal pur_list_data

        return {"pur-list": pur_list_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 143)).order_by(Queasy.char1).all():
        pur_list = Pur_list()
        pur_list_data.append(pur_list)

        pur_list.number1 = queasy.number1
        pur_list.char1 = queasy.char1
        pur_list.char3 = queasy.char3

    return generate_output()