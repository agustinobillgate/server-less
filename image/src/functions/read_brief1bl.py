from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Brief

def read_brief1bl(case_type:int, int1:int, int2:int, int3:int, char1:str, char2:str):
    t_brief_list = []
    brief = None

    t_brief = None

    t_brief_list, T_brief = create_model_like(Brief)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_list, brief


        nonlocal t_brief
        nonlocal t_brief_list
        return {"t-brief": t_brief_list}

    def assign_it():

        nonlocal t_brief_list, brief


        nonlocal t_brief
        nonlocal t_brief_list


        t_brief = T_brief()
        t_brief_list.append(t_brief)

        buffer_copy(brief, t_brief)

    if case_type == 1:

        brief = db_session.query(Brief).filter(
                (func.lower(Briefbezeich) == (char1).lower()) &  (Briefnr != int1)).first()

        if brief:
            assign_it()
    elif case_type == 2:

        for brief in db_session.query(Brief).filter(
                (Briefkateg == int1)).all():
            assign_it()
    elif case_type == 3:

        brief = db_session.query(Brief).filter(
                ((Briefkateg + 600) == int1)).first()

        if brief:
            assign_it()
    elif case_type == 4:

        brief = db_session.query(Brief).filter(
                (func.lower(Briefbezeich) == (char1).lower()) &  (Briefnr != int1) &  (Briefkateg == int2)).first()

        if brief:
            assign_it()
    elif case_type == 5:

        for brief in db_session.query(Brief).all():
            assign_it()
    elif case_type == 6:

        brief = db_session.query(Brief).filter(
                (Briefnr == int1)).first()

        if brief:
            assign_it()

    return generate_output()