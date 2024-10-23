from functions.additional_functions import *
import decimal
from models import Queasy

def bqtrelig_admin_btn_delartbl(rec_id:int):
    err = 0
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, queasy
        nonlocal rec_id


        return {"err": err}


    queasy = db_session.query(Queasy).filter(
             (Queasy._recid == rec_id)).first()
    db_session.delete(queasy)
    pass

    return generate_output()