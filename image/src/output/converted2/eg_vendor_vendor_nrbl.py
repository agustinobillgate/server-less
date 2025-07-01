#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_vendor

def eg_vendor_vendor_nrbl(curr_select:string, vendor_vendor_nr:int, rec_id:int):

    prepare_cache ([Eg_vendor])

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


    eg_vendor = get_cache (Eg_vendor, {"_recid": [(eq, rec_id)]})

    if curr_select.lower()  == ("chg").lower() :

        sub = get_cache (Eg_vendor, {"vendor_nr": [(eq, vendor_vendor_nr)],"_recid": [(ne, eg_vendor._recid)]})

    elif curr_select.lower()  == ("add").lower() :

        sub = get_cache (Eg_vendor, {"vendor_nr": [(eq, vendor_vendor_nr)]})

    if sub:
        avail_sub = True

    return generate_output()