from functions.additional_functions import *
import decimal
from models import Eg_vperform, Eg_vendor

def eg_vendor_btn_delartbl(vendor_vendor_nr:int, rec_id:int):
    fl_code = 0
    eg_vperform = eg_vendor = None

    egperform = None

    Egperform = create_buffer("Egperform",Eg_vperform)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_vperform, eg_vendor
        nonlocal vendor_vendor_nr, rec_id
        nonlocal egperform


        nonlocal egperform
        return {"fl_code": fl_code}


    egperform = db_session.query(Egperform).filter(
             (Egperform.vendor_nr == vendor_vendor_nr)).first()

    if egPerform:
        fl_code = 1

        return generate_output()

    eg_vendor = db_session.query(Eg_vendor).filter(
             (Eg_vendor._recid == rec_id)).first()
    db_session.delete(eg_vendor)
    pass

    return generate_output()