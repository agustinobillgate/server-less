#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Briefzei, Htparam, Brief

def prepare_gl_wordvibl(briefnr:int):

    prepare_cache ([Htparam, Brief])

    gl_file = False
    htp_list_list = []
    t_briefzei_list = []
    gl_nr:int = 0
    briefzei = htparam = brief = None

    htp_list = t_briefzei = None

    htp_list_list, Htp_list = create_model("Htp_list", {"nr":int, "fchar":string, "bezeich":string})
    t_briefzei_list, T_briefzei = create_model_like(Briefzei)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gl_file, htp_list_list, t_briefzei_list, gl_nr, briefzei, htparam, brief
        nonlocal briefnr


        nonlocal htp_list, t_briefzei
        nonlocal htp_list_list, t_briefzei_list

        return {"gl_file": gl_file, "htp-list": htp_list_list, "t-briefzei": t_briefzei_list}

    def create_list():

        nonlocal gl_file, htp_list_list, t_briefzei_list, gl_nr, briefzei, htparam, brief
        nonlocal briefnr


        nonlocal htp_list, t_briefzei
        nonlocal htp_list_list, t_briefzei_list

        keychar:string = ""

        htparam = get_cache (Htparam, {"paramnr": [(eq, 987)]})
        gl_nr = htparam.finteger

        brief = get_cache (Brief, {"briefnr": [(eq, briefnr)]})

        htparam = get_cache (Htparam, {"paramnr": [(eq, 600)]})
        keychar = htparam.fchar

        if brief.briefkateg == gl_nr:
            gl_file = True

            for htparam in db_session.query(Htparam).filter(
                     (Htparam.paramgruppe == 39) & (Htparam.paramnr != 2030)).order_by(Htparam.fchar).all():
                htp_list = Htp_list()
                htp_list_list.append(htp_list)

                htp_list.nr = htparam.paramnr

                if substring(htparam.fchar, 0, 1) == (".").lower() :
                    htp_list.fchar = htparam.fchar
                else:
                    htp_list.fchar = keychar + htparam.fchar
                htp_list.bezeich = htparam.bezeichnung
        else:

            for htparam in db_session.query(Htparam).filter(
                     (Htparam.paramgruppe == 17)).order_by(Htparam.reihenfolge).all():
                htp_list = Htp_list()
                htp_list_list.append(htp_list)

                htp_list.nr = htparam.paramnr
                htp_list.fchar = keychar + htparam.fchar
                htp_list.bezeich = htparam.bezeichnung


    create_list()

    for briefzei in db_session.query(Briefzei).order_by(Briefzei._recid).all():
        t_briefzei = T_briefzei()
        t_briefzei_list.append(t_briefzei)

        buffer_copy(briefzei, t_briefzei)

    return generate_output()