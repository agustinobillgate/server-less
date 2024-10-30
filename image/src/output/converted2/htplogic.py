from functions.additional_functions import *
import decimal
from models import Htparam

def htplogic(htparamnum:int):
    htplogic = None
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htplogic, htparam
        nonlocal htparamnum

        return {"htplogic": htplogic}

    htplogic = None

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == htparamnum)).first()

    if htparam:
        htplogic = htparam.flogical

    return generate_output()

    return generate_output()