#using conversion tools version: 1.0.0.117

# ============================
# Rulita, 21-10-2025 
# Issue : New compile program
# ============================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Waehrung, Exrate

def nt_exrate():

    prepare_cache ([Htparam, Waehrung, Exrate])

    lvcarea:string = "nt-exrate"
    bill_date:date = None
    htparam = waehrung = exrate = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, bill_date, htparam, waehrung, exrate

        return {}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate

    for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():

        exrate = get_cache (Exrate, {"datum": [(eq, bill_date)],"artnr": [(eq, waehrung.waehrungsnr)]})

        if not exrate:
            exrate = Exrate()
            db_session.add(exrate)

            exrate.artnr = waehrung.waehrungsnr
            exrate.datum = bill_date
            exrate.betrag =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    return generate_output()