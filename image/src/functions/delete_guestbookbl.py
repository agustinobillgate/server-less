from functions.additional_functions import *
import decimal
from models import Guestbook

def delete_guestbookbl(gastno:int):
    guestbook = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal guestbook


        return {}


    guestbook = db_session.query(Guestbook).filter(
            (Guestbook.gastnr == gastno)).first()

    if guestbook:
        db_session.delete(guestbook)


    return generate_output()