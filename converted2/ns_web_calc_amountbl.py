# using conversion tools version: 1.0.0.117
"""_yusufwijasena_04/12/2025

        remark: - fix error cannot calculate amount when price == None
                - added validation when price == None
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.read_exratebl import read_exratebl
from functions.read_waehrungbl import read_waehrungbl
from models import Exrate, Waehrung


def ns_web_calc_amountbl(t_artikel_artart: int, foreign_rate: bool, t_artikel_pricetab: bool, balance_foreign: Decimal, transdate: date, t_artikel_betriebsnr: int, double_currency: bool, price_decimal: int, price: Decimal, balance: Decimal, exchg_rate: Decimal, qty: int, t_artikel_artgrp: int):
    amount_foreign = to_decimal("0.0")
    amount = to_decimal("0.0")
    avrg_kurs: Decimal = 1
    i: int = 0
    n: int = 0
    rate_defined: bool = False
    exrate = waehrung = None

    t_exrate = w1 = None

    t_exrate_data, T_exrate = create_model_like(Exrate)
    w1_data, W1 = create_model_like(Waehrung)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount_foreign, amount, avrg_kurs, i, n, rate_defined, exrate, waehrung
        nonlocal t_artikel_artart, foreign_rate, t_artikel_pricetab, balance_foreign, transdate, t_artikel_betriebsnr, double_currency, price_decimal, price, balance, exchg_rate, qty, t_artikel_artgrp
        nonlocal t_exrate, w1
        nonlocal t_exrate_data, w1_data

        return {
            "amount_foreign": amount_foreign,
            "amount": amount
        }

    if (t_artikel_artart == 2 or t_artikel_artart == 4 or t_artikel_artart == 6 or t_artikel_artart == 7):

        if (t_artikel_pricetab and balance_foreign != 0 and double_currency):
            amount_foreign = to_decimal(price)
            amount = to_decimal(
                round(price * balance / balance_foreign, price_decimal))

            return generate_output()

        elif (not t_artikel_pricetab and balance != 0 and double_currency):
            amount = to_decimal(price)
            amount_foreign = to_decimal(
                round(price * balance_foreign / balance, 2))

            return generate_output()

        if foreign_rate or t_artikel_pricetab:
            if double_currency and balance_foreign != 0:
                avrg_kurs = to_decimal(balance) / to_decimal(balance_foreign)

            if t_artikel_pricetab and t_artikel_betriebsnr != 0:

                if transdate != None:
                    t_exrate_data = get_output(read_exratebl(
                        1, t_artikel_betriebsnr, transdate))

                    t_exrate = query(t_exrate_data, first=True)

                    if t_exrate:
                        rate_defined = True
                        avrg_kurs = to_decimal(t_exrate.betrag)

                if not rate_defined:
                    w1_data = get_output(read_waehrungbl(
                        7, t_artikel_betriebsnr, None))

                    w1 = query(w1_data, first=True)

                    if w1:
                        avrg_kurs = to_decimal(
                            w1.ankauf) / to_decimal(w1.einheit)
                    else:
                        avrg_kurs = to_decimal(exchg_rate)
            else:
                avrg_kurs = to_decimal(exchg_rate)
        else:
            avrg_kurs = to_decimal(exchg_rate)

        if t_artikel_pricetab:
            amount_foreign = to_decimal(price) * to_decimal(qty)
            amount = to_decimal(price) * \
                to_decimal(avrg_kurs) * to_decimal(qty)
            amount = to_decimal(round(amount, price_decimal))
        else:
            if price:
                amount = to_decimal(price) * qty
            else:
                amount = to_decimal(0) * qty
            amount_foreign = to_decimal(round(amount / avrg_kurs, 6))
    else:
        if double_currency:
            amount_foreign = to_decimal(price) * to_decimal(qty)
            amount = to_decimal(price) * \
                to_decimal(exchg_rate) * to_decimal(qty)
            amount = to_decimal(round(amount, price_decimal))
        else:
            if t_artikel_pricetab:
                w1_data = get_output(read_waehrungbl(
                    7, t_artikel_betriebsnr, None))

                w1 = query(w1_data, first=True)

                if w1:
                    avrg_kurs = to_decimal(w1.ankauf) / to_decimal(w1.einheit)
                else:
                    avrg_kurs = to_decimal(exchg_rate)
                amount_foreign = to_decimal(price) * to_decimal(qty)
                amount = to_decimal(amount_foreign) * to_decimal(avrg_kurs)
            else:
                amount = to_decimal(price) * to_decimal(qty)
                amount_foreign = to_decimal(round(amount / exchg_rate, 6))
            amount = to_decimal(round(amount, price_decimal))

    return generate_output()
