#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_print_receiving_cld_3bl import prepare_print_receiving_cld_3bl

def prepare_print_receiving1_webbl(pvilanguage:int, docu_nr:string, user_init:string, po_nr:string, lief_nr:int, store:int, to_date:date):
    show_price = False
    crterm = 0
    d_purchase = False
    unit_price = to_decimal("0.0")
    l_lieferant_firma = ""
    avail_l_lager = False
    t_lager_nr = 0
    t_bezeich = ""
    print_list_data = []
    curr_price:Decimal = to_decimal("0.0")

    str_list = print_list = None

    str_list_data, Str_list = create_model("Str_list", {"artnr":string, "qty":Decimal, "warenwert":string, "munit":string, "fibu":string, "fibu_ze":string, "addvat_value":Decimal, "bezeich":string, "lscheinnr":string, "unit_price":Decimal, "disc_amount":Decimal, "addvat_amount":Decimal, "disc_amount2":Decimal, "vat_amount":Decimal})
    print_list_data, Print_list = create_model("Print_list", {"artnr":string, "bezeich":string, "qty":Decimal, "warenwert":string, "price":Decimal, "munit":string, "fibu":string, "lscheinnr":string, "fibu_ze":string, "addvat_value":Decimal, "disc_amount":Decimal, "addvat_amount":Decimal, "disc_amount2":Decimal, "vat_amount":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, print_list_data, curr_price
        nonlocal pvilanguage, docu_nr, user_init, po_nr, lief_nr, store, to_date


        nonlocal str_list, print_list
        nonlocal str_list_data, print_list_data

        return {"show_price": show_price, "crterm": crterm, "d_purchase": d_purchase, "unit_price": unit_price, "l_lieferant_firma": l_lieferant_firma, "avail_l_lager": avail_l_lager, "t_lager_nr": t_lager_nr, "t_bezeich": t_bezeich, "print-list": print_list_data}

    show_price, crterm, d_purchase, unit_price, l_lieferant_firma, avail_l_lager, t_lager_nr, t_bezeich, str_list_data = get_output(prepare_print_receiving_cld_3bl(pvilanguage, docu_nr, user_init, po_nr, lief_nr, store, to_date))

    for str_list in query(str_list_data):
        print_list = Print_list()
        print_list_data.append(print_list)

        print_list.artnr = str_list.artnr
        print_list.bezeich = str_list.bezeich
        print_list.price =  to_decimal(str_list.unit_price)
        print_list.qty =  to_decimal(str_list.qty)
        print_list.warenwert = str_list.warenwert
        print_list.lscheinnr = str_list.lscheinnr
        print_list.fibu = str_list.fibu
        print_list.munit = str_list.munit
        print_list.fibu_ze = str_list.fibu_ze
        print_list.addvat_value =  to_decimal(str_list.addvat_value)


        print_list.disc_amount =  to_decimal(str_list.disc_amount)
        print_list.disc_amount2 =  to_decimal(str_list.disc_amount2)
        print_list.addvat_amount =  to_decimal(str_list.addvat_amount)
        print_list.vat_amount =  to_decimal(str_list.vat_amount)

        if str_list.disc_amount != 0:
            print_list.price =  to_decimal(print_list.price) + to_decimal(str_list.disc_amount)

        if str_list.vat_amount != 0:
            print_list.price =  to_decimal(print_list.price) - to_decimal(str_list.vat_amount)

    return generate_output()