from functions.additional_functions import *
import decimal
from functions.htpint import htpint

def prepare_ap_paylistbl():
    price_decimal = 0


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal


        return {"price_decimal": price_decimal}

    price_decimal = get_output(htpint(491))

    return generate_output()