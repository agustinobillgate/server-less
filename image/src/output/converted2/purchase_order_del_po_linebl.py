#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order, L_orderhdr

def purchase_order_del_po_linebl(billdate:date, rec_id:int, l_orderhdr_rec_id:int, bediener_username:string):

    prepare_cache ([L_order, L_orderhdr])

    del_mainpo = False
    l_order = l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal del_mainpo, l_order, l_orderhdr
        nonlocal billdate, rec_id, l_orderhdr_rec_id, bediener_username

        return {"del_mainpo": del_mainpo}

    def del_po_line():

        nonlocal del_mainpo, l_order, l_orderhdr
        nonlocal billdate, rec_id, l_orderhdr_rec_id, bediener_username

        l_od = None
        L_od =  create_buffer("L_od",L_order)
        pass
        l_order.loeschflag = 2
        l_order.lieferdatum = billdate
        l_order.lief_fax[1] = bediener_username


        pass

        l_od = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(gt, 0)],"loeschflag": [(eq, 0)]})

        if not l_od:

            l_od = get_cache (L_order, {"docu_nr": [(eq, l_orderhdr.docu_nr)],"pos": [(eq, 0)]})
            l_od.loeschflag = 2
            l_od.lieferdatum_eff = billdate
            l_od.lief_fax[2] = bediener_username


            pass
        del_mainpo = True

    l_order = get_cache (L_order, {"_recid": [(eq, rec_id)]})

    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, l_orderhdr_rec_id)]})
    del_po_line()

    return generate_output()