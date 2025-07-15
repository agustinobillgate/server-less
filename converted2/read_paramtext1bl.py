#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Paramtext, Htparam, Zimkateg, Zimmer

def read_paramtext1bl(case_type:int, int1:int, int2:int, int3:int, char1:string):

    prepare_cache ([Htparam, Zimkateg])

    t_paramtext_data = []
    paramtext = htparam = zimkateg = zimmer = None

    t_paramtext = None

    t_paramtext_data, T_paramtext = create_model_like(Paramtext)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_paramtext_data, paramtext, htparam, zimkateg, zimmer
        nonlocal case_type, int1, int2, int3, char1


        nonlocal t_paramtext
        nonlocal t_paramtext_data

        return {"t-paramtext": t_paramtext_data}

    def assign_it():

        nonlocal t_paramtext_data, paramtext, htparam, zimkateg, zimmer
        nonlocal case_type, int1, int2, int3, char1


        nonlocal t_paramtext
        nonlocal t_paramtext_data


        t_paramtext = T_paramtext()
        t_paramtext_data.append(t_paramtext)

        buffer_copy(paramtext, t_paramtext)


    def filter_it():

        nonlocal t_paramtext_data, paramtext, htparam, zimkateg, zimmer
        nonlocal case_type, int1, int2, int3, char1


        nonlocal t_paramtext
        nonlocal t_paramtext_data

        zimkateg = get_cache (Zimkateg, {"kurzbez": [(eq, entry(0, char1, ";"))]})

        if not zimkateg:

            return

        for t_paramtext in query(t_paramtext_data):

            zimmer = get_cache (Zimmer, {"zikatnr": [(eq, zimkateg.zikatnr)],"setup": [(eq, t_paramtext.txtnr - 9200)]})

            if not zimmer:
                t_paramtext_data.remove(t_paramtext)


    if case_type == 1:

        paramtext = get_cache (Paramtext, {"ptexte": [(eq, char1)],"sprachcode": [(ne, int1)]})

        if paramtext:
            assign_it()
    elif case_type == 2:

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= int1) & (Paramtext.txtnr <= int2)).order_by(Paramtext._recid).all():
            assign_it()
    elif case_type == 3:

        paramtext = get_cache (Paramtext, {"ptexte": [(eq, char1)],"txtnr": [(ne, int1),(gt, int2)]})

        if paramtext:
            assign_it()
    elif case_type == 4:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 987)]})
        int1 = 600 + htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 433)]})
        int2 = 600 + htparam.finteger

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 601) & (Paramtext.txtnr <= 699) & (Paramtext.ptexte != "") & (Paramtext.txtnr != int1) & (Paramtext.txtnr != int2)).order_by(Paramtext._recid).all():
            assign_it()
    elif case_type == 5:

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 601) & (Paramtext.txtnr <= 699) & (Paramtext.ptexte != "")).order_by(Paramtext._recid).all():
            assign_it()
    elif case_type == 6:

        paramtext = get_cache (Paramtext, {"ptexte": [(eq, char1)],"txtnr": [(ne, int1)]})

        if paramtext:
            assign_it()
    elif case_type == 7:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, int1)]})

        if paramtext:
            assign_it()
    elif case_type == 8:

        paramtext = get_cache (Paramtext, {"txtnr": [(eq, int1)],"sprachcode": [(eq, int2)]})

        if paramtext:
            assign_it()
    elif case_type == 9:

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= int1) & (Paramtext.txtnr <= int2) & (Paramtext.ptexte != "")).order_by(Paramtext._recid).all():
            assign_it()
    elif case_type == 10:

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= int1) & (Paramtext.txtnr <= int2) & (Paramtext.ptexte != "")).order_by(Paramtext._recid).all():
            assign_it()
        filter_it()

    return generate_output()