from functions.additional_functions import *
import decimal
from models import Queasy

def outlet_shiftadmin_btn_delartbl(rec_id:int):
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        return {}


    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == rec_id)).first()

    queasy = db_session.query(Queasy).first()
    db_session.delete(queasy)

    return generate_output()