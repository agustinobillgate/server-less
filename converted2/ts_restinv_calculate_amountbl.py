#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, Artikel, Waehrung, Exrate, Htparam

def ts_restinv_calculate_amountbl(rec_id:int, double_currency:bool, price:Decimal, qty:int, exchg_rate:Decimal, price_decimal:int, transdate:date, cancel_flag:bool, foreign_rate:bool):

    prepare_cache ([H_artikel, Artikel, Waehrung, Exrate])

    amount_foreign = to_decimal("0.0")
    amount = to_decimal("0.0")
    fl_code = 0
    fl_code1 = 0
    h_artikel = artikel = waehrung = exrate = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount_foreign, amount, fl_code, fl_code1, h_artikel, artikel, waehrung, exrate, htparam
        nonlocal rec_id, double_currency, price, qty, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate

        return {"price": price, "amount_foreign": amount_foreign, "amount": amount, "fl_code": fl_code, "fl_code1": fl_code1}

    def calculate_amount():

        nonlocal amount_foreign, amount, fl_code, fl_code1, h_artikel, artikel, waehrung, exrate, htparam
        nonlocal rec_id, double_currency, price, qty, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate

        avrg_kurs:Decimal = 1
        rate_defined:bool = False
        answer:bool = False
        artikel1 = None
        w1 = None
        Artikel1 =  create_buffer("Artikel1",Artikel)
        W1 =  create_buffer("W1",Waehrung)

        if double_currency:
            amount_foreign =  to_decimal(price) * to_decimal(qty)
            amount =  to_decimal(price) * to_decimal(exchg_rate) * to_decimal(qty)
            amount = to_decimal(round(amount , price_decimal))


        else:

            if h_artikel.artart == 0:

                artikel1 = get_cache (Artikel, {"artnr": [(eq, h_artikel.artnrfront)],"departement": [(eq, h_artikel.departement)]})

                if artikel1 and artikel1.pricetab and artikel1.betriebsnr != 0:

                    if transdate != None:

                        exrate = get_cache (Exrate, {"artnr": [(eq, artikel1.betriebsnr)],"datum": [(eq, transdate)]})

                        if exrate:
                            rate_defined = True
                            avrg_kurs =  to_decimal(exrate.betrag)

                    if not rate_defined:

                        w1 = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel1.betriebsnr)],"ankauf": [(ne, 0)]})

                        if w1:
                            avrg_kurs =  to_decimal(w1.ankauf) / to_decimal(w1.einheit)
                        else:
                            avrg_kurs =  to_decimal(exchg_rate)
                    else:
                        avrg_kurs =  to_decimal(exchg_rate)
                else:
                    avrg_kurs =  to_decimal(exchg_rate)

                if artikel1.pricetab and not cancel_flag:
                    amount_foreign =  to_decimal(price) * to_decimal(qty)
                    price =  to_decimal(price) * to_decimal(avrg_kurs)
                    amount =  to_decimal(price) * to_decimal(qty)
                    amount = to_decimal(round(amount , price_decimal))
                else:
                    amount =  to_decimal(price) * to_decimal(qty)

                    if foreign_rate:
                        amount_foreign = to_decimal(round(amount / exchg_rate , 2))
            else:
                amount =  to_decimal(price) * to_decimal(qty)
                amount = to_decimal(round(amount , price_decimal))

        if (amount > 99999999) or (amount < -99999999):
            fl_code = 1

        if amount < 0 and h_artikel.artart == 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 261)]})

            if htparam.flogical:
                fl_code1 = 1

    h_artikel = get_cache (H_artikel, {"_recid": [(eq, rec_id)]})
    calculate_amount()

    return generate_output()