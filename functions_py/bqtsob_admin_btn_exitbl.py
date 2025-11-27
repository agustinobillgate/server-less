#using conversion tools version: 1.0.0.117
#-------------------------------------------------------
# Rd, 27/11/2025, with_for_update added
#-------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

queasy_list_data, Queasy_list = create_model_like(Queasy)

def bqtsob_admin_btn_exitbl(queasy_list_data:[Queasy_list], icase:int, recid_queasy:int):

    prepare_cache ([Queasy])

    queasy = None

    queasy_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal icase, recid_queasy


        nonlocal queasy_list

        return {}

    def fill_new_queasy():

        nonlocal queasy
        nonlocal icase, recid_queasy


        nonlocal queasy_list


        queasy.key = 151
        queasy.char1 = queasy_list.char1
        queasy.char3 = queasy_list.char3


    queasy_list = query(queasy_list_data, first=True)

    if icase == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()
    else:

        # queasy = get_cache (Queasy, {"_recid": [(eq, recid_queasy)]})
        queasy = db_session.query(Queasy).filter(
                 (Queasy._recid == recid_queasy)).with_for_update().first()
        queasy.char3 = queasy_list.char3
        pass

    return generate_output()