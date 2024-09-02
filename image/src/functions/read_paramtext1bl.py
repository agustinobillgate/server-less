from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Paramtext, Htparam, Zimkateg, Zimmer

def read_paramtext1bl(case_type:int, int1:int, int2:int, int3:int, char1:str):
    t_paramtext_list = []
    paramtext = htparam = zimkateg = zimmer = None

    t_paramtext = None

    t_paramtext_list, T_paramtext = create_model_like(Paramtext)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_paramtext_list, paramtext, htparam, zimkateg, zimmer


        nonlocal t_paramtext
        nonlocal t_paramtext_list
        return {"t-paramtext": t_paramtext_list}

    def assign_it():

        nonlocal t_paramtext_list, paramtext, htparam, zimkateg, zimmer


        nonlocal t_paramtext
        nonlocal t_paramtext_list


        t_paramtext = T_paramtext()
        t_paramtext_list.append(t_paramtext)

        buffer_copy(paramtext, t_paramtext)

    def filter_it():

        nonlocal t_paramtext_list, paramtext, htparam, zimkateg, zimmer


        nonlocal t_paramtext
        nonlocal t_paramtext_list

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.kurzbez == entry(0, char1, ";"))).first()

        if not zimkateg:

            return

        for t_paramtext in query(t_paramtext_list):

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zikatnr == zimkateg.zikatnr) &  (Zimmer.setup == t_paramtext.txtnr - 9200)).first()

            if not zimmer:
                t_paramtext_list.remove(t_paramtext)

    if case_type == 1:

        paramtext = db_session.query(Paramtext).filter(
                (func.lower(Paramtext.ptexte) == (char1).lower()) &  (Paramtext.sprachcode != int1)).first()

        if paramtext:
            assign_it()
    elif case_type == 2:

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= int1) &  (Paramtext.txtnr <= int2)).all():
            assign_it()
    elif case_type == 3:

        paramtext = db_session.query(Paramtext).filter(
                (func.lower(Paramtext.ptexte) == (char1).lower()) &  (Paramtext.txtnr != int1) &  (Paramtext.txtnr > int2)).first()

        if paramtext:
            assign_it()
    elif case_type == 4:

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 987)).first()
        int1 = 600 + htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 433)).first()
        int2 = 600 + htparam.finteger

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 601) &  (Paramtext.txtnr <= 699) &  (Paramtext.ptexte != "") &  (Paramtext.txtnr != int1) &  (Paramtext.txtnr != int2)).all():
            assign_it()
    elif case_type == 5:

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 601) &  (Paramtext.txtnr <= 699) &  (Paramtext.ptexte != "")).all():
            assign_it()
    elif case_type == 6:

        paramtext = db_session.query(Paramtext).filter(
                (func.lower(Paramtext.ptexte) == (char1).lower()) &  (Paramtext.txtnr != int1)).first()

        if paramtext:
            assign_it()
    elif case_type == 7:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == int1)).first()

        if paramtext:
            assign_it()
    elif case_type == 8:

        paramtext = db_session.query(Paramtext).filter(
                (Paramtext.txtnr == int1) &  (Paramtext.sprachcode == int2)).first()

        if paramtext:
            assign_it()
    elif case_type == 9:

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= int1) &  (Paramtext.txtnr <= int2) &  (Paramtext.ptexte != "")).all():
            assign_it()
    elif case_type == 10:

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= int1) &  (Paramtext.txtnr <= int2) &  (Paramtext.ptexte != "")).all():
            assign_it()
        filter_it()

    return generate_output()