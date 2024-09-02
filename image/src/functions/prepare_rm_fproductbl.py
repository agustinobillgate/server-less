from functions.additional_functions import *
import decimal
from datetime import date
from models import Waehrung, Htparam

def prepare_rm_fproductbl():
    bfast_art = 0
    lunch_art = 0
    dinner_art = 0
    lundin_art = 0
    local_curr = 0
    new_contrate = False
    curr_date = None
    double_currency = False
    exchg_rate = 0
    price_decimal = 0
    waehrung = htparam = None

    wrung = None

    Wrung = Waehrung

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bfast_art, lunch_art, dinner_art, lundin_art, local_curr, new_contrate, curr_date, double_currency, exchg_rate, price_decimal, waehrung, htparam
        nonlocal wrung


        nonlocal wrung
        return {"bfast_art": bfast_art, "lunch_art": lunch_art, "dinner_art": dinner_art, "lundin_art": lundin_art, "local_curr": local_curr, "new_contrate": new_contrate, "curr_date": curr_date, "double_currency": double_currency, "exchg_rate": exchg_rate, "price_decimal": price_decimal}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    curr_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 125)).first()
    bfast_art = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 227)).first()
    lunch_art = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 228)).first()
    dinner_art = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 229)).first()
    lundin_art = finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()

    wrung = db_session.query(Wrung).filter(
            (Wrung.wabkurz == htparam.fchar)).first()
    local_curr = wrung.waehrungsnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    double_currency = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit
    else:
        exchg_rate = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    return generate_output()