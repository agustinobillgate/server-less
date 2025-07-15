#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Brief

def load_briefbl(briefno:int):
    t_brief_data = []
    brief = None

    t_brief = None

    t_brief_data, T_brief = create_model_like(Brief)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_data, brief
        nonlocal briefno


        nonlocal t_brief
        nonlocal t_brief_data

        return {"t-brief": t_brief_data}

    for brief in db_session.query(Brief).filter(
             (Brief.briefkateg == briefno)).order_by(Brief._recid).all():
        t_brief = T_brief()
        t_brief_data.append(t_brief)

        buffer_copy(brief, t_brief)

    return generate_output()