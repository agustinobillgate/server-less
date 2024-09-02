from functions.additional_functions import *
import decimal
from models import Queasy

def basetup_email_btn_exitbl(email_list:[Email_list], icase:int, recid_queasy:int):
    queasy = None

    email_list = None

    email_list_list, Email_list = create_model_like(Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy


        nonlocal email_list
        nonlocal email_list_list
        return {}

    def fill_new_email_setup():

        nonlocal queasy


        nonlocal email_list
        nonlocal email_list_list


        queasy.key = 138
        queasy.number1 = email_list.number1
        queasy.char1 = email_list.char1
        queasy.char2 = email_list.char2

    email_list = query(email_list_list, first=True)

    if icase == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_email_setup()
    else:

        queasy = db_session.query(Queasy).filter(
                (Queasy._recid == recid_queasy)).first()
        queasy.char1 = email_list.char1
        queasy.char2 = email_list.char2

        queasy = db_session.query(Queasy).first()

    return generate_output()