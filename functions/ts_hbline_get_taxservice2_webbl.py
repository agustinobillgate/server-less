#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_hbline_get_taxservicebl import ts_hbline_get_taxservicebl
from models import H_bill

t_amount_list_data, T_amount_list = create_model("T_amount_list", {"nr":int, "anzahl":int, "menu_recid":int, "amount":Decimal})

def ts_hbline_get_taxservice2_webbl(vmode:int, hbill_recid:int, menu_nr:int, dept:int, artnr:int, price:Decimal, anzahl:int, incl_vat:bool, balance:Decimal, t_amount_list_data:[T_amount_list]):

    prepare_cache ([H_bill])

    amount = to_decimal("0.0")
    fact_scvat:Decimal = to_decimal("0.0")
    curr_nr:int = 0
    curr_balance:Decimal = to_decimal("0.0")
    h_bill = None

    menu_list = t_amount_list = None

    menu_list_data, Menu_list = create_model("Menu_list", {"request":string, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "price":Decimal, "betrag":Decimal, "voucher":string}, {"anzahl": 1})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal amount, fact_scvat, curr_nr, curr_balance, h_bill
        nonlocal vmode, hbill_recid, menu_nr, dept, artnr, price, anzahl, incl_vat, balance


        nonlocal menu_list, t_amount_list
        nonlocal menu_list_data

        return {"amount": amount, "balance": balance, "t-amount-list": t_amount_list_data}


    h_bill = get_cache (H_bill, {"_recid": [(eq, hbill_recid)]})

    if h_bill:
        curr_balance =  to_decimal(h_bill.saldo)

    if vmode == 1:

        if not incl_vat:
            fact_scvat = get_output(ts_hbline_get_taxservicebl(artnr, dept))

            t_amount_list = query(t_amount_list_data, filters=(lambda t_amount_list: t_amount_list.nr == menu_nr), first=True)

            if not t_amount_list:
                t_amount_list = T_amount_list()
                t_amount_list_data.append(t_amount_list)

                t_amount_list.nr = menu_nr
                t_amount_list.anzahl = anzahl
                t_amount_list.amount = ( to_decimal(price) * to_decimal(fact_scvat)) * to_decimal(anzahl)


                amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)
            else:

                if t_amount_list.anzahl != anzahl:
                    t_amount_list.anzahl = anzahl
                    t_amount_list.amount = ( to_decimal(price) * to_decimal(fact_scvat)) * to_decimal(anzahl)

            amount =  to_decimal("0")

            for t_amount_list in query(t_amount_list_data):
                amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)
            amount =  to_decimal(amount) + to_decimal(balance)
        else:

            t_amount_list = query(t_amount_list_data, filters=(lambda t_amount_list: t_amount_list.nr == menu_nr), first=True)

            if not t_amount_list:
                t_amount_list = T_amount_list()
                t_amount_list_data.append(t_amount_list)

                t_amount_list.nr = menu_nr
                t_amount_list.anzahl = anzahl
                t_amount_list.amount =  to_decimal(price) * to_decimal(anzahl)


                amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)
            else:

                if t_amount_list.anzahl != anzahl:
                    t_amount_list.anzahl = anzahl
                    t_amount_list.amount = ( to_decimal(price) * to_decimal(fact_scvat)) * to_decimal(anzahl)

            amount =  to_decimal("0")

            for t_amount_list in query(t_amount_list_data):
                amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)
            amount =  to_decimal(amount) + to_decimal(balance)
    else:

        t_amount_list = query(t_amount_list_data, filters=(lambda t_amount_list: t_amount_list.nr == menu_nr), first=True)

        if t_amount_list:
            t_amount_list_data.remove(t_amount_list)
        amount =  to_decimal("0")

        for t_amount_list in query(t_amount_list_data):
            amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)
        amount =  to_decimal(amount) + to_decimal(balance)

    return generate_output()