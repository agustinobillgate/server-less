from functions.additional_functions import *
import decimal
from models import Guestbud

def guestbud1_btn_delbl(rec_id:int):
    guestbud = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestbud


        return {}


    guestbud = db_session.query(Guestbud).filter(
            (Guestbud._recid == rec_id)).first()

    guestbud = db_session.query(Guestbud).first()
    db_session.delete(guestbud)

    return generate_output()