#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters, Briefzei

def fo_loadmacro_step1bl(briefnr:int):

    prepare_cache ([Briefzei])

    art_list_list = []
    n:int = 0
    l:int = 0
    continued:bool = False
    c:string = ""
    ct:string = ""
    i:int = 0
    j:int = 0
    parameters = briefzei = None

    brief_list = art_list = parambuff = None

    brief_list_list, Brief_list = create_model("Brief_list", {"b_text":string})
    art_list_list, Art_list = create_model("Art_list", {"str_art":string, "anzahl":int})

    Parambuff = create_buffer("Parambuff",Parameters)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_list_list, n, l, continued, c, ct, i, j, parameters, briefzei
        nonlocal briefnr
        nonlocal parambuff


        nonlocal brief_list, art_list, parambuff
        nonlocal brief_list_list, art_list_list

        return {"art-list": art_list_list}


    for briefzei in db_session.query(Briefzei).filter(
             (Briefzei.briefnr == briefnr)).order_by(Briefzei.briefzeilnr).all():
        j = 1
        for i in range(1,length(briefzei.texte)  + 1) :

            if asc(substring(briefzei.texte, i - 1, 1)) == 10:
                n = i - j
                c = substring(briefzei.texte, j - 1, n)
                l = length(c)

                if not continued:
                    brief_list = Brief_list()
                    brief_list_list.append(brief_list)

                brief_list.b_text = brief_list.b_text + c
                j = i + 1
        n = length(briefzei.texte) - j + 1
        c = substring(briefzei.texte, j - 1, n)

        if not continued:
            brief_list = Brief_list()
            brief_list_list.append(brief_list)

        b_text = b_text + c

    art_list = query(art_list_list, first=True)

    if not art_list:

        for brief_list in query(brief_list_list):

            if b_text == "" or substring(b_text, 0, 1) == ("#").lower() :
                pass
            else:
                art_list = Art_list()
                art_list_list.append(art_list)

                for i in range(1,num_entries(b_text, " ")  + 1) :

                    if substring(entry(i - 1, b_text, " ") , 0, 1) == ("^").lower() :
                        art_list.str_art = entry(i - 1, b_text, " ")
                        art_list.anzahl = 0

    else:

        for art_list in query(art_list_list, filters=(lambda art_list: art_list.anzahl != 0)):
            art_list.anzahl = 0


    parameters = get_cache (Parameters, {"progname": [(eq, "fo-macro")],"section": [(eq, to_string(briefnr))]})
    while None != parameters:

        parambuff = db_session.query(Parambuff).filter(
                     (Parambuff._recid == parameters._recid)).first()
        db_session.delete(parambuff)

        curr_recid = parameters._recid
        parameters = db_session.query(Parameters).filter(
                 (Parameters.progname == ("FO-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (Parameters._recid > curr_recid)).first()

    return generate_output()