from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_order

def po_list_check_delbl(pvilanguage:int, l_orderhdr_docu_nr:str):
    msg_str = ""
    msg_str1 = ""
    lvcarea:str = "po_list"
    l_order = None

    l_order1 = None

    L_order1 = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str1, lvcarea, l_order
        nonlocal l_order1


        nonlocal l_order1
        return {"msg_str": msg_str, "msg_str1": msg_str1}

    def check_del():

        nonlocal msg_str, msg_str1, lvcarea, l_order
        nonlocal l_order1


        nonlocal l_order1


        L_order1 = L_order

        l_order1 = db_session.query(L_order1).filter(
                (func.lower(L_order1.docu_nr) == (l_orderhdr_docu_nr).lower()) &  (L_order1.pos > 0) &  (L_order1.loeschflag == 0) &  (L_order1.geliefert != 0)).first()

        if not l_order1:
            msg_str = msg_str + chr(2) + "&Q" + translateExtended ("Are you sure you want to CLOSE the order document", lvcarea, "") + " " + l_orderhdr_docu_nr + "?"
        else:

            l_order1 = db_session.query(L_order1).filter(
                    (func.lower(L_order1.docu_nr) == (l_orderhdr_docu_nr).lower()) &  (L_order1.pos > 0) &  (L_order1.loeschflag == 0) &  ((L_order1.geliefert != L_order1.anzahl))).first()

            if l_order1:
                msg_str1 = msg_str1 + chr(2) + "&W" + translateExtended ("The order items are not yet completely delivered.", lvcarea, "")
            msg_str = msg_str + chr(2) + "&Q" + translateExtended ("Are you sure you want to CLOSE the order document", lvcarea, "") + " " + l_orderhdr_docu_nr + "?"

    check_del()

    return generate_output()