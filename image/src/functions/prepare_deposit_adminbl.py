from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from models import Htparam, Artikel, Waehrung

def prepare_deposit_adminbl():
    fdate = None
    bill_date = None
    long_digit = False
    price_decimal = 0
    depo_foreign = False
    depo_curr = 0
    foreign_curr = 0
    p_60 = 0
    htparam = artikel = waehrung = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fdate, bill_date, long_digit, price_decimal, depo_foreign, depo_curr, foreign_curr, p_60, htparam, artikel, waehrung


        return {"fdate": fdate, "bill_date": bill_date, "long_digit": long_digit, "price_decimal": price_decimal, "depo_foreign": depo_foreign, "depo_curr": depo_curr, "foreign_curr": foreign_curr, "p_60": p_60}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    fdate = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    bill_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 120)).first()

    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()
    depo_foreign = artikel.pricetab
    depo_curr = artikel.betriebsnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()
    foreign_curr = waehrungsnr
    p_60 = get_output(htpint(60))

    return generate_output()