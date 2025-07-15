#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from functions.delete_paramtextbl import delete_paramtextbl
from models import Brief

def wordcateg_admin_btn_delbl(int1:int, int2:int, int3:int):
    success_flag = False
    brief = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, brief
        nonlocal int1, int2, int3

        return {"success_flag": success_flag}


    brief = db_session.query(Brief).filter(
             ((Brief.briefkateg + 600) == int1)).first()

    if brief:

        return generate_output()
    else:
        success_flag = get_output(delete_paramtextbl(1, int1, int2, int3))

    return generate_output()