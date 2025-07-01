#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Parameters, Gl_acct, Artikel

excel_list_list, Excel_list = create_model("Excel_list", {"curr_xlsrow":int, "curr_xlscol":int, "curr_val":string})

def load_macro_webbl(briefnr:int, excel_list_list:[Excel_list]):

    prepare_cache ([Gl_acct])

    coa_list_list = []
    error_list_list = []
    error_flag = False
    flag_combo:bool = False
    row_combo:int = 0
    str:string = ""
    str2:string = ""
    parameters = gl_acct = artikel = None

    excel_list = coa_list = error_list = t_parameters = parambuff = None

    coa_list_list, Coa_list = create_model("Coa_list", {"fibukonto":string, "anzahl":int})
    error_list_list, Error_list = create_model("Error_list", {"curr_xlsrow":int, "curr_xlscol":int, "curr_val":string, "msg":string})
    t_parameters_list, T_parameters = create_model_like(Parameters)

    Parambuff = create_buffer("Parambuff",Parameters)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal coa_list_list, error_list_list, error_flag, flag_combo, row_combo, str, str2, parameters, gl_acct, artikel
        nonlocal briefnr
        nonlocal parambuff


        nonlocal excel_list, coa_list, error_list, t_parameters, parambuff
        nonlocal coa_list_list, error_list_list, t_parameters_list

        return {"coa-list": coa_list_list, "error-list": error_list_list, "error_flag": error_flag}


    for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
        coa_list = Coa_list()
        coa_list_list.append(coa_list)

        coa_list.fibukonto = gl_acct.fibukonto

    for excel_list in query(excel_list_list, sort_by=[("curr_xlsrow",False),("curr_xlscol",False)]):

        if matches(excel_list.curr_val,r"*combo-on*"):
            flag_combo = True
            row_combo = excel_list.curr_xlsrow

        if matches(excel_list.curr_val,r"*combo-off*"):
            flag_combo = False

        if substring(excel_list.curr_val, 0, 1) == ("$").lower()  or substring(excel_list.curr_val, 0, 1) == ("^").lower() :
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            t_parameters.progname = "GL-Macro"
            t_parameters.section = to_string(briefnr)
            t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") +\
                    "-" + to_string(excel_list.curr_xlscol, "99")
            str = entry(0, substring(excel_list.curr_val, 1) , ".")
            str2 = entry(0, str, ":")

            if curr_xlsrow > row_combo and flag_combo:
                t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") + "-" + to_string(excel_list.curr_xlscol, "99") + "-" + "combo"

            if num_entries(str, ":") > 1 and substring(excel_list.curr_val, 0, 1) == ("^").lower() :
                t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") + "-" + to_string(excel_list.curr_xlscol, "99") + "-" + "CF"

            if substring(excel_list.curr_val, 0, 1) == ("$").lower() :
                t_parameters.vstring = excel_list.curr_val

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*segmrev*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*segmpers*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*segmroom*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-tot-rm*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-act-rm*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-ooo*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-rrom-90*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-rrom-91*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-occ-rm*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-rm-wig*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-nguest*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-day-use*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-numcompl*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-rm-rsv*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-rm-arr*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-prs-arr*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-rm-dep*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-prs-dep*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-rm-wig*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-noshow*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-newres*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-cancel*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-earco*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-rm-arrtmr*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-prs-arrtmr*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")

            elif substring(excel_list.curr_val, 0, 1) == ("^").lower()  and matches(excel_list.curr_val,r"*stat-rm-deptmr*"):
                t_parameters.vstring = entry(0, substring(excel_list.curr_val, 1) , ".")


            else:

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, str2)]})

                artikel = get_cache (Artikel, {"departement": [(eq, to_int(substring(str2, 0, 2)))],"artnr": [(eq, to_int(substring(str2, 2)))]})

                if not gl_acct:

                    if artikel:
                        pass
                    else:

                        if flag_combo:
                            pass
                        else:
                            error_list = Error_list()
                            error_list_list.append(error_list)

                            buffer_copy(excel_list, error_list)
                            error_list.msg = "GL AcctNo not found in cell"
                            error_flag = True

                elif gl_acct:

                    coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.fibukonto == gl_acct.fibukonto), first=True)

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
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "debit-lsyear":
                        t_parameters.vtype = 79
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "credit-lsyear":
                        t_parameters.vtype = 80
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "debit-lsmonth":
                        t_parameters.vtype = 81
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "credit-lsmonth":
                        t_parameters.vtype = 82
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "mapcoa":
                        t_parameters.vtype = 88
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "LYLASTMON":
                        t_parameters.vtype = 89
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "debit-today":
                        t_parameters.vtype = 90
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "credit-today":
                        t_parameters.vtype = 91
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "debit-MTD":
                        t_parameters.vtype = 92
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "credit-MTD":
                        t_parameters.vtype = 93
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "debit-YTD":
                        t_parameters.vtype = 94
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "credit-YTD":
                        t_parameters.vtype = 95
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "today-balance":
                        t_parameters.vtype = 96
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "MTD-balance":
                        t_parameters.vtype = 97
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "YTD-balance":
                        t_parameters.vtype = 98
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LJAN":
                        t_parameters.vtype = 99
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LFEB":
                        t_parameters.vtype = 100
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LMAR":
                        t_parameters.vtype = 101
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LAPR":
                        t_parameters.vtype = 102
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LMAY":
                        t_parameters.vtype = 103
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LJUN":
                        t_parameters.vtype = 104
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LJUL":
                        t_parameters.vtype = 105
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LAUG":
                        t_parameters.vtype = 106
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LSEP":
                        t_parameters.vtype = 107
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LOCT":
                        t_parameters.vtype = 108
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LNOV":
                        t_parameters.vtype = 109
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "2LDEC":
                        t_parameters.vtype = 110
                    else:
                        error_list = Error_list()
                        error_list_list.append(error_list)

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
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "mtd-budget":
                        t_parameters.vtype = 84
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "ytd-budget":
                        t_parameters.vtype = 85
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "l-mtd":
                        t_parameters.vtype = 86
                    elif entry(1, substring(excel_list.curr_val, 1) , ".") == "l-ytd":
                        t_parameters.vtype = 87
                    else:
                        error_list = Error_list()
                        error_list_list.append(error_list)

                        buffer_copy(excel_list, error_list)
                        error_list.msg = "Postfix not defined"
                        error_flag = True

                        return generate_output()

            if t_parameters.vstring != "" and substring(excel_list.curr_val, 0, 1) == ("^").lower()  and t_parameters.vtype == 0:
                t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") + "-" + to_string(excel_list.curr_xlscol, "99") + "-" + "FO"

                if flag_combo:
                    t_parameters.varname = to_string(excel_list.curr_xlsrow, "9999") + "-" + to_string(excel_list.curr_xlscol, "99") + "-" + "comboFO"

                if entry(1, substring(excel_list.curr_val, 1) , ".") == "MTD":
                    t_parameters.vtype = 23
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "YTD":
                    t_parameters.vtype = 24
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "today":
                    t_parameters.vtype = 83
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "mtd-budget":
                    t_parameters.vtype = 84
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "ytd-budget":
                    t_parameters.vtype = 85
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "l-mtd":
                    t_parameters.vtype = 86
                elif entry(1, substring(excel_list.curr_val, 1) , ".") == "l-ytd":
                    t_parameters.vtype = 87
                else:
                    error_list = Error_list()
                    error_list_list.append(error_list)

                    buffer_copy(excel_list, error_list)
                    error_list.msg = "Postfix not defined"
                    error_flag = True

    for coa_list in query(coa_list_list, filters=(lambda coa_list: coa_list.anzahl != 0)):
        coa_list_list.remove(coa_list)

    if not error_flag:

        t_parameters = query(t_parameters_list, first=True)

        parameters = get_cache (Parameters, {"progname": [(eq, "gl-macro")],"section": [(eq, t_parameters.section)]})
        while None != parameters:

            parambuff = db_session.query(Parambuff).filter(
                         (Parambuff._recid == parameters._recid)).first()
            db_session.delete(parambuff)
            pass

            curr_recid = parameters._recid
            parameters = db_session.query(Parameters).filter(
                     (Parameters.progname == ("GL-Macro").lower()) & (Parameters.section == t_parameters.section) & (Parameters._recid > curr_recid)).first()

        for t_parameters in query(t_parameters_list):
            parameters = Parameters()
            db_session.add(parameters)

            buffer_copy(t_parameters, parameters)

    return generate_output()