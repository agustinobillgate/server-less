#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 28/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Eg_vendor

vendor_data, Vendor = create_model_like(Eg_vendor)

def eg_vendor_btn_exitbl(vendor_data:[Vendor], case_type:int, rec_id:int):

    prepare_cache ([Eg_vendor])

    fl_code = 0
    eg_vendor = None

    vendor = queasy1 = None

    Queasy1 = create_buffer("Queasy1",Eg_vendor)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_vendor
        nonlocal case_type, rec_id
        nonlocal queasy1


        nonlocal vendor, queasy1

        return {"fl_code": fl_code}

    def fill_new_vendor():

        nonlocal fl_code, eg_vendor
        nonlocal case_type, rec_id
        nonlocal queasy1


        nonlocal vendor, queasy1


        eg_vendor.vendor_nr = vendor.vendor_nr
        eg_vendor.bezeich = vendor.bezeich
        eg_vendor.address = vendor.address
        eg_vendor.phone = vendor.phone
        eg_vendor.website = vendor.website
        eg_vendor.email = vendor.email
        eg_vendor.fax = vendor.fax
        eg_vendor.contact_person = vendor.contact_person


    vendor = query(vendor_data, first=True)

    if case_type == 1:
        eg_vendor = Eg_vendor()
        db_session.add(eg_vendor)

        fill_new_vendor()

    elif case_type == 2:

        # eg_vendor = get_cache (Eg_vendor, {"_recid": [(eq, rec_id)]})
        eg_vendor = db_session.query(Eg_vendor).filter(Eg_vendor._recid == rec_id).with_for_update().first()

        queasy1 = get_cache (Eg_vendor, {"vendor_nr": [(eq, vendor.vendor_nr)],"_recid": [(ne, eg_vendor._recid)]})

        if queasy1:
            fl_code = 1

            return generate_output()
        else:
            pass
            eg_vendor.vendor_nr = vendor.vendor_nr
            eg_vendor.bezeich = vendor.bezeich
            eg_vendor.address = vendor.address
            eg_vendor.phone = vendor.phone
            eg_vendor.website = vendor.website
            eg_vendor.email = vendor.email
            eg_vendor.fax = vendor.fax
            eg_vendor.contact_person = vendor.contact_person
            pass
            pass

    return generate_output()