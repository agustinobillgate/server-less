#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

email_list_data, Email_list = create_model_like(Queasy)

def basetup_email_btn_exitbl(email_list_data:[Email_list], icase:int, recid_queasy:int):

    prepare_cache ([Queasy])

    queasy = None

    email_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal icase, recid_queasy


        nonlocal email_list

        return {}

    def fill_new_email_setup():

        nonlocal queasy
        nonlocal icase, recid_queasy


        nonlocal email_list


        queasy.key = 138
        queasy.number1 = email_list.number1
        queasy.char1 = email_list.char1
        queasy.char2 = email_list.char2


    email_list = query(email_list_data, first=True)

    if icase == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_email_setup()
    else:

        queasy = get_cache (Queasy, {"_recid": [(eq, recid_queasy)]})
        queasy.char1 = email_list.char1
        queasy.char2 = email_list.char2
        pass

    return generate_output()