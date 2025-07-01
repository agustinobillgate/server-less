#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Brief

t_brief_list, T_brief = create_model_like(Brief)

def write_briefbl(case_type:int, t_brief_list:[T_brief]):
    success_flag = False
    brief = None

    t_brief = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, brief
        nonlocal case_type


        nonlocal t_brief

        return {"success_flag": success_flag}

    t_brief = query(t_brief_list, first=True)

    if not t_brief:

        return generate_output()

    if case_type == 1:
        brief = Brief()
        db_session.add(brief)

        buffer_copy(t_brief, brief)
        pass
        success_flag = True
    elif case_type == 2:

        brief = get_cache (Brief, {"briefnr": [(eq, t_brief.briefnr)]})

        if brief:
            buffer_copy(t_brief, brief)
            pass
            success_flag = True

    return generate_output()