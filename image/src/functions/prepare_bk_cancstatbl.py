from functions.additional_functions import *
import decimal
from models import Htparam

def prepare_bk_cancstatbl():
    p_417 = ""
    p_547 = 0
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_417, p_547, htparam


        return {"p_417": p_417, "p_547": p_547}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 417)).first()
    p_417 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 547)).first()
    p_547 = htparam.finteger

    return generate_output()