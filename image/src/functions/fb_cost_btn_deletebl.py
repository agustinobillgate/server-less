from functions.additional_functions import *
import decimal
from models import Queasy

def fb_cost_btn_deletebl(price_list_artnr:int):
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        return {}


    queasy = db_session.query(Queasy).filter(
            (Queasy.KEY == 142) &  (Queasy.number1 == price_list_artnr)).first()
    queasy.number1 = 0
    queasy.number2 = 0
    queasy.deci1 = 0
    queasy.deci2 = 0
    queasy.date1 = None
    queasy.date2 = None
    queasy.char2 = ""

    return generate_output()