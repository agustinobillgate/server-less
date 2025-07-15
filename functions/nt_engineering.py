from functions.additional_functions import *
import decimal
from functions.nt_egstat import nt_egstat
from models import Htparam

def nt_engineering():
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 319)).first()

    if htparam.paramgruppe != 99 or htparam.flogical == False:

        return generate_output()
    else:
        get_output(nt_egstat())

    return generate_output()