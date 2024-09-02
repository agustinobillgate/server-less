from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, L_order, L_orderhdr

def mn_del_old_pobl():
    i = 0
    ci_date:date = None
    htparam = l_order = l_orderhdr = None

    l_od = None

    L_od = L_order

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, l_order, l_orderhdr
        nonlocal l_od


        nonlocal l_od
        return {"i": i}

    def del_old_po():

        nonlocal i, ci_date, htparam, l_order, l_orderhdr
        nonlocal l_od


        nonlocal l_od

        anz:int = 0
        L_od = L_order

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 237)).first()

        if htparam.feldtyp == 1:
            anz = htparam.finteger

            if anz < 60:
                anz = 60
        else:
            anz = 60

        l_order = db_session.query(L_order).filter(
                (L_order.loeschflag >= 1) &  (L_order.pos == 0)).first()
        while None != l_order:

            if (l_order.lieferdatum_eff + anz) < ci_date:
                i = i + 1

                for l_od in db_session.query(L_od).filter(
                            (L_od.docu_nr == l_order.docu_nr) &  (L_od.pos > 0)).all():
                    db_session.delete(l_od)

                l_orderhdr = db_session.query(L_orderhdr).filter(
                            (L_orderhdr.docu_nr == l_order.docu_nr)).first()

                if l_orderhdr:
                    db_session.delete(l_orderhdr)

                l_order = db_session.query(L_order).first()
                db_session.delete(l_order)


            l_order = db_session.query(L_order).filter(
                    (L_order.loeschflag >= 1) &  (L_order.pos == 0)).first()


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    del_old_po()

    return generate_output()