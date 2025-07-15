#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def select_ordertakerbl():

    prepare_cache ([Queasy])

    queasy_list_data = []
    queasy = None

    queasy_list = None

    queasy_list_data, Queasy_list = create_model("Queasy_list", {"number1":int, "char1":string, "char2":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy_list_data, queasy


        nonlocal queasy_list
        nonlocal queasy_list_data

        return {"queasy-list": queasy_list_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 10)).order_by(Queasy.char2).all():
        queasy_list = Queasy_list()
        queasy_list_data.append(queasy_list)

        queasy_list.number1 = queasy.number1
        queasy_list.char1 = queasy.char1
        queasy_list.char2 = queasy.char2

    return generate_output()