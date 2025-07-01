#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Briefzei, Gl_main

def gl_wordvi_choose_btnbl(case_type:string, int1:int):

    prepare_cache ([Briefzei, Gl_main])

    char1 = ""
    briefzei = gl_main = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal char1, briefzei, gl_main
        nonlocal case_type, int1

        return {"char1": char1}


    if case_type.lower()  == ("btn-insert").lower() :

        briefzei = get_cache (Briefzei, {"briefnr": [(eq, int1)],"briefzeilnr": [(eq, 1)]})

        if briefzei:
            char1 = briefzei.texte

    elif case_type.lower()  == ("btn-glmain").lower() :

        gl_main = get_cache (Gl_main, {"nr": [(eq, int1)]})
        char1 = to_string(gl_main.code)

    return generate_output()