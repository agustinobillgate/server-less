from functions.additional_functions import *
import decimal
from datetime import date
from models import L_op

def po_invoice_mi_confirmbl(s_list:[S_list]):
    l_op = None

    s_list = s_list1 = None

    s_list_list, S_list = create_model("S_list", {"s_recid":int, "datum":date, "artnr":int, "bezeich":str, "einzelpreis":decimal, "price0":decimal, "anzahl":decimal, "anz0":decimal, "brutto":decimal, "val0":decimal, "disc":decimal, "disc0":decimal, "disc2":decimal, "disc20":decimal, "disc_amt":decimal, "disc2_amt":decimal, "vat":decimal, "warenwert":decimal, "vat0":decimal, "vat_amt":decimal, "betriebsnr":int}, {"price0": None})

    S_list1 = S_list
    s_list1_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_op
        nonlocal s_list1


        nonlocal s_list, s_list1
        nonlocal s_list_list
        return {}

    for s_list1 in query(s_list1_list, filters=(lambda s_list1 :s_list1.betriebsnr == 0 or s_list1.betriebsnr == 10)):

        l_op = db_session.query(L_op).filter(
                (L_op._recid == s_list1.s_recid)).first()

        if l_op.betriebsnr == 0 or l_op.betriebsnr == 10:
            l_op.betriebsnr = l_op.betriebsnr + 1
            s_list1.betriebsnr = s_list1.betriebsnr + 1

        l_op = db_session.query(L_op).first()

    return generate_output()