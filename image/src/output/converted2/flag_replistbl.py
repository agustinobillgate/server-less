#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Reslin_queasy

def flag_replistbl(s_resnr:int, s_reslinnr:int, s_ind:int, s_done:bool, s_recid:int):

    prepare_cache ([Reslin_queasy])

    reslin_queasy = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal reslin_queasy
        nonlocal s_resnr, s_reslinnr, s_ind, s_done, s_recid

        return {}


    reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, s_resnr)],"reslinnr": [(eq, s_reslinnr)],"_recid": [(eq, s_recid)]})

    if reslin_queasy:
        pass

        if s_ind == 1:
            reslin_queasy.deci1 =  to_decimal(to_int(s_done))

        elif s_ind == 2:
            reslin_queasy.deci2 =  to_decimal(to_int(s_done))

        elif s_ind == 3:
            reslin_queasy.deci3 =  to_decimal(to_int(s_done))
        pass

    return generate_output()