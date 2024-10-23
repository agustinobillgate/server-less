from functions.additional_functions import *
import decimal
from models import Eg_vendor

def eg_vendor_vendor_nrbl(curr_select:str, vendor_vendor_nr:int, rec_id:int):
    avail_sub = False
    eg_vendor = None

    sub = None

    Sub = create_buffer("Sub",Eg_vendor)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_sub, eg_vendor
        nonlocal curr_select, vendor_vendor_nr, rec_id
        nonlocal sub


        nonlocal sub
        return {"avail_sub": avail_sub}


    eg_vendor = db_session.query(Eg_vendor).filter(
             (Eg_vendor._recid == rec_id)).first()

    if curr_select.lower()  == ("chg").lower() :

        sub = db_session.query(Sub).filter(
                 (Sub.vendor_nr == vendor_vendor_nr) & (Sub._recid != eg_vendor._recid)).first()

    elif curr_select.lower()  == ("add").lower() :

        sub = db_session.query(Sub).filter(
                 (Sub.vendor_nr == vendor_vendor_nr)).first()

    if sub:
        avail_sub = True

    return generate_output()