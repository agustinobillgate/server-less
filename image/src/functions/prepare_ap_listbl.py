from functions.additional_functions import *
import decimal
from models import Htparam

def prepare_ap_listbl():
    price_decimal = 0
    comments = ""
    htparam = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, comments, htparam


        return {"price_decimal": price_decimal, "comments": comments}

    def init_display():

        nonlocal price_decimal, comments, htparam

        if l_kredit:
            comments = l_kredit.bemerk
        else:
            comments = ""


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger
    init_display()

    return generate_output()