from functions.additional_functions import *
import decimal
from models import Queasy

def bookengine_admin_btn_deletebl(number1:int):
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal number1


        return {}


    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 159) & (Queasy.number1 == number1)).first()

    if queasy:
        db_session.delete(queasy)
        pass

    return generate_output()