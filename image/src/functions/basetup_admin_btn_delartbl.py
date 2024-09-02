from functions.additional_functions import *
import decimal
from models import Bk_setup

def basetup_admin_btn_delartbl(recid_bk_setup:int):
    bk_setup = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_setup


        return {}


    bk_setup = db_session.query(Bk_setup).filter(
            (Bk_setup._recid == recid_bk_setup)).first()
    db_session.delete(bk_setup)


    return generate_output()