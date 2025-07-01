#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, Htparam, H_bill, Artikel, Waehrung, Exrate

def ts_restinv_round_billamountbl(pvilanguage:int, price_decimal:int, curr_dept:int, rec_id:int, rest_amount:Decimal, double_currency:bool, exchg_rate:Decimal, transdate:date, cancel_flag:bool, foreign_rate:bool):

    prepare_cache ([Htparam, H_bill, Artikel, Exrate])

    printed = ""
    billart = 0
    qty = 0
    description = ""
    price = to_decimal("0.0")
    fl_code = 0
    fl_code1 = 0
    amount_foreign = to_decimal("0.0")
    amount = to_decimal("0.0")
    msg_str = ""
    t_h_artikel_list = []
    lvcarea:string = "TS-restinv"
    gst_logic:bool = False
    h_artikel = htparam = h_bill = artikel = waehrung = exrate = None

    t_h_artikel = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal printed, billart, qty, description, price, fl_code, fl_code1, amount_foreign, amount, msg_str, t_h_artikel_list, lvcarea, gst_logic, h_artikel, htparam, h_bill, artikel, waehrung, exrate
        nonlocal pvilanguage, price_decimal, curr_dept, rec_id, rest_amount, double_currency, exchg_rate, transdate, cancel_flag, foreign_rate


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        return {"printed": printed, "billart": billart, "qty": qty, "description": description, "price": price, "fl_code": fl_code, "fl_code1": fl_code1, "amount_foreign": amount_foreign, "amount": amount, "msg_str": msg_str, "t-h-artikel": t_h_artikel_list}

    def round_billamount():

        nonlocal printed, billart, qty, description, price, fl_code, fl_code1, amount_foreign, amount, msg_str, t_h_artikel_list, lvcarea, gst_logic, h_artikel, htparam, h_bill, artikel, waehrung, exrate
        nonlocal pvilanguage, price_decimal, curr_dept, rec_id, double_currency, exchg_rate, transdate, cancel_flag, foreign_rate


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        rest_amount:Decimal = to_decimal("0.0")

        htparam = get_cache (Htparam, {"paramnr": [(eq, 738)]})

        if htparam.finteger == 0:

            return

        h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})

        if h_bill.flag == 1:

            return

        if gst_logic:
            rest_amount =  to_decimal("0")
            rest_amount = calc_round(h_bill.saldo)
            rest_amount =  to_decimal(rest_amount) - to_decimal(h_bill.saldo)
        else:
            rest_amount =  to_decimal(h_bill.saldo) - truncate(to_decimal(h_bill.saldo) , 0)

        if rest_amount == 0:

            return

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, curr_dept)]})

        if not artikel:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("F/O Article not found (Param 738):", lvcarea, "") + " " + to_string(htparam.finteger)

            return

        if artikel.artart != 0:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Rouding F/O Article type must be Revenue: ", lvcarea, "") + " " + to_string(htparam.finteger) + "-" + artikel.bezeich

            return

        h_artikel = get_cache (H_artikel, {"artnrfront": [(eq, artikel.artnr)],"departement": [(eq, curr_dept)]})

        if not h_artikel:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("POS rounding Article not found.", lvcarea, "")

            return
        t_h_artikel = T_h_artikel()
        t_h_artikel_list.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = h_artikel._recid

        if h_artikel.artart != 0:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("POS Rouding Article's type must be Revenue: ", lvcarea, "") + " " + to_string(htparam.finteger) + "-" + h_artikel.bezeich

            return
        printed = ""
        billart = h_artikel.artnr
        qty = 1
        description = h_artikel.bezeich

        if gst_logic:
            price =  to_decimal(rest_amount)
        else:

            if rest_amount > 0:

                if rest_amount < 0.5:
                    price =  - to_decimal(rest_amount)
                else:
                    price =  to_decimal("1") - to_decimal(rest_amount)
            else:

                if (- rest_amount) < 0.5:
                    price =  - to_decimal(rest_amount)
                else:
                    price =  - to_decimal((1) + to_decimal(rest_amount))
        fl_code = 1
        calculate_amount()


    def calculate_amount():

        nonlocal printed, billart, qty, description, price, fl_code, fl_code1, amount_foreign, amount, msg_str, t_h_artikel_list, lvcarea, gst_logic, h_artikel, htparam, h_bill, artikel, waehrung, exrate
        nonlocal pvilanguage, price_decimal, curr_dept, rec_id, rest_amount, double_currency, exchg_rate, transdate, cancel_flag, foreign_rate


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

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

                        w1 = db_session.query(W1).filter(
                                 (W1.waehrungsnr == artikel1.betriebsnr) & (W1.ankauf != 0)).first()

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
                    amount = to_decimal(round(amount , price_decimal))
            else:
                amount =  to_decimal(price) * to_decimal(qty)
                amount = to_decimal(round(amount , price_decimal))

        if (amount > 99999999) or (amount < -99999999):
            pass

        if amount < 0 and h_artikel.artart == 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 261)]})

            if htparam.flogical:
                fl_code1 = 1


    def calc_round(amount1:Decimal):

        nonlocal printed, billart, qty, description, price, fl_code, fl_code1, amount_foreign, amount, msg_str, t_h_artikel_list, lvcarea, gst_logic, h_artikel, htparam, h_bill, artikel, waehrung, exrate
        nonlocal pvilanguage, price_decimal, curr_dept, rec_id, rest_amount, double_currency, exchg_rate, transdate, cancel_flag, foreign_rate


        nonlocal t_h_artikel
        nonlocal t_h_artikel_list

        amount2 = to_decimal("0.0")

        def generate_inner_output():
            return (amount2)


        if amount1 - truncate(amount1, 1) <= 0.02:
            amount2 = to_decimal(round(amount1 , 1))

        elif (amount1 - truncate(amount1, 1) >= 0.02 and amount1 - truncate(amount1, 1) <= 0.05) or (amount1 - truncate(amount1, 1) == 0.06 or amount1 - truncate(amount1, 1) == 0.07):
            amount2 =  to_decimal(truncate(amount1 , 1)) + to_decimal(0.05)
        else:
            amount2 = to_decimal(round(amount1 , 1))

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 376)]})

    if htparam:

        if not htparam.flogical and entry(0, htparam.fchar, ";") == ("GST(MA)").lower() :
            gst_logic = True
    round_billamount()

    return generate_output()