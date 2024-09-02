from functions.additional_functions import *
import decimal
from models import Eg_maintain

def eg_maincalendardel_reqactbl(smaintain_maintainnr:int):
    flag = 0
    eg_maintain = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, eg_maintain


        return {"flag": flag}


    eg_maintain = db_session.query(Eg_maintain).filter(
            (Eg_maintain.maintainnr == smaintain_maintainnr)).first()

    if eg_maintain:
        eg_maintain.delete_flag = False
        eg_maintain.cancel_date = None
        flag = 1

    return generate_output()