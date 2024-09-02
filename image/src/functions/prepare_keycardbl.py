from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpchar import htpchar

def prepare_keycardbl():
    ci_date = None
    fintimeto = ""
    t_ch_gvccardprogram = ""


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, fintimeto, t_ch_gvccardprogram


        return {"ci_date": ci_date, "fintimeto": fintimeto, "t_ch_gvccardprogram": t_ch_gvccardprogram}

    ci_date = get_output(htpdate(87))
    fintimeto = get_output(htpchar(925))
    t_ch_gvccardprogram = get_output(htpchar(921))

    return generate_output()