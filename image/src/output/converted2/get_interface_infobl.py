from functions.additional_functions import *
import decimal
from models import Queasy

def get_interface_infobl(usersession:str):
    data = None
    finishflag = None
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal data, finishflag, queasy
        nonlocal usersession


        return {"data": data, "finishflag": finishflag}


    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 999) & (Queasy.char1 == usersession)).order_by(Queasy._recid.desc()).first()

    if queasy:
        finishflag = queasy.logi1
        data = queasy.char2

        if finishflag:
            db_session.delete(queasy)

    return generate_output()