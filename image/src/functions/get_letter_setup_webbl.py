from functions.additional_functions import *
import decimal
from models import Brief, Briefzei

def get_letter_setup_webbl(briefnr:int):
    t_brief_list = []
    brief = briefzei = None

    t_brief = None

    t_brief_list, T_brief = create_model_like(Brief, {"efield":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_brief_list, brief, briefzei


        nonlocal t_brief
        nonlocal t_brief_list
        return {"t-brief": t_brief_list}

    brief = db_session.query(Brief).filter(
            (briefnr == briefnr)).first()

    if brief:
        t_brief = T_brief()
        t_brief_list.append(t_brief)

        buffer_copy(brief, t_brief)

        briefzei = db_session.query(Briefzei).filter(
                (Briefzei.briefnr == briefnr) &  (Briefzei.briefzeilnr == 1)).first()

        if briefzei:
            t_brief.efield = briefzei.texte

    return generate_output()