#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_hbline_get_taxservicebl import ts_hbline_get_taxservicebl
from models import H_bill, Htparam

t_amount_list_data, T_amount_list = create_model("T_amount_list", {"nr":int, "anzahl":int, "menu_recid":int, "amount":Decimal, "orig_amount":Decimal, "unit_price":Decimal, "artnr":int})

def ts_hbline_get_taxservice3_webbl(vmode:int, hbill_recid:int, menu_nr:int, dept:int, artnr:int, price:Decimal, anzahl:int, incl_vat:bool, balance:Decimal, t_amount_list_data:[T_amount_list]):

    prepare_cache ([H_bill, Htparam])

    amount = to_decimal("0.0")
    t_out_list_data = []
    fact_scvat:Decimal = to_decimal("0.0")
    curr_nr:int = 0
    curr_balance:Decimal = to_decimal("0.0")
    price_decimal:int = 0
    h_bill = htparam = None

    menu_list = t_amount_list = t_out_list = None

    menu_list_data, Menu_list = create_model("Menu_list", {"request":string, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "price":Decimal, "betrag":Decimal, "voucher":string}, {"anzahl": 1})
    t_out_list_data, T_out_list = create_model("T_out_list", {"amount":Decimal, "orig_amount":Decimal, "amt_balance":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, t_out_list_data, fact_scvat, curr_nr, curr_balance, price_decimal, h_bill, htparam
        nonlocal vmode, hbill_recid, menu_nr, dept, artnr, price, anzahl, incl_vat, balance


        nonlocal menu_list, t_amount_list, t_out_list
        nonlocal menu_list_data, t_out_list_data

        return {"balance": balance, "t-amount-list": t_amount_list_data, "amount": amount, "t-out-list": t_out_list_data}

    h_bill = get_cache (H_bill, {"_recid": [(eq, hbill_recid)]})

    if h_bill:
        curr_balance =  to_decimal(h_bill.saldo)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    if vmode == 1:
        fact_scvat = get_output(ts_hbline_get_taxservicebl(artnr, dept))
        t_out_list = T_out_list()
        t_out_list_data.append(t_out_list)


        if not incl_vat:

            t_amount_list = query(t_amount_list_data, filters=(lambda t_amount_list: t_amount_list.nr == menu_nr), first=True)

            if not t_amount_list:
                t_amount_list = T_amount_list()
                t_amount_list_data.append(t_amount_list)

                t_amount_list.nr = menu_nr
                t_amount_list.artnr = artnr
                t_amount_list.anzahl = anzahl
                t_amount_list.unit_price =  to_decimal(price)
                t_amount_list.amount = ( to_decimal(price) * to_decimal(fact_scvat)) * to_decimal(anzahl)
                t_amount_list.orig_amount =  to_decimal(price) * to_decimal(anzahl)
                t_amount_list.amount = to_decimal(round(t_amount_list.amount , price_decimal))
                amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)


            else:

                if t_amount_list.anzahl != anzahl:
                    t_amount_list.anzahl = anzahl
                    t_amount_list.amount = ( to_decimal(price) * to_decimal(fact_scvat)) * to_decimal(anzahl)
                    t_amount_list.orig_amount =  to_decimal(price) * to_decimal(anzahl)
                    t_amount_list.amount = to_decimal(round(t_amount_list.amount , price_decimal))


            amount =  to_decimal("0")

            for t_amount_list in query(t_amount_list_data):
                amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)
                t_out_list.orig_amount =  to_decimal(t_out_list.orig_amount) + to_decimal(t_amount_list.orig_amount)
            t_out_list.amount =  to_decimal(amount)
            amount =  to_decimal(amount) + to_decimal(balance)
            t_out_list.amt_balance =  to_decimal(amount)
        else:

            t_amount_list = query(t_amount_list_data, filters=(lambda t_amount_list: t_amount_list.nr == menu_nr), first=True)

            if not t_amount_list:
                t_amount_list = T_amount_list()
                t_amount_list_data.append(t_amount_list)

                t_amount_list.nr = menu_nr
                t_amount_list.artnr = artnr
                t_amount_list.anzahl = anzahl
                t_amount_list.unit_price =  to_decimal(price)
                t_amount_list.amount =  to_decimal(price) * to_decimal(anzahl)
                t_amount_list.amount = to_decimal(round(t_amount_list.amount , price_decimal))
                t_amount_list.orig_amount = ( to_decimal(price) * to_decimal(anzahl)) / to_decimal(fact_scvat)
                amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)


            else:

                if t_amount_list.anzahl != anzahl:
                    t_amount_list.anzahl = anzahl
                    t_amount_list.amount =  to_decimal(price) * to_decimal(anzahl)
                    t_amount_list.orig_amount = ( to_decimal(price) * to_decimal(anzahl)) / to_decimal(fact_scvat)
                    t_amount_list.amount = to_decimal(round(t_amount_list.amount , price_decimal))


            amount =  to_decimal("0")

            for t_amount_list in query(t_amount_list_data):
                amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)
                t_out_list.orig_amount =  to_decimal(t_out_list.orig_amount) + to_decimal(t_amount_list.orig_amount)
            t_out_list.amount =  to_decimal(amount)
            amount =  to_decimal(amount) + to_decimal(balance)
            t_out_list.amt_balance =  to_decimal(amount)
    else:
        t_out_list = T_out_list()
        t_out_list_data.append(t_out_list)


        t_amount_list = query(t_amount_list_data, filters=(lambda t_amount_list: t_amount_list.nr == menu_nr), first=True)

        if t_amount_list:
            t_amount_list_data.remove(t_amount_list)
        amount =  to_decimal("0")

        for t_amount_list in query(t_amount_list_data):
            amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)
            t_out_list.orig_amount =  to_decimal(t_out_list.orig_amount) + to_decimal(t_amount_list.orig_amount)
        t_out_list.amount =  to_decimal(amount)
        amount =  to_decimal(amount) + to_decimal(balance)
        t_out_list.amt_balance =  to_decimal(amount)
        curr_nr = 0

        for t_amount_list in query(t_amount_list_data, filters=(lambda t_amount_list: t_amount_list.nr > 0), sort_by=[("nr",False)]):
            curr_nr = curr_nr + 1
            t_amount_list.nr = curr_nr

    return generate_output()