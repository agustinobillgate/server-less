from functions.additional_functions import *
import decimal
from models import Bk_setup

ba_list_list, Ba_list = create_model_like(Bk_setup)

def basetup_admin_btn_exitbl(ba_list_list:[Ba_list], icase:int, recid_bk_setup:int):
    bk_setup = None

    ba_list = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_setup
        nonlocal icase, recid_bk_setup


        nonlocal ba_list
        nonlocal ba_list_list
        return {}

    def fill_new_bk_setup():

        nonlocal bk_setup
        nonlocal icase, recid_bk_setup


        nonlocal ba_list
        nonlocal ba_list_list


        bk_setup.setup_id = ba_list.setup_id
        bk_setup.bezeichnung = ba_list.bezeich


    ba_list = query(ba_list_list, first=True)

    if icase == 1:
        bk_setup = Bk_setup()
        db_session.add(bk_setup)

        fill_new_bk_setup()
    else:

        bk_setup = db_session.query(Bk_setup).filter(
                 (Bk_setup._recid == recid_bk_setup)).first()
        bk_setup.bezeichnung = ba_list.bezeich

    return generate_output()