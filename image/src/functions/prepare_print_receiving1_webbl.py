from functions.additional_functions import *
import decimal
from datetime import date
from functions.prepare_print_receiving_cldbl import prepare_print_receiving_cldbl

def prepare_print_receiving1_webbl(pvilanguage:int, docu_nr:str, user_init:str, po_nr:str, lief_nr:int, store:int, to_date:date):
    show_price = False
    crterm = 0
    d_purchase = False
    unit_price = 0
    l_lieferant_firma = ""
    avail_l_lager = False
    t_lager_nr = 0
    t_bezeich = ""
    print_list_list = []

    str_list = print_list = None

    str_list_list, Str_list = create_model("Str_list", {"artnr":int, "qty":decimal, "warenwert":decimal, "munit":str, "s":str, "fibu":str})
    print_list_list, Print_list = create_model("Print_list", {"artnr":str, "bezeich":str, "qty":str, "warenwert":str, "price":str, "munit":str, "fibu":str, "lscheinnr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, print_list_list


        nonlocal str_list, print_list
        nonlocal str_list_list, print_list_list
        return {"show_price": show_price, "crterm": crterm, "d_purchase": d_purchase, "unit_price": unit_price, "l_lieferant_firma": l_lieferant_firma, "avail_l_lager": avail_l_lager, "t_lager_nr": t_lager_nr, "t_bezeich": t_bezeich, "print-list": print_list_list}

    show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, str_list_list = get_output(prepare_print_receiving_cldbl(pvilanguage, docu_nr, user_init, po_nr, lief_nr, store, to_date))

    for str_list in query(str_list_list):
        print_list = Print_list()
        print_list_list.append(print_list)

        print_list.artnr = substring(str_list.s, 0, 7)
        print_list.bezeich = substring(str_list.s, 7, 24)
        print_list.price = substring(str_list.s, 31, 15)
        print_list.qty = substring(str_list.s, 46, 10)
        print_list.warenwert = substring(str_list.s, 56, 15)
        print_list.lscheinnr = substring(str_list.s, 71, 20)
        print_list.fibu = str_list.fibu
        print_list.munit = str_list.munit

    return generate_output()