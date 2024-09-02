from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Htparam

def prepare_get_license_cashlessbl():
    cashless_license = False
    cashless_minsaldo = 0
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cashless_license, cashless_minsaldo, htparam


        return {"cashless_license": cashless_license, "cashless_minsaldo": cashless_minsaldo}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1022) &  (func.lower(Htparam.bezeich) != "not used") &  (Htparam.flogical)).first()

    if htparam:
        cashless_license = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 586)).first()

    if htparam:
        cashless_minsaldo = htparam.fdecimal

    return generate_output()