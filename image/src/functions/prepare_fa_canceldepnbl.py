from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate

def prepare_fa_canceldepnbl():
    datum = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal datum


        return {"datum": datum}

    datum = get_output(htpdate(881))

    return generate_output()