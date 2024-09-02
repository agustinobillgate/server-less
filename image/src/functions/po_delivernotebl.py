from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import L_ophdr

def po_delivernotebl(docu_nr:str):
    delivernote_list_list = []
    l_ophdr = None

    delivernote_list = None

    delivernote_list_list, Delivernote_list = create_model("Delivernote_list", {"datum":date, "lager_nr":int, "docu_nr":str, "lscheinnr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal delivernote_list_list, l_ophdr


        nonlocal delivernote_list
        nonlocal delivernote_list_list
        return {"delivernote-list": delivernote_list_list}

    for l_ophdr in db_session.query(L_ophdr).filter(
            (func.lower(L_ophdr.op_typ) == "STI") &  (func.lower(L_ophdr.(docu_nr).lower()) == (docu_nr).lower())).all():
        delivernote_list = Delivernote_list()
        delivernote_list_list.append(delivernote_list)

        buffer_copy(l_ophdr, delivernote_list)

    return generate_output()