#using conversion tools version: 1.0.0.119
"""_yusufwijasena_13/11/2025

    Ticket ID: 62BADE
        _remark_:   - fix python indentation
                    - only convert to py
"""
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy

def if_lodgiq_check_na_flagbl():

    prepare_cache ([Htparam, Queasy])

    na_flag = False
    p_110:date = None
    htparam = queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal na_flag, p_110, htparam, queasy

        return {
            "na_flag": na_flag
        }


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    p_110 = htparam.fdate

    queasy = get_cache (Queasy, {"key": [(eq, 297)]})

    if queasy:
        if queasy.date1 < p_110:
            queasy.date1 = p_110
            na_flag = True
        else:
            na_flag = False
    else:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 297
        queasy.date1 = p_110
        queasy.logi1 = False

    return generate_output()