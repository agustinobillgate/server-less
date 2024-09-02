from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Parameters, Gl_acct, Artikel

def load_macro_step1bl(briefnr:int):
    coa_list_list = []
    art_list_list = []
    vstring:str = ""
    i:int = 0
    j:int = 0
    parameters = gl_acct = artikel = None

    coa_list = art_list = parambuff = None

    coa_list_list, Coa_list = create_model("Coa_list", {"fibukonto":str, "anzahl":int})
    art_list_list, Art_list = create_model("Art_list", {"code":str})

    Parambuff = Parameters

    db_session = local_storage.db_session

    def generate_output():
        nonlocal coa_list_list, art_list_list, vstring, i, j, parameters, gl_acct, artikel
        nonlocal parambuff


        nonlocal coa_list, art_list, parambuff
        nonlocal coa_list_list, art_list_list
        return {"coa-list": coa_list_list, "art-list": art_list_list}


    coa_list = query(coa_list_list, first=True)

    if not coa_list:

        for gl_acct in db_session.query(Gl_acct).all():
            coa_list = Coa_list()
            coa_list_list.append(coa_list)

            coa_list.fibukonto = gl_acct.fibukonto


    else:

        for coa_list in query(coa_list_list, filters=(lambda coa_list :coa_list.anzahl != 0)):
            coa_list.anzahl = 0

    art_list_list.clear()

    for artikel in db_session.query(Artikel).all():
        art_list = Art_list()
        art_list_list.append(art_list)

        art_list.CODE = to_string(departement, "99") + to_string(artnr, "9999")

    parameters = db_session.query(Parameters).filter(
            (func.lower(Parameters.progname) == "GL_Macro") &  (Parameters.SECTION == to_string(briefnr))).first()
    while None != parameters:

        parambuff = db_session.query(Parambuff).filter(
                    (Parambuff._recid == parameters._recid)).first()
        db_session.delete(parambuff)


        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "GL_Macro") &  (Parameters.SECTION == to_string(briefnr))).first()

    return generate_output()