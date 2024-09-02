from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate

def prepare_comp_stataccorbl():
    f_date = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal f_date


        return {"f_date": f_date}

    f_date = get_output(htpdate(87))

    return generate_output()