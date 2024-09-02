from functions.additional_functions import *
import decimal
from models import Brief, Htparam, Paramtext, Guestbook

def fo_wordadminbl():
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

    def createGuestno(letterno:int):

        nonlocal kateg, kategbezeich, briefnr, t_brief_list, brief, htparam, paramtext, guestbook


        nonlocal t_brief
        nonlocal t_brief_list

        outstr:str = ""
        i:int = 0
        outstr = to_string(letterno)
        for i in range(1,8 - len(to_string(letterno))  + 1) :
            outstr = "0" + outstr
        outstr = "-2" + outstr
        return outstr


    t_brief_list.clear()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 433)).first()
    kateg = htparam.finteger

    paramtext = db_session.query(Paramtext).filter(
            (Paramtext.txtnr == (kateg + 600))).first()
    kategbezeich = paramtext.ptext
    briefnr = 0

    for brief in db_session.query(Brief).filter(
            (Briefkateg == kateg)).all():
        t_brief = T_brief()
        t_brief_list.append(t_brief)


        guestbook = db_session.query(Guestbook).filter(
                (Guestbook.gastnr == int (createGuestno (briefnr)))).first()

        if not guestbook:
            buffer_copy(brief, t_brief)
        else:
            buffer_copy(brief, t_brief)
            t_brief.FNAME = "(CLOUD) " + brief.fname

        if briefnr > briefnr:
            briefnr = briefnr

    for brief in db_session.query(Brief).all():

        if briefnr > briefnr:
            briefnr = briefnr
    briefnr = briefnr + 1

    return generate_output()