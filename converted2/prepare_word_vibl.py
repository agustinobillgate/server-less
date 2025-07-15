#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Brief, Briefzei

def prepare_word_vibl(briefnr:int):

    prepare_cache ([Htparam, Brief, Briefzei])

    word_exist = False
    efield = ""
    ebuffer = ""
    sms_kateg = 0
    htp_list_data = []
    gl_nr:int = 0
    gl_file:bool = False
    htparam = brief = briefzei = None

    htp_list = None

    htp_list_data, Htp_list = create_model("Htp_list", {"nr":int, "fchar":string, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal word_exist, efield, ebuffer, sms_kateg, htp_list_data, gl_nr, gl_file, htparam, brief, briefzei
        nonlocal briefnr


        nonlocal htp_list
        nonlocal htp_list_data

        return {"word_exist": word_exist, "efield": efield, "ebuffer": ebuffer, "sms_kateg": sms_kateg, "htp-list": htp_list_data}

    def create_list():

        nonlocal word_exist, efield, ebuffer, sms_kateg, htp_list_data, gl_nr, gl_file, htparam, brief, briefzei
        nonlocal briefnr


        nonlocal htp_list
        nonlocal htp_list_data

        keychar:string = ""

        htparam = get_cache (Htparam, {"paramnr": [(eq, 987)]})
        gl_nr = htparam.finteger

        brief = get_cache (Brief, {"briefnr": [(eq, briefnr)]})

        if not brief:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 600)]})
        keychar = htparam.fchar

        if brief.briefkateg == gl_nr:
            gl_file = True

            for htparam in db_session.query(Htparam).filter(
                     (Htparam.paramgruppe == 39) & (Htparam.paramnr != 2030)).order_by(Htparam.reihenfolge).all():
                htp_list = Htp_list()
                htp_list_data.append(htp_list)

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
                htp_list_data.append(htp_list)

                htp_list.nr = htparam.paramnr
                htp_list.fchar = keychar + htparam.fchar
                htp_list.bezeich = htparam.bezeichnung
            htp_list = Htp_list()
            htp_list_data.append(htp_list)

            htp_list.nr = 9999
            htp_list.fchar = keychar + "supp1"
            htp_list.bezeich = "Supplier1(P/R)"


            htp_list = Htp_list()
            htp_list_data.append(htp_list)

            htp_list.nr = 9998
            htp_list.fchar = keychar + "supp2"
            htp_list.bezeich = "Supplier2(P/R)"


            htp_list = Htp_list()
            htp_list_data.append(htp_list)

            htp_list.nr = 9997
            htp_list.fchar = keychar + "supp3"
            htp_list.bezeich = "Supplier3(P/R)"


            htp_list = Htp_list()
            htp_list_data.append(htp_list)

            htp_list.nr = 9996
            htp_list.fchar = keychar + "du-price2"
            htp_list.bezeich = "DU-Price2(P/R)"


            htp_list = Htp_list()
            htp_list_data.append(htp_list)

            htp_list.nr = 9995
            htp_list.fchar = keychar + "du-price3"
            htp_list.bezeich = "DU-Price3(P/R)"


            htp_list = Htp_list()
            htp_list_data.append(htp_list)

            htp_list.nr = 9994
            htp_list.fchar = keychar + "cont"
            htp_list.bezeich = "Content Article(P/R)"


            htp_list = Htp_list()
            htp_list_data.append(htp_list)

            htp_list.nr = 9993
            htp_list.fchar = keychar + "t-amount"
            htp_list.bezeich = "Total Amount(P/R)"


            htp_list = Htp_list()
            htp_list_data.append(htp_list)

            htp_list.nr = 9992
            htp_list.fchar = keychar + "Supps"
            htp_list.bezeich = "Supplier Selected(P/R)"


            htp_list = Htp_list()
            htp_list_data.append(htp_list)

            htp_list.nr = 9991
            htp_list.fchar = keychar + "du-price1"
            htp_list.bezeich = "DU-Price1(P/R)"


    def fill_words():

        nonlocal word_exist, efield, ebuffer, sms_kateg, htp_list_data, gl_nr, gl_file, htparam, brief, briefzei
        nonlocal briefnr


        nonlocal htp_list
        nonlocal htp_list_data

        briefzei = get_cache (Briefzei, {"briefnr": [(eq, briefnr)],"briefzeilnr": [(eq, 1)]})

        if briefzei:
            word_exist = True
            efield = briefzei.texte
            ebuffer = briefzei.texte

    create_list()
    fill_words()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 839)]})
    sms_kateg = htparam.finteger

    return generate_output()