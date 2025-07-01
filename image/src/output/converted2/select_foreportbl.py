#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Brief, Htparam

def select_foreportbl():

    prepare_cache ([Htparam])

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

    htparam = get_cache (Htparam, {"paramnr": [(eq, 433)]})
    fo_nr = htparam.finteger

    for brief in db_session.query(Brief).filter(
             (Brief.briefkateg == fo_nr)).order_by(Brief.briefnr).all():
        t_brief = T_brief()
        t_brief_list.append(t_brief)

        buffer_copy(brief, t_brief)

    return generate_output()