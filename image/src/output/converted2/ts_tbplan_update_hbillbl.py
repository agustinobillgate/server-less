#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ts_tbplan_update_hbillbl(rec_id:int, hostnr:int, pax:int, gname:string, hoga_resnr:int, hoga_reslinnr:int):

    prepare_cache ([H_bill])

    h_bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal h_bill
        nonlocal rec_id, hostnr, pax, gname, hoga_resnr, hoga_reslinnr

        return {}


    if gname == None:
        gname = ""

    h_bill = get_cache (H_bill, {"_recid": [(eq, rec_id)]})

    if h_bill:
        pass

        if h_bill.bilname.lower()  != (gname).lower() :
            h_bill.resnr = hoga_resnr
            h_bill.reslinnr = hoga_reslinnr
        h_bill.service[1] = hostnr
        h_bill.belegung = pax
        h_bill.bilname = gname
        pass
        pass

    return generate_output()