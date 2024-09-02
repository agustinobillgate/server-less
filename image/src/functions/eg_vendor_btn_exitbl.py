from functions.additional_functions import *
import decimal
from models import Eg_vendor

def eg_vendor_btn_exitbl(vendor:[Vendor], case_type:int, rec_id:int):
    fl_code = 0
    eg_vendor = None

    vendor = queasy1 = None

    vendor_list, Vendor = create_model_like(Eg_vendor)

    Queasy1 = Eg_vendor

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fl_code, eg_vendor
        nonlocal queasy1


        nonlocal vendor, queasy1
        nonlocal vendor_list
        return {"fl_code": fl_code}

    def fill_new_vendor():

        nonlocal fl_code, eg_vendor
        nonlocal queasy1


        nonlocal vendor, queasy1
        nonlocal vendor_list


        eg_vendor.vendor_nr = vendor.vendor_nr
        eg_vendor.bezeich = vendor.bezeich
        eg_vendor.address = vendor.address
        eg_vendor.phone = vendor.phone
        eg_vendor.website = vendor.website
        eg_vendor.email = vendor.email
        eg_vendor.fax = vendor.fax
        eg_vendor.contact_person = vendor.contact_person

    vendor = query(vendor_list, first=True)

    if case_type == 1:
        eg_vendor = Eg_vendor()
        db_session.add(eg_vendor)

        fill_new_vendor()

    elif case_type == 2:

        eg_vendor = db_session.query(Eg_vendor).filter(
                (Eg_vendor._recid == rec_id)).first()

        queasy1 = db_session.query(Queasy1).filter(
                (Queasy1.vendor_nr == vendor.vendor_nr) &  (Queasy1._recid != eg_vendor._recid)).first()

        if queasy1:
            fl_code = 1

            return generate_output()
        else:

            eg_vendor = db_session.query(Eg_vendor).first()
            eg_vendor.vendor_nr = vendor.vendor_nr
            eg_vendor.bezeich = vendor.bezeich
            eg_vendor.address = vendor.address
            eg_vendor.phone = vendor.phone
            eg_vendor.website = vendor.website
            eg_vendor.email = vendor.email
            eg_vendor.fax = vendor.fax
            eg_vendor.contact_person = vendor.contact_person

            eg_vendor = db_session.query(Eg_vendor).first()


    return generate_output()