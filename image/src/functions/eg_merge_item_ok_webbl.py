from functions.additional_functions import *
import decimal
from models import Eg_request, Eg_property

def eg_merge_item_ok_webbl(item_nr:int, merge_nr:int):
    success_flag1 = False
    success_flag2 = False
    eg_request = eg_property = None

    buf_eg_request = None

    Buf_eg_request = Eg_request

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag1, success_flag2, eg_request, eg_property
        nonlocal buf_eg_request


        nonlocal buf_eg_request
        return {"success_flag1": success_flag1, "success_flag2": success_flag2}


    for eg_request in db_session.query(Eg_request).all():

        buf_eg_request = db_session.query(Buf_eg_request).filter(
                (Buf_eg_request.reqnr == eg_request.reqnr) &  (Buf_eg_request.propertynr == item_nr)).first()

        if buf_eg_request:

            buf_eg_request = db_session.query(Buf_eg_request).first()
            buf_eg_request.propertynr = merge_nr

            buf_eg_request = db_session.query(Buf_eg_request).first()

            success_flag1 = True

    eg_property = db_session.query(Eg_property).filter(
            (Eg_property.nr == item_nr)).first()

    if eg_property:

        eg_property = db_session.query(Eg_property).first()
        db_session.delete(eg_property)

        success_flag2 = True

    return generate_output()