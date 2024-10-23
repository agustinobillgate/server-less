from functions.additional_functions import *
import decimal
from models import Queasy, Bediener

def bqtcat_admin_btn_delartbl(rec_id:int):
    err = 0
    queasy = bediener = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err, queasy, bediener
        nonlocal rec_id


        return {"err": err}


    queasy = db_session.query(Queasy).filter(
             (Queasy._recid == rec_id)).first()

    bediener = db_session.query(Bediener).filter(
             (Bediener.user_group == int (queasy.char1)) & (Bediener.flag == 0)).first()

    if bediener:
        err = 1
    else:
        db_session.delete(queasy)
        pass

    return generate_output()