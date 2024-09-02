from functions.additional_functions import *
import decimal
from models import Katpreis

def rmcat_rate_btn_delbl(rec_id:int):
    katpreis = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal katpreis


        return {}


    katpreis = db_session.query(Katpreis).filter(
            (Katpreis._recid == rec_id)).first()

    katpreis = db_session.query(Katpreis).first()
    db_session.delete(katpreis)


    return generate_output()