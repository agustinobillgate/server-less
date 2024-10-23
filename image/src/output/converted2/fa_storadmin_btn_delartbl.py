from functions.additional_functions import *
import decimal
from models import Fa_lager

def fa_storadmin_btn_delartbl(rec_id:int):
    fa_lager = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_lager
        nonlocal rec_id


        return {}


    fa_lager = db_session.query(Fa_lager).filter(
             (Fa_lager._recid == rec_id)).first()

    if fa_lager:
        db_session.delete(fa_lager)
        pass

    return generate_output()