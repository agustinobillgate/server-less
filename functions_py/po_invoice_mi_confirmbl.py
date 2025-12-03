#using conversion tools version: 1.0.0.119

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_op

s_list_data, S_list = create_model("S_list", {"s_recid":int, "datum":date, "artnr":int, "bezeich":string, "einzelpreis":Decimal, "price0":Decimal, "anzahl":Decimal, "anz0":Decimal, "brutto":Decimal, "val0":Decimal, "disc":Decimal, "disc0":Decimal, "disc2":Decimal, "disc20":Decimal, "disc_amt":Decimal, "disc2_amt":Decimal, "vat":Decimal, "warenwert":Decimal, "vat0":Decimal, "vat_amt":Decimal, "betriebsnr":int}, {"price0": None})

def po_invoice_mi_confirmbl(s_list_data:[S_list]):

    prepare_cache ([L_op])

    l_op = None

    s_list = s_list1 = None

    S_list1 = S_list
    s_list1_data = s_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op
        nonlocal s_list1


        nonlocal s_list, s_list1

        return {"s-list": s_list_data}

    for s_list1 in query(s_list1_data, filters=(lambda s_list1: s_list1.betriebsnr == 0 or s_list1.betriebsnr == 10)):

        l_op = db_session.query(L_op).filter(L_op._recid == s_list1.s_recid).with_for_update().first()

        if l_op.betriebsnr == 0 or l_op.betriebsnr == 10:
            l_op.betriebsnr = l_op.betriebsnr + 1
            s_list1.betriebsnr = s_list1.betriebsnr + 1


        pass

    return generate_output()