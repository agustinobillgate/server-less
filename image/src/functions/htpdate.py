from functions.additional_functions import *
import decimal
from models import Htparam

def htpdate(htparamnum:int):
    htpdate = None
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpdate, htparam


        return {"htpdate": htpdate}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == htparamnum)).first()

    if htparam:
        htpdate = htparam.fdate

    return generate_output()