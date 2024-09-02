from functions.additional_functions import *
import decimal
from models import Brief

t_brief_list, T_brief = create_model_like(Brief)

def write_briefbl(case_type:int, t_brief_list:[T_brief]):
    success_flag = False
    brief = None
    t_brief = None
    db_session = local_storage.db_session

    def generate_output():
        nonlocal success_flag, brief
        nonlocal t_brief
        global t_brief_list
        return {"success_flag": success_flag}

    t_brief = query(t_brief_list, first=True)

    if not t_brief:
        return generate_output()

    if case_type == 1:
        brief = Brief()
        db_session.add(brief)
        buffer_copy(t_brief, brief)
        success_flag = True

    elif case_type == 2:
        brief = db_session.query(Brief).filter((Brief.briefnr == t_brief.briefnr)).first()

        if brief:
            buffer_copy(t_brief, brief)
            success_flag = True

    return generate_output()