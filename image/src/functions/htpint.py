from functions.additional_functions import *
import decimal
from models import Htparam

def htpint(htparamnum:int):
    htpint = 0
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpint, htparam


        return {"htpint": htpint}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == htparamnum)).first()

    if htparam:
        htpint = htparam.finteger

    return generate_output()