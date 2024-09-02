from functions.additional_functions import *
import decimal
from models import Queasy

def select_ordertakerbl():
    queasy_list_list = []
    queasy = None

    queasy_list = None

    queasy_list_list, Queasy_list = create_model("Queasy_list", {"number1":int, "char1":str, "char2":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy_list_list, queasy


        nonlocal queasy_list
        nonlocal queasy_list_list
        return {"queasy-list": queasy_list_list}

    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 10)).all():
        queasy_list = Queasy_list()
        queasy_list_list.append(queasy_list)

        queasy_list.number1 = queasy.number1
        queasy_list.char1 = queasy.char1
        queasy_list.char2 = queasy.char2

    return generate_output()