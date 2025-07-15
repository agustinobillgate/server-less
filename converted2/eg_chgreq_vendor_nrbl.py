#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_vendor

def eg_chgreq_vendor_nrbl(v_vendor_nr:int):

    prepare_cache ([Eg_vendor])

    avail_ven = False
    ven_bezeich = ""
    eg_vendor = None

    ven = None

    Ven = create_buffer("Ven",Eg_vendor)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_ven, ven_bezeich, eg_vendor
        nonlocal v_vendor_nr
        nonlocal ven


        nonlocal ven

        return {"avail_ven": avail_ven, "ven_bezeich": ven_bezeich}


    ven = get_cache (Eg_vendor, {"vendor_nr": [(eq, v_vendor_nr)]})

    if ven:
        ven_bezeich = ven.bezeich
        avail_ven = True

    return generate_output()