from functions.additional_functions import *
import decimal
from models import Salesbud

def salesbud_btn_delbl(rec_id:int):
    salesbud = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal salesbud


        return {}


    salesbud = db_session.query(Salesbud).filter(
            (Salesbud._recid == rec_id)).first()
    db_session.delete(salesbud)


    return generate_output()