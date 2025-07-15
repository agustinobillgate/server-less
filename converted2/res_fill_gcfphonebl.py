#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def res_fill_gcfphonebl(inp_gastnr:int, phone_str:string):

    prepare_cache ([Guest])

    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest
        nonlocal inp_gastnr, phone_str

        return {}


    guest = get_cache (Guest, {"gastnr": [(eq, inp_gastnr)]})

    if guest:
        pass
        guest.mobil_telefon = phone_str
        pass

    return generate_output()