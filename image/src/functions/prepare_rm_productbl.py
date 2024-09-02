from functions.additional_functions import *
import decimal
from models import Htparam, Waehrung

def prepare_rm_productbl():
    price_decimal = 0
    foreign_nr = 0
    f_log = False
    htparam = waehrung = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal price_decimal, foreign_nr, f_log, htparam, waehrung


        return {"price_decimal": price_decimal, "foreign_nr": foreign_nr, "f_log": f_log}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    if htparam.fchar != "":

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            foreign_nr = waehrungsnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 143)).first()
    f_log = htparam.flogical

    return generate_output()