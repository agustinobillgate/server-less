from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Briefzei, Brief, Htparam

def prepare_fo_wordvibl(briefnr:int):
    t_briefzei_list = []
    htp_list_list = []
    briefzei = brief = htparam = None

    htp_list = t_briefzei = None

    htp_list_list, Htp_list = create_model("Htp_list", {"nr":int, "fchar":str, "bezeich":str})
    t_briefzei_list, T_briefzei = create_model_like(Briefzei)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_briefzei_list, htp_list_list, briefzei, brief, htparam


        nonlocal htp_list, t_briefzei
        nonlocal htp_list_list, t_briefzei_list
        return {"t-briefzei": t_briefzei_list, "htp-list": htp_list_list}

    def create_list():

        nonlocal t_briefzei_list, htp_list_list, briefzei, brief, htparam


        nonlocal htp_list, t_briefzei
        nonlocal htp_list_list, t_briefzei_list

        keychar:str = ""

        brief = db_session.query(Brief).filter(
                (briefnr == briefnr)).first()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 600)).first()
        keychar = htparam.fchar

        for htparam in db_session.query(Htparam).filter(
                (Htparam.paramgruppe == 8) &  (func.lower(Htparam.bezeich) != "Not Used")).all():
            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.nr = htparam.paramnr

            if substring(htparam.fchar, 0, 1) == ".":
                htp_list.fchar = htparam.fchar
            else:
                htp_list.fchar = keychar + htparam.fchar
            htp_list.bezeich = htparam.bezeich
        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.nr = 9092
        htp_list.fchar = keychar + "SourceRev"
        htp_list.bezeich = "Logding Revenue of selected Source"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.nr = 9813
        htp_list.fchar = keychar + "SourceRoom"
        htp_list.bezeich = "Rooms of selected Source"


        htp_list = Htp_list()
        htp_list_list.append(htp_list)

        htp_list.nr = 9814
        htp_list.fchar = keychar + "SourcePers"
        htp_list.bezeich = "Number of Pax of selected Source"

    def fill_words():

        nonlocal t_briefzei_list, htp_list_list, briefzei, brief, htparam


        nonlocal htp_list, t_briefzei
        nonlocal htp_list_list, t_briefzei_list

        for briefzei in db_session.query(Briefzei).filter(
                (Briefzei.briefnr == briefnr)).all():
            t_briefzei = T_briefzei()
            t_briefzei_list.append(t_briefzei)

            buffer_copy(briefzei, t_briefzei)

    create_list()
    fill_words()

    return generate_output()