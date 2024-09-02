from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate

def prepare_fa_upgradelistbl():
    p_110 = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal p_110


        return {"p_110": p_110}

    p_110 = get_output(htpdate(110))

    return generate_output()