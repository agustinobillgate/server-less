#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd 24/7/2025
# gitlab: 354
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Parameters, Briefzei

excel_list_data, Excel_list = create_model("Excel_list", {"curr_xlsrow":int, "curr_xlscol":int, "curr_val":string})

def fo_load_macro_webbl(briefnr:int, excel_list_data:[Excel_list]):

    prepare_cache ([Briefzei])

    error_list_data = []
    error_flag = False
    n:int = 0
    l:int = 0
    continued:bool = False
    c:string = ""
    ct:string = ""
    ch:string = ""
    curr_str:string = ""
    i:int = 0
    j:int = 0
    counter:int = 0
    counter_i:int = 0
    chcol:List[string] = ["A", "B", "c", "D", "E", "F", "G", "H", "i", "j", "K", "l", "M", "n", "O", "P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ"]
    mbuff:List[string] = ["jan", "feb", "mar", "apr", "mei", "jun", "jul", "aug", "sep", "oct", "nov", "des"]
    parameters = briefzei = None

    excel_list = error_list = brief_list = art_list = t_parameters = parambuff = None

    error_list_data, Error_list = create_model("Error_list", {"curr_xlsrow":int, "curr_xlscol":int, "curr_val":string, "msg":string})
    brief_list_data, Brief_list = create_model("Brief_list", {"b_text":string})
    art_list_data, Art_list = create_model("Art_list", {"str_art":string, "anzahl":int})
    t_parameters_data, T_parameters = create_model_like(Parameters)

    Parambuff = create_buffer("Parambuff",Parameters)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_list_data, error_flag, n, l, continued, c, ct, ch, curr_str, i, j, counter, counter_i, chcol, mbuff, parameters, briefzei
        nonlocal briefnr
        nonlocal parambuff


        nonlocal excel_list, error_list, brief_list, art_list, t_parameters, parambuff
        nonlocal error_list_data, brief_list_data, art_list_data, t_parameters_data

        return {"error-list": error_list_data, "error_flag": error_flag}

    def create_colom(i:int):

        nonlocal error_list_data, error_flag, n, l, continued, c, ct, ch, curr_str, j, counter, counter_i, chcol, mbuff, parameters, briefzei
        nonlocal briefnr
        nonlocal parambuff


        nonlocal excel_list, error_list, brief_list, art_list, t_parameters, parambuff
        nonlocal error_list_data, brief_list_data, art_list_data, t_parameters_data

        ch = ""

        def generate_inner_output():
            return (ch)


        if i > 26:

            if i % 26 == 0:
                ch = chcol[to_int(truncate(i / 26 , 0)) - 1 - 1] + "Z"
            else:
                ch = chcol[to_int(truncate(i / 26 , 0)) - 1] + chcol[i % 26 - 1]
        else:
            ch = chcol[i - 1]

        return generate_inner_output()


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
                    brief_list_data.append(brief_list)

                brief_list.b_text = brief_list.b_text + c
                j = i + 1
        n = length(briefzei.texte) - j + 1
        c = substring(briefzei.texte, j - 1, n)

        if not continued:
            brief_list = Brief_list()
            brief_list_data.append(brief_list)

        # Rd, 24/7/2025
        # add table name
        # b_text = b_text + c
        brief_list.b_text = brief_list.b_text + c

    for brief_list in query(brief_list_data):
        # Rd, 24/7/2025
        # add table name brief_list
        # if b_text == "" or substring(b_text, 0, 1) == ("#").lower() :
        if brief_list.b_text == "" or substring(brief_list.b_text, 0, 1) == ("#").lower() :
            pass
        else:
            art_list = Art_list()
            art_list_data.append(art_list)

            # Rd, 24/7/2025
            # add table name brief_list
            # for i in range(1,num_entries(b_text, " ")  + 1) :
            #     if substring(entry(i - 1, b_text, " ") , 0, 1) == ("^").lower() :
            #         art_list.str_art = entry(i - 1, b_text, " ")
            #         art_list.anzahl = 0
            for i in range(1,num_entries(brief_list.b_text, " ")  + 1) :
                if substring(entry(i - 1, brief_list.b_text, " ") , 0, 1) == ("^").lower() :
                    art_list.str_art = entry(i - 1, brief_list.b_text, " ")
                    art_list.anzahl = 0

    for excel_list in query(excel_list_data, sort_by=[("curr_xlsrow",False),("curr_xlscol",False)]):

        if substring(excel_list.curr_val, 0, 1) == ("$").lower()  or substring(excel_list.curr_val, 0, 1) == ("^").lower() :
            ch = create_colom(excel_list.curr_xlscol)
            t_parameters = T_parameters()
            t_parameters_data.append(t_parameters)

            t_parameters.progname = "FO-Macro"
            t_parameters.section = to_string(briefnr)
            t_parameters.varname = ch + to_string(excel_list.curr_xlsrow)
            curr_str = excel_list.curr_val

            if curr_str == None:
                curr_str = ""

            if substring(curr_str, 0, 1) == ("$").lower() :
                t_parameters.vstring = curr_str


            else:

                art_list = query(art_list_data, filters=(lambda art_list: art_list.str_art.lower()  == (curr_str).lower()  or art_list.str_art.lower()  == entry(0, (curr_str).lower() , ".")), first=True)

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
                    elif entry(1, curr_str, ".") == "lytd-budget":
                        t_parameters.vtype = 828
                    elif entry(1, curr_str, ".") == "ly-budget":
                        t_parameters.vtype = 827
                    elif entry(1, curr_str, ".") == "lm-budget":
                        t_parameters.vtype = 819
                    elif entry(1, curr_str, ".") == "ytd-budget":
                        t_parameters.vtype = 818
                    elif entry(1, curr_str, ".") == "mtd-budget":
                        t_parameters.vtype = 817
                    elif entry(1, curr_str, ".") == "budget":
                        t_parameters.vtype = 816
                    elif entry(1, curr_str, ".") == "l-ytd":
                        t_parameters.vtype = 815
                    elif entry(1, curr_str, ".") == "l-mtd":
                        t_parameters.vtype = 196
                    elif entry(1, curr_str, ".") == "lytoday":
                        t_parameters.vtype = 185
                    elif entry(1, curr_str, ".") == "p-mtd":
                        t_parameters.vtype = 96
                    elif entry(1, curr_str, ".") == "ytd":
                        t_parameters.vtype = 95
                    elif entry(1, curr_str, ".") == "mtd":
                        t_parameters.vtype = 94
                    elif entry(1, curr_str, ".") == "today":
                        t_parameters.vtype = 93
                    elif entry(1, curr_str, ".") == "yesterday":
                        t_parameters.vtype = 9199
                    elif entry(1, curr_str, ".") == "lm-today":
                        t_parameters.vtype = 9198
                    elif entry(1, curr_str, ".") == "ny-budget":
                        t_parameters.vtype = 9197
                    elif entry(1, curr_str, ".") == "nmtd-budget":
                        t_parameters.vtype = 9196
                    elif entry(1, curr_str, ".") == "nytd-budget":
                        t_parameters.vtype = 9195
                    elif entry(1, curr_str, ".") == "today-serv":
                        t_parameters.vtype = 9194
                    elif entry(1, curr_str, ".") == "today-tax":
                        t_parameters.vtype = 9193
                    elif entry(1, curr_str, ".") == "mtd-serv":
                        t_parameters.vtype = 9192
                    elif entry(1, curr_str, ".") == "mtd-tax":
                        t_parameters.vtype = 9191
                    elif entry(1, curr_str, ".") == "ytd-serv":
                        t_parameters.vtype = 9190
                    elif entry(1, curr_str, ".") == "ytd-tax":
                        t_parameters.vtype = 9189
                    elif entry(1, curr_str, ".") == "lmtoday-serv":
                        t_parameters.vtype = 9188
                    elif entry(1, curr_str, ".") == "lmtoday-tax":
                        t_parameters.vtype = 9187
                    elif entry(1, curr_str, ".") == "pmtd-serv":
                        t_parameters.vtype = 9186
                    elif entry(1, curr_str, ".") == "pmtd-tax":
                        t_parameters.vtype = 9185
                    elif entry(1, curr_str, ".") == "lmtd-serv":
                        t_parameters.vtype = 9184
                    elif entry(1, curr_str, ".") == "lmtd-tax":
                        t_parameters.vtype = 9183
                    elif entry(1, curr_str, ".") == "lm-mtd":
                        t_parameters.vtype = 9182
                    elif entry(1, curr_str, ".") == "lm-ytd":
                        t_parameters.vtype = 9181
                    elif entry(1, curr_str, ".") == "lmtd-tax":
                        t_parameters.vtype = 9183
                    elif entry(1, curr_str, ".") == "lytd-serv":
                        t_parameters.vtype = 9200
                    elif entry(1, curr_str, ".") == "lytd-tax":
                        t_parameters.vtype = 9201
                    elif entry(1, curr_str, ".") == "lytoday-serv":
                        t_parameters.vtype = 9202
                    elif entry(1, curr_str, ".") == "lytoday-tax":
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

                        if entry(1, curr_str, ".") == to_string(counter) + "serv":
                            t_parameters.vtype = 9230 + counter
                            break

                        if entry(1, curr_str, ".") == to_string(counter) + "tax":
                            t_parameters.vtype = 9261 + counter
                            break
                    for counter_i in range(1,12 + 1) :

                        if entry(1, curr_str, ".") == mbuff[counter_i - 1]:
                            t_parameters.vtype = 9200 + counter_i
                            t_parameters.vstring = entry(0, curr_str, ".") + "." + mbuff[counter_i - 1]


                else:
                    error_list = Error_list()
                    error_list_data.append(error_list)

                    buffer_copy(excel_list, error_list)
                    error_list.msg = "Postfix not defined in Macro"
                    error_flag = True

    if not error_flag:

        parameters = get_cache (Parameters, {"progname": [(eq, "fo-macro")],"section": [(eq, to_string(briefnr))]})
        while None != parameters:

            parambuff = db_session.query(Parambuff).filter(
                         (Parambuff._recid == parameters._recid)).first()
            db_session.delete(parambuff)

            curr_recid = parameters._recid
            parameters = db_session.query(Parameters).filter(
                     (Parameters.progname == ("FO-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (Parameters._recid > curr_recid)).first()

        for t_parameters in query(t_parameters_data):
            parameters = Parameters()
            db_session.add(parameters)

            buffer_copy(t_parameters, parameters)

    return generate_output()