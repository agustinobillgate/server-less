from functions.additional_functions import *
import decimal
from models import Htparam

def htpdate(htparamnum:int):
    htpdate = get_current_date()
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htpdate, htparam
        nonlocal htparamnum

        return {"htpdate": htpdate}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == htparamnum)).first()

    if htparam:
        htpdate = htparam.fdate

    return generate_output()

    return generate_output()