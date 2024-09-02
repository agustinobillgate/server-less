from functions.additional_functions import *
import decimal
from models import Waehrung, Artikel

def fo_invoice_check_pricebl(l_price:decimal, t_artnr:int, t_departement:int):
    waehrung = artikel = None

    w1 = None

    W1 = Waehrung

    db_session = local_storage.db_session

    def generate_output():
        nonlocal waehrung, artikel
        nonlocal w1


        nonlocal w1
        return {}


    artikel = db_session.query(Artikel).filter(
            (Artikel.artnr == t_artnr) &  (Artikel.departement == t_departement)).first()

    w1 = db_session.query(W1).filter(
            (W1.waehrungsnr == artikel.betriebsnr)).first()

    if w1:
        l_price = l_price * w1.ankauf / w1.einheit

    return generate_output()