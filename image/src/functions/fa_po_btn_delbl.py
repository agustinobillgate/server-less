from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Fa_order, Fa_ordheader

def fa_po_btn_delbl(q_order_nr:str, user_init:str, billdate:date):
    fa_order = fa_ordheader = None

    fa_od = fa_odhd = None

    Fa_od = Fa_order
    Fa_odhd = Fa_ordheader

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fa_order, fa_ordheader
        nonlocal fa_od, fa_odhd


        nonlocal fa_od, fa_odhd
        return {}

    def del_po():

        nonlocal fa_order, fa_ordheader
        nonlocal fa_od, fa_odhd


        nonlocal fa_od, fa_odhd


        Fa_od = Fa_order
        Fa_odhd = Fa_ordheader

        fa_odhd = db_session.query(Fa_odhd).filter(
                (func.lower(Fa_odhd.order_nr) == (q_order_nr).lower())).first()
        fa_odhd.activeflag = 2
        fa_odhd.Delete_By = user_init
        fa_odhd.Delete_Date = billdate
        fa_odhd.Delete_Time = get_current_time_in_seconds()


        for fa_od in db_session.query(Fa_od).filter(
                (Fa_od.order_nr == fa_ordheader.order_nr) &  (Fa_od.activeflag == 0)).all():
            fa_od.activeflag = 2
            fa_od.Delete_By = user_init
            fa_od.Delete_Date = billdate
            fa_od.Delete_Time = get_current_time_in_seconds()


    del_po()

    return generate_output()