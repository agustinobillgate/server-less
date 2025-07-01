#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Brief, Paramtext

def load_all_letter_adminbl():

    prepare_cache ([Paramtext])

    t_brief_list = []
    kateg:int = 0
    brief = paramtext = None

    t_brief = None

    t_brief_list, T_brief = create_model_like(Brief, {"rec_id":int, "category":int, "category_str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_list, kateg, brief, paramtext


        nonlocal t_brief
        nonlocal t_brief_list

        return {"t-brief": t_brief_list}

    for paramtext in db_session.query(Paramtext).filter(
             (Paramtext.txtnr >= 601) & (Paramtext.txtnr <= 699) & (Paramtext.ptexte != "")).order_by(Paramtext._recid).all():
        kateg = (paramtext.txtnr - 600)

        for brief in db_session.query(Brief).filter(
                 (Brief.briefkateg == kateg)).order_by(Brief.briefkateg, Brief.briefnr).all():
            t_brief = T_brief()
            t_brief_list.append(t_brief)

            buffer_copy(brief, t_brief)
            t_brief.rec_id = brief._recid
            t_brief.category = kateg
            t_brief.category_str = paramtext.ptexte

    return generate_output()