from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung, Exrate

def nt_exrate():
    lvcarea:str = "nt-exrate"
    bill_date:date = None
    htparam = waehrung = exrate = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, bill_date, htparam, waehrung, exrate

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    for waehrung in db_session.query(Waehrung).order_by(Waehrung._recid).all():

        exrate = db_session.query(Exrate).filter(
                 (Exrate.datum == bill_date) & (Exrate.artnr == waehrung.waehrungsnr)).first()

        if not exrate:
            exrate = Exrate()
            db_session.add(exrate)

            exrate.artnr = waehrung.waehrungsnr
            exrate.datum = bill_date
            exrate.betrag =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

    return generate_output()