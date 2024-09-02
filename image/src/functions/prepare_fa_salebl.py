from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Fa_artikel, Mathis

def prepare_fa_salebl(nr:int):
    last_close = None
    datum = None
    qty = 0
    amt = 0
    mathis_name = ""
    mathis_asset = ""
    fa_artikel_anzahl = 0
    htparam = fa_artikel = mathis = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal last_close, datum, qty, amt, mathis_name, mathis_asset, fa_artikel_anzahl, htparam, fa_artikel, mathis


        return {"last_close": last_close, "datum": datum, "qty": qty, "amt": amt, "mathis_name": mathis_name, "mathis_asset": mathis_asset, "fa_artikel_anzahl": fa_artikel_anzahl}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 558)).first()
    last_close = fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 372)).first()
    datum = htparam.fdate

    fa_artikel = db_session.query(Fa_artikel).filter(
            (Fa_artikel.nr == nr)).first()
    qty = fa_artikel.anzahl
    amt = fa_artikel.book_wert
    fa_artikel_anzahl = fa_artikel.anzahl

    mathis = db_session.query(Mathis).filter(
            (Mathis.nr == fa_artikel.nr)).first()
    mathis_name = mathis.name
    mathis_asset = mathis.asset

    return generate_output()