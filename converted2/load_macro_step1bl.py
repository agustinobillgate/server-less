#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters, Gl_acct, Artikel

def load_macro_step1bl(briefnr:int):

    prepare_cache ([Gl_acct])

    coa_list_data = []
    art_list_data = []
    vstring:string = ""
    i:int = 0
    j:int = 0
    parameters = gl_acct = artikel = None

    coa_list = art_list = parambuff = None

    coa_list_data, Coa_list = create_model("Coa_list", {"fibukonto":string, "anzahl":int})
    art_list_data, Art_list = create_model("Art_list", {"code":string})

    Parambuff = create_buffer("Parambuff",Parameters)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal coa_list_data, art_list_data, vstring, i, j, parameters, gl_acct, artikel
        nonlocal briefnr
        nonlocal parambuff


        nonlocal coa_list, art_list, parambuff
        nonlocal coa_list_data, art_list_data

        return {"coa-list": coa_list_data, "art-list": art_list_data}


    coa_list = query(coa_list_data, first=True)

    if not coa_list:

        for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
            coa_list = Coa_list()
            coa_list_data.append(coa_list)

            coa_list.fibukonto = gl_acct.fibukonto


    else:

        for coa_list in query(coa_list_data, filters=(lambda coa_list: coa_list.anzahl != 0)):
            coa_list.anzahl = 0

    art_list_data.clear()

    for artikel in db_session.query(Artikel).order_by(Artikel._recid).all():
        art_list = Art_list()
        art_list_data.append(art_list)

        art_list.code = to_string(departement, "99") + to_string(artnr, "9999")

    parameters = get_cache (Parameters, {"progname": [(eq, "gl-macro")],"section": [(eq, to_string(briefnr))]})
    while None != parameters:

        parambuff = db_session.query(Parambuff).filter(
                     (Parambuff._recid == parameters._recid)).first()
        db_session.delete(parambuff)

        curr_recid = parameters._recid
        parameters = db_session.query(Parameters).filter(
                 (Parameters.progname == ("GL-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (Parameters._recid > curr_recid)).first()

    return generate_output()