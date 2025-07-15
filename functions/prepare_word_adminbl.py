#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Brief, Paramtext

def prepare_word_adminbl(kateg:int):

    prepare_cache ([Paramtext])

    kategbezeich = ""
    t_brief_data = []
    kategnr:int = 0
    brief = paramtext = None

    t_brief = None

    t_brief_data, T_brief = create_model_like(Brief, {"rec_id":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kategbezeich, t_brief_data, kategnr, brief, paramtext
        nonlocal kateg


        nonlocal t_brief
        nonlocal t_brief_data

        return {"kategbezeich": kategbezeich, "t-brief": t_brief_data}

    if kateg != None:
        kategnr = kateg + 600
    else:
        kateg = 0

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, (kateg + 600))]})

    if paramtext:
        kategbezeich = paramtext.ptexte

    for brief in db_session.query(Brief).filter(
             (Brief.briefkateg == kateg)).order_by(Brief.briefnr).all():
        t_brief = T_brief()
        t_brief_data.append(t_brief)

        buffer_copy(brief, t_brief)
        t_brief.rec_id = brief._recid

    return generate_output()