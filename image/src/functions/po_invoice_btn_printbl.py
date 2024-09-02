from functions.additional_functions import *
import decimal
from datetime import date
from models import L_artikel, L_untergrup

def po_invoice_btn_printbl(s_list:[S_list]):
    sub_list_list = []
    l_artikel = l_untergrup = None

    s_list = sub_list = None

    s_list_list, S_list = create_model("S_list", {"s_recid":int, "datum":date, "artnr":int, "bezeich":str, "einzelpreis":decimal, "price0":decimal, "anzahl":decimal, "anz0":decimal, "brutto":decimal, "val0":decimal, "disc":decimal, "disc0":decimal, "disc2":decimal, "disc20":decimal, "disc_amt":decimal, "disc2_amt":decimal, "vat":decimal, "warenwert":decimal, "vat0":decimal, "vat_amt":decimal, "betriebsnr":int}, {"price0": None})
    sub_list_list, Sub_list = create_model("Sub_list", {"zwkum":int, "bezeich":str, "amt":decimal, "disc":decimal, "disc2":decimal, "vat":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal sub_list_list, l_artikel, l_untergrup


        nonlocal s_list, sub_list
        nonlocal s_list_list, sub_list_list
        return {"sub-list": sub_list_list}


    for s_list in query(s_list_list):

        l_artikel = db_session.query(L_artikel).filter(
                (L_artikel.artnr == s_list.artnr)).first()

        l_untergrup = db_session.query(L_untergrup).filter(
                (L_untergrup.zwkum == l_artikel.zwkum)).first()

        sub_list = query(sub_list_list, filters=(lambda sub_list :sub_list.zwkum == l_untergrup.zwkum), first=True)

        if not sub_list:
            sub_list = Sub_list()
            sub_list_list.append(sub_list)

            sub_list.zwkum = l_untergrup.zwkum
            sub_list.bezeich = l_untergrup.bezeich
        sub_list.amt = sub_list.amt + s_list.brutto
        sub_list.disc = sub_list.disc + s_list.disc_amt
        sub_list.disc2 = sub_list.disc2 + s_list.disc2_amt
        sub_list.vat = sub_list.vat + s_list.vat_amt

    return generate_output()