from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import L_order

def purchase_order_del_pobl(billdate:date, q2_list_docu_nr:str, bediener_username:str):
    l_order = None

    l_od = l_od1 = None

    L_od = L_order
    L_od1 = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal l_od, l_od1


        nonlocal l_od, l_od1
        return {}

    def del_po():

        nonlocal l_order
        nonlocal l_od, l_od1


        nonlocal l_od, l_od1


        L_od = L_order
        L_od1 = L_order

        l_od = db_session.query(L_od).filter(
                (func.lower(L_od.docu_nr) == (q2_list_docu_nr).lower()) &  (L_od.pos == 0)).first()
        l_od.loeschflag = 2
        l_od.lieferdatum_eff = billdate
        l_od.lief_fax[2] = bediener_username

        l_od = db_session.query(L_od).first()

        for l_od1 in db_session.query(L_od1).filter(
                (func.lower(L_od1.docu_nr) == (q2_list_docu_nr).lower()) &  (L_od1.pos > 0) &  (L_od1.loeschflag == 0)).all():

            l_od = db_session.query(L_od).filter(
                    (L_od._recid == l_od1._recid)).first()
            l_od.loeschflag = 2
            l_od.lieferdatum = billdate
            l_od.lief_fax[1] = bediener_username

            l_od = db_session.query(L_od).first()

    del_po()

    return generate_output()