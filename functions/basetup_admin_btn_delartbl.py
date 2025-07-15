#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_setup

def basetup_admin_btn_delartbl(recid_bk_setup:int):
    bk_setup = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bk_setup
        nonlocal recid_bk_setup

        return {}


    bk_setup = get_cache (Bk_setup, {"_recid": [(eq, recid_bk_setup)]})

    if bk_setup:

        bk_setup = db_session.query(Bk_setup).first()
        db_session.delete(bk_setup)

    return generate_output()