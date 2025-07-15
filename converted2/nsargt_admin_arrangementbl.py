#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Arrangement

def nsargt_admin_arrangementbl(p_arrangement:string, p_argtnr:int):
    avail_arr = False
    arrangement = None

    arr1 = None

    Arr1 = create_buffer("Arr1",Arrangement)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_arr, arrangement
        nonlocal p_arrangement, p_argtnr
        nonlocal arr1


        nonlocal arr1

        return {"avail_arr": avail_arr}


    arr1 = db_session.query(Arr1).filter(
             (Arr1.arrangement == (p_arrangement).lower()) & (Arr1.argtnr != p_argtnr)).first()

    if arr1:
        avail_arr = True

    return generate_output()