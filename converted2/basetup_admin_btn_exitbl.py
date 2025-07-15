#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_setup

ba_list_data, Ba_list = create_model_like(Bk_setup)

def basetup_admin_btn_exitbl(ba_list_data:[Ba_list], icase:int, recid_bk_setup:int):

    prepare_cache ([Bk_setup])

    bk_setup = None

    ba_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_setup
        nonlocal icase, recid_bk_setup


        nonlocal ba_list

        return {}

    def fill_new_bk_setup():

        nonlocal bk_setup
        nonlocal icase, recid_bk_setup


        nonlocal ba_list


        bk_setup.setup_id = ba_list.setup_id
        bk_setup.bezeichnung = ba_list.bezeichnung


    ba_list = query(ba_list_data, first=True)

    if icase == 1:
        bk_setup = Bk_setup()
        db_session.add(bk_setup)

        fill_new_bk_setup()
        pass
    else:

        bk_setup = get_cache (Bk_setup, {"_recid": [(eq, recid_bk_setup)]})

        if bk_setup:
            pass
            bk_setup.bezeichnung = ba_list.bezeichnung


            pass
            pass

    return generate_output()