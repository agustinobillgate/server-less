#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Brief, Briefzei

def get_letter_setup_webbl(briefnr:int):

    prepare_cache ([Briefzei])

    t_brief_list = []
    brief = briefzei = None

    t_brief = None

    t_brief_list, T_brief = create_model_like(Brief, {"efield":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_list, brief, briefzei
        nonlocal briefnr


        nonlocal t_brief
        nonlocal t_brief_list

        return {"t-brief": t_brief_list}

    brief = get_cache (Brief, {"briefnr": [(eq, briefnr)]})

    if brief:
        t_brief = T_brief()
        t_brief_list.append(t_brief)

        buffer_copy(brief, t_brief)

        briefzei = get_cache (Briefzei, {"briefnr": [(eq, briefnr)],"briefzeilnr": [(eq, 1)]})

        if briefzei:
            t_brief.efield = briefzei.texte

    return generate_output()