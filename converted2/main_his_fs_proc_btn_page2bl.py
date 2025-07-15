#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Zwkum

def main_his_fs_proc_btn_page2bl():

    prepare_cache ([Htparam])

    lavail = False
    htparam = zwkum = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lavail, htparam, zwkum

        return {"lavail": lavail}

    lavail = False

    htparam = get_cache (Htparam, {"paramnr": [(eq, 900)]})

    if htparam:

        zwkum = get_cache (Zwkum, {"departement": [(eq, htparam.finteger)],"zknr": [(lt, 100)]})

        if zwkum:
            lavail = True

    return generate_output()