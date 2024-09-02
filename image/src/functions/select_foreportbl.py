from functions.additional_functions import *
import decimal
from models import Brief, Htparam

def select_foreportbl():
    t_brief_list = []
    fo_nr:int = 0
    brief = htparam = None

    t_brief = None

    t_brief_list, T_brief = create_model_like(Brief)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_list, fo_nr, brief, htparam


        nonlocal t_brief
        nonlocal t_brief_list
        return {"t-brief": t_brief_list}

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 433)).first()
    fo_nr = htparam.finteger

    for brief in db_session.query(Brief).filter(
            (Briefkateg == fo_nr)).all():
        t_brief = T_brief()
        t_brief_list.append(t_brief)

        buffer_copy(brief, t_brief)

    return generate_output()