#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import L_lieferant

def prepare_ap_debtlistbl():
    gst_flag = False
    l_lieferant = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gst_flag, l_lieferant

        return {"gst_flag": gst_flag}


    l_lieferant = get_cache (L_lieferant, {"firma": [(eq, "gst")]})

    if l_lieferant:
        gst_flag = True


    else:
        gst_flag = False

    return generate_output()