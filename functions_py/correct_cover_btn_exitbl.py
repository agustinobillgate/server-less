#using conversion tools version: 1.0.0.117

# =============================================
# Rulita, 28-11-2025
# - Added with_for_update all query 
# =============================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_umsatz

def correct_cover_btn_exitbl(datum:date, dept:int, pax:int, fpax:int, bpax:int):

    prepare_cache ([H_umsatz])

    h_umsatz = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_umsatz
        nonlocal datum, dept, pax, fpax, bpax

        return {}


    # h_umsatz = get_cache (H_umsatz, {"datum": [(eq, datum)],"departement": [(eq, dept)],"betriebsnr": [(eq, dept)]})

    if h_umsatz:
        # pass
        h_umsatz.anzahl = pax
        h_umsatz.betrag =  to_decimal(fpax)
        h_umsatz.nettobetrag =  to_decimal(bpax)

        db_session.refresh(h_umsatz, with_for_update=True)
        # pass

    return generate_output()
