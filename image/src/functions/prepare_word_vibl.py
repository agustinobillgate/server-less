from functions.additional_functions import *
import decimal
from models import Htparam, Brief, Briefzei

def prepare_word_vibl(briefnr:int):
    word_exist = False
    efield = ""
    ebuffer = ""
    sms_kateg = 0
    htp_list_list = []
    gl_nr:int = 0
    gl_file:bool = False
    htparam = brief = briefzei = None

    htp_list = None

    htp_list_list, Htp_list = create_model("Htp_list", {"nr":int, "fchar":str, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal word_exist, efield, ebuffer, sms_kateg, htp_list_list, gl_nr, gl_file, htparam, brief, briefzei


        nonlocal htp_list
        nonlocal htp_list_list
        return {"word_exist": word_exist, "efield": efield, "ebuffer": ebuffer, "sms_kateg": sms_kateg, "htp-list": htp_list_list}

    def create_list():

        nonlocal word_exist, efield, ebuffer, sms_kateg, htp_list_list, gl_nr, gl_file, htparam, brief, briefzei


        nonlocal htp_list
        nonlocal htp_list_list

        keychar:str = ""

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 987)).first()
        gl_nr = htparam.finteger

        brief = db_session.query(Brief).filter(
                (briefnr == briefnr)).first()

        if not brief:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 600)).first()
        keychar = htparam.fchar

        if briefkateg == gl_nr:
            gl_file = True

            for htparam in db_session.query(Htparam).filter(
                    (Htparam.paramgruppe == 39) &  (Htparam.paramnr != 2030)).all():
                htp_list = Htp_list()
                htp_list_list.append(htp_list)

                htp_list.nr = htparam.paramnr

                if substring(htparam.fchar, 0, 1) == ".":
                    htp_list.fchar = htparam.fchar
                else:
                    htp_list.fchar = keychar + htparam.fchar
                htp_list.bezeich = htparam.bezeich
        else:

            for htparam in db_session.query(Htparam).filter(
                    (Htparam.paramgruppe == 17)).all():
                htp_list = Htp_list()
                htp_list_list.append(htp_list)

                htp_list.nr = htparam.paramnr
                htp_list.fchar = keychar + htparam.fchar
                htp_list.bezeich = htparam.bezeich
            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.nr = 9999
            htp_list.fchar = keychar + "supp1"
            htp_list.bezeich = "Supplier1(P/R)"


            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.nr = 9998
            htp_list.fchar = keychar + "supp2"
            htp_list.bezeich = "Supplier2(P/R)"


            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.nr = 9997
            htp_list.fchar = keychar + "supp3"
            htp_list.bezeich = "Supplier3(P/R)"


            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.nr = 9996
            htp_list.fchar = keychar + "du_price2"
            htp_list.bezeich = "DU_Price2(P/R)"


            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.nr = 9995
            htp_list.fchar = keychar + "du_price3"
            htp_list.bezeich = "DU_Price3(P/R)"


            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.nr = 9994
            htp_list.fchar = keychar + "cont"
            htp_list.bezeich = "Content Article(P/R)"


            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.nr = 9993
            htp_list.fchar = keychar + "t_amount"
            htp_list.bezeich = "Total Amount(P/R)"


            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.nr = 9992
            htp_list.fchar = keychar + "Supps"
            htp_list.bezeich = "Supplier Selected(P/R)"


            htp_list = Htp_list()
            htp_list_list.append(htp_list)

            htp_list.nr = 9991
            htp_list.fchar = keychar + "du_price1"
            htp_list.bezeich = "DU_Price1(P/R)"

    def fill_words():

        nonlocal word_exist, efield, ebuffer, sms_kateg, htp_list_list, gl_nr, gl_file, htparam, brief, briefzei


        nonlocal htp_list
        nonlocal htp_list_list

        briefzei = db_session.query(Briefzei).filter(
                (Briefzei.briefnr == briefnr) &  (Briefzeilnr == 1)).first()

        if briefzei:
            word_exist = True
            efield = briefzei.texte
            ebuffer = briefzei.texte


    create_list()
    fill_words()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 839)).first()
    sms_kateg = htparam.finteger

    return generate_output()