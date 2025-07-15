#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import B_storno

def sales_activity_list_btnchgbl(resnr:int, str:string, outnr:int):

    prepare_cache ([B_storno])

    b_storno = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal b_storno
        nonlocal resnr, str, outnr

        return {}


    b_storno = get_cache (B_storno, {"bankettnr": [(eq, resnr)]})
    pass
    b_storno.grund[outnr - 1] = str
    pass

    return generate_output()