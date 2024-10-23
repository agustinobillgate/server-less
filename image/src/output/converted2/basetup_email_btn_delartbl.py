from functions.additional_functions import *
import decimal
from models import Queasy

def basetup_email_btn_delartbl(recid_queasy:int):
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal recid_queasy


        return {}


    queasy = db_session.query(Queasy).filter(
             (Queasy._recid == recid_queasy)).first()
    db_session.delete(queasy)
    pass

    return generate_output()