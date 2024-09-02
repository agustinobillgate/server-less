from functions.additional_functions import *
import decimal
from datetime import date
from models import H_artikel, Htparam, H_bill, Artikel, Waehrung, Exrate

def ts_restinv_round_billamountbl(pvilanguage:int, price_decimal:int, curr_dept:int, rec_id:int, rest_amount:decimal, double_currency:bool, exchg_rate:decimal, transdate:date, cancel_flag:bool, foreign_rate:bool):
    printed = ""
    billart = 0
    qty = 0
    description = ""
    price = 0
    fl_code = 0
    fl_code1 = 0
    amount_foreign = 0
    amount = 0
    msg_str = ""
    t_h_artikel_list = []
    lvcarea:str = "TS_restinv"
    gst_logic:bool = False
    h_artikel = htparam = h_bill = artikel = waehrung = exrate = None

    t_h_artikel = artikel1 = w1 = None

    t_h_artikel_list, T_h_artikel = create_model_like(H_artikel, {"rec_id":int})

    Artikel1 = Artikel
    W1 = Waehrung

    db_session = local_storage.db_session

    def generate_output():
        nonlocal printed, billart, qty, description, price, fl_code, fl_code1, amount_foreign, amount, msg_str, t_h_artikel_list, lvcarea, gst_logic, h_artikel, htparam, h_bill, artikel, waehrung, exrate
        nonlocal artikel1, w1


        nonlocal t_h_artikel, artikel1, w1
        nonlocal t_h_artikel_list
        return {"printed": printed, "billart": billart, "qty": qty, "description": description, "price": price, "fl_code": fl_code, "fl_code1": fl_code1, "amount_foreign": amount_foreign, "amount": amount, "msg_str": msg_str, "t-h-artikel": t_h_artikel_list}

    def round_billamount():

        nonlocal printed, billart, qty, description, price, fl_code, fl_code1, amount_foreign, amount, msg_str, t_h_artikel_list, lvcarea, gst_logic, h_artikel, htparam, h_bill, artikel, waehrung, exrate
        nonlocal artikel1, w1


        nonlocal t_h_artikel, artikel1, w1
        nonlocal t_h_artikel_list

        rest_amount:decimal = 0

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 738)).first()

        if htparam.finteger == 0:

            return

        h_bill = db_session.query(H_bill).filter(
                (H_bill._recid == rec_id)).first()

        if h_bill.flag == 1:

            return

        if gst_logic:
            rest_amount = 0
            rest_amount = calc_round(h_bill.saldo)
            rest_amount = rest_amount - h_bill.saldo
        else:
            rest_amount = h_bill.saldo - truncate(h_bill.saldo, 0)

        if rest_amount == 0:

            return

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == htparam.finteger) &  (Artikel.departement == curr_dept)).first()

        if not artikel:
            msg_str = msg_str + chr(2) + translateExtended ("F/O Article not found (Param 738):", lvcarea, "") + " " + to_string(htparam.finteger)

            return

        if artikel.artart != 0:
            msg_str = msg_str + chr(2) + translateExtended ("Rouding F/O Article type must be Revenue: ", lvcarea, "") + " " + to_string(htparam.finteger) + "-" + artikel.bezeich

            return

        h_artikel = db_session.query(H_artikel).filter(
                (H_artikel.artnrfront == artikel.artnr) &  (H_artikel.departement == curr_dept)).first()

        if not h_artikel:
            msg_str = msg_str + chr(2) + translateExtended ("POS rounding Article not found.", lvcarea, "")

            return
        t_h_artikel = T_h_artikel()
        t_h_artikel_list.append(t_h_artikel)

        buffer_copy(h_artikel, t_h_artikel)
        t_h_artikel.rec_id = h_artikel._recid

        if h_artikel.artart != 0:
            msg_str = msg_str + chr(2) + translateExtended ("POS Rouding Article's type must be Revenue: ", lvcarea, "") + " " + to_string(htparam.finteger) + "-" + h_artikel.bezeich

            return
        printed = ""
        billart = h_artikel.artnr
        qty = 1
        description = h_artikel.bezeich

        if gst_logic:
            price = rest_amount
        else:

            if rest_amount > 0:

                if rest_amount < 0.5:
                    price = - rest_amount
                else:
                    price = 1 - rest_amount
            else:

                if (- rest_amount) < 0.5:
                    price = - rest_amount
                else:
                    price = - (1 + rest_amount)
        fl_code = 1
        calculate_amount()

    def calculate_amount():

        nonlocal printed, billart, qty, description, price, fl_code, fl_code1, amount_foreign, amount, msg_str, t_h_artikel_list, lvcarea, gst_logic, h_artikel, htparam, h_bill, artikel, waehrung, exrate
        nonlocal artikel1, w1


        nonlocal t_h_artikel, artikel1, w1
        nonlocal t_h_artikel_list

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
            pass

        if amount < 0 and h_artikel.artart == 0:

            htparam = db_session.query(Htparam).filter(
                    (Htparam.paramnr == 261)).first()

            if htparam.flogical:
                fl_code1 = 1

    def calc_round(amount1:decimal):

        nonlocal printed, billart, qty, description, price, fl_code, fl_code1, amount_foreign, amount, msg_str, t_h_artikel_list, lvcarea, gst_logic, h_artikel, htparam, h_bill, artikel, waehrung, exrate
        nonlocal artikel1, w1


        nonlocal t_h_artikel, artikel1, w1
        nonlocal t_h_artikel_list

        amount2 = 0

        def generate_inner_output():
            return amount2

        if amount1 - truncate(amount1, 1) <= 0.02:
            amount2 = round(amount1, 1)

        elif (amount1 - truncate(amount1, 1) >= 0.02 and amount1 - truncate(amount1, 1) <= 0.05) or (amount1 - truncate(amount1, 1) == 0.06 or amount1 - truncate(amount1, 1) == 0.07):
            amount2 = truncate(amount1, 1) + 0.05
        else:
            amount2 = round(amount1, 1)


        return generate_inner_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 376)).first()

    if htparam:

        if not htparam.flogic and entry(0, htparam.fchar, ";") == "GST(MA)":
            gst_logic = True
    ound_billamount()

    return generate_output()