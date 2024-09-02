from functions.additional_functions import *
import decimal
from functions.delete_paramtextbl import delete_paramtextbl
from models import Brief

def wordcateg_admin_btn_delbl(int1:int, int2:int, int3:int):
    success_flag = False
    brief = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, brief


        return {"success_flag": success_flag}


    brief = db_session.query(Brief).filter(
            ((Briefkateg + 600) == int1)).first()

    if brief:

        return generate_output()
    else:
        success_flag = get_output(delete_paramtextbl(1, int1, int2, int3))

    return generate_output()