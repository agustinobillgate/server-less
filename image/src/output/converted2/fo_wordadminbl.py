#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Brief, Htparam, Paramtext, Guestbook

def fo_wordadminbl():

    prepare_cache ([Htparam, Paramtext])

    kateg = 0
    kategbezeich = ""
    briefnr = 0
    t_brief_list = []
    brief = htparam = paramtext = guestbook = None

    t_brief = None

    t_brief_list, T_brief = create_model_like(Brief)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal kateg, kategbezeich, briefnr, t_brief_list, brief, htparam, paramtext, guestbook


        nonlocal t_brief
        nonlocal t_brief_list

        return {"kateg": kateg, "kategbezeich": kategbezeich, "briefnr": briefnr, "t-brief": t_brief_list}

    def createguestno(letterno:int):

        nonlocal kateg, kategbezeich, briefnr, t_brief_list, brief, htparam, paramtext, guestbook


        nonlocal t_brief
        nonlocal t_brief_list

        outstr:string = ""
        i:int = 0
        outstr = to_string(letterno)
        for i in range(1,8 - length(to_string(letterno))  + 1) :
            outstr = "0" + outstr
        outstr = "-2" + outstr
        return outstr

    t_brief_list.clear()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 433)]})
    kateg = htparam.finteger

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, (kateg + 600))]})
    kategbezeich = paramtext.ptexte
    briefnr = 0

    for brief in db_session.query(Brief).filter(
             (Brief.briefkateg == kateg)).order_by(Brief.briefnr).all():
        t_brief = T_brief()
        t_brief_list.append(t_brief)


        guestbook = get_cache (Guestbook, {"gastnr": [(eq, int (createguestno (brief.briefnr)))]})

        if not guestbook:
            buffer_copy(brief, t_brief)
        else:
            buffer_copy(brief, t_brief)
            t_brief.fname = "(CLOUD) " + brief.fname

        if brief.briefnr > briefnr:
            briefnr = brief.briefnr

    for brief in db_session.query(Brief).order_by(Brief.briefnr).all():

        if brief.briefnr > briefnr:
            briefnr = brief.briefnr
    briefnr = briefnr + 1

    return generate_output()