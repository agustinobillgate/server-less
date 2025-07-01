#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import L_order

def purchase_order_del_pobl(billdate:date, q2_list_docu_nr:string, bediener_username:string):

    prepare_cache ([L_order])

    l_order = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal l_order
        nonlocal billdate, q2_list_docu_nr, bediener_username

        return {}

    def del_po():

        nonlocal l_order
        nonlocal billdate, q2_list_docu_nr, bediener_username

        l_od = None
        l_od1 = None
        L_od =  create_buffer("L_od",L_order)
        L_od1 =  create_buffer("L_od1",L_order)

        l_od = get_cache (L_order, {"docu_nr": [(eq, q2_list_docu_nr)],"pos": [(eq, 0)]})
        l_od.loeschflag = 2
        l_od.lieferdatum_eff = billdate
        l_od.lief_fax[2] = bediener_username


        pass

        for l_od1 in db_session.query(L_od1).filter(
                 (L_od1.docu_nr == (q2_list_docu_nr).lower()) & (L_od1.pos > 0) & (L_od1.loeschflag == 0)).order_by(L_od1._recid).all():

            l_od = get_cache (L_order, {"_recid": [(eq, l_od1._recid)]})
            l_od.loeschflag = 2
            l_od.lieferdatum = billdate
            l_od.lief_fax[1] = bediener_username


            pass


    del_po()

    return generate_output()