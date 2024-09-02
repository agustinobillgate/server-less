from functions.additional_functions import *
import decimal
from functions.ts_hbline_get_taxservicebl import ts_hbline_get_taxservicebl

def ts_hbline_get_taxservice_webbl(vmode:int, menu_nr:int, dept:int, artnr:int, price:decimal, anzahl:int, incl_vat:bool, amount:decimal, t_amount_list:[T_amount_list]):
    fact_scvat:decimal = 0
    curr_nr:int = 0

    menu_list = t_amount_list = None

    menu_list_list, Menu_list = create_model("Menu_list", {"request":str, "krecid":int, "posted":bool, "nr":int, "artnr":int, "bezeich":str, "anzahl":int, "price":decimal, "betrag":decimal, "voucher":str}, {"anzahl": 1})
    t_amount_list_list, T_amount_list = create_model("T_amount_list", {"nr":int, "menu_recid":int, "amount":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fact_scvat, curr_nr


        nonlocal menu_list, t_amount_list
        nonlocal menu_list_list, t_amount_list_list
        return {}


    if vmode == 1:

        if not incl_vat:
            fact_scvat = get_output(ts_hbline_get_taxservicebl(artnr, dept))
            t_amount_list = T_amount_list()
            t_amount_list_list.append(t_amount_list)

            t_amount_list.nr = menu_nr
            t_amount_list.amount = (price * fact_scvat) * anzahl


            amount = amount + t_amount_list.amount
        else:
            t_amount_list = T_amount_list()
            t_amount_list_list.append(t_amount_list)

            t_amount_list.nr = menu_nr
            t_amount_list.amount = price * anzahl


            amount = amount + t_amount_list.amount
    else:

        t_amount_list = query(t_amount_list_list, filters=(lambda t_amount_list :t_amount_list.nr == menu_nr), first=True)

        if t_amount_list:
            amount = amount - t_amount_list.amount
            t_amount_list_list.remove(t_amount_list)
        curr_nr = 0

        for t_amount_list in query(t_amount_list_list, filters=(lambda t_amount_list :t_amount_list.nr > 0)):
            curr_nr = curr_nr + 1
            t_amount_list.nr = curr_nr

    return generate_output()