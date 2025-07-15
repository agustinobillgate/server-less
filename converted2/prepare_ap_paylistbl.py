#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.htpint import htpint

def prepare_ap_paylistbl():
    price_decimal = 0

    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal

        return {"price_decimal": price_decimal}

    price_decimal = get_output(htpint(491))

    return generate_output()