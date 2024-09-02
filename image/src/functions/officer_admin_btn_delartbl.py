from functions.additional_functions import *
import decimal
from models import Queasy, Nation

def officer_admin_btn_delartbl(rec_id:int):
    err_code = 0
    queasy = nation = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_code, queasy, nation


        return {"err_code": err_code}


    queasy = db_session.query(Queasy).filter(
            (Queasy._recid == rec_id)).first()

    nation = db_session.query(Nation).filter(
            (Nation.untergruppe == queasy.number3)).first()

    if nation:
        err_code = 1

        return generate_output()

    queasy = db_session.query(Queasy).first()
    db_session.delete(queasy)

    return generate_output()