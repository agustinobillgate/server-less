#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_maintain

def eg_maincalendardel_reqactbl(smaintain_maintainnr:int):

    prepare_cache ([Eg_maintain])

    flag = 0
    eg_maintain = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, eg_maintain
        nonlocal smaintain_maintainnr

        return {"flag": flag}


    eg_maintain = get_cache (Eg_maintain, {"maintainnr": [(eq, smaintain_maintainnr)]})

    if eg_maintain:
        eg_maintain.delete_flag = False
        eg_maintain.cancel_date = None
        flag = 1

    return generate_output()