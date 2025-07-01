#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_request, Eg_property

def eg_merge_item_ok_webbl(item_nr:int, merge_nr:int):

    prepare_cache ([Eg_request])

    success_flag1 = False
    success_flag2 = False
    eg_request = eg_property = None

    buf_eg_request = None

    Buf_eg_request = create_buffer("Buf_eg_request",Eg_request)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag1, success_flag2, eg_request, eg_property
        nonlocal item_nr, merge_nr
        nonlocal buf_eg_request


        nonlocal buf_eg_request

        return {"success_flag1": success_flag1, "success_flag2": success_flag2}


    for eg_request in db_session.query(Eg_request).order_by(Eg_request._recid).all():

        buf_eg_request = get_cache (Eg_request, {"reqnr": [(eq, eg_request.reqnr)],"propertynr": [(eq, item_nr)]})

        if buf_eg_request:
            pass
            buf_eg_request.propertynr = merge_nr
            pass
            pass
            success_flag1 = True

    eg_property = get_cache (Eg_property, {"nr": [(eq, item_nr)]})

    if eg_property:
        pass
        db_session.delete(eg_property)
        pass
        success_flag2 = True

    return generate_output()