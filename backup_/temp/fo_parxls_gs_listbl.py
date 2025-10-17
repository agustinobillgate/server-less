#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.prepare_fo_parxlsbl import prepare_fo_parxlsbl
from functions.fo_parxls_gsbl import fo_parxls_gsbl
from models import Brief, Parameters

def fo_parxls_gs_listbl(pvilanguage:int, briefnr:int, from_date:date, to_date:date, link:string):
    msg_str = ""
    mess_result = "Failed to generate data"
    success_flag = False
    lvcarea:string = "fo-parxls-gs"
    ch:string = ""
    xls_dir:string = ""
    budget_flag:bool = False
    ytd_flag:bool = False
    lytd_flag:bool = False
    lmtd_flag:bool = False
    pmtd_flag:bool = False
    budget_all:bool = False
    serv_vat:bool = False
    zeit:int = 0
    no_decimal:bool = False
    prog_error:bool = False
    error_nr:int = 0
    curr_row:int = 0
    curr_column:int = 0
    curr_cmd:int = 0
    curr_texte:string = ""
    curr_pos:int = 0
    actual_cmd:int = 0
    grp_nr:int = 0
    curr_nr:int = 0
    varname:string = ""
    bezeich:string = ""
    grpflag:int = 0
    lfrom_date:date = None
    lto_date:date = None
    jan1:date = None
    ljan1:date = None
    pfrom_date:date = None
    pto_date:date = None
    curr_month:int = 1
    n:int = 0
    keycmd:string = ""
    keyvar:string = ""
    foreign_flag:bool = False
    foreign_nr:int = 0
    start_date:date = None
    lytoday:date = None
    lytoday_flag:bool = True
    price_decimal:int = 0
    msg_ans:bool = False
    outfile_dir:string = ""
    anz0:int = 0
    datum:date = None
    brief = parameters = None

    detail_list = brief_list = batch_list = htp_list = htv_list = t_brief = w1 = w2 = t_parameters = None

    detail_list_data, Detail_list = create_model("Detail_list", {"nr":int, "str_buffer":string, "field_value":[Decimal,12], "use_flag":[bool,12]})
    brief_list_data, Brief_list = create_model("Brief_list", {"b_text":string})
    batch_list_data, Batch_list = create_model("Batch_list", {"briefnr":int, "fname":string})
    htp_list_data, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":string})
    htv_list_data, Htv_list = create_model("Htv_list", {"paramnr":int, "fchar":string})
    t_brief_data, T_brief = create_model_like(Brief)
    w1_data, W1 = create_model("W1", {"nr":int, "varname":string, "main_code":int, "s_artnr":string, "artnr":int, "dept":int, "grpflag":int, "done":bool, "bezeich":string, "int_flag":bool, "tday":Decimal, "tday_serv":Decimal, "tday_tax":Decimal, "mtd_serv":Decimal, "mtd_tax":Decimal, "ytd_serv":Decimal, "ytd_tax":Decimal, "yesterday":Decimal, "saldo":Decimal, "lastmon":Decimal, "pmtd_serv":Decimal, "pmtd_tax":Decimal, "lmtd_serv":Decimal, "lmtd_tax":Decimal, "lastyr":Decimal, "lytoday":Decimal, "ytd_saldo":Decimal, "lytd_saldo":Decimal, "year_saldo":[Decimal,12], "mon_saldo":[Decimal,31], "mon_budget":[Decimal,31], "mon_lmtd":[Decimal,31], "tbudget":Decimal, "budget":Decimal, "lm_budget":Decimal, "lm_today":Decimal, "lm_today_serv":Decimal, "lm_today_tax":Decimal, "lm_mtd":Decimal, "lm_ytd":Decimal, "ly_budget":Decimal, "ny_budget":Decimal, "ytd_budget":Decimal, "nytd_budget":Decimal, "nmtd_budget":Decimal, "lytd_budget":Decimal, "lytd_serv":Decimal, "lytd_tax":Decimal, "lytoday_serv":Decimal, "lytoday_tax":Decimal, "month_budget":Decimal, "year_budget":Decimal, "tischnr":int, "mon_serv":[Decimal,31], "mon_tax":[Decimal,31]})
    w2_data, W2 = create_model("W2", {"val_sign":int, "nr1":int, "nr2":int}, {"val_sign": 1})
    t_parameters_data, T_parameters = create_model_like(Parameters)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        return {"msg_str": msg_str, "mess_result": mess_result, "success_flag": success_flag}

    def create_var0(texte:string, int_flag:bool):

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        subtext:string = ""
        subtext = get_subtext(texte, subtext)

        if subtext == "":
            msg_str = translateExtended ("Program expected a new key variable name .xxx", lvcarea, "") + chr_unicode(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
            prog_error = True
            error_nr = - 1

            return

        elif substring(subtext, 0, 1) != (keyvar).lower() :
            msg_str = translateExtended ("Program expected", lvcarea, "") + " " + keyvar + " " + translateExtended ("for any variable", lvcarea, "") + chr_unicode(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
            prog_error = True
            error_nr = - 1

            return
        else:
            varname = subtext
            w1 = W1()
            w1_data.append(w1)

            curr_nr = curr_nr + 1
            w1.nr = curr_nr
            w1.int_flag = int_flag
            w1.varname = varname
            w1.main_code = curr_cmd
            curr_column = length(curr_texte) + 1
            curr_cmd = 0


    def create_var1(texte:string, int_flag:bool):

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        subtext:string = ""
        correct:bool = False
        nr:int = 0

        if texte == "":

            return
        subtext = get_subtext(texte, subtext)

        if subtext == "":
            msg_str = translateExtended ("Program expected a new key variable name .xxx", lvcarea, "") + chr_unicode(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
            prog_error = True
            error_nr = - 1

            return

        elif substring(subtext, 0, 1) != (keyvar).lower() :
            msg_str = translateExtended ("Program expected", lvcarea, "") + " " + keyvar + " " + translateExtended ("for any variable", lvcarea, "") + chr_unicode(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
            prog_error = True
            error_nr = - 1

            return
        else:
            varname = subtext
            subtext = trim(substring(texte, curr_column - 1, length(texte) - curr_column + 1))

            if curr_cmd == 800 or curr_cmd == 180 or curr_cmd == 181 or curr_cmd == 9985 or curr_cmd == 9986 or curr_cmd == 1995 or curr_cmd == 1996 or curr_cmd == 1997 or curr_cmd == 1998 or curr_cmd == 1999:
                pass
            else:
                correct = check_integer(subtext)

            if correct:
                nr = to_int(subtext)
            w1 = W1()
            w1_data.append(w1)

            curr_nr = curr_nr + 1
            w1.nr = curr_nr
            w1.int_flag = int_flag
            w1.varname = varname
            w1.main_code = curr_cmd

            if curr_cmd == 192:
                w1.dept = nr

            elif curr_cmd == 197:
                w1.dept = nr

            elif curr_cmd == 552:
                w1.dept = nr
            else:
                w1.artnr = nr

            if curr_cmd == 1921:
                w1.dept = nr

            if curr_cmd == 1922:
                w1.dept = nr

            if curr_cmd == 1923:
                w1.dept = nr

            if curr_cmd == 1924:
                w1.dept = nr

            if curr_cmd == 1971:
                w1.dept = nr

            if curr_cmd == 1972:
                w1.dept = nr

            if curr_cmd == 1973:
                w1.dept = nr

            if curr_cmd == 1974:
                w1.dept = nr

            if curr_cmd == 1991:
                w1.dept = nr

            if curr_cmd == 1992:
                w1.dept = nr

            if curr_cmd == 1993:
                w1.dept = nr

            if curr_cmd == 1994:
                w1.dept = nr

            if curr_cmd == 2001:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2002:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2003:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2004:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2005:
                w1.dept = nr

            if curr_cmd == 2006:
                w1.dept = nr

            if curr_cmd == 2007:
                w1.dept = nr

            if curr_cmd == 2008:
                w1.dept = nr

            if curr_cmd == 2009:
                w1.dept = nr

            if curr_cmd == 2010:
                w1.dept = nr

            if curr_cmd == 2011:
                w1.dept = nr

            if curr_cmd == 2012:
                w1.dept = nr

            if curr_cmd == 2013:
                w1.dept = nr

            if curr_cmd == 2014:
                w1.dept = nr

            if curr_cmd == 2015:
                w1.dept = nr

            if curr_cmd == 2016:
                w1.dept = nr

            if curr_cmd == 2020:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2021:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2022:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2023:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2024:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2025:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2026:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2027:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2028:
                w1.dept = nr

            if curr_cmd == 2029:
                w1.dept = nr

            if curr_cmd == 2032:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2033:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2034:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2035:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2036:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2037:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2038:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2039:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2040:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2041:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2042:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2043:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2044:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2045:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2046:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2047:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2048:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2049:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2050:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2051:
                w1.dept = to_int(substring(subtext, 1, 3))

            if curr_cmd == 2052:
                w1.dept = nr

            if curr_cmd == 2053:
                w1.dept = nr

            if curr_cmd == 2054:
                w1.dept = nr

            if curr_cmd == 2055:
                w1.dept = nr

            if curr_cmd == 2056:
                w1.dept = nr

            if curr_cmd == 2057:
                w1.dept = nr

            if curr_cmd == 2058:
                w1.dept = nr

            if curr_cmd == 2059:
                w1.dept = nr

            if curr_cmd == 800 or curr_cmd == 180 or curr_cmd == 181 or curr_cmd == 9985 or curr_cmd == 9986 or curr_cmd == 1995 or curr_cmd == 1996 or curr_cmd == 1997 or curr_cmd == 1998 or curr_cmd == 1999:
                w1.s_artnr = subtext
            curr_column = length(curr_texte) + 1
            curr_cmd = 0


    def create_var2(texte:string, int_flag:bool):

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        subtext:string = ""
        correct:bool = False
        nr:int = 0
        dept:int = 0
        subtext = get_subtext(texte, subtext)

        if subtext == "":
            msg_str = translateExtended ("Program expected a new key variable name .xxx", lvcarea, "") + chr_unicode(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
            prog_error = True
            error_nr = - 1

            return

        elif substring(subtext, 0, 1) != (keyvar).lower() :
            msg_str = translateExtended ("Program expected", lvcarea, "") + " " + keyvar + " " + translateExtended ("for any variable", lvcarea, "") + chr_unicode(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
            prog_error = True
            error_nr = - 1

            return
        else:
            varname = subtext
            subtext = trim(substring(texte, curr_column - 1, length(texte) - curr_column + 1))
            correct = check_integer(subtext)

            if correct:
                dept = to_int(substring(subtext, 0, 2))
                nr = to_int(substring(subtext, 2, 6))
            w1 = W1()
            w1_data.append(w1)

            curr_nr = curr_nr + 1
            w1.nr = curr_nr
            w1.int_flag = int_flag
            w1.varname = varname
            w1.main_code = curr_cmd
            w1.artnr = nr
            w1.dept = dept
            curr_column = length(curr_texte) + 1
            curr_cmd = 0


    def create_w1():

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        ind = 0
        w1_nr:int = 0

        def generate_inner_output():
            return (ind)

        w1 = W1()
        w1_data.append(w1)

        curr_nr = curr_nr + 1
        ind = curr_nr
        w1_nr = curr_nr
        w1.nr = curr_nr
        w1.varname = varname
        w1.grpflag = grpflag

        if grpflag == 2:
            w1.bezeich = bezeich

        elif grpflag == 9:
            w1.bezeich = bezeich

        return generate_inner_output()


    def create_w2(ind:int, nr2:int, nr:int, val_sign:int):

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        n:int = 0

        if nr == 2:
            w2 = W2()
            w2_data.append(w2)

            w2.nr1 = ind
            w2.nr2 = nr2
        w2.val_sign = val_sign


    def analyse_textheader(texte:string):

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        subtext:string = ""
        subtext = get_subtext(texte, subtext)

        if subtext != "":
            interprete_subtext(texte, subtext)


    def get_subtext(texte:string, subtext:string):

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        j:int = 0
        stopped:bool = False

        def generate_inner_output():
            return (subtext)

        texte = trim(substring(texte, curr_column - 1, length(texte) - curr_column + 1))
        stopped = False
        j = 1
        while not stopped:

            if j == length(texte) or substring(texte, j + 1 - 1, 1) == " ":
                stopped = True
            else:
                j = j + 1
        subtext = substring(texte, 0, j)
        curr_column = curr_column + j + 1

        return generate_inner_output()


    def interprete_subtext(texte:string, subtext:string):

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        j:int = 0
        found:bool = False

        htp_list = query(htp_list_data, first=True)
        while None != htp_list and not found:

            if htp_list.fchar.lower()  == (subtext).lower() :
                found = True
                curr_cmd = htp_list.paramnr

            htp_list = query(htp_list_data, next=True)

        if not found:
            msg_str = translateExtended ("Can not understand line", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
            prog_error = True
            error_nr = - 1

            return


    def check_integer(texte:string):

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        correct = True
        i:int = 0

        def generate_inner_output():
            return (correct)


        if length(texte) == 0:
            correct = False
        for i in range(1,length(texte)  + 1) :

            if asc(substring(texte, i - 1, 1)) > 57 or asc(substring(texte, i, 1)) < 48:
                correct = False

        if not correct:
            msg_str = translateExtended ("Program expected a number : ", lvcarea, "") + texte + chr_unicode(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
            prog_error = True
            error_nr = - 1

            return generate_inner_output()

        return generate_inner_output()


    def create_group(texte:string):

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        subtext:string = ""
        correct:bool = False
        subtext = get_subtext(texte, subtext)

        if subtext == "":
            msg_str = translateExtended ("Program expected a variable name", lvcarea, "") + chr_unicode(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
            prog_error = True
            error_nr = - 1

            return

        elif substring(subtext, 0, 1) != (keyvar).lower() :
            msg_str = translateExtended ("Program expected", lvcarea, "") + " " + keyvar + " " + translateExtended ("for any variable", lvcarea, "") + chr_unicode(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
            prog_error = True
            error_nr = - 1

            return
        else:
            varname = subtext
            bezeich = trim(substring(texte, curr_column - 1, length(texte) - curr_column + 1))

            if bezeich == "":
                msg_str = translateExtended ("Program expected a description", lvcarea, "") + chr_unicode(10) + translateExtended ("at line number : ", lvcarea, "") + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
                prog_error = True
                error_nr = - 1

                return
            else:
                grpflag = 2
                grp_nr = create_w1()
                curr_column = length(texte) + 1


    def create_group_variable(texte:string):

        nonlocal msg_str, mess_result, success_flag, lvcarea, ch, xls_dir, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, budget_all, serv_vat, zeit, no_decimal, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, curr_pos, actual_cmd, grp_nr, curr_nr, varname, bezeich, grpflag, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, curr_month, n, keycmd, keyvar, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, price_decimal, msg_ans, outfile_dir, anz0, datum, brief, parameters
        nonlocal pvilanguage, briefnr, from_date, to_date, link


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, t_brief, w1, w2, t_parameters
        nonlocal detail_list_data, brief_list_data, batch_list_data, htp_list_data, htv_list_data, t_brief_data, w1_data, w2_data, t_parameters_data

        i:int = 0
        val_sign:int = 1

        htp_list = query(htp_list_data, filters=(lambda htp_list: htp_list.paramnr == 287), first=True)

        if texte == htp_list.fchar:
            actual_cmd = 0

            return

        if substring(texte, 0, 1) == ("-").lower() :
            val_sign = - 1
            texte = substring(texte, 1, length(texte))
            texte = trim(texte)

        if substring(texte, 0, 1) == (keyvar).lower() :

            w1 = query(w1_data, filters=(lambda w1: w1.varname.lower()  == (texte).lower()), first=True)

            if not w1:
                msg_str = translateExtended ("No such variable found", lvcarea, "") + " "+ texte + chr_unicode(10) + translateExtended ("at line number :", lvcarea, "") + " " + to_string(curr_row) + chr_unicode(10) + substring(curr_texte, 0, length(curr_texte))
                prog_error = True
                error_nr = - 1

                return
            else:
                create_w2(grp_nr, w1.nr, 2, val_sign)

    xls_dir, msg_str, serv_vat, foreign_nr, start_date, price_decimal, no_decimal, keycmd, keyvar, outfile_dir, anz0, htv_list_data, htp_list_data, brief_list_data, t_brief_data, t_parameters_data = get_output(prepare_fo_parxlsbl(pvilanguage, briefnr))
    zeit = get_current_time_in_seconds()
    detail_list = Detail_list()
    detail_list_data.append(detail_list)

    detail_list.nr = 0

    if get_month(to_date) == 2 and get_day(to_date) == 29:
        lytoday = date_mdy(2, 28, get_year(to_date) - timedelta(days=1))


    else:
        lytoday = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - timedelta(days=1))


    jan1 = date_mdy(1, 1, get_year(to_date))
    ljan1 = date_mdy(1, 1, get_year(to_date) - timedelta(days=1))

    if (start_date != None) and (start_date > from_date):
        from_date = start_date
        jan1 = start_date
        ljan1 = date_mdy(get_month(jan1) , get_day(jan1) , get_year(jan1) - timedelta(days=1))
    pto_date = from_date - timedelta(days=1)

    if (get_month(to_date) == get_month(to_date + 1)):

        if get_month(pto_date) == 2:

            if get_day(to_date) < get_day(pto_date):
                pto_date = date_mdy(get_month(pto_date) , get_day(to_date) , get_year(pto_date))
        else:
            pto_date = date_mdy(get_month(pto_date) , get_day(to_date) , get_year(pto_date))
    pfrom_date = date_mdy(get_month(pto_date) , 1, get_year(pto_date))

    if (get_month(to_date) != 2) or (get_day(to_date) != 29):
        lto_date = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - timedelta(days=1))
    else:
        lto_date = date_mdy(get_month(to_date) , 28, get_year(to_date) - timedelta(days=1))
    lfrom_date = date_mdy(get_month(to_date) , 1, get_year(lto_date))

    t_brief = query(t_brief_data, first=True)
    batch_list = Batch_list()
    batch_list_data.append(batch_list)

    batch_list.briefnr = briefnr
    batch_list.fname = t_brief.fname

    for brief_list in query(brief_list_data):
        curr_texte = trim(b_text)
        curr_pos = 1
        curr_column = 1
        curr_row = curr_row + 1

        for detail_list in query(detail_list_data, filters=(lambda detail_list: detail_list.nr > 0)):
            detail_list_data.remove(detail_list)

        detail_list = query(detail_list_data, filters=(lambda detail_list: detail_list.nr == 0), first=True)
        detail_list.str_buffer = ""
        for n in range(1,12 + 1) :
            detail_list.field_value[n - 1] = 0
            detail_list.use_flag[n - 1] = False

        if substring(curr_texte, 0, 1) != ("#").lower() :

            if actual_cmd == 0 and curr_texte != "":
                analyse_textheader(curr_texte)

                if prog_error:

                    return generate_output()

                if curr_cmd == 184:
                    foreign_flag = True

                elif curr_cmd == 801:
                    budget_flag = True

                elif curr_cmd == 802:
                    ytd_flag = True

                elif curr_cmd == 803:
                    lytd_flag = True

                elif curr_cmd == 841:
                    lmtd_flag = True

                elif curr_cmd == 804:
                    pmtd_flag = True

                elif curr_cmd == 829:
                    budget_all = True

                elif curr_cmd == 182:
                    create_var0(curr_texte, False)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 183:
                    create_var0(curr_texte, False)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 807 or curr_cmd == 808 or curr_cmd == 811 or curr_cmd == 812:
                    create_var0(curr_texte, False)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 129 or curr_cmd == 805 or curr_cmd == 806 or curr_cmd == 810 or curr_cmd == 122 or curr_cmd == 752 or curr_cmd == 288 or curr_cmd == 1019:
                    create_var0(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd >= 753 and curr_cmd <= 755:
                    create_var0(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 85 or curr_cmd == 86 or curr_cmd == 106 or curr_cmd == 107 or curr_cmd == 187 or curr_cmd == 188 or curr_cmd == 189 or curr_cmd == 190 or curr_cmd == 191 or curr_cmd == 193 or curr_cmd == 194 or curr_cmd == 195 or curr_cmd == 211 or curr_cmd == 231 or curr_cmd == 742 or curr_cmd == 750 or curr_cmd == 751 or curr_cmd == 969 or curr_cmd == 9106 or curr_cmd == 7194 or curr_cmd == 7195 or curr_cmd == 9188 or curr_cmd == 9190 or curr_cmd == 9000:
                    create_var0(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 92:
                    create_var1(curr_texte, False)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 800:
                    create_var1(curr_texte, False)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 9985 or curr_cmd == 9986 or curr_cmd == 1995 or curr_cmd == 1996 or curr_cmd == 1997 or curr_cmd == 1998 or curr_cmd == 1999:
                    create_var1(curr_texte, False)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 179:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 180 or curr_cmd == 181:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 813 or curr_cmd == 814 or (curr_cmd >= 756 and curr_cmd <= 758):
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 192:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 197:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 552:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1921:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1922:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1923:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1924:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1971:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1972:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1973:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1974:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1991:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1992:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1993:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1994:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1008:
                    create_var2(curr_texte, False)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 809:
                    create_var2(curr_texte, False)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 1084:
                    create_var2(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 2001:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2002:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2003:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2004:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2005:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2006:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2007:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2008:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2009:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2010:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2011:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2012:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2013:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2014:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2015:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2016:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2020:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2021:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2022:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2023:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2024:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2025:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2026:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2027:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2028:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2029:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2031:
                    create_var3(curr_texte, True)

                elif curr_cmd == 2032:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2033:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2034:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2035:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2036:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2037:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2038:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2039:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2040:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2041:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2042:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2043:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2044:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2045:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2046:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2047:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2048:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2049:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2050:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2051:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2052:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2053:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2054:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2055:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2056:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2057:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2058:
                    create_var1(curr_texte, True)

                elif curr_cmd == 2059:
                    create_var1(curr_texte, True)

                elif curr_cmd == 9092:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 9813:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 9814:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 8092:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 8813:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 8814:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 9981:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 9982:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 9983:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 9984:
                    create_var1(curr_texte, True)

                    if prog_error:

                        return generate_output()

                elif curr_cmd == 840:
                    actual_cmd = curr_cmd
                    create_group(curr_texte)

                    if prog_error:

                        return generate_output()

            elif actual_cmd == 840 and curr_texte != "":
                create_group_variable(curr_texte)

                if prog_error:

                    return generate_output()

    if prog_error:

        return generate_output()
    msg_str, error_nr = get_output(fo_parxls_gsbl(pvilanguage, ytd_flag, jan1, ljan1, lfrom_date, lto_date, pfrom_date, pto_date, from_date, to_date, start_date, lytd_flag, lmtd_flag, pmtd_flag, lytoday_flag, lytoday, foreign_flag, budget_flag, foreign_nr, price_decimal, briefnr, link, budget_all, w1_data, w2_data))

    if msg_str != "":

        return generate_output()
    else:
        mess_result = "Successfully generate data"
        success_flag = True

    return generate_output()