from functions.additional_functions import *
import decimal
from models import Htparam

def htpchar(htparamnum:int):
    htpchar = ""
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpchar, htparam


        return {"htpchar": htpchar}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == htparamnum)).first()

    if htparam:
        htpchar = htparam.fchar

    return generate_output()