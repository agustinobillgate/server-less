#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Uebertrag

def gl_outstandbl(date1:date, int1:int, deci1:Decimal):

    prepare_cache ([Uebertrag])

    uebertrag = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal uebertrag
        nonlocal date1, int1, deci1

        return {}


    uebertrag = get_cache (Uebertrag, {"datum": [(eq, date1)],"betriebsnr": [(eq, int1)]})

    if uebertrag:
        uebertrag.betrag =  to_decimal(deci1)


        pass

    return generate_output()