from functions.additional_functions import *
import decimal
from models import Waehrung, Artikel

def fo_invoice_return_qtybl(t_artnr:int, balance:decimal):
    exrate = 0
    price = 0
    msg = 0
    waehrung = artikel = None

    w1 = None

    W1 = Waehrung

    db_session = local_storage.db_session

    def generate_output():
        nonlocal exrate, price, msg, waehrung, artikel
        nonlocal w1


        nonlocal w1
        return {"exrate": exrate, "price": price, "msg": msg}


    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == t_artnr)).first()

    w1 = db_session.query(W1).filter(
            (W1.waehrungsnr == artikel.betriebsnr)).first()

    if w1:
        exrate = w1.ankauf / w1.einheit
    else:
        msg = 1
    price = - balance / exrate

    return generate_output()