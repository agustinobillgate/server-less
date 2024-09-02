from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Waehrung

def prepare_hums_costbl():
    to_date = None
    from_date = None
    double_currency = False
    foreign_nr = 0
    exchg_rate = 0
    htparam = waehrung = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal to_date, from_date, double_currency, foreign_nr, exchg_rate, htparam, waehrung


        return {"to_date": to_date, "from_date": from_date, "double_currency": double_currency, "foreign_nr": foreign_nr, "exchg_rate": exchg_rate}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    to_date = fdate
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    if htparam.fchar != "":

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr
            exchg_rate = waehrung.ankauf / waehrung.einheit

    return generate_output()