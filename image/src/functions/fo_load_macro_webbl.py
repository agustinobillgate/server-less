from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Parameters, Briefzei, Error_list

def fo_load_macro_webbl(briefnr:int, excel_list:[Excel_list]):
    error_list_list = []
    error_flag = False
    n:int = 0
    l:int = 0
    continued:bool = False
    c:str = ""
    ct:str = ""
    ch:str = ""
    curr_str:str = ""
    i:int = 0
    j:int = 0
    counter:int = 0
    counter_i:int = 0
    chcol:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", "", ""]
    mbuff:[str] = ["", "", "", "", "", "", "", "", "", "", "", "", ""]
    parameters = briefzei = error_list = None

    excel_list = error_list = brief_list = art_list = t_parameters = parambuff = None

    excel_list_list, Excel_list = create_model("Excel_list", {"curr_xlsrow":int, "curr_xlscol":int, "curr_val":str})
    error_list_list, Error_list = create_model("Error_list", {"curr_xlsrow":int, "curr_xlscol":int, "curr_val":str, "msg":str})
    brief_list_list, Brief_list = create_model("Brief_list", {"b_text":str})
    art_list_list, Art_list = create_model("Art_list", {"str_art":str, "anzahl":int})
    t_parameters_list, T_parameters = create_model_like(Parameters)

    Parambuff = Parameters

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_list_list, error_flag, n, l, continued, c, ct, ch, curr_str, i, j, counter, counter_i, chcol, mbuff, parameters, briefzei, error_list
        nonlocal parambuff


        nonlocal excel_list, error_list, brief_list, art_list, t_parameters, parambuff
        nonlocal excel_list_list, error_list_list, brief_list_list, art_list_list, t_parameters_list
        return {"error-list": error_list_list, "error_flag": error_flag}

    def create_colom(i:int):

        nonlocal error_list_list, error_flag, n, l, continued, c, ct, ch, curr_str, i, j, counter, counter_i, chcol, mbuff, parameters, briefzei, error_list
        nonlocal parambuff


        nonlocal excel_list, error_list, brief_list, art_list, t_parameters, parambuff
        nonlocal excel_list_list, error_list_list, brief_list_list, art_list_list, t_parameters_list

        ch = ""

        def generate_inner_output():
            return ch

        if i > 26:

            if i % 26 == 0:
                ch = chcol[to_int(truncate(i / 26 , 0)) - 1 - 1] + "Z"
            else:
                ch = chcol[to_int(truncate(i / 26 , 0)) - 1] + chcol[i % 26 - 1]
        else:
            ch = chcol[i - 1]


        return generate_inner_output()

    for briefzei in db_session.query(Briefzei).filter(
            (Briefzei.briefnr == briefnr)).all():
        j = 1
        for i in range(1,len(briefzei.texte)  + 1) :

            if ord(substring(briefzei.texte, i - 1, 1)) == 10:
                n = i - j
                c = substring(briefzei.texte, j - 1, n)
                l = len(c)

                if not continued:
                    brief_list = Brief_list()
                brief_list_list.append(brief_list)

                brief_list.b_text = brief_list.b_text + c
                j = i + 1
        n = len(briefzei.texte) - j + 1
        c = substring(briefzei.texte, j - 1, n)

        if not continued:
            brief_list = Brief_list()
        brief_list_list.append(brief_list)

        b_text = b_text + c

    for brief_list in query(brief_list_list):

        if b_text == "" or substring(b_text, 0, 1) == "#":
            pass
        else:
            art_list = Art_list()
            art_list_list.append(art_list)

            for i in range(1,num_entries(b_text, " ")  + 1) :

                if substring(entry(i - 1, b_text, " ") , 0, 1) == "^":
                    art_list.str_art = entry(i - 1, b_text, " ")
                    art_list.anzahl = 0

    for excel_list in query(excel_list_list):

        if substring(excel_list.curr_val, 0, 1) == "$" or substring(excel_list.curr_val, 0, 1) == "^":
            ch = create_colom(excel_list.curr_xlscol)
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            t_parameters.progname = "FO_Macro"
            t_parameters.SECTION = to_string(briefnr)
            t_parameters.varname = ch + to_string(excel_list.curr_xlsrow)
            curr_str = excel_list.curr_val

            if curr_str == None:
                curr_str = ""

            if substring(curr_str, 0, 1) == "$":
                t_parameters.vstring = curr_str


            else:

                art_list = query(art_list_list, filters=(lambda art_list :art_list.str_art.lower()  == (curr_str).lower()  or art_list.str_art.lower()  == entry(0, (curr_str).lower() , ".")), first=True)

                if art_list:
                    t_parameters.vstring = entry(0, curr_str, ".")
                    art_list.anzahl = art_list.anzahl + 1

                    if entry(1, curr_str, ".") == "rlyddiff":
                        t_parameters.vtype = 2047
                    elif entry(1, curr_str, ".") == "lyddiff":
                        t_parameters.vtype = 2046
                    elif entry(1, curr_str, ".") == "lytdbg":
                        t_parameters.vtype = 2045
                    elif entry(1, curr_str, ".") == "lytdbl":
                        t_parameters.vtype = 2044
                    elif entry(1, curr_str, ".") == "ryddiff":
                        t_parameters.vtype = 2043
                    elif entry(1, curr_str, ".") == "rlydiff":
                        t_parameters.vtype = 2069
                    elif entry(1, curr_str, ".") == "rlmdiff":
                        t_parameters.vtype = 2068
                    elif entry(1, curr_str, ".") == "rdiff":
                        t_parameters.vtype = 2067
                    elif entry(1, curr_str, ".") == "yddiff":
                        t_parameters.vtype = 2066
                    elif entry(1, curr_str, ".") == "lydiff":
                        t_parameters.vtype = 2065
                    elif entry(1, curr_str, ".") == "lmdiff":
                        t_parameters.vtype = 822
                    elif entry(1, curr_str, ".") == "mdiff":
                        t_parameters.vtype = 821
                    elif entry(1, curr_str, ".") == "diff":
                        t_parameters.vtype = 820
                    elif entry(1, curr_str, ".") == "lytd_budget":
                        t_parameters.vtype = 828
                    elif entry(1, curr_str, ".") == "ly_budget":
                        t_parameters.vtype = 827
                    elif entry(1, curr_str, ".") == "lm_budget":
                        t_parameters.vtype = 819
                    elif entry(1, curr_str, ".") == "ytd_budget":
                        t_parameters.vtype = 818
                    elif entry(1, curr_str, ".") == "mtd_budget":
                        t_parameters.vtype = 817
                    elif entry(1, curr_str, ".") == "budget":
                        t_parameters.vtype = 816
                    elif entry(1, curr_str, ".") == "l_ytd":
                        t_parameters.vtype = 815
                    elif entry(1, curr_str, ".") == "l_mtd":
                        t_parameters.vtype = 196
                    elif entry(1, curr_str, ".") == "lytoday":
                        t_parameters.vtype = 185
                    elif entry(1, curr_str, ".") == "p_mtd":
                        t_parameters.vtype = 96
                    elif entry(1, curr_str, ".") == "ytd":
                        t_parameters.vtype = 95
                    elif entry(1, curr_str, ".") == "mtd":
                        t_parameters.vtype = 94
                    elif entry(1, curr_str, ".") == "today":
                        t_parameters.vtype = 93
                    elif entry(1, curr_str, ".") == "yesterday":
                        t_parameters.vtype = 9199
                    elif entry(1, curr_str, ".") == "lm_today":
                        t_parameters.vtype = 9198
                    elif entry(1, curr_str, ".") == "ny_budget":
                        t_parameters.vtype = 9197
                    elif entry(1, curr_str, ".") == "nmtd_budget":
                        t_parameters.vtype = 9196
                    elif entry(1, curr_str, ".") == "nytd_budget":
                        t_parameters.vtype = 9195
                    elif entry(1, curr_str, ".") == "today_serv":
                        t_parameters.vtype = 9194
                    elif entry(1, curr_str, ".") == "today_tax":
                        t_parameters.vtype = 9193
                    elif entry(1, curr_str, ".") == "mtd_serv":
                        t_parameters.vtype = 9192
                    elif entry(1, curr_str, ".") == "mtd_tax":
                        t_parameters.vtype = 9191
                    elif entry(1, curr_str, ".") == "ytd_serv":
                        t_parameters.vtype = 9190
                    elif entry(1, curr_str, ".") == "ytd_tax":
                        t_parameters.vtype = 9189
                    elif entry(1, curr_str, ".") == "lmtoday_serv":
                        t_parameters.vtype = 9188
                    elif entry(1, curr_str, ".") == "lmtoday_tax":
                        t_parameters.vtype = 9187
                    elif entry(1, curr_str, ".") == "pmtd_serv":
                        t_parameters.vtype = 9186
                    elif entry(1, curr_str, ".") == "pmtd_tax":
                        t_parameters.vtype = 9185
                    elif entry(1, curr_str, ".") == "lmtd_serv":
                        t_parameters.vtype = 9184
                    elif entry(1, curr_str, ".") == "lmtd_tax":
                        t_parameters.vtype = 9183
                    elif entry(1, curr_str, ".") == "lm_mtd":
                        t_parameters.vtype = 9182
                    elif entry(1, curr_str, ".") == "lm_ytd":
                        t_parameters.vtype = 9181
                    elif entry(1, curr_str, ".") == "lmtd_tax":
                        t_parameters.vtype = 9183
                    elif entry(1, curr_str, ".") == "lytd_serv":
                        t_parameters.vtype = 9200
                    elif entry(1, curr_str, ".") == "lytd_tax":
                        t_parameters.vtype = 9201
                    elif entry(1, curr_str, ".") == "lytoday_serv":
                        t_parameters.vtype = 9202
                    elif entry(1, curr_str, ".") == "lytoday_tax":
                        t_parameters.vtype = 9203
                for counter in range(1,31 + 1) :

                    if entry(1, curr_str, ".") == to_string(counter):
                        t_parameters.vtype = 9149 + counter
                        break

                    if entry(1, curr_str, ".") == to_string(counter) + "budget":
                        t_parameters.vtype = 9118 + counter
                        break

                    if entry(1, curr_str, ".") == to_string(counter) + "lytoday":
                        t_parameters.vtype = 8119 + counter
                        break
                for counter_i in range(1,12 + 1) :

                    if entry(1, curr_str, ".") == mbuff[counter_i - 1]:
                        t_parameters.vtype = 9200 + counter_i
                        t_parameters.vstring = entry(0, curr_str, ".") + "." + mbuff[counter_i - 1]


            else:
                error_list = Error_list()
                db_session.add(error_list)

                buffer_copy(excel_list, error_list)
                error_list.msg = "Postfix not defined in Macro"
                error_flag = True

    if not error_flag:

        parameters = db_session.query(Parameters).filter(
                (func.lower(Parameters.progname) == "FO_Macro") &  (Parameters.SECTION == to_string(briefnr))).first()
        while None != parameters:

            parambuff = db_session.query(Parambuff).filter(
                        (Parambuff._recid == parameters._recid)).first()
            db_session.delete(parambuff)


            parameters = db_session.query(Parameters).filter(
                    (func.lower(Parameters.progname) == "FO_Macro") &  (Parameters.SECTION == to_string(briefnr))).first()

        for t_parameters in query(t_parameters_list):
            parameters = Parameters()
            db_session.add(parameters)

            buffer_copy(t_parameters, parameters)

    return generate_output()