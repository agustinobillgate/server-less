from functions.additional_functions import *
import decimal
from models import Briefzei, Gl_main

def gl_wordvi_choose_btnbl(case_type:str, int1:int):
    char1 = ""
    briefzei = gl_main = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal char1, briefzei, gl_main
        nonlocal case_type, int1


        return {"char1": char1}


    if case_type.lower()  == ("btn-insert").lower() :

        briefzei = db_session.query(Briefzei).filter(
                 (Briefzei.briefnr == int1) & (Briefzei.briefzeilnr == 1)).first()

        if briefzei:
            char1 = briefzei.texte

    elif case_type.lower()  == ("btn-glmain").lower() :

        gl_main = db_session.query(Gl_main).filter(
                 (Gl_main.nr == int1)).first()
        char1 = to_string(gl_main.code)

    return generate_output()