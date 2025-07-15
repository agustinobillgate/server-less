#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Brief, Briefzei

def word_admin_btn_delnamebl(kateg:int, b_list_briefnr:int, recid_brief:int):
    t_brief_data = []
    brief = briefzei = None

    t_brief = None

    t_brief_data, T_brief = create_model_like(Brief, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_data, brief, briefzei
        nonlocal kateg, b_list_briefnr, recid_brief


        nonlocal t_brief
        nonlocal t_brief_data

        return {"t-brief": t_brief_data}

    brief = get_cache (Brief, {"_recid": [(eq, recid_brief)]})

    if brief:

        briefzei = get_cache (Briefzei, {"briefnr": [(eq, b_list_briefnr)],"briefzeilnr": [(eq, 1)]})

        if briefzei:
            db_session.delete(briefzei)
            pass
        pass
        db_session.delete(brief)
        pass

    for brief in db_session.query(Brief).filter(
             (Brief.briefkateg == kateg)).order_by(Brief.briefnr).all():
        t_brief = T_brief()
        t_brief_data.append(t_brief)

        buffer_copy(brief, t_brief)
        t_brief.rec_id = brief._recid

    return generate_output()