#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Printer

def rarticle_admin_bondruckernrbl(h_bondruckernr:int, h_bondrucker:int):
    flag = 0
    printer = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, printer
        nonlocal h_bondruckernr, h_bondrucker

        return {"flag": flag}


    printer = get_cache (Printer, {"nr": [(eq, h_bondruckernr)],"bondrucker": [(eq, True)]})

    if not printer and h_bondrucker != 0:
        flag = 1

    return generate_output()