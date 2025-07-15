#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

setup_list_data, Setup_list = create_model("Setup_list", {"payment":string, "statistic":string, "outlets":string})

def setup_new_drrbl(setup_list_data:[Setup_list]):

    prepare_cache ([Queasy])

    queasy = None

    setup_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal setup_list

        return {}

    setup_list = query(setup_list_data, first=True)

    if setup_list:

        queasy = get_cache (Queasy, {"key": [(eq, 265)]})

        if queasy:
            pass
            queasy.char1 = ""
            queasy.char2 = ""
            queasy.char3 = ""


            queasy.char1 = setup_list.payment
            queasy.char2 = setup_list.statistic
            queasy.char3 = setup_list.outlets


            pass
            pass
        else:
            queasy = Queasy()
            db_session.add(queasy)

            queasy.key = 265
            queasy.char1 = setup_list.payment
            queasy.char2 = setup_list.statistic
            queasy.char3 = setup_list.outlets

    return generate_output()