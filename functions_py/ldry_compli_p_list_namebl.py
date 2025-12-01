#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 01/12/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import H_bill

def ldry_compli_p_list_namebl(c_list_rechnr:int, c_list_dept:int, gname:string):

    prepare_cache ([H_bill])

    h_bill = None

    db_session = local_storage.db_session
    gname = gname.strip()

    def generate_output():
        nonlocal h_bill
        nonlocal c_list_rechnr, c_list_dept, gname

        return {}


    # h_bill = get_cache (H_bill, {"rechnr": [(eq, c_list_rechnr)],"departement": [(eq, c_list_dept)]})
    h_bill = db_session.query(H_bill).filter(
                 (H_bill.rechnr == c_list_rechnr) &
                 (H_bill.departement == c_list_dept)).with_for_update().first()   

    if h_bill:
        pass
        h_bill.bilname = gname
        pass

    return generate_output()