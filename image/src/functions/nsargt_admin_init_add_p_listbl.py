from functions.additional_functions import *
import decimal
from models import Arrangement

def nsargt_admin_init_add_p_listbl():
    i = 0
    arrangement = None

    arr = None

    Arr = Arrangement

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, arrangement
        nonlocal arr


        nonlocal arr
        return {"i": i}


    for arr in db_session.query(Arr).all():

        if i < arr.argtnr:
            i = arr.argtnr
    i = i + 1

    return generate_output()