from functions.additional_functions import *
import decimal
from models import Brief, Paramtext

def prepare_word_adminbl(kateg:int):
    kategbezeich = ""
    t_brief_list = []
    brief = paramtext = None

    t_brief = None

    t_brief_list, T_brief = create_model_like(Brief, {"rec_id":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal kategbezeich, t_brief_list, brief, paramtext


        nonlocal t_brief
        nonlocal t_brief_list
        return {"kategbezeich": kategbezeich, "t-brief": t_brief_list}

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == (kateg + 600))).first()
    kategbezeich = paramtext.ptext

    for brief in db_session.query(Brief).filter(
            (Briefkateg == kateg)).all():
        t_brief = T_brief()
        t_brief_list.append(t_brief)

        buffer_copy(brief, t_brief)
        t_brief.rec_id = brief._recid

    return generate_output()