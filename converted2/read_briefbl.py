#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Brief

def read_briefbl(briefno:int, grpno:int):
    t_brief_data = []
    brief = None

    t_brief = None

    t_brief_data, T_brief = create_model_like(Brief)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_data, brief
        nonlocal briefno, grpno


        nonlocal t_brief
        nonlocal t_brief_data

        return {"t-brief": t_brief_data}

    if briefno != 0 and (grpno == 0 or grpno == None):

        brief = get_cache (Brief, {"briefnr": [(eq, briefno)]})

        if brief:
            t_brief = T_brief()
            t_brief_data.append(t_brief)

            buffer_copy(brief, t_brief)

    elif grpno != 0:

        if briefno != 0:

            brief = get_cache (Brief, {"briefkateg": [(eq, grpno)],"briefnr": [(eq, briefno)]})

            if brief:
                t_brief = T_brief()
                t_brief_data.append(t_brief)

                buffer_copy(brief, t_brief)
        else:

            for brief in db_session.query(Brief).filter(
                     (Brief.briefkateg == grpno)).order_by(Brief.briefnr).all():
                t_brief = T_brief()
                t_brief_data.append(t_brief)

                buffer_copy(brief, t_brief)

    return generate_output()