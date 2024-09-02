from functions.additional_functions import *
import decimal
from datetime import date
from functions.read_exratebl import read_exratebl
from functions.read_waehrungbl import read_waehrungbl
from models import Exrate, Waehrung

def ns_web_calc_amountbl(t_artikel_artart:int, foreign_rate:bool, t_artikel_pricetab:bool, balance_foreign:decimal, transdate:date, t_artikel_betriebsnr:int, double_currency:bool, price_decimal:int, price:decimal, balance:decimal, exchg_rate:decimal, qty:int, t_artikel_artgrp:int):
    amount_foreign = 0
    amount = 0
    avrg_kurs:decimal = 1
    i:int = 0
    n:int = 0
    rate_defined:bool = False
    exrate = waehrung = None

    t_exrate = w1 = None

    t_exrate_list, T_exrate = create_model_like(Exrate)
    w1_list, W1 = create_model_like(Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount_foreign, amount, avrg_kurs, i, n, rate_defined, exrate, waehrung


        nonlocal t_exrate, w1
        nonlocal t_exrate_list, w1_list
        return {"amount_foreign": amount_foreign, "amount": amount}


    if (t_artikel_artart == 2 or t_artikel_artart == 4 or t_artikel_artart == 6 or t_artikel_artart == 7):

        if (t_artikel_pricetab and balance_foreign != 0 and double_currency):
            amount_foreign = price
            amount = round(price * balance / balance_foreign, price_decimal)

            return generate_output()

        elif (not t_artikel_pricetab and balance != 0 and double_currency):
            amount = price
            amount_foreign = round(price * balance_foreign / balance, 2)

            return generate_output()

        if foreign_rate or t_artikel_pricetab:

            if double_currency and balance_foreign != 0:
                avrg_kurs = balance / balance_foreign

            if t_artikel_pricetab and t_artikel_betriebsnr != 0:

                if transdate != None:
                    t_exrate_list = get_output(read_exratebl(1, t_artikel_betriebsnr, transdate))

                    t_exrate = query(t_exrate_list, first=True)

                    if t_exrate:
                        rate_defined = True
                        avrg_kurs = t_exrate.betrag

                if not rate_defined:
                    w1_list = get_output(read_waehrungbl(7, t_artikel_betriebsnr, None))

                    w1 = query(w1_list, first=True)

                    if w1:
                        avrg_kurs = w1.ankauf / w1.einheit
                    else:
                        avrg_kurs = exchg_rate
            else:
                avrg_kurs = exchg_rate
        else:
            avrg_kurs = exchg_rate

        if t_artikel_pricetab:
            amount_foreign = price * qty
            amount = price * avrg_kurs * qty
            amount = round(amount, price_decimal)
        else:
            amount = price * qty
            amount = round(amount, price_decimal)
            amount_foreign = round(amount / avrg_kurs, 6)
    else:

        if double_currency:
            amount_foreign = price * qty
            amount = price * exchg_rate * qty
            amount = round(amount, price_decimal)
        else:

            if t_artikel_pricetab:
                w1_list = get_output(read_waehrungbl(7, t_artikel_betriebsnr, None))

                w1 = query(w1_list, first=True)

                if w1:
                    avrg_kurs = w1.ankauf / w1.einheit
                else:
                    avrg_kurs = exchg_rate
                amount_foreign = price * qty
                amount = amount_foreign * avrg_kurs
            else:
                amount = price * qty
                amount_foreign = round(amount / exchg_rate, 6)
            amount = round(amount, price_decimal)

    return generate_output()