#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Brief

def read_brief1bl(case_type:int, int1:int, int2:int, int3:int, char1:string, char2:string):
    t_brief_list = []
    brief = None

    t_brief = None

    t_brief_list, T_brief = create_model_like(Brief)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_list, brief
        nonlocal case_type, int1, int2, int3, char1, char2


        nonlocal t_brief
        nonlocal t_brief_list

        return {"t-brief": t_brief_list}

    def assign_it():

        nonlocal t_brief_list, brief
        nonlocal case_type, int1, int2, int3, char1, char2


        nonlocal t_brief
        nonlocal t_brief_list


        t_brief = T_brief()
        t_brief_list.append(t_brief)

        buffer_copy(brief, t_brief)


    if case_type == 1:

        brief = get_cache (Brief, {"briefbezeich": [(eq, char1)],"briefnr": [(ne, int1)]})

        if brief:
            assign_it()
    elif case_type == 2:

        for brief in db_session.query(Brief).filter(
                 (Brief.briefkateg == int1)).order_by(Brief._recid).all():
            assign_it()
    elif case_type == 3:

        brief = get_cache (Brief, {"briefkateg": [(eq, int1 - 600)]})

        if brief:
            assign_it()
    elif case_type == 4:

        brief = get_cache (Brief, {"briefbezeich": [(eq, char1)],"briefnr": [(ne, int1)],"briefkateg": [(eq, int2)]})

        if brief:
            assign_it()
    elif case_type == 5:

        for brief in db_session.query(Brief).order_by(Brief._recid).all():
            assign_it()
    elif case_type == 6:

        brief = get_cache (Brief, {"briefnr": [(eq, int1)]})

        if brief:
            assign_it()

    return generate_output()