from functions.additional_functions import *
import decimal
from datetime import date
from functions.prepare_fo_parexcelbl import prepare_fo_parexcelbl
from models import Segmentstat

def fo_parexcel_listbl(pvilanguage:int, briefnr:int, to_date:date, check_only:bool, view_only:bool, jobnr:str):
    msg_str = ""
    success_flag = False
    lvcarea:str = "fo-parexcel"
    budget_flag:bool = False
    ytd_flag:bool = False
    lytd_flag:bool = False
    lmtd_flag:bool = False
    pmtd_flag:bool = False
    integer_flag:bool = False
    serv_vat:bool = False
    zeit:int = 0
    margin_c:str = ""
    len_flag:bool = True
    detail_nr:int = 0
    no_decimal:bool = False
    num_digit:int = 12
    value_filled:bool = False
    prog_error:bool = False
    error_nr:int = 0
    curr_row:int = 0
    curr_column:int = 0
    curr_cmd:int = 0
    curr_texte:str = ""
    actual_cmd:int = 0
    detail_loop:int = 0
    grp_nr:int = 0
    curr_nr:int = 0
    varname:str = ""
    bezeich:str = ""
    grpflag:int = 0
    textlen:int = 30
    report_title:str = ""
    from_date:date = None
    lfrom_date:date = None
    lto_date:date = None
    jan1:date = None
    ljan1:date = None
    pfrom_date:date = None
    pto_date:date = None
    outfile_dir:str = ""
    efield:str = ""
    dayname:List[str] = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
    curr_loop:int = 0
    f_lmargin:bool = False
    lmargin:int = 1
    nskip:int = 1
    ntab:int = 1
    n:int = 0
    curr_pos:int = 0
    keycmd:str = ""
    keyvar:str = ""
    infile:str = ""
    outfile:str = ""
    foreign_flag:bool = False
    foreign_nr:int = 0
    start_date:date = None
    lytoday:date = None
    lytoday_flag:bool = False
    ratio_flag:int = 0
    price_decimal:int = 0
    msg_ans:bool = False
    datum:date = None
    segmentstat = None

    detail_list = brief_list = batch_list = htp_list = htv_list = w1 = w2 = w11 = parent_w1 = child_w1 = w1_ratio = segmbuff = None

    detail_list_list, Detail_list = create_model("Detail_list", {"nr":int, "str_buffer":str, "field_value":[decimal,12], "use_flag":[bool,12]})
    brief_list_list, Brief_list = create_model("Brief_list", {"b_text":str})
    batch_list_list, Batch_list = create_model("Batch_list", {"briefnr":int, "fname":str})
    htp_list_list, Htp_list = create_model("Htp_list", {"paramnr":int, "fchar":str})
    htv_list_list, Htv_list = create_model("Htv_list", {"paramnr":int, "fchar":str})
    w1_list, W1 = create_model("W1", {"nr":int, "varname":str, "main_code":int, "artnr":int, "s_artnr":str, "dept":int, "grpflag":int, "done":bool, "bezeich":str, "int_flag":bool, "tday":decimal, "saldo":decimal, "lastmon":decimal, "lastyr":decimal, "lytoday":decimal, "ytd_saldo":decimal, "lytd_saldo":decimal, "tbudget":decimal, "budget":decimal, "lm_budget":decimal, "ly_budget":decimal, "ytd_budget":decimal, "lytd_budget":decimal})
    w2_list, W2 = create_model("W2", {"val_sign":int, "nr1":int, "nr2":int}, {"val_sign": 1})
    w11_list, W11 = create_model("W11", {"nr":int, "debit":decimal, "credit":decimal})

    Parent_w1 = W1
    parent_w1_list = w1_list

    Child_w1 = W1
    child_w1_list = w1_list

    W1_ratio = W1
    w1_ratio_list = w1_list

    Segmbuff = create_buffer("Segmbuff",Segmentstat)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list
        return {"msg_str": msg_str, "success_flag": success_flag}

    def create_var0(texte:str, int_flag:bool):

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

        subtext:str = ""
        subtext = get_subtext(texte, subtext)

        if subtext == "":
            msg_str = translateExtended ("Program expected a new key variable name .xxx", lvcarea, "") + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return

        elif substring(subtext, 0, 1) != (keyvar).lower() :
            msg_str = translateExtended ("Program expected", lvcarea, "") + " " + keyvar + " " + translateExtended ("for any variable", lvcarea, "") + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return
        else:
            varname = subtext
            w1 = W1()
            w1_list.append(w1)

            curr_nr = curr_nr + 1
            w1.nr = curr_nr
            w1.int_flag = int_flag
            w1.varname = varname
            w1.main_code = curr_cmd
            curr_column = len(curr_texte) + 1
            curr_cmd = 0


    def create_var1(texte:str, int_flag:bool):

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

        subtext:str = ""
        correct:bool = False
        nr:int = 0
        subtext = get_subtext(texte, subtext)

        if subtext == "":
            msg_str = translateExtended ("Program expected a new key variable name .xxx", lvcarea, "") + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return

        elif substring(subtext, 0, 1) != (keyvar).lower() :
            msg_str = translateExtended ("Program expected", lvcarea, "") + " " + keyvar + " " + translateExtended ("for any variable", lvcarea, "") + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return
        else:
            varname = subtext
            subtext = trim(substring(texte, curr_column - 1, len(texte) - curr_column + 1))

            if curr_cmd == 800 or curr_cmd == 180 or curr_cmd == 181:
                pass
            else:
                correct = check_integer(subtext)

            if correct:
                nr = to_int(subtext)
            w1 = W1()
            w1_list.append(w1)

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
            curr_column = len(curr_texte) + 1
            curr_cmd = 0


    def create_var2(texte:str, int_flag:bool):

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

        subtext:str = ""
        correct:bool = False
        nr:int = 0
        dept:int = 0
        subtext = get_subtext(texte, subtext)

        if subtext == "":
            msg_str = translateExtended ("Program expected a new key variable name .xxx", lvcarea, "") + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return

        elif substring(subtext, 0, 1) != (keyvar).lower() :
            msg_str = translateExtended ("Program expected", lvcarea, "") + " " + keyvar + " " + translateExtended ("for any variable", lvcarea, "") + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return
        else:
            varname = subtext
            subtext = trim(substring(texte, curr_column - 1, len(texte) - curr_column + 1))
            correct = check_integer(subtext)

            if correct:
                dept = to_int(substring(subtext, 0, 2))
                nr = to_int(substring(subtext, 2, 6))
            w1 = W1()
            w1_list.append(w1)

            curr_nr = curr_nr + 1
            w1.nr = curr_nr
            w1.int_flag = int_flag
            w1.varname = varname
            w1.main_code = curr_cmd
            w1.artnr = nr
            w1.dept = dept
            curr_column = len(curr_texte) + 1
            curr_cmd = 0


    def create_w1():

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

        ind = 0
        w1_nr:int = 0

        def generate_inner_output():
            return (ind)

        w1 = W1()
        w1_list.append(w1)

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

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

        n:int = 0

        if nr == 2:
            w2 = W2()
            w2_list.append(w2)

            w2.nr1 = ind
            w2.nr2 = nr2
        w2.val_sign = val_sign


    def analyse_textheader(texte:str):

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

        subtext:str = ""
        subtext = get_subtext(texte, subtext)

        if subtext != "":
            interprete_subtext(texte, subtext)


    def get_subtext(texte:str, subtext:str):

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

        j:int = 0
        stopped:bool = False

        def generate_inner_output():
            return (subtext)

        texte = trim(substring(texte, curr_column - 1, len(texte) - curr_column + 1))
        stopped = False
        j = 1
        while not stopped:

            if j == len(texte) or substring(texte, j + 1 - 1, 1) == " ":
                stopped = True
            else:
                j = j + 1
        subtext = substring(texte, 0, j)
        curr_column = curr_column + j + 1

        return generate_inner_output()


    def interprete_subtext(texte:str, subtext:str):

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

        j:int = 0
        found:bool = False

        htp_list = query(htp_list_list, first=True)
        while None != htp_list and not found:

            if htp_list.fchar.lower()  == (subtext).lower() :
                found = True
                curr_cmd = htp_list.paramnr

            htp_list = query(htp_list_list, next=True)

        if not found:
            msg_str = translateExtended ("Can not understand line", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return


    def check_integer(texte:str):

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

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
            msg_str = translateExtended ("Program expected a number : ", lvcarea, "") + texte + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return generate_inner_output()

        return generate_inner_output()


    def create_group(texte:str):

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

        subtext:str = ""
        correct:bool = False
        subtext = get_subtext(texte, subtext)

        if subtext == "":
            msg_str = translateExtended ("Program expected a variable name", lvcarea, "") + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return

        elif substring(subtext, 0, 1) != (keyvar).lower() :
            msg_str = translateExtended ("Program expected", lvcarea, "") + " " + keyvar + " " + translateExtended ("for any variable", lvcarea, "") + chr(10) + translateExtended ("at line number", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
            prog_error = True
            error_nr = - 1

            return
        else:
            varname = subtext
            bezeich = trim(substring(texte, curr_column - 1, len(texte) - curr_column + 1))

            if bezeich == "":
                msg_str = translateExtended ("Program expected a description", lvcarea, "") + chr(10) + translateExtended ("at line number : ", lvcarea, "") + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
                prog_error = True
                error_nr = - 1

                return
            else:
                grpflag = 2
                grp_nr = create_w1()
                curr_column = len(texte) + 1


    def create_group_variable(texte:str):

        nonlocal msg_str, success_flag, lvcarea, budget_flag, ytd_flag, lytd_flag, lmtd_flag, pmtd_flag, integer_flag, serv_vat, zeit, margin_c, len_flag, detail_nr, no_decimal, num_digit, value_filled, prog_error, error_nr, curr_row, curr_column, curr_cmd, curr_texte, actual_cmd, detail_loop, grp_nr, curr_nr, varname, bezeich, grpflag, textlen, report_title, from_date, lfrom_date, lto_date, jan1, ljan1, pfrom_date, pto_date, outfile_dir, efield, dayname, curr_loop, f_lmargin, lmargin, nskip, ntab, n, curr_pos, keycmd, keyvar, infile, outfile, foreign_flag, foreign_nr, start_date, lytoday, lytoday_flag, ratio_flag, price_decimal, msg_ans, datum, segmentstat
        nonlocal pvilanguage, briefnr, to_date, check_only, view_only, jobnr
        nonlocal parent_w1, child_w1, w1_ratio, segmbuff


        nonlocal detail_list, brief_list, batch_list, htp_list, htv_list, w1, w2, w11, parent_w1, child_w1, w1_ratio, segmbuff
        nonlocal detail_list_list, brief_list_list, batch_list_list, htp_list_list, htv_list_list, w1_list, w2_list, w11_list

        i:int = 0
        val_sign:int = 1

        htp_list = query(htp_list_list, filters=(lambda htp_list: htp_list.paramnr == 287), first=True)

        if texte == htp_list.fchar:
            actual_cmd = 0

            return

        if substring(texte, 0, 1) == ("-").lower() :
            val_sign = - 1
            texte = substring(texte, 1, len(texte))
            texte = trim(texte)

        if substring(texte, 0, 1) == (keyvar).lower() :

            w1 = query(w1_list, filters=(lambda w1: w1.varname.lower()  == (texte).lower()), first=True)

            if not w1:
                msg_str = translateExtended ("No such variable found", lvcarea, "") + " "+ texte + chr(10) + translateExtended ("at line number :", lvcarea, "") + " " + to_string(curr_row) + chr(10) + substring(curr_texte, 0, len(curr_texte))
                prog_error = True
                error_nr = - 1

                return
            else:
                create_w2(grp_nr, w1.nr, 2, val_sign)


    zeit = get_current_time_in_seconds()
    serv_vat, foreign_nr, start_date, price_decimal, no_decimal, outfile_dir, keycmd, keyvar, batch_list_list, htv_list_list, htp_list_list, brief_list_list = get_output(prepare_fo_parexcelbl(briefnr))
    detail_list = Detail_list()
    detail_list_list.append(detail_list)

    detail_list.nr = 0
    from_date = get_current_date() - timedelta(days=1)

    if to_date == None:

        return generate_output()
    from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))
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

    batch_list = query(batch_list_list, first=True)

    for brief_list in query(brief_list_list):
        curr_texte = trim(b_text)
        curr_pos = 1
        curr_column = 1
        curr_row = curr_row + 1

        for detail_list in query(detail_list_list, filters=(lambda detail_list: detail_list.nr > 0)):
            detail_list_list.remove(detail_list)

        detail_list = query(detail_list_list, filters=(lambda detail_list: detail_list.nr == 0), first=True)
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

            elif actual_cmd == 840 and curr_texte != "":
                create_group_variable(curr_texte)

    if check_only and error_nr == 0:
        msg_str = translateExtended ("Syntax is correct.", lvcarea, "")
        success_flag = True

    return generate_output()