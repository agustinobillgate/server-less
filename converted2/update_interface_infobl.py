#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

def update_interface_infobl(usersession:string, body:string):

    prepare_cache ([Queasy])

    queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal usersession, body

        return {}


    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 999) & (Queasy.char1 == usersession) & (Queasy.logi1 == False)).order_by(Queasy._recid.desc()).first()

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 999
        queasy.char1 = usersession

    if body != "":

        if matches(body,r"*ifStart*"):
            queasy.logi1 = True
            queasy.date1 = get_current_date()
            queasy.number1 = get_current_time_in_seconds()
            queasy.char2 = body
        else:
            queasy.date1 = get_current_date()
            queasy.number1 = get_current_time_in_seconds()
            queasy.char2 = body
            queasy.logi1 = True

    return generate_output()