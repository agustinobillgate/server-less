#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_ophdr

def po_delivernotebl(docu_nr:string):
    delivernote_list_list = []
    l_ophdr = None

    delivernote_list = None

    delivernote_list_list, Delivernote_list = create_model("Delivernote_list", {"datum":date, "lager_nr":int, "docu_nr":string, "lscheinnr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal delivernote_list_list, l_ophdr
        nonlocal docu_nr


        nonlocal delivernote_list
        nonlocal delivernote_list_list

        return {"delivernote-list": delivernote_list_list}

    for l_ophdr in db_session.query(L_ophdr).filter(
             (L_ophdr.op_typ == ("STI").lower()) & (L_ophdr.docu_nr == (docu_nr).lower())).order_by(L_ophdr.lager_nr).all():
        delivernote_list = Delivernote_list()
        delivernote_list_list.append(delivernote_list)

        buffer_copy(l_ophdr, delivernote_list)

    return generate_output()