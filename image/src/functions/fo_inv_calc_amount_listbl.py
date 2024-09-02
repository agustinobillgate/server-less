from functions.additional_functions import *
import decimal
from datetime import date
from functions.fo_invoice_calculate_amountbl import fo_invoice_calculate_amountbl
from models import Exrate, Waehrung

def fo_inv_calc_amount_listbl(transdate:date, betriebsnr:int, artart:int, pricetab:bool, balance_foreign:decimal, double_currency:bool, balance:decimal, price:decimal, price_decimal:int, foreign_rate:bool, p_145:int, epreis:decimal, adrflag:bool, artgrp:int, qty:int, res_exrate:decimal, exchg_rate:decimal, zipreis:decimal):
    amount_foreign = 0
    amount = 0
    avrg_kurs = 0
    rate_defined = False
    msg_int = 0
    msg_str = ""
    i:int = 0
    n:int = 0
    exrate = waehrung = None

    t_artikel = t_exrate = t_waehrung = None

    t_artikel_list, T_artikel = create_model("T_artikel", {"artnr":int, "bezeich":str, "epreis":decimal, "departement":int, "artart":int, "activeflag":bool, "artgrp":int, "bezaendern":bool, "autosaldo":bool, "pricetab":bool, "betriebsnr":int, "resart":bool, "zwkum":int})
    t_exrate_list, T_exrate = create_model_like(Exrate)
    t_waehrung_list, T_waehrung = create_model_like(Waehrung)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount_foreign, amount, avrg_kurs, rate_defined, msg_int, msg_str, i, n, exrate, waehrung


        nonlocal t_artikel, t_exrate, t_waehrung
        nonlocal t_artikel_list, t_exrate_list, t_waehrung_list
        return {"amount_foreign": amount_foreign, "amount": amount, "avrg_kurs": avrg_kurs, "rate_defined": rate_defined, "msg_int": msg_int, "msg_str": msg_str}


    t_exrate_list, t_waehrung_list = get_output(fo_invoice_calculate_amountbl(transdate, betriebsnr))

    if (artart == 2 or artart == 4 or artart == 6 or artart == 7):

        if (pricetab and balance_foreign != 0 and double_currency):
            amount_foreign = price
            amount = round(price * balance / balance_foreign, price_decimal)

            return generate_output()

        elif (not pricetab and balance != 0 and double_currency):
            amount = price
            amount_foreign = round(price * balance_foreign / balance, 2)

            return generate_output()

        if foreign_rate or pricetab:

            if double_currency and balance_foreign != 0:
                avrg_kurs = balance / balance_foreign

            if pricetab and betriebsnr != 0:

                if transdate != None:

                    t_exrate = query(t_exrate_list, first=True)

                    if t_exrate:
                        rate_defined = True
                        avrg_kurs = t_exrate.betrag

                if not rate_defined:

                    t_waehrung = query(t_waehrung_list, filters=(lambda t_waehrung :t_waehrungsnr == betriebsnr and t_waehrung.ankauf != 0), first=True)

                    if t_waehrung:
                        avrg_kurs = t_waehrung.ankauf / t_waehrung.einheit
                    else:
                        avrg_kurs = exchg_rate
            else:
                avrg_kurs = exchg_rate
        else:
            avrg_kurs = exchg_rate

        if pricetab:
            amount_foreign = price * qty
            amount = price * avrg_kurs * qty
            amount = round(amount, price_decimal)
        else:
            amount = price * qty
            amount = round(amount, price_decimal)

            if balance != 0:
                amount_foreign = round(balance_foreign / balance * amount, 6)
            else:
                amount_foreign = round(amount / exchg_rate, 6)
    else:

        if double_currency:

            if artart == 9 and artgrp == 0 and adrflag:
                amount_foreign = price * qty / exchg_rate
                amount = price * qty
                amount = round(amount, price_decimal)
            else:
                amount_foreign = price * qty
                amount = price * exchg_rate * qty
                amount = round(amount, price_decimal)
        else:

            if artart == 9 and artgrp != 0:

                if pricetab:

                    t_waehrung = query(t_waehrung_list, filters=(lambda t_waehrung :t_waehrungsnr == betriebsnr and t_waehrung.ankauf != 0), first=True)

                    if t_waehrung:
                        avrg_kurs = t_waehrung.ankauf / t_waehrung.einheit
                    else:
                        avrg_kurs = exchg_rate
                    amount_foreign = price * qty
                    amount = amount_foreign * avrg_kurs
                else:
                    amount = price * qty
                    amount_foreign = round(amount / res_exrate, 6)
                amount = round(amount, price_decimal)

            elif artart == 9 and not adrflag and foreign_rate:
                amount = price * qty
                amount_foreign = zipreis * qty
            else:

                if pricetab:

                    t_waehrung = query(t_waehrung_list, filters=(lambda t_waehrung :t_waehrungsnr == betriebsnr and t_waehrung.ankauf != 0), first=True)

                    if t_waehrung:
                        avrg_kurs = t_waehrung.ankauf / t_waehrung.einheit
                    else:
                        avrg_kurs = exchg_rate
                    amount_foreign = price * qty
                    amount = amount_foreign * avrg_kurs
                else:
                    amount = price * qty
                    amount_foreign = round(amount / res_exrate, 6)
                amount = round(amount, price_decimal)

    if (artart == 0 or artart == 8) and epreis == 0 and double_currency:
        msg_int = 1

    elif (artart == 2 or artart == 7 or artart == 6) and double_currency:
        msg_int = 2

    if artart == 9 and artgrp == 0 and foreign_rate and price_decimal == 0:

        if p_145 != 0:
            n = 1
            for i in range(1,p_145 + 1) :
                n = n * 10
            amount = round(amount / n, 0) * n

    if qty < 0 and artart == 9 and artgrp == 0:
        msg_str = "1"

    elif qty > 1 and artart == 9 and artgrp == 0:
        msg_str = "2"

    return generate_output()