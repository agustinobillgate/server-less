#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, L_order, L_orderhdr

def mn_del_old_pobl():

    prepare_cache ([Htparam])

    i = 0
    ci_date:date = None
    htparam = l_order = l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, ci_date, htparam, l_order, l_orderhdr

        return {"i": i}

    def del_old_po():

        nonlocal i, ci_date, htparam, l_order, l_orderhdr

        anz:int = 0
        l_od = None
        L_od =  create_buffer("L_od",L_order)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 237)]})

        if htparam.feldtyp == 1:
            anz = htparam.finteger

            if anz < 60:
                anz = 60
        else:
            anz = 60

        l_order = get_cache (L_order, {"loeschflag": [(ge, 1)],"pos": [(eq, 0)]})
        while None != l_order:

            if (l_order.lieferdatum_eff + anz) < ci_date:
                i = i + 1

                for l_od in db_session.query(L_od).filter(
                             (L_od.docu_nr == l_order.docu_nr) & (L_od.pos > 0)).order_by(L_od._recid).all():
                    db_session.delete(l_od)

                l_orderhdr = get_cache (L_orderhdr, {"docu_nr": [(eq, l_order.docu_nr)]})

                if l_orderhdr:
                    db_session.delete(l_orderhdr)
                pass
                db_session.delete(l_order)

            curr_recid = l_order._recid
            l_order = db_session.query(L_order).filter(
                     (L_order.loeschflag >= 1) & (L_order.pos == 0) & (L_order._recid > curr_recid)).first()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    del_old_po()

    return generate_output()