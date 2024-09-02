from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Arrangement

def nsargt_admin_arrangementbl(p_arrangement:str, p_argtnr:int):
    avail_arr = False
    arrangement = None

    arr1 = None

    Arr1 = Arrangement

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_arr, arrangement
        nonlocal arr1


        nonlocal arr1
        return {"avail_arr": avail_arr}


    arr1 = db_session.query(Arr1).filter(
            (func.lower(Arr1.arrangement) == (p_arrangement).lower()) &  (Arr1.argtnr != p_argtnr)).first()

    if arr1:
        avail_arr = True

    return generate_output()