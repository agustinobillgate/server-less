from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Queasy

def pos_dashboard_check_neworderbl(session_prm:str):
    found_new_order = False
    queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal found_new_order, queasy


        return {"found_new_order": found_new_order}


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 225) &  (func.lower(Queasy.char1) == "orderbill") &  (func.lower(Queasy.char3) == (session_prm).lower()) &  (Queasy.logi1) &  (Queasy.logi2 == False) &  (Queasy.logi3 == False)).first()

    if queasy:
        found_new_order = True

        return generate_output()