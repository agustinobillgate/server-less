#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import H_artikel, Artikel, Waehrung, H_bill_line, Exrate, Htparam

input_list_data, Input_list = create_model("Input_list", {"rec_id":int, "double_currency":bool, "price":Decimal, "qty":int, "exchg_rate":Decimal, "price_decimal":int, "transdate":date, "cancel_flag":bool, "foreign_rate":bool, "void_recid":int})

def ts_restinv_calculate_amount_webbl(input_list_data:[Input_list]):

    prepare_cache ([H_artikel, H_bill_line, Exrate])

    output_list_data = []
    rec_id:int = 0
    double_currency:bool = False
    price:Decimal = to_decimal("0.0")
    qty:int = 0
    exchg_rate:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    transdate:date = None
    cancel_flag:bool = False
    foreign_rate:bool = False
    void_recid:int = 0
    amount_foreign:Decimal = to_decimal("0.0")
    amount:Decimal = to_decimal("0.0")
    fl_code:int = 0
    fl_code1:int = 0
    h_artikel = artikel = waehrung = h_bill_line = exrate = htparam = None

    input_list = output_list = None

    output_list_data, Output_list = create_model("Output_list", {"price":Decimal, "amount_foreign":Decimal, "amount":Decimal, "fl_code":int, "fl_code1":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, rec_id, double_currency, price, qty, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate, void_recid, amount_foreign, amount, fl_code, fl_code1, h_artikel, artikel, waehrung, h_bill_line, exrate, htparam


        nonlocal input_list, output_list
        nonlocal output_list_data

        return {"output-list": output_list_data}

    def calculate_amount():

        nonlocal output_list_data, rec_id, double_currency, price, qty, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate, void_recid, amount_foreign, amount, fl_code, fl_code1, h_artikel, artikel, waehrung, h_bill_line, exrate, htparam


        nonlocal input_list, output_list
        nonlocal output_list_data

        avrg_kurs:Decimal = 1
        rate_defined:bool = False
        answer:bool = False
        artikel1 = None
        w1 = None
        Artikel1 =  create_buffer("Artikel1",Artikel)
        W1 =  create_buffer("W1",Waehrung)

        if double_currency:

            if h_artikel.epreis1 == 0:

                h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, void_recid)]})

                if h_bill_line:
                    amount_foreign =  - to_decimal(h_bill_line.nettobetrag)
                    amount =  - to_decimal(h_bill_line.nettobetrag) * to_decimal(exchg_rate)
                    amount = to_decimal(round(amount , price_decimal))
                    price =  to_decimal(h_bill_line.nettobetrag) / to_decimal(qty) * -1
                else:
                    amount_foreign =  to_decimal(price) * to_decimal(qty)
                    amount =  to_decimal(price) * to_decimal(exchg_rate) * to_decimal(qty)
                    amount = to_decimal(round(amount , price_decimal))


            else:
                amount_foreign =  to_decimal(price) * to_decimal(qty)
                amount =  to_decimal(price) * to_decimal(exchg_rate) * to_decimal(qty)
                amount = to_decimal(round(amount , price_decimal))


        else:

            if h_artikel.artart == 0:

                artikel1 = db_session.query(Artikel1).filter(
                         (Artikel1.artnr == h_artikel.artnrfront) & (Artikel1.departement == h_artikel.departement)).first()

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

                    if h_artikel.epreis1 == 0:

                        h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, void_recid)]})

                        if h_bill_line:
                            price =  to_decimal(h_bill_line.nettobetrag) / to_decimal(qty) * -1
                            amount_foreign =  to_decimal(price) * to_decimal(qty)
                            price =  to_decimal(price) * to_decimal(avrg_kurs)
                            amount =  to_decimal(price) * to_decimal(qty)
                            amount = to_decimal(round(amount , price_decimal))
                        else:
                            amount_foreign =  to_decimal(price) * to_decimal(qty)
                            price =  to_decimal(price) * to_decimal(avrg_kurs)
                            amount =  to_decimal(price) * to_decimal(qty)
                            amount = to_decimal(round(amount , price_decimal))
                    else:
                        amount_foreign =  to_decimal(price) * to_decimal(qty)
                        price =  to_decimal(price) * to_decimal(avrg_kurs)
                        amount =  to_decimal(price) * to_decimal(qty)
                        amount = to_decimal(round(amount , price_decimal))
                else:

                    if h_artikel.epreis1 == 0:

                        h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, void_recid)]})

                        if h_bill_line:
                            amount =  - to_decimal(h_bill_line.nettobetrag)
                            amount = to_decimal(round(amount , price_decimal))

                            if foreign_rate:
                                amount_foreign = to_decimal(round(amount / exchg_rate , 2))
                            price =  to_decimal(h_bill_line.nettobetrag) / to_decimal(qty) * -1
                        else:
                            amount =  to_decimal(price) * to_decimal(qty)

                            if foreign_rate:
                                amount_foreign = to_decimal(round(amount / exchg_rate , 2))
                            amount = to_decimal(round(amount , price_decimal))
                    else:
                        amount =  to_decimal(price) * to_decimal(qty)

                        if foreign_rate:
                            amount_foreign = to_decimal(round(amount / exchg_rate , 2))
                        amount = to_decimal(round(amount , price_decimal))
            else:

                if h_artikel.epreis1 == 0:

                    h_bill_line = get_cache (H_bill_line, {"_recid": [(eq, void_recid)]})

                    if h_bill_line:
                        amount =  - to_decimal(h_bill_line.nettobetrag)
                        amount = to_decimal(round(amount , price_decimal))
                        price =  to_decimal(h_bill_line.nettobetrag) / to_decimal(qty) * -1
                    else:
                        amount =  to_decimal(price) * to_decimal(qty)
                        amount = to_decimal(round(amount , price_decimal))
                else:
                    amount =  to_decimal(price) * to_decimal(qty)
                    amount = to_decimal(round(amount , price_decimal))

        if (amount > 99999999) or (amount < -99999999):
            fl_code = 1

        if amount < 0 and h_artikel.artart == 0:

            htparam = get_cache (Htparam, {"paramnr": [(eq, 261)]})

            if htparam.flogical:
                fl_code1 = 1


    def create_output():

        nonlocal output_list_data, rec_id, double_currency, price, qty, exchg_rate, price_decimal, transdate, cancel_flag, foreign_rate, void_recid, amount_foreign, amount, fl_code, fl_code1, h_artikel, artikel, waehrung, h_bill_line, exrate, htparam


        nonlocal input_list, output_list
        nonlocal output_list_data


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.price =  to_decimal(input_list.price)
        output_list.amount_foreign =  to_decimal(amount_foreign)
        output_list.amount =  to_decimal(amount)
        output_list.fl_code = fl_code
        output_list.fl_code1 = fl_code1

    input_list = query(input_list_data, first=True)

    if not input_list:

        return generate_output()
    else:
        rec_id = input_list.rec_id
        double_currency = input_list.double_currency
        price =  to_decimal(input_list.price)
        qty = input_list.qty
        exchg_rate =  to_decimal(input_list.exchg_rate)
        price_decimal = input_list.price_decimal
        transdate = input_list.transdate
        cancel_flag = input_list.cancel_flag
        foreign_rate = input_list.foreign_rate
        void_recid = input_list.void_recid

    h_artikel = get_cache (H_artikel, {"_recid": [(eq, rec_id)]})
    calculate_amount()
    create_output()

    return generate_output()