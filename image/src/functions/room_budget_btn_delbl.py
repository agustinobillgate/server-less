from functions.additional_functions import *
import decimal
from models import Rmbudget

def room_budget_btn_delbl(rec_id:int):
    rmbudget = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmbudget


        return {}


    rmbudget = db_session.query(Rmbudget).filter(
            (Rmbudget._recid == rec_id)).first()

    rmbudget = db_session.query(Rmbudget).first()
    db_session.delete(rmbudget)


    return generate_output()