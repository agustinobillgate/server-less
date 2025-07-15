#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam

def prepare_ap_listbl():

    prepare_cache ([Htparam])

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger
    init_display()

    return generate_output()