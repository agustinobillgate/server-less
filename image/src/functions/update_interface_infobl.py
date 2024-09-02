from functions.additional_functions import *
import decimal
import re
from models import Queasy

def update_interface_infobl(usersession:str, body:str):
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        return {}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 999) &  (Queasy.char1 == usersession) &  (Queasy.logi1 == False)).first()

    if not queasy:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 999
        queasy.char1 = usersession

    if body != "":

        if re.match(".*ifStart.*",body):
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