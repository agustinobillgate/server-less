from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Briefzei, Gl_main, Gl_department, Exrate, Htparam, Gl_acct, Waehrung, Gl_accthis, Brief

def prepare_gl_parxls2bl(pvilanguage:int, briefnr:int, to_date:date, close_month:int):
    end_month = 0
    prev_month = 0
    beg_month = 0
    keycmd = ""
    keyvar = ""
    keycont = ""
    c_param64 = ""
    c_param977 = ""
    c_param170 = ""
    c_param144 = ""
    c_foreign_nr = 0
    d_param795 = None
    xls_dir = ""
    prog_error = False
    error_nr = 0
    msg_str = ""
    htv_list_list = []
    htp_list_list = []
    brief_list_list = []
    batch_list_list = []
    briefzei_list_list = []
    gl_main_list_list = []
    gl_department_list_list = []
    t_gl_acct_list = []
    t_exrate_list = []
    t_exrate1_list = []
    t_gl_accthis_list = []
    batch_file:bool = False
    curr_row:int = 0
    curr_texte:str = ""
    lvcarea:str = "gl-parxls"
    i:int = 0
    briefzei = gl_main = gl_department = exrate = htparam = gl_acct = waehrung = gl_accthis = brief = None

    htv_list = htp_list = brief_list = batch_list = briefzei_list = gl_main_list = gl_department_list = t_gl_acct = t_exrate = t_exrate1 = t_gl_accthis = None

    htv_list_list, Htv_list = create_model("Htv_list", {"paramnr":int, "fchar":str})
    htp_list_list, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":str})
    brief_list_list, Brief_list = create_model("Brief_list", {"b_text":str})
    batch_list_list, Batch_list = create_model("Batch_list", {"briefnr":int, "fname":str})
    briefzei_list_list, Briefzei_list = create_model_like(Briefzei)
    gl_main_list_list, Gl_main_list = create_model_like(Gl_main)
    gl_department_list_list, Gl_department_list = create_model_like(Gl_department)
    t_gl_acct_list, T_gl_acct = create_model("T_gl_acct", {"fibukonto":str, "bezeich":str, "acc_type":int, "main_nr":int, "deptnr":int, "actual":[decimal,12], "budget":[decimal,12], "last_yr":[decimal,12], "ly_budget":[decimal,12], "debit":[decimal,12]})
    t_exrate_list, T_exrate = create_model_like(Exrate)
    t_exrate1_list, T_exrate1 = create_model_like(Exrate)
    t_gl_accthis_list, T_gl_accthis = create_model("T_gl_accthis", {"fibukonto":str, "year":int, "actual":[decimal,12], "budget":[decimal,12], "last_yr":[decimal,12], "ly_budget":[decimal,12], "debit":[decimal,12]})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal end_month, prev_month, beg_month, keycmd, keyvar, keycont, c_param64, c_param977, c_param170, c_param144, c_foreign_nr, d_param795, xls_dir, prog_error, error_nr, msg_str, htv_list_list, htp_list_list, brief_list_list, batch_list_list, briefzei_list_list, gl_main_list_list, gl_department_list_list, t_gl_acct_list, t_exrate_list, t_exrate1_list, t_gl_accthis_list, batch_file, curr_row, curr_texte, lvcarea, i, briefzei, gl_main, gl_department, exrate, htparam, gl_acct, waehrung, gl_accthis, brief
        nonlocal pvilanguage, briefnr, to_date, close_month


        nonlocal htv_list, htp_list, brief_list, batch_list, briefzei_list, gl_main_list, gl_department_list, t_gl_acct, t_exrate, t_exrate1, t_gl_accthis
        nonlocal htv_list_list, htp_list_list, brief_list_list, batch_list_list, briefzei_list_list, gl_main_list_list, gl_department_list_list, t_gl_acct_list, t_exrate_list, t_exrate1_list, t_gl_accthis_list

        return {"end_month": end_month, "prev_month": prev_month, "beg_month": beg_month, "keycmd": keycmd, "keyvar": keyvar, "keycont": keycont, "c_param64": c_param64, "c_param977": c_param977, "c_param170": c_param170, "c_param144": c_param144, "c_foreign_nr": c_foreign_nr, "d_param795": d_param795, "xls_dir": xls_dir, "prog_error": prog_error, "error_nr": error_nr, "msg_str": msg_str, "htv-list": htv_list_list, "htp-list": htp_list_list, "brief-list": brief_list_list, "batch-list": batch_list_list, "briefzei-list": briefzei_list_list, "gl-main-list": gl_main_list_list, "gl-department-list": gl_department_list_list, "t-gl-acct": t_gl_acct_list, "t-exrate": t_exrate_list, "t-exrate1": t_exrate1_list, "t-gl-accthis": t_gl_accthis_list}

    def fill_list():

        nonlocal end_month, prev_month, beg_month, keycmd, keyvar, keycont, c_param64, c_param977, c_param170, c_param144, c_foreign_nr, d_param795, xls_dir, prog_error, error_nr, msg_str, htv_list_list, htp_list_list, brief_list_list, batch_list_list, briefzei_list_list, gl_main_list_list, gl_department_list_list, t_gl_acct_list, t_exrate_list, t_exrate1_list, t_gl_accthis_list, batch_file, curr_row, curr_texte, lvcarea, briefzei, gl_main, gl_department, exrate, htparam, gl_acct, waehrung, gl_accthis, brief
        nonlocal pvilanguage, briefnr, to_date, close_month


        nonlocal htv_list, htp_list, brief_list, batch_list, briefzei_list, gl_main_list, gl_department_list, t_gl_acct, t_exrate, t_exrate1, t_gl_accthis
        nonlocal htv_list_list, htp_list_list, brief_list_list, batch_list_list, briefzei_list_list, gl_main_list_list, gl_department_list_list, t_gl_acct_list, t_exrate_list, t_exrate1_list, t_gl_accthis_list

        i:int = 0
        j:int = 0
        n:int = 0
        c:str = ""
        l:int = 0
        continued:bool = False

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 600)).first()
        keycmd = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 2030)).first()
        keyvar = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 1122)).first()
        keycont = keycmd + htparam.fchar

        for htparam in db_session.query(Htparam).filter(
                 (Htparam.paramgruppe == 39) & (Htparam.paramnr != 2030)).order_by(len(Htparam.fchar).desc()).all():

            if substring(htparam.fchar, 0 , 1) == (".").lower() :
                htv_list = Htv_list()
                htv_list_list.append(htv_list)

                htv_list.paramnr = htparam.paramnr
                htv_list.fchar = htparam.fchar
            else:
                htp_list = Htp_list()
                htp_list_list.append(htp_list)

                htp_list.paramnr = htparam.paramnr
                htp_list.fchar = keycmd + htparam.fchar
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 2055
        htv_list.fchar = ".a"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 2059
        htv_list.fchar = ".2"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 2067
        htv_list.fchar = ".3"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 2057
        htv_list.fchar = ".4"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 2058
        htv_list.fchar = ".5"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 2062
        htv_list.fchar = ".6"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 2043
        htv_list.fchar = ".7"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 2044
        htv_list.fchar = ".8"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 2056
        htv_list.fchar = ".9"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 2069
        htv_list.fchar = ".10"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3001
        htv_list.fchar = ".BJAN"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3002
        htv_list.fchar = ".BFEB"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3003
        htv_list.fchar = ".BMAR"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3004
        htv_list.fchar = ".BAPR"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3005
        htv_list.fchar = ".BMAY"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3006
        htv_list.fchar = ".BJUN"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3007
        htv_list.fchar = ".BJUL"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3008
        htv_list.fchar = ".BAUG"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3009
        htv_list.fchar = ".BSEP"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3010
        htv_list.fchar = ".BOCT"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3011
        htv_list.fchar = ".BNOV"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3012
        htv_list.fchar = ".BDEC"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3021
        htv_list.fchar = ".NBJAN"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3022
        htv_list.fchar = ".NBFEB"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3023
        htv_list.fchar = ".NBMAR"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3024
        htv_list.fchar = ".NBAPR"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3025
        htv_list.fchar = ".NBMAY"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3026
        htv_list.fchar = ".NBJUN"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3027
        htv_list.fchar = ".NBJUL"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3028
        htv_list.fchar = ".NBAUG"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3029
        htv_list.fchar = ".NBSEP"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3030
        htv_list.fchar = ".NBOCT"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3031
        htv_list.fchar = ".NBNOV"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3032
        htv_list.fchar = ".NBDEC"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3041
        htv_list.fchar = ".JAN"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3042
        htv_list.fchar = ".FEB"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3043
        htv_list.fchar = ".MAR"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3044
        htv_list.fchar = ".APR"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3045
        htv_list.fchar = ".MAY"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3046
        htv_list.fchar = ".JUN"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3047
        htv_list.fchar = ".JUL"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3048
        htv_list.fchar = ".AUG"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3049
        htv_list.fchar = ".SEP"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3050
        htv_list.fchar = ".OCT"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3051
        htv_list.fchar = ".NOV"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3052
        htv_list.fchar = ".DEC"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3061
        htv_list.fchar = ".LJAN"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3062
        htv_list.fchar = ".LFEB"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3063
        htv_list.fchar = ".LMAR"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3064
        htv_list.fchar = ".LAPR"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3065
        htv_list.fchar = ".LMAY"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3066
        htv_list.fchar = ".LJUN"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3067
        htv_list.fchar = ".LJUL"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3068
        htv_list.fchar = ".LAUG"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3069
        htv_list.fchar = ".LSEP"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3070
        htv_list.fchar = ".LOCT"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3071
        htv_list.fchar = ".LNOV"
        htv_list = Htv_list()
        htv_list_list.append(htv_list)

        htv_list.paramnr = 3072
        htv_list.fchar = ".LDEC"

        for briefzei in db_session.query(Briefzei).filter(
                     (Briefzei.briefnr == briefnr)).order_by(Briefzei.briefzeilnr).all():
            j = 1
            for i in range(1,len(briefzei.texte)  + 1) :

                if asc(substring(briefzei.texte, i - 1, 1)) == 10:
                    n = i - j
                    c = substring(briefzei.texte, j - 1, n)
                    l = len(c)

                    if not continued:
                        brief_list = Brief_list()
                    brief_list_list.append(brief_list)

                    brief_list.b_text = brief_list.b_text + c
                    j = i + 1

                    if l > len((keycont).lower() ) and substring(c, l - len((keycont).lower() ) + 1 - 1, len((keycont).lower() )) == (keycont).lower() :
                        continued = True
                        b_text = substring(b_text, 0, len(b_text) - len(keycont))
                    else:
                        continued = False
            n = len(briefzei.texte) - j + 1
            c = substring(briefzei.texte, j - 1, n)

            if not continued:
                brief_list = Brief_list()
            brief_list_list.append(brief_list)

            b_text = b_text + c


    def check_batch():

        nonlocal end_month, prev_month, beg_month, keycmd, keyvar, keycont, c_param64, c_param977, c_param170, c_param144, c_foreign_nr, d_param795, xls_dir, prog_error, error_nr, msg_str, htv_list_list, htp_list_list, brief_list_list, batch_list_list, briefzei_list_list, gl_main_list_list, gl_department_list_list, t_gl_acct_list, t_exrate_list, t_exrate1_list, t_gl_accthis_list, batch_file, curr_row, curr_texte, lvcarea, i, briefzei, gl_main, gl_department, exrate, htparam, gl_acct, waehrung, gl_accthis, brief
        nonlocal pvilanguage, briefnr, to_date, close_month


        nonlocal htv_list, htp_list, brief_list, batch_list, briefzei_list, gl_main_list, gl_department_list, t_gl_acct, t_exrate, t_exrate1, t_gl_accthis
        nonlocal htv_list_list, htp_list_list, brief_list_list, batch_list_list, briefzei_list_list, gl_main_list_list, gl_department_list_list, t_gl_acct_list, t_exrate_list, t_exrate1_list, t_gl_accthis_list

        texte:str = ""
        correct:bool = False
        bnr:int = 0
        row_nr:int = 0
        return_flag:bool = False

        htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == 2038), first=True)

        for brief_list in query(brief_list_list):
            row_nr = row_nr + 1
            texte = trim(brief_list.b_text)

            if batch_file:
                correct = check_integer(texte)

                if correct:
                    bnr = to_int(texte)

                    brief = db_session.query(Brief).filter(
                             (Brief.briefnr == bnr)).first()

                    if not brief:
                        msg_str = msg_str + chr(2) + translateExtended ("No such report file number", lvcarea, "") + " " + to_string(bnr) + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(row_nr) + chr(10) + substring(texte, 0, len(texte))
                        prog_error = True
                        error_nr = - 1
                        return_flag = True
                        break
                    batch_list = Batch_list()
                    batch_list_list.append(batch_list)

                    batch_list.briefnr = bnr
                    batch_list.fname = brief.fname
                else:
                    return_flag = True
                    break

            if texte == htp_list.fchar:
                batch_file = True

        if return_flag:

            return

        if not batch_file:
            batch_list = Batch_list()
            batch_list_list.append(batch_list)


            brief = db_session.query(Brief).filter(
                     (Brief.briefnr == briefnr)).first()
            batch_list.briefnr = briefnr
            batch_list.fname = brief.fname


    def check_integer(texte:str):

        nonlocal end_month, prev_month, beg_month, keycmd, keyvar, keycont, c_param64, c_param977, c_param170, c_param144, c_foreign_nr, d_param795, xls_dir, prog_error, error_nr, msg_str, htv_list_list, htp_list_list, brief_list_list, batch_list_list, briefzei_list_list, gl_main_list_list, gl_department_list_list, t_gl_acct_list, t_exrate_list, t_exrate1_list, t_gl_accthis_list, batch_file, curr_row, curr_texte, lvcarea, briefzei, gl_main, gl_department, exrate, htparam, gl_acct, waehrung, gl_accthis, brief
        nonlocal pvilanguage, briefnr, to_date, close_month


        nonlocal htv_list, htp_list, brief_list, batch_list, briefzei_list, gl_main_list, gl_department_list, t_gl_acct, t_exrate, t_exrate1, t_gl_accthis
        nonlocal htv_list_list, htp_list_list, brief_list_list, batch_list_list, briefzei_list_list, gl_main_list_list, gl_department_list_list, t_gl_acct_list, t_exrate_list, t_exrate1_list, t_gl_accthis_list

        correct = True
        i:int = 0

        def generate_inner_output():
            return (correct)


        if len(texte) == 0:
            correct = False
        for i in range(1,len(texte)  + 1) :

            if asc(substring(texte, i - 1, 1)) > 57 or asc(substring(texte, i, 1)) < 48:
                correct = False

        if not correct:
            msg_str = msg_str + chr(2) + translateExtended ("Program expected a number:", lvcarea, "") + " " + texte + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return generate_inner_output()

        return generate_inner_output()


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 418)).first()

    if htparam.fchar == "":
        msg_str = msg_str + chr(2) + translateExtended ("Excel Output Directory not defined (Param 418 Grp 15)", lvcarea, "")

        return generate_output()
    xls_dir = htparam.fchar

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 993)).first()
    end_month = htparam.finteger
    beg_month = htparam.finteger + 1

    if beg_month > 12:
        beg_month = 1
    prev_month = close_month - 1

    if prev_month == 0:
        prev_month = 12

    if close_month == 0:

        return generate_output()
    fill_list()
    check_batch()

    if prog_error:

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 64)).first()
    c_param64 = htparam.fchar

    for briefzei in db_session.query(Briefzei).filter(
             (Briefzei.briefnr == briefnr)).order_by(Briefzei.briefzeilnr).all():
        briefzei_list = Briefzei_list()
        briefzei_list_list.append(briefzei_list)

        buffer_copy(briefzei, briefzei_list)

    for gl_main in db_session.query(Gl_main).order_by(Gl_main._recid).all():
        gl_main_list = Gl_main_list()
        gl_main_list_list.append(gl_main_list)

        buffer_copy(gl_main, gl_main_list)

    for gl_department in db_session.query(Gl_department).order_by(Gl_department._recid).all():
        gl_department_list = Gl_department_list()
        gl_department_list_list.append(gl_department_list)

        buffer_copy(gl_department, gl_department_list)

    for gl_acct in db_session.query(Gl_acct).order_by(Gl_acct._recid).all():
        t_gl_acct = T_gl_acct()
        t_gl_acct_list.append(t_gl_acct)

        t_gl_acct.fibukonto = gl_acct.fibukonto
        t_gl_acct.bezeich = gl_acct.bezeich
        t_gl_acct.acc_type = gl_acct.acc_type
        t_gl_acct.main_nr = gl_acct.main_nr
        t_gl_acct.deptnr = gl_acct.deptnr


        for i in range(1,12 + 1) :
            t_gl_acct.actual[i - 1] = gl_acct.actual[i - 1]
            t_gl_acct.budget[i - 1] = gl_acct.budget[i - 1]
            t_gl_acct.last_yr[i - 1] = gl_acct.last_yr[i - 1]
            t_gl_acct.ly_budget[i - 1] = gl_acct.ly_budget[i - 1]
            t_gl_acct.debit[i - 1] = gl_acct.debit[i - 1]

    for exrate in db_session.query(Exrate).filter(
             (Exrate.artnr == 99999) | (Exrate.artnr == 99998)).order_by(Exrate._recid).all():
        t_exrate = T_exrate()
        t_exrate_list.append(t_exrate)

        buffer_copy(exrate, t_exrate)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 795)).first()
    d_param795 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 977)).first()
    c_param977 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 170)).first()
    c_param170 = htparam.fchar

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 144)).first()
    c_param144 = htparam.fchar

    if c_param144 != "":

        waehrung = db_session.query(Waehrung).filter(
                 (func.lower(Waehrung.wabkurz) == (c_param144).lower())).first()

        if waehrung:
            c_foreign_nr = waehrung.waehrungsnr

    if c_foreign_nr != 0:

        for exrate in db_session.query(Exrate).filter(
                 (Exrate.artnr == c_foreign_nr)).order_by(Exrate._recid).all():
            t_exrate1 = T_exrate1()
            t_exrate1_list.append(t_exrate1)

            buffer_copy(exrate, t_exrate1)

    for gl_accthis in db_session.query(Gl_accthis).filter(
             (Gl_accthis.year == get_year(to_date))).order_by(Gl_accthis._recid).all():
        t_gl_accthis = T_gl_accthis()
        t_gl_accthis_list.append(t_gl_accthis)

        t_gl_accthis.fibukonto = gl_accthis.fibukonto
        t_gl_accthis.year = gl_accthis.year


        for i in range(1,12 + 1) :
            t_gl_accthis.actual[i - 1] = gl_accthis.actual[i - 1]
            t_gl_accthis.budget[i - 1] = gl_accthis.budget[i - 1]
            t_gl_accthis.last_yr[i - 1] = gl_accthis.last_yr[i - 1]
            t_gl_accthis.ly_budget[i - 1] = gl_accthis.ly_budget[i - 1]
            t_gl_accthis.debit[i - 1] = gl_accthis.debit[i - 1]

    return generate_output()