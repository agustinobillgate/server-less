#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Briefzei

def write_briefzeibl(case_type:int, int1:int, int2:int, int3:int, char1:string, word_exist:bool):

    prepare_cache ([Briefzei])

    success_flag = False
    briefzei = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, briefzei
        nonlocal case_type, int1, int2, int3, char1, word_exist

        return {"success_flag": success_flag}


    if case_type == 1:

        if not word_exist:
            briefzei = Briefzei()
            db_session.add(briefzei)

            briefzei.briefnr = int1
            briefzei.briefzeilnr = int2
            pass
        else:

            briefzei = get_cache (Briefzei, {"briefnr": [(eq, int1)]})
        briefzei.texte = char1
        pass
        success_flag = True

    return generate_output()