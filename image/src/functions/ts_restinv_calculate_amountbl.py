from functions.additional_functions import *
import decimal
from datetime import date
from models import H_artikel, Artikel, Waehrung, Exrate, Htparam

def ts_restinv_calculate_amountbl(rec_id:int, double_currency:bool, price:decimal, qty:int, exchg_rate:decimal, price_decimal:int, transdate:date, cancel_flag:bool, foreign_rate:bool):
    amount_foreign = 0
    amount = 0
    fl_code = 0
    fl_code1 = 0
    h_artikel = artikel = waehrung = exrate = htparam = None

    artikel1 = w1 = None

    Artikel1 = Artikel
    W1 = Waehrung

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount_foreign, amount, fl_code, fl_code1, h_artikel, artikel, waehrung, exrate, htparam
        nonlocal artikel1, w1


        nonlocal artikel1, w1
        return {"amount_foreign": amount_foreign, "amount": amount, "fl_code": fl_code, "fl_code1": fl_code1}

    def calculate_amount():

        nonlocal amount_foreign, amount, fl_code, fl_code1, h_artikel, artikel, waehrung, exrate, htparam
        nonlocal artikel1, w1


        nonlocal artikel1, w1

        avrg_kurs:decimal = 1
        rate_defined:bool = False
        answer:bool = False
        Artikel1 = Artikel
        W1 = Waehrung

        if double_currency:
            amount_foreign = price * qty
            amount = price * exchg_rate * qty
            amount = round(amount, price_decimal)


        else:

            if h_artikel.artart == 0:

                artikel1 = db_session.query(Artikel1).filter(
                        (Artikel1.artnr == h_artikel.artnrfront) &  (Artikel1.departement == h_artikel.departement)).first()

                if artikel1 and artikel1.pricetab and artikel1.betriebsnr != 0:

                    if transdate != None:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.artnr == artikel1.betriebsnr) &  (Exrate.datum == transdate)).first()

                        if exrate:
                            rate_defined = True
                            avrg_kurs = exrate.betrag

                    if not rate_defined:

                        w1 = db_session.query(W1).filter(
                                (W1.waehrungsnr == artikel1.betriebsnr) &  (W1.ankauf != 0)).first()

                        if w1:
                            avrg_kurs = w1.ankauf / w1.einheit
                        else:
                            avrg_kurs = exchg_rate
                    else:
                        avrg_kurs = exchg_rate
                else:
                    avrg_kurs = exchg_rate

                if artikel1.pricetab and not cancel_flag:
                    amount_foreign = price * qty
                    price = price * avrg_kurs
                    amount = price * qty
                    amount = round(amount, price_decimal)
                else:
                    amount = price * qty

                    if foreign_rate:
                        amount_foreign = round(amount / exchg_rate, 2)
                    amount = round(amount, price_decimal)
            else:
                amount = price * qty
                amount = round(amount, price_decimal)

        if (amount > 99999999) or (amount < -99999999):
            fl_code = 1

        if amount < 0 and h_artikel.artart == 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 261)).first()

            if htparam.flogical:
                fl_code1 = 1


    h_artikel = db_session.query(H_artikel).filter(
            (H_artikel._recid == rec_id)).first()
    calculate_amount()

    return generate_output()