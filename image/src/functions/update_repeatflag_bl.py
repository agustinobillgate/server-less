from functions.additional_functions import *
import decimal
from models import Queasy

def update_repeatflag_bl():
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        return {}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 167)).first()

    if queasy:

        queasy = db_session.query(Queasy).first()
        queasy.date1 = get_current_date()
        queasy.logi1 = True

    else:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 167
        queasy.date1 = get_current_date()
        queasy.logi1 = True

    return generate_output()