from functions.additional_functions import *
import decimal
from models import Queasy

queasy_list_list, Queasy_list = create_model_like(Queasy)

def bqtcat_admin_btn_exitbl(queasy_list_list:[Queasy_list], icase:int, recid_queasy:int):
    queasy = None

    queasy_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal queasy
        nonlocal icase, recid_queasy


        nonlocal queasy_list
        nonlocal queasy_list_list
        return {}

    def fill_new_queasy():

        nonlocal queasy
        nonlocal icase, recid_queasy


        nonlocal queasy_list
        nonlocal queasy_list_list


        queasy.key = 150
        queasy.char1 = queasy_list.char1
        queasy.char3 = queasy_list.char3


    queasy_list = query(queasy_list_list, first=True)

    if icase == 1:
        queasy = Queasy()
        db_session.add(queasy)

        fill_new_queasy()
    else:

        queasy = db_session.query(Queasy).filter(
                 (Queasy._recid == recid_queasy)).first()
        queasy.char3 = queasy_list.char3

    return generate_output()