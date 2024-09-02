from functions.additional_functions import *
import decimal
from models import Htparam

def htpdec(htparamnum:int):
    htpdecimal = 0
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpdecimal, htparam


        return {"htpdecimal": htpdecimal}

    htpdecimal = 0

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == htparamnum)).first()

    if htparam:
        htpdecimal = htparam.fdecimal

    return generate_output()