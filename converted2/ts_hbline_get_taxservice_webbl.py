#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.ts_hbline_get_taxservicebl import ts_hbline_get_taxservicebl

t_amount_list_data, T_amount_list = create_model("T_amount_list", {"nr":int, "menu_recid":int, "amount":Decimal})

def ts_hbline_get_taxservice_webbl(vmode:int, menu_nr:int, dept:int, artnr:int, price:Decimal, anzahl:int, incl_vat:bool, amount:Decimal, t_amount_list_data:[T_amount_list]):
    fact_scvat:Decimal = to_decimal("0.0")
    curr_nr:int = 0

    menu_list = t_amount_list = None

    menu_list_data, Menu_list = create_model("Menu_list", {"request":string, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":string, "anzahl":int, "price":Decimal, "betrag":Decimal, "voucher":string}, {"anzahl": 1})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fact_scvat, curr_nr
        nonlocal vmode, menu_nr, dept, artnr, price, anzahl, incl_vat, amount


        nonlocal menu_list, t_amount_list
        nonlocal menu_list_data

        return {"amount": amount, "t-amount-list": t_amount_list_data}


    if vmode == 1:

        if not incl_vat:
            fact_scvat = get_output(ts_hbline_get_taxservicebl(artnr, dept))
            t_amount_list = T_amount_list()
            t_amount_list_data.append(t_amount_list)

            t_amount_list.nr = menu_nr
            t_amount_list.amount = ( to_decimal(price) * to_decimal(fact_scvat)) * to_decimal(anzahl)


            amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)
        else:
            t_amount_list = T_amount_list()
            t_amount_list_data.append(t_amount_list)

            t_amount_list.nr = menu_nr
            t_amount_list.amount =  to_decimal(price) * to_decimal(anzahl)


            amount =  to_decimal(amount) + to_decimal(t_amount_list.amount)
    else:

        t_amount_list = query(t_amount_list_data, filters=(lambda t_amount_list: t_amount_list.nr == menu_nr), first=True)

        if t_amount_list:
            amount =  to_decimal(amount) - to_decimal(t_amount_list.amount)
            t_amount_list_data.remove(t_amount_list)
        curr_nr = 0

        for t_amount_list in query(t_amount_list_data, filters=(lambda t_amount_list: t_amount_list.nr > 0), sort_by=[("nr",False)]):
            curr_nr = curr_nr + 1
            t_amount_list.nr = curr_nr

    return generate_output()