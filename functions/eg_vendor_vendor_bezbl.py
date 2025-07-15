#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_vendor

def eg_vendor_vendor_bezbl(curr_select:string, vendor_bezeich:string, rec_id:int):

    prepare_cache ([Eg_vendor])

    avail_sub = False
    eg_vendor = None

    queasy1 = None

    Queasy1 = create_buffer("Queasy1",Eg_vendor)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_sub, eg_vendor
        nonlocal curr_select, vendor_bezeich, rec_id
        nonlocal queasy1


        nonlocal queasy1

        return {"avail_sub": avail_sub}


    eg_vendor = get_cache (Eg_vendor, {"_recid": [(eq, rec_id)]})

    if curr_select.lower()  == ("chg").lower() :

        queasy1 = get_cache (Eg_vendor, {"bezeich": [(eq, vendor_bezeich)],"_recid": [(ne, eg_vendor._recid)]})

    elif curr_select.lower()  == ("add").lower() :

        queasy1 = get_cache (Eg_vendor, {"bezeich": [(eq, vendor_bezeich)]})

    if queasy1:
        avail_sub = True

    return generate_output()