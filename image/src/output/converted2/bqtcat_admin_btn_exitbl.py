#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

queasy_list_list, Queasy_list = create_model_like(Queasy)

def bqtcat_admin_btn_exitbl(queasy_list_list:[Queasy_list], icase:int, recid_queasy:int):

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


        queasy.key = 150
        queasy.char1 = queasy_list.char1
        queasy.char3 = queasy_list.char3


    queasy_list = query(queasy_list_list, first=True)

    if icase == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()
    else:

        queasy = get_cache (Queasy, {"_recid": [(eq, recid_queasy)]})
        queasy.char3 = queasy_list.char3
        pass

    return generate_output()