#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Arrangement

def nsargt_admin_init_add_p_listbl():

    prepare_cache ([Arrangement])

    i = 0
    arrangement = None

    arr = None

    Arr = create_buffer("Arr",Arrangement)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, arrangement
        nonlocal arr


        nonlocal arr

        return {"i": i}


    for arr in db_session.query(Arr).order_by(Arr._recid).all():

        if i < arr.argtnr:
            i = arr.argtnr
    i = i + 1

    return generate_output()