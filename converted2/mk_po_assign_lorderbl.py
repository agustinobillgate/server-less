#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import L_orderhdr, L_order

t_l_orderhdr_data, T_l_orderhdr = create_model_like(L_orderhdr, {"rec_id":int})

def mk_po_assign_lorderbl(t_l_orderhdr_data:[T_l_orderhdr], lief_nr:int, docu_nr:string, pr:string, curr_liefnr:int):

    prepare_cache ([L_orderhdr, L_order])

    globaldisc:Decimal = to_decimal("0.0")
    l_orderhdr = l_order = None

    t_l_orderhdr = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal globaldisc, l_orderhdr, l_order
        nonlocal lief_nr, docu_nr, pr, curr_liefnr


        nonlocal t_l_orderhdr

        return {}

    def assign_lorder():

        nonlocal globaldisc, l_orderhdr, l_order
        nonlocal lief_nr, docu_nr, pr, curr_liefnr


        nonlocal t_l_orderhdr

        l_order = get_cache (L_order, {"docu_nr": [(eq, docu_nr)],"pos": [(eq, 0)],"loeschflag": [(eq, 0)],"lief_nr": [(eq, curr_liefnr)]})

        if l_order:
            l_order.lief_nr = lief_nr
            l_order.lief_fax[0] = pr
            l_order.warenwert =  to_decimal(globaldisc)

        for l_order in db_session.query(L_order).filter(
                 (L_order.docu_nr == (docu_nr).lower()) & (L_order.loeschflag == 0) & (L_order.lief_nr == curr_liefnr)).order_by(L_order._recid).all():
            l_order.lief_nr = lief_nr
            l_order.betriebsnr = 0

        if curr_liefnr != lief_nr:
            l_orderhdr.lief_nr = lief_nr
        pass


    t_l_orderhdr = query(t_l_orderhdr_data, first=True)

    l_orderhdr = get_cache (L_orderhdr, {"_recid": [(eq, t_l_orderhdr.rec_id)]})

    if num_entries(t_l_orderhdr.lief_fax[2], chr_unicode(2)) > 1:
        globaldisc =  to_decimal(to_decimal(entry(1 , t_l_orderhdr.lief_fax[2] , chr_unicode(2)))) / to_decimal("100")
        t_l_orderhdr.lief_fax[2] = entry(0, t_l_orderhdr.lief_fax[2], chr_unicode(2))


    buffer_copy(t_l_orderhdr, l_orderhdr)
    assign_lorder()

    return generate_output()