#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_artikel, L_untergrup

s_list_list, S_list = create_model("S_list", {"s_recid":int, "datum":date, "artnr":int, "bezeich":string, "einzelpreis":Decimal, "price0":Decimal, "anzahl":Decimal, "anz0":Decimal, "brutto":Decimal, "val0":Decimal, "disc":Decimal, "disc0":Decimal, "disc2":Decimal, "disc20":Decimal, "disc_amt":Decimal, "disc2_amt":Decimal, "vat":Decimal, "warenwert":Decimal, "vat0":Decimal, "vat_amt":Decimal, "betriebsnr":int}, {"price0": None})

def po_invoice_btn_printbl(s_list_list:[S_list]):

    prepare_cache ([L_artikel, L_untergrup])

    sub_list_list = []
    l_artikel = l_untergrup = None

    s_list = sub_list = None

    sub_list_list, Sub_list = create_model("Sub_list", {"zwkum":int, "bezeich":string, "amt":Decimal, "disc":Decimal, "disc2":Decimal, "vat":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal sub_list_list, l_artikel, l_untergrup


        nonlocal s_list, sub_list
        nonlocal sub_list_list

        return {"sub-list": sub_list_list}


    for s_list in query(s_list_list, sort_by=[("bezeich",False),("betriebsnr",False)]):

        l_artikel = get_cache (L_artikel, {"artnr": [(eq, s_list.artnr)]})

        l_untergrup = get_cache (L_untergrup, {"zwkum": [(eq, l_artikel.zwkum)]})

        sub_list = query(sub_list_list, filters=(lambda sub_list: sub_list.zwkum == l_untergrup.zwkum), first=True)

        if not sub_list:
            sub_list = Sub_list()
            sub_list_list.append(sub_list)

            sub_list.zwkum = l_untergrup.zwkum
            sub_list.bezeich = l_untergrup.bezeich
        sub_list.amt =  to_decimal(sub_list.amt) + to_decimal(s_list.brutto)
        sub_list.disc =  to_decimal(sub_list.disc) + to_decimal(s_list.disc_amt)
        sub_list.disc2 =  to_decimal(sub_list.disc2) + to_decimal(s_list.disc2_amt)
        sub_list.vat =  to_decimal(sub_list.vat) + to_decimal(s_list.vat_amt)

    return generate_output()