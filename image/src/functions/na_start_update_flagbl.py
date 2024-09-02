from functions.additional_functions import *
import decimal
from models import Htparam

def na_start_update_flagbl(htparam_recid:int):
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal htparam


        return {}


    htparam = db_session.query(Htparam).filter(
                (Htparam._recid == htparam_recid)).first()
    htparam.flogical = False


    return generate_output()