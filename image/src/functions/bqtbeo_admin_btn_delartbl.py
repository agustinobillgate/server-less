from functions.additional_functions import *
import decimal
from models import Queasy

def bqtbeo_admin_btn_delartbl(recid_queasy:int):
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        return {}


    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == recid_queasy)).first()
    db_session.delete(queasy)


    return generate_output()