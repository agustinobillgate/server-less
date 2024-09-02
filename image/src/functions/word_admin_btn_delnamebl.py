from functions.additional_functions import *
import decimal
from models import Brief, Briefzei

def word_admin_btn_delnamebl(kateg:int, b_list_briefnr:int, recid_brief:int):
    t_brief_list = []
    brief = briefzei = None

    t_brief = None

    t_brief_list, T_brief = create_model_like(Brief, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_list, brief, briefzei


        nonlocal t_brief
        nonlocal t_brief_list
        return {"t-brief": t_brief_list}

    brief = db_session.query(Brief).filter(
            (Brief._recid == recid_brief)).first()

    briefzei = db_session.query(Briefzei).filter(
            (Briefzei.briefnr == b_list_briefnr) &  (Briefzeilnr == 1)).first()

    if briefzei:
        db_session.delete(briefzei)

    brief = db_session.query(Brief).first()
    db_session.delete(brief)

    for brief in db_session.query(Brief).filter(
            (Briefkateg == kateg)).all():
        t_brief = T_brief()
        t_brief_list.append(t_brief)

        buffer_copy(brief, t_brief)
        t_brief.rec_id = brief._recid

    return generate_output()