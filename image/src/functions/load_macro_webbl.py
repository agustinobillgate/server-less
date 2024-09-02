from functions.additional_functions import *
import decimal
import re
from sqlalchemy import func
from models import Parameters, Gl_acct, Artikel, error_list

excel_list_list, Excel_list = create_model("Excel_list", {"curr_xlsrow":int, "curr_xlscol":int, "curr_val":str})
coa_list_list, Coa_list = create_model("Coa_list", {"fibukonto":str, "anzahl":int})
error_list_list, Error_list = create_model("Error_list", {"curr_xlsrow":int, "curr_xlscol":int, "curr_val":str, "msg":str})
t_parameters_list, T_parameters = create_model_like(Parameters)

def load_macro_webbl(briefnr:int, excel_list:[Excel_list]):
    coa_list_list = []
    error_list_list = []
    error_flag = False
    flag_combo:bool = False
    row_combo:int = 0
    str:str = ""
    str2:str = ""
    parameters = gl_acct = artikel = error_list = None
    excel_list = coa_list = error_list = t_parameters = parambuff = None
    Parambuff = Parameters

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_flag, flag_combo, row_combo, str, str2, parameters, gl_acct, artikel, error_list
        nonlocal parambuff

        nonlocal excel_list, coa_list, error_list, t_parameters, parambuff
        global excel_list_list, coa_list_list, error_list_list, t_parameters_list
        return {"coa-list": coa_list_list, "error-list": error_list_list, "error_flag": error_flag}


    for gl_acct in db_session.query(Gl_acct).all():
        coa_list = Coa_list()
        coa_list_list.append(coa_list)

        coa_list.fibukonto = gl_acct.fibukonto

    for excel_list in query(excel_list_list):

        if re.match(".*combo_on.*",excel_list.curr_val):
            flag_combo = True
            row_combo = excel_list.curr_xlsrow

        if re.match(".*combo_off.*",excel_list.curr_val):
            flag_combo = False

        if substring(excel_list.curr_val, 0, 1) == "$" or substring(excel_list.curr_val, 0, 1) == "^":
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            t_parameters.progname = "GL_Macro"
            t_parameters.SECTION = to_string(briefnr)
            t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") +\
                    "-" + to_string(excel_list.curr_xlscol, "99")
            str = entry(0, substring(excel_list.curr_val, 1) , ".")
            str2 = entry(0, str, ":")

            if curr_xlsrow > row_combo and flag_combo:
                t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") + "-" + to_string(excel_list.curr_xlscol, "99") + "-" + "combo"

            if num_entries(str, ":") > 1 and substring(excel_list.curr_val, 0, 1) == "^":
                t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") + "-" + to_string(excel_list.curr_xlscol, "99") + "-" + "CF"

            if substring(excel_list.curr_val, 0, 1) == "$":
                t_parameters.vstring = excel_list.curr_val

            elif substring(excel_list.curr_val, 0, 1) == "^" and re.match(".*segmrev.*",excel_list.curr_val):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == "^" and re.match(".*segmpers.*",excel_list.curr_val):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == "^" and re.match(".*segmroom.*",excel_list.curr_val):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")


            else:

                gl_acct = db_session.query(Gl_acct).filter(
                        (func.lower(Gl_acct.fibukonto) == (str2).lower())).first()

                artikel = db_session.query(Artikel).filter(
                        (Artikel.departement == to_int(substring(str2, 0, 2))) &  (Artikel.artnr == to_int(substring(str2, 2)))).first()

                if not gl_acct:

                    if artikel:
                        pass
                    else:

                        if flag_combo:
                            pass
                        else:
                            error_list = Error_list()
                            db_session.add(error_list)

                            buffer_copy(excel_list, error_list)
                            error_list.msg = "GL AcctNo not found in cell"
                            error_flag = True

                elif gl_acct:

                    coa_list = query(coa_list_list, filters=(lambda coa_list :coa_list.fibukonto == gl_acct.fibukonto), first=True)

                    if coa_list:
                        coa_list.anzahl = coa_list.anzahl + 1
                    t_parameters.vstring = str

                    if entry(1, substring(excel_list.curr_val, 1) , ".") == "BALANCE":
                        t_parameters.vtype = 1
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "YDBALANCE":
                        t_parameters.vtype = 2
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LASTMON":
                        t_parameters.vtype = 3
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LASTYR":
                        t_parameters.vtype = 4
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LYTDBL":
                        t_parameters.vtype = 5
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BUDGET":
                        t_parameters.vtype = 6
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "YDBUDGET":
                        t_parameters.vtype = 7
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LMBUDGET":
                        t_parameters.vtype = 8
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LYBUDGET":
                        t_parameters.vtype = 9
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LYTDBG":
                        t_parameters.vtype = 10
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "JAN":
                        t_parameters.vtype = 11
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "FEB":
                        t_parameters.vtype = 12
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "MAR":
                        t_parameters.vtype = 13
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "APR":
                        t_parameters.vtype = 14
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "MAY":
                        t_parameters.vtype = 15
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "JUN":
                        t_parameters.vtype = 16
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "JUL":
                        t_parameters.vtype = 17
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "AUG":
                        t_parameters.vtype = 18
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "SEP":
                        t_parameters.vtype = 19
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "OCT":
                        t_parameters.vtype = 20
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NOV":
                        t_parameters.vtype = 21
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "DEC":
                        t_parameters.vtype = 22
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "DEBIT":
                        t_parameters.vtype = 25
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "CREDIT":
                        t_parameters.vtype = 26
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "DIFF":
                        t_parameters.vtype = 27
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LMDIFF":
                        t_parameters.vtype = 28
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BJAN":
                        t_parameters.vtype = 31
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BFEB":
                        t_parameters.vtype = 32
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BMAR":
                        t_parameters.vtype = 33
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BAPR":
                        t_parameters.vtype = 34
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BMAY":
                        t_parameters.vtype = 35
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BJUN":
                        t_parameters.vtype = 36
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BJUL":
                        t_parameters.vtype = 37
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BAUG":
                        t_parameters.vtype = 38
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BSEP":
                        t_parameters.vtype = 39
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BOCT":
                        t_parameters.vtype = 40
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BNOV":
                        t_parameters.vtype = 41
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "BDEC":
                        t_parameters.vtype = 42
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LJAN":
                        t_parameters.vtype = 43
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LFEB":
                        t_parameters.vtype = 44
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LMAR":
                        t_parameters.vtype = 45
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LAPR":
                        t_parameters.vtype = 46
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LMAY":
                        t_parameters.vtype = 47
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LJUN":
                        t_parameters.vtype = 48
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LJUL":
                        t_parameters.vtype = 49
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LAUG":
                        t_parameters.vtype = 50
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LSEP":
                        t_parameters.vtype = 51
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LOCT":
                        t_parameters.vtype = 52
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LNOV":
                        t_parameters.vtype = 53
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LDEC":
                        t_parameters.vtype = 54
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBJAN":
                        t_parameters.vtype = 55
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBFEB":
                        t_parameters.vtype = 56
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBMAR":
                        t_parameters.vtype = 57
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBAPR":
                        t_parameters.vtype = 58
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBMAY":
                        t_parameters.vtype = 59
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBJUN":
                        t_parameters.vtype = 60
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBJUL":
                        t_parameters.vtype = 61
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBAUG":
                        t_parameters.vtype = 62
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBSEP":
                        t_parameters.vtype = 63
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBOCT":
                        t_parameters.vtype = 64
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBNOV":
                        t_parameters.vtype = 65
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "NBDEC":
                        t_parameters.vtype = 66
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBJAN":
                        t_parameters.vtype = 67
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBFEB":
                        t_parameters.vtype = 68
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBMAR":
                        t_parameters.vtype = 69
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBAPR":
                        t_parameters.vtype = 70
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBMAY":
                        t_parameters.vtype = 71
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBJUN":
                        t_parameters.vtype = 72
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBJUL":
                        t_parameters.vtype = 73
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBAUG":
                        t_parameters.vtype = 74
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBSEP":
                        t_parameters.vtype = 75
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBOCT":
                        t_parameters.vtype = 76
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBNOV":
                        t_parameters.vtype = 77
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LBDEC":
                        t_parameters.vtype = 78
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "debit_lsyear":
                        t_parameters.vtype = 79
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "credit_lsyear":
                        t_parameters.vtype = 80
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "debit_lsmonth":
                        t_parameters.vtype = 81
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "credit_lsmonth":
                        t_parameters.vtype = 82
                    else:
                        error_list = Error_list()
                        db_session.add(error_list)

                        buffer_copy(excel_list, error_list)
                        error_list.msg = "Postfix not defined"
                        error_flag = True

            if (artikel and not gl_acct) or flag_combo:
                t_parameters.vstring = str
                t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") + "-" + to_string(excel_list.curr_xlscol, "99") + "-" + "REV"

                if flag_combo:
                    t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") + "-" + to_string(excel_list.curr_xlscol, "99") + "-" + "comboREV"

                if entry(1, substring(excel_list.curr_val, 1) , ".") == "MTD":
                    t_parameters.vtype = 23
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "YTD":
                    t_parameters.vtype = 24
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "today":
                    t_parameters.vtype = 83
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "mtd_budget":
                    t_parameters.vtype = 84
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "ytd_budget":
                    t_parameters.vtype = 85
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "l_mtd":
                    t_parameters.vtype = 86
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "l_ytd":
                    t_parameters.vtype = 87
                else:
                    error_list = Error_list()
                    db_session.add(error_list)

                    buffer_copy(excel_list, error_list)
                    error_list.msg = "Postfix not defined"
                    error_flag = True

                    return generate_output()

        if t_parameters.vstring != "" and substring(excel_list.curr_val, 0, 1) == "^" and t_parameters.vtype == 0:
            t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") + "-" + to_string(excel_list.curr_xlscol, "99") + "-" + "FO"

            if flag_combo:
                t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") + "-" + to_string(excel_list.curr_xlscol, "99") + "-" + "comboFO"

            if entry(1, substring(excel_list.curr_val, 1) , ".") == "MTD":
                t_parameters.vtype = 23
            elif entry(1, substring(excel_list.curr_val, 1) , ".") == "YTD":
                t_parameters.vtype = 24
            elif entry(1, substring(excel_list.curr_val, 1) , ".") == "today":
                t_parameters.vtype = 83
            elif entry(1, substring(excel_list.curr_val, 1) , ".") == "mtd_budget":
                t_parameters.vtype = 84
            elif entry(1, substring(excel_list.curr_val, 1) , ".") == "ytd_budget":
                t_parameters.vtype = 85
            elif entry(1, substring(excel_list.curr_val, 1) , ".") == "l_mtd":
                t_parameters.vtype = 86
            elif entry(1, substring(excel_list.curr_val, 1) , ".") == "l_ytd":
                t_parameters.vtype = 87
            else:
                error_list = Error_list()
                db_session.add(error_list)

                buffer_copy(excel_list, error_list)
                error_list.msg = "Postfix not defined"
                error_flag = True

    for coa_list in query(coa_list_list, filters=(lambda coa_list :coa_list.anzahl != 0)):
        coa_list_list.remove(coa_list)

    if not error_flag:

        t_parameters = query(t_parameters_list, first=True)
        if t_parameters is not None:
            tsection = t_parameters.section
            parameters = db_session.query(Parameters).filter(
                    (func.lower(Parameters.progname) == "GL_Macro") &  (Parameters.section == tsection)).first()
            while None != parameters:

                parambuff = db_session.query(Parambuff).filter(
                            (Parambuff._recid == parameters._recid)).first()
                db_session.delete(parambuff)

                parameters = db_session.query(Parameters).filter(
                        (func.lower(Parameters.progname) == "GL_Macro") &  (Parameters.section == tsection)).first()

            for t_parameters in query(t_parameters_list):
                parameters = Parameters()
                db_session.add(parameters)

                buffer_copy(t_parameters, parameters)

    return generate_output()