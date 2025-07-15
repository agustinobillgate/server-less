#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Fa_order, Fa_ordheader

def fa_po_btn_delbl(q_order_nr:string, user_init:string, billdate:date):

    prepare_cache ([Fa_order, Fa_ordheader])

    fa_order = fa_ordheader = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_order, fa_ordheader
        nonlocal q_order_nr, user_init, billdate

        return {}

    def del_po():

        nonlocal fa_order, fa_ordheader
        nonlocal q_order_nr, user_init, billdate

        fa_od = None
        fa_odhd = None
        Fa_od =  create_buffer("Fa_od",Fa_order)
        Fa_odhd =  create_buffer("Fa_odhd",Fa_ordheader)

        fa_odhd = get_cache (Fa_ordheader, {"order_nr": [(eq, q_order_nr)]})
        fa_odhd.activeflag = 2
        fa_odhd.delete_by = user_init
        fa_odhd.delete_date = billdate
        fa_odhd.delete_time = get_current_time_in_seconds()


        pass

        for fa_od in db_session.query(Fa_od).filter(
                 (Fa_od.order_nr == fa_ordheader.order_nr) & (Fa_od.activeflag == 0)).order_by(Fa_od._recid).all():
            fa_od.activeflag = 2
            fa_od.delete_by = user_init
            fa_od.delete_date = billdate
            fa_od.delete_time = get_current_time_in_seconds()


        pass


    del_po()

    return generate_output()