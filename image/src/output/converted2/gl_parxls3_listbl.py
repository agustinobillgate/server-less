from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servvat import calc_servvat
from functions.gl_parxls1_find_exratebl import gl_parxls1_find_exratebl
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.glacct_cashflow_1bl import glacct_cashflow_1bl
from models import Parameters, Gl_accthis, Gl_acct, Artikel, Exrate, Waehrung, Htparam, Paramtext, Gl_jouhdr, Gl_journal, Umsatz, Genstat, Segmentstat, Budget, Zinrstat, Zkstat, Segment

def gl_parxls3_listbl(briefnr:int, from_date:date, to_date:date, user_init:str, gl_month:int, link:str):
    mess_result = "Failed to generate data"
    month_str:List[str] = ["JANUARY", "FEBRUARY", "MARCH", "APRIL", "MAY", "JUNE", "JULY", "AUGUST", "SEPTEMBER", "OCTOBER", "FalseVEMBER", "DECEMBER"]
    chcol:List[str] = ["A", "B", "C", "D", "E", "F", "G", "H", "i", "j", "K", "L", "M", "N", "O", "P", "Q", "R", "s", "T", "U", "V", "W", "X", "Y", "Z", "AA", "AB", "AC", "AD", "AE", "AF", "AG", "AH", "AI", "AJ", "AK", "AL", "AM", "AN", "AO", "AP", "AQ", "AR", "AS", "AT", "AU", "AV", "AW", "AX", "AY", "AZ"]
    curr_date:date = None
    curr_i:int = 0
    curr_row:int = 0
    curr_col:int = 0
    serv:decimal = to_decimal("0.0")
    vat:decimal = to_decimal("0.0")
    fact:decimal = to_decimal("0.0")
    n_betrag:decimal = to_decimal("0.0")
    credit:decimal = to_decimal("0.0")
    debit:decimal = to_decimal("0.0")
    frate:decimal = 1
    price_decimal:int = 0
    gl_year:int = 0
    from_year:decimal = to_decimal("0.0")
    to_year:decimal = to_decimal("0.0")
    foreign_flag:bool = False
    prev_str:str = ""
    cell_val:str = ""
    exrate_betrag:decimal = to_decimal("0.0")
    hist_flag:bool = False
    curr_close_year:int = 0
    found_flag:bool = False
    ytd_bal:decimal = to_decimal("0.0")
    val_sign:int = 0
    j:int = 0
    i:int = 0
    diff:decimal = to_decimal("0.0")
    lmdiff:decimal = to_decimal("0.0")
    mtd_betrag:decimal = to_decimal("0.0")
    ytd_betrag:decimal = to_decimal("0.0")
    start_row:int = 0
    start_col:int = 0
    end_row:int = 0
    end_col:int = 0
    htl_no:str = ""
    datum1:date = None
    jan1:date = None
    ljan1:date = None
    lfrom_date:date = None
    lto_date:date = None
    cash_flow:bool = False
    foreign_curr:decimal = to_decimal("0.0")
    ct1:int = 0
    mon_saldo:List[decimal] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    vat2:decimal = to_decimal("0.0")
    ytd_flag:bool = True
    d_flag:bool = False
    n_serv:decimal = to_decimal("0.0")
    n_tax:decimal = to_decimal("0.0")
    actual_exrate:List[decimal] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    budget_exrate:List[decimal] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lyear_exrate:List[decimal] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    blyear_exrate:List[decimal] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    bnyear_exrate:List[decimal] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    parameters = gl_accthis = gl_acct = artikel = exrate = waehrung = htparam = paramtext = gl_jouhdr = gl_journal = umsatz = genstat = segmentstat = budget = zinrstat = zkstat = segment = None

    t_parameters = t_gl_accthis = glacct_list = t_gl_acct = t_artikel = t_umsz = g_list = temp_list = coa_list = t_list = stat_list = rev_list = b_stat_list = b_stat = buff_exrate = b_param = None

    t_parameters_list, T_parameters = create_model_like(Parameters)
    t_gl_accthis_list, T_gl_accthis = create_model_like(Gl_accthis)
    glacct_list_list, Glacct_list = create_model_like(Gl_acct)
    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)
    t_artikel_list, T_artikel = create_model_like(Artikel)
    t_umsz_list, T_umsz = create_model("T_umsz", {"curr_date":date, "artnr":int, "dept":int, "fact":decimal, "betrag":decimal})
    g_list_list, G_list = create_model("G_list", {"datum":date, "grecid":int, "fibu":str}, {"datum": None})
    temp_list_list, Temp_list = create_model("Temp_list", {"vstring":str, "debit":decimal, "credit":decimal})
    coa_list_list, Coa_list = create_model("Coa_list", {"fibu":str})
    t_list_list, T_list = create_model("T_list", {"cf":int, "fibukonto":str, "debit":decimal, "credit":decimal, "debit_lsyear":decimal, "credit_lsyear":decimal, "debit_lsmonth":decimal, "credit_lsmonth":decimal, "balance":decimal, "ly_balance":decimal, "pm_balance":decimal, "debit_today":decimal, "credit_today":decimal, "debit_mtd":decimal, "credit_mtd":decimal, "debit_ytd":decimal, "credit_ytd":decimal, "today_balance":decimal, "mtd_balance":decimal, "ytd_balance":decimal})
    stat_list_list, Stat_list = create_model("Stat_list", {"ct":int, "descr":str, "departement":int, "t_day":decimal, "mtd":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "flag":str})
    rev_list_list, Rev_list = create_model("Rev_list", {"ct":int, "descr":str, "departement":int, "t_day":decimal, "dper":decimal, "mtd":decimal, "mtd_per":decimal, "mtd_budget":decimal, "variance":decimal, "ytd":decimal, "ytd_budget":decimal, "ytd_per":decimal, "flag":str, "flag_grup":bool})

    B_stat_list = Stat_list
    b_stat_list_list = stat_list_list

    B_stat = Stat_list
    b_stat_list = stat_list_list

    Buff_exrate = create_buffer("Buff_exrate",Exrate)
    B_param = create_buffer("B_param",Parameters)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list
        return {"mess_result": mess_result}

    def fill_exrate():

        nonlocal mess_result, month_str, chcol, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        to_month:int = 0
        ind:int = 0
        curr_yr:int = 0
        last_yr:int = 0
        next_yr:int = 0
        curr_date:date = None
        lyear_date:date = None
        nyear_date:date = None
                        to_month = get_month(to_date)
                        curr_yr = get_year(to_date)
                        last_yr = get_year(to_date) - 1
                        next_yr = get_year(to_date) + 1


                        for ind in range(1,to_month + 1) :

                            if ind == 12:
                                curr_date = date_mdy(12, 31, curr_yr)
                                lyear_date = date_mdy(12, 31, last_yr)
                                nyear_date = date_mdy(12, 31, next_yr)


                            else:
                                curr_date = date_mdy(ind, 1, curr_yr) + timedelta(days=35)
                                curr_date = date_mdy(get_month(curr_date) , 1, curr_yr) - timedelta(days=1)
                                lyear_date = date_mdy(ind, 1, last_yr) + timedelta(days=35)
                                lyear_date = date_mdy(get_month(lyear_date) , 1, last_yr) - timedelta(days=1)
                                nyear_date = date_mdy(ind, 1, next_yr) + timedelta(days=35)
                                nyear_date = date_mdy(get_month(nyear_date) , 1, next_yr) - timedelta(days=1)

                            exrate = db_session.query(Exrate).filter(
                                     (Exrate.artnr == 99999) & (Exrate.datum == curr_date)).first()

                            if exrate:
                                actual_exrate[ind - 1] = exrate.betrag

                            exrate = db_session.query(Exrate).filter(
                                     (Exrate.artnr == 99999) & (Exrate.datum == lyear_date)).first()

                            if exrate:
                                lyear_exrate[ind - 1] = exrate.betrag

                            exrate = db_session.query(Exrate).filter(
                                     (Exrate.artnr == 99998) & (Exrate.datum == curr_date)).first()

                            if exrate:
                                budget_exrate[ind - 1] = exrate.betrag

                            exrate = db_session.query(Exrate).filter(
                                     (Exrate.artnr == 99998) & (Exrate.datum == lyear_date)).first()

                            if exrate:
                                blyear_exrate[ind - 1] = exrate.betrag

                            exrate = db_session.query(Exrate).filter(
                                     (Exrate.artnr == 99998) & (Exrate.datum == nyear_date)).first()

                            if exrate:
                                bnyear_exrate[ind - 1] = exrate.betrag


    def find_exrate(curr_date:date):

        nonlocal mess_result, month_str, chcol, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        foreign_nr:int = 0

                        if foreign_flag:

                            buff_exrate = db_session.query(Buff_exrate).filter(
                                     (Buff_exrate.artnr == 99999) & (Buff_exrate.datum == curr_date)).first()

                            if buff_exrate:

                                return

                        htparam = db_session.query(Htparam).filter(
                                 (Htparam.paramnr == 144)).first()

                        if htparam.fchar != "":

                            waehrung = db_session.query(Waehrung).filter(
                                     (Waehrung.wabkurz == htparam.fchar)).first()

                            if waehrung:
                                foreign_nr = waehrung.waehrungsnr

                        if foreign_nr != 0:

                            buff_exrate = db_session.query(Buff_exrate).filter(
                                     (Buff_exrate.artnr == foreign_nr) & (Buff_exrate.datum == curr_date)).first()
                        else:

                            buff_exrate = db_session.query(Buff_exrate).filter(
                                     (Buff_exrate.datum == curr_date)).first()


    def decode_string(in_str:str):

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

                        s = in_str
                        j = asc(substring(s, 0, 1)) - 70
                        len_ = len(in_str) - 1
                        s = substring(in_str, 1, len_)
                        for len_ in range(1,len(s)  + 1) :
                            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    def fill_tot_room():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, mon_saldo, vat2, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        s_param = None
        prev_param:str = ""
        ytd_flag:bool = False
        lytd_flag:bool = False
        lmtd_flag:bool = False
        ytd_budget_flag:bool = False
        mtd_budget_flag:bool = False
        nr:int = 0
        segm:int = 0
        mm:int = 0
        prev_segm:int = 0
        tday_rev:decimal = to_decimal("0.0")
        tday_pers:decimal = to_decimal("0.0")
        tday_room:decimal = to_decimal("0.0")
        mtd_rev:decimal = to_decimal("0.0")
        mtd_pers:decimal = to_decimal("0.0")
        mtd_room:decimal = to_decimal("0.0")
        ytd_rev:decimal = to_decimal("0.0")
        ytd_pers:decimal = to_decimal("0.0")
        ytd_room:decimal = to_decimal("0.0")
        ltday_rev:decimal = to_decimal("0.0")
        ltday_pers:decimal = to_decimal("0.0")
        ltday_room:decimal = to_decimal("0.0")
        lmtd_rev:decimal = to_decimal("0.0")
        lmtd_pers:decimal = to_decimal("0.0")
        lmtd_room:decimal = to_decimal("0.0")
        lytd_rev:decimal = to_decimal("0.0")
        lytd_pers:decimal = to_decimal("0.0")
        lytd_room:decimal = to_decimal("0.0")
        btday_rev:decimal = to_decimal("0.0")
        btday_pers:decimal = to_decimal("0.0")
        btday_room:decimal = to_decimal("0.0")
        bmtd_rev:decimal = to_decimal("0.0")
        bmtd_pers:decimal = to_decimal("0.0")
        bmtd_room:decimal = to_decimal("0.0")
        bytd_rev:decimal = to_decimal("0.0")
        bytd_pers:decimal = to_decimal("0.0")
        bytd_room:decimal = to_decimal("0.0")
        do_it:bool = False
        s_param = None
        prev_param:str = ""
        ytd_flag:bool = False
        lytd_flag:bool = False
        lmtd_flag:bool = False
        ytd_budget_flag:bool = False
        mtd_budget_flag:bool = False
        mm:int = 0
        cell_datum:str = ""
        saldo_betrag:decimal = to_decimal("0.0")
        ytd_betrag:decimal = to_decimal("0.0")
        t_betrag:decimal = to_decimal("0.0")
        lastyr_betrag:decimal = to_decimal("0.0")
        lytd_saldo:decimal = to_decimal("0.0")
        tbudget:decimal = to_decimal("0.0")
        mtd_budget:decimal = to_decimal("0.0")
        ytd_budget:decimal = to_decimal("0.0")
        do_it:bool = False
        key_word:str = ""
        do_it:bool = False
        t_day:decimal = to_decimal("0.0")
        mtd:decimal = to_decimal("0.0")
        mtd_budget:decimal = to_decimal("0.0")
        ytd:decimal = to_decimal("0.0")
        ytd_budget:decimal = to_decimal("0.0")
        variance:decimal = to_decimal("0.0")
        ct1:int = 0
        datum:date = None
        anz:int = 0
        anz0:int = 0
        d_flag:bool = False
        dlmtd_flag:bool = False
                        S_param =  create_buffer("S_param",Parameters)

                        for s_param in db_session.query(S_param).filter(
                                 (func.lower(S_param.progname) == ("GL-macro").lower()) & (S_param.section == to_string(briefnr)) & (num_entries(S_param.vstring, ":") == 1) & (num_entries(S_param.varname, "-") == 3) & (entry(2, S_param.varname, "-") == ("FO").lower()) & (substring(S_param.vstring, 0, 4) == ("segm").lower())).order_by(S_param.varname).all():
                            curr_row = to_int(entry(0, s_param.varname, "-"))
                            curr_col = to_int(entry(1, s_param.varname, "-"))
                            end_row = curr_row
                            end_col = curr_col
                            do_it = False

                            if prev_param != s_param.varname:
                                prev_param = s_param.varname

                                if entry(0, s_param.vstring, "-") == ("segmrev").lower() :
                                    nr = 1

                                elif entry(0, s_param.vstring, "-") == ("segmpers").lower() :
                                    nr = 2

                                elif entry(0, s_param.vstring, "-") == ("segmroom").lower() :
                                    nr = 3

                                if num_entries(s_param.vstring, "-") > 1:
                                    segm = to_int(entry(1, s_param.vstring, "-"))
                                t_parameters = T_parameters()
                                t_parameters_list.append(t_parameters)

                                buffer_copy(s_param, t_parameters)

                                if s_param.vtype == 24:
                                    ytd_flag = True

                                if s_param.vtype == 84:
                                    mtd_budget_flag = True

                                if s_param.vtype == 85:
                                    ytd_budget_flag = True

                                if s_param.vtype == 86:
                                    lmtd_flag = True

                                if s_param.vtype == 87:
                                    lytd_flag = True

                            if ytd_flag:
                                datum1 = jan1
                            else:
                                datum1 = from_date
                            mm = get_month(to_date)
                            tday_rev =  to_decimal("0")
                            tday_pers =  to_decimal("0")
                            tday_room =  to_decimal("0")
                            mtd_rev =  to_decimal("0")
                            mtd_pers =  to_decimal("0")
                            mtd_room =  to_decimal("0")
                            ltday_rev =  to_decimal("0")
                            ltday_pers =  to_decimal("0")
                            ltday_room =  to_decimal("0")
                            lmtd_rev =  to_decimal("0")
                            lmtd_pers =  to_decimal("0")
                            lmtd_room =  to_decimal("0")
                            lytd_rev =  to_decimal("0")
                            lytd_pers =  to_decimal("0")
                            lytd_room =  to_decimal("0")
                            btday_rev =  to_decimal("0")
                            btday_pers =  to_decimal("0")
                            btday_room =  to_decimal("0")
                            bmtd_rev =  to_decimal("0")
                            bmtd_pers =  to_decimal("0")
                            bmtd_room =  to_decimal("0")
                            bytd_rev =  to_decimal("0")
                            bytd_pers =  to_decimal("0")
                            bytd_room =  to_decimal("0")
                            ytd_rev =  to_decimal("0")
                            ytd_pers =  to_decimal("0")
                            ytd_room =  to_decimal("0")

                            for genstat in db_session.query(Genstat).filter(
                                     (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode == segm) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1))]).order_by(Genstat.segmentcode).all():

                                if genstat.datum == to_date:

                                    if nr == 1:
                                        tday_rev =  to_decimal(tday_rev) + to_decimal(genstat.logis)

                                    if nr == 2:
                                        tday_pers =  to_decimal(tday_pers) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                                    if nr == 3:
                                        tday_room =  to_decimal(tday_room) + to_decimal("1")

                                if get_month(genstat.datum) == mm:

                                    if nr == 1:
                                        mtd_rev =  to_decimal(mtd_rev) + to_decimal(genstat.logis)

                                    if nr == 2:
                                        mtd_pers =  to_decimal(mtd_pers) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                                    if nr == 3:
                                        mtd_room =  to_decimal(mtd_room) + to_decimal("1")

                                if nr == 1:
                                    ytd_rev =  to_decimal(ytd_rev) + to_decimal(genstat.logis)

                                if nr == 2:
                                    ytd_pers =  to_decimal(ytd_pers) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                                if nr == 3:
                                    ytd_room =  to_decimal(ytd_room) + to_decimal("1")

                            if s_param.vtype == 83:

                                if tday_rev != 0:

                                    elif tday_pers != 0:

                                        elif tday_room != 0:
                                            else:

                                            elif s_param.vtype == 23:

                                                if mtd_rev != 0:

                                                    elif mtd_pers != 0:

                                                        elif mtd_room != 0:
                                                            else:

                                                            elif s_param.vtype == 24:

                                                                if ytd_rev != 0:

                                                                    elif ytd_pers != 0:

                                                                        elif ytd_room != 0:
                                                                            else:

                                                                            if lmtd_flag or lytd_flag:

                                                                                if lytd_flag:
                                                                                    datum1 = ljan1
                                                                                else:
                                                                                    datum1 = lfrom_date
                                                                                mm = get_month(lto_date)
                                                                                prev_segm = 0

                                                                                for genstat in db_session.query(Genstat).filter(
                                                                                         (Genstat.datum >= datum1) & (Genstat.datum <= lto_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode == segm) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1))]).order_by(Genstat.segmentcode).all():

                                                                                    if genstat.datum == lto_date:

                                                                                        if nr == 1:
                                                                                            ltday_rev =  to_decimal(ltday_rev) + to_decimal(genstat.logis)

                                                                                        if nr == 2:
                                                                                            ltday_pers =  to_decimal(ltday_pers) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                                                                                        if nr == 3:
                                                                                            ltday_room =  to_decimal(ltday_room) + to_decimal("1")

                                                                                    if get_month(genstat.datum) == mm:

                                                                                        if nr == 1:
                                                                                            lmtd_rev =  to_decimal(lmtd_rev) + to_decimal(genstat.logis)

                                                                                        if nr == 2:
                                                                                            lmtd_pers =  to_decimal(lmtd_pers) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                                                                                        if nr == 3:
                                                                                            lmtd_room =  to_decimal(lmtd_room) + to_decimal("1")

                                                                                    if nr == 1:
                                                                                        lytd_rev =  to_decimal(ytd_rev) + to_decimal(genstat.logis)

                                                                                    if nr == 2:
                                                                                        lytd_pers =  to_decimal(ytd_pers) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                                                                                    if nr == 3:
                                                                                        lytd_room =  to_decimal(ytd_room) + to_decimal("1")

                                                                                if s_param.vtype == 86:

                                                                                    if lmtd_rev != 0:

                                                                                        elif lmtd_pers != 0:

                                                                                            elif lmtd_room != 0:
                                                                                                else:

                                                                                                elif s_param.vtype == 87:

                                                                                                    if lytd_rev != 0:

                                                                                                        elif lytd_pers != 0:

                                                                                                            elif lytd_room != 0:
                                                                                                                else:

                                                                                                            if mtd_budget_flag or ytd_budget_flag:

                                                                                                                if ytd_budget_flag:
                                                                                                                    datum1 = jan1
                                                                                                                else:
                                                                                                                    datum1 = from_date
                                                                                                                mm = get_month(to_date)
                                                                                                                prev_segm = 0

                                                                                                                for segmentstat in db_session.query(Segmentstat).filter(
                                                                                                                         (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segm)).order_by(Segmentstat.segmentcode).all():

                                                                                                                    if segmentstat.datum == to_date:

                                                                                                                        if nr == 1:
                                                                                                                            btday_rev =  to_decimal(btday_rev) + to_decimal(segmentstat.budlogis)

                                                                                                                        if nr == 2:
                                                                                                                            btday_pers =  to_decimal(btday_pers) + to_decimal(segmentstat.budpersanz)

                                                                                                                        if nr == 3:
                                                                                                                            btday_room =  to_decimal(btday_room) + to_decimal(segmentstat.budzimmeranz)

                                                                                                                    if get_month(segmentstat.datum) == mm:

                                                                                                                        if nr == 1:
                                                                                                                            bmtd_rev =  to_decimal(bmtd_rev) + to_decimal(segmentstat.budlogis)

                                                                                                                        if nr == 2:
                                                                                                                            bmtd_pers =  to_decimal(bmtd_pers) + to_decimal(segmentstat.budpersanz)

                                                                                                                        if nr == 3:
                                                                                                                            bmtd_room =  to_decimal(bmtd_room) + to_decimal(segmentstat.budzimmeranz)

                                                                                                                    if nr == 1:
                                                                                                                        bytd_rev =  to_decimal(bytd_rev) + to_decimal(segmentstat.budlogis)

                                                                                                                    if nr == 2:
                                                                                                                        bytd_pers =  to_decimal(bytd_pers) + to_decimal(segmentstat.budpersanz)

                                                                                                                    if nr == 3:
                                                                                                                        bytd_room =  to_decimal(bytd_room) + to_decimal(segmentstat.budzimmeranz)

                                                                                                                if s_param.vtype == 84:

                                                                                                                    if bmtd_rev != 0:

                                                                                                                        elif bmtd_pers != 0:

                                                                                                                            elif bmtd_room != 0:
                                                                                                                                else:

                                                                                                                                elif s_param.vtype == 85:

                                                                                                                                    if bytd_rev != 0:

                                                                                                                                        elif bytd_pers != 0:

                                                                                                                                            elif bytd_room != 0:
                                                                                                                                                else:
                                                                                                                                        S_param =  create_buffer("S_param",Parameters)

                                                                                                                                    for s_param in db_session.query(S_param).filter(
                                                                                                                                             (func.lower(S_param.progname) == ("GL-macro").lower()) & (S_param.section == to_string(briefnr)) & (num_entries(S_param.vstring, ":") == 1) & (num_entries(S_param.varname, "-") == 3) & (entry(2, S_param.varname, "-") == ("REV").lower())).order_by(S_param.varname).all():
                                                                                                                                        curr_row = to_int(entry(0, s_param.varname, "-"))
                                                                                                                                        curr_col = to_int(entry(1, s_param.varname, "-"))
                                                                                                                                        end_row = curr_row
                                                                                                                                        end_col = curr_col
                                                                                                                                        do_it = False

                                                                                                                                        if prev_param != s_param.varname:
                                                                                                                                            prev_param = s_param.varname
                                                                                                                                            saldo_betrag =  to_decimal("0")
                                                                                                                                            ytd_betrag =  to_decimal("0")
                                                                                                                                            t_betrag =  to_decimal("0")
                                                                                                                                            lastyr_betrag =  to_decimal("0")
                                                                                                                                            lytd_saldo =  to_decimal("0")
                                                                                                                                            tbudget =  to_decimal("0")
                                                                                                                                            mtd_budget =  to_decimal("0")
                                                                                                                                            ytd_budget =  to_decimal("0")

                                                                                                                                            if s_param.vtype == 24:
                                                                                                                                                ytd_flag = True

                                                                                                                                            if s_param.vtype == 84:
                                                                                                                                                mtd_budget_flag = True

                                                                                                                                            if s_param.vtype == 85:
                                                                                                                                                ytd_budget_flag = True

                                                                                                                                            if s_param.vtype == 86:
                                                                                                                                                lmtd_flag = True

                                                                                                                                            if s_param.vtype == 87:
                                                                                                                                                lytd_flag = True

                                                                                                                                        artikel = db_session.query(Artikel).filter(
                                                                                                                                                 (Artikel.artnr == to_int(substring(s_param.vstring, 2))) & (Artikel.departement == to_int(substring(s_param.vstring, 0, 2)))).first()

                                                                                                                                        if artikel:

                                                                                                                                            if ytd_flag:
                                                                                                                                                datum1 = jan1
                                                                                                                                            else:
                                                                                                                                                datum1 = from_date
                                                                                                                                            mm = get_month(to_date)

                                                                                                                                            for umsatz in db_session.query(Umsatz).filter(
                                                                                                                                                     (Umsatz.datum >= datum1) & (Umsatz.datum <= to_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement)).order_by(Umsatz._recid).all():
                                                                                                                                                serv =  to_decimal("0")
                                                                                                                                                vat =  to_decimal("0")


                                                                                                                                                serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                                                                                                                                                fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                                                                                                                                                n_betrag =  to_decimal("0")

                                                                                                                                                if foreign_flag:
                                                                                                                                                    find_exrate(curr_date)

                                                                                                                                                    if buff_exrate:
                                                                                                                                                        frate =  to_decimal(buff_exrate.betrag)
                                                                                                                                                n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate))
                                                                                                                                                n_betrag = to_decimal(round(n_betrag , 2))

                                                                                                                                                if umsatz.datum == to_date:
                                                                                                                                                    t_betrag =  to_decimal(t_betrag) + to_decimal(n_betrag)

                                                                                                                                                if get_month(umsatz.datum) == mm:
                                                                                                                                                    saldo_betrag =  to_decimal(saldo_betrag) + to_decimal(n_betrag)
                                                                                                                                                ytd_betrag =  to_decimal(ytd_betrag) + to_decimal(n_betrag)

                                                                                                                                            if s_param.vtype == 23 and do_it == False:

                                                                                                                                                if saldo_betrag != 0:
                                                                                                                                                    else:
                                                                                                                                                        do_it = True

                                                                                                                                                elif s_param.vtype == 24 and do_it == False:

                                                                                                                                                    if ytd_betrag != 0:
                                                                                                                                                        else:
                                                                                                                                                            do_it = True

                                                                                                                                                    if lmtd_flag or lytd_flag:

                                                                                                                                                        if lytd_flag:
                                                                                                                                                            datum1 = ljan1
                                                                                                                                                        else:
                                                                                                                                                            datum1 = lfrom_date
                                                                                                                                                        mm = get_month(lto_date)

                                                                                                                                                        for umsatz in db_session.query(Umsatz).filter(
                                                                                                                                                                 (Umsatz.datum >= datum1) & (Umsatz.datum <= lto_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement)).order_by(Umsatz._recid).all():
                                                                                                                                                            serv =  to_decimal("0")
                                                                                                                                                            vat =  to_decimal("0")


                                                                                                                                                            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                                                                                                                                                            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                                                                                                                                                            n_betrag =  to_decimal("0")

                                                                                                                                                            if foreign_flag:
                                                                                                                                                                find_exrate(curr_date)

                                                                                                                                                                if buff_exrate:
                                                                                                                                                                    frate =  to_decimal(buff_exrate.betrag)
                                                                                                                                                            n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate))
                                                                                                                                                            n_betrag = to_decimal(round(n_betrag , 2))

                                                                                                                                                            if get_month(umsatz.datum) == mm:
                                                                                                                                                                lastyr_betrag =  to_decimal(lastyr_betrag) + to_decimal(n_betrag)
                                                                                                                                                            lytd_saldo =  to_decimal(lytd_saldo) + to_decimal(n_betrag)

                                                                                                                                                        if s_param.vtype == 86 and do_it == False:

                                                                                                                                                            if lastyr_betrag != 0:
                                                                                                                                                                else:
                                                                                                                                                                    do_it = True

                                                                                                                                                            elif s_param.vtype == 87 and do_it == False:

                                                                                                                                                                if lytd_saldo != 0:
                                                                                                                                                                    else:
                                                                                                                                                                        do_it = True

                                                                                                                                                            if mtd_budget_flag or ytd_budget_flag:

                                                                                                                                                                if ytd_budget_flag:
                                                                                                                                                                    datum1 = jan1
                                                                                                                                                                else:
                                                                                                                                                                    datum1 = from_date
                                                                                                                                                                mm = get_month(to_date)

                                                                                                                                                                for budget in db_session.query(Budget).filter(
                                                                                                                                                                         (Budget.artnr == artikel.artnr) & (Budget.departement == artikel.departement) & (Budget.datum >= datum1) & (Budget.datum <= to_date)).order_by(Budget.artnr).all():

                                                                                                                                                                    if budget.datum == to_date:
                                                                                                                                                                        tbudget =  to_decimal(tbudget) + to_decimal(budget.betrag)

                                                                                                                                                                    if get_month(budget.datum) == mm:
                                                                                                                                                                        mtd_budget =  to_decimal(mtd_budget) + to_decimal(budget.betrag)
                                                                                                                                                                    ytd_budget =  to_decimal(ytd_budget) + to_decimal(budget.betrag)

                                                                                                                                                                if s_param.vtype == 84 and do_it == False:

                                                                                                                                                                    if mtd_budget != 0:
                                                                                                                                                                        else:
                                                                                                                                                                            do_it = True

                                                                                                                                                                    elif s_param.vtype == 85 and do_it == False:

                                                                                                                                                                        if ytd_budget != 0:
                                                                                                                                                                            else:
                                                                                                                                                                                do_it = True

                                                                                                                                                            for b_param in db_session.query(B_param).filter(
                                                                                                                                                                     (func.lower(B_param.progname) == ("GL-macro").lower()) & (B_param.section == to_string(briefnr)) & (num_entries(B_param.vstring, ":") == 1) & (num_entries(B_param.varname, "-") == 3) & (entry(2, B_param.varname, "-") == ("FO").lower()) & (substring(B_param.vstring, 0, 4) == ("stat").lower())).order_by(B_param.varname).all():
                                                                                                                                                                key_word = b_param.vstring
                                                                                                                                                                curr_row = to_int(entry(0, b_param.varname, "-"))
                                                                                                                                                                curr_col = to_int(entry(1, b_param.varname, "-"))
                                                                                                                                                                end_row = curr_row
                                                                                                                                                                end_col = curr_col
                                                                                                                                                                do_it = False

                                                                                                                                                                stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == (key_word).lower()), first=True)

                                                                                                                                                                if stat_list:

                                                                                                                                                                    if stat_list.flag.lower()  == ("stat-nguest").lower() :
                                                                                                                                                                        pass

                                                                                                                                                                    if b_param.vtype == 83 and stat_list.t_day != 0:

                                                                                                                                                                        elif b_param.vtype == 23 and stat_list.mtd != 0:

                                                                                                                                                                            elif b_param.vtype == 24 and stat_list.ytd != 0:
                                                                                                                                                                                else:

                                                                                                                                                                            for artikel in db_session.query(Artikel).filter(
                                                                                                                                                                                     ((Artikel.artart == 0) | (Artikel.artart == 8)) & (Artikel.umsatzart == 1) & (Artikel.departement == 0)).order_by(Artikel._recid).all():
                                                                                                                                                                            for curr_date in date_range(from_date,to_date) :
                                                                                                                                                                                serv =  to_decimal("0")
                                                                                                                                                                                vat =  to_decimal("0")

                                                                                                                                                                                umsatz = db_session.query(Umsatz).filter(
                                                                                                                                                                                         (Umsatz.datum == curr_date) & (Umsatz.artnr == artikel.artnr) & (Umsatz.departement == artikel.departement)).first()

                                                                                                                                                                                if umsatz:
                                                                                                                                                                                    serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
                                                                                                                                                                                fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat) + to_decimal(vat2)
                                                                                                                                                                                d_flag = None ! == umsatz and (get_month(umsatz.datum) == get_month(to_date)) and (get_year(umsatz.datum) == get_year(to_date))
                                                                                                                                                                                n_betrag =  to_decimal("0")

                                                                                                                                                                                if umsatz:

                                                                                                                                                                                    if foreign_flag:
                                                                                                                                                                                        find_exrate(curr_date)

                                                                                                                                                                                        if exrate:
                                                                                                                                                                                            frate =  to_decimal(exrate.betrag)
                                                                                                                                                                                    n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate) )
                                                                                                                                                                                    n_serv =  to_decimal(n_betrag) * to_decimal(serv)
                                                                                                                                                                                    n_tax =  to_decimal(n_betrag) * to_decimal(vat)

                                                                                                                                                                                    if umsat.datum == to_date:
                                                                                                                                                                                        t_day =  to_decimal(t_day) + to_decimal(n_betrag)

                                                                                                                                                                                    if price_decimal == 0:
                                                                                                                                                                                        n_betrag = to_decimal(round(n_betrag , 0))
                                                                                                                                                                                        n_serv = to_decimal(round(n_serv , 0))
                                                                                                                                                                                        n_tax = to_decimal(round(n_tax , 0))

                                                                                                                                                                                budget = db_session.query(Budget).filter(
                                                                                                                                                                                         (Budget.artnr == artikel.artnr) & (Budget.departement == artikel.departement) & (Budget.datum == curr_date)).first()

                                                                                                                                                                                if curr_date < from_date:

                                                                                                                                                                                    if umsatz:
                                                                                                                                                                                        ytd =  to_decimal(ytd) + to_decimal(n_betrag)

                                                                                                                                                                                    if budget:
                                                                                                                                                                                        ytd_budget =  to_decimal(ytd_budget) + to_decimal(budget.betrag)


                                                                                                                                                                                else:

                                                                                                                                                                                    if umsatz:

                                                                                                                                                                                        if ytd_flag:
                                                                                                                                                                                            ytd =  to_decimal(ytd) + to_decimal(n_betrag)

                                                                                                                                                                                        if get_month(curr_date) == get_month(to_date):
                                                                                                                                                                                            mtd =  to_decimal(mtd) + to_decimal(mon_saldo[get_day(umsatz.datum) - 1]) + to_decimal(n_betrag)

                                                                                                                                                                                    if budget:
                                                                                                                                                                                        mtd_budget =  to_decimal(mtd_budget) + to_decimal(budget.betrag)
                                                                                                                                                                                variance =  to_decimal(mtd) - to_decimal(mtd_budget)


                                                                                                                                                                            ct1 = ct1 + 1
                                                                                                                                                                            rev_list = Rev_list()
                                                                                                                                                                            rev_list_list.append(rev_list)

                                                                                                                                                                            rev_list.ct = ct
                                                                                                                                                                            rev_list.flag = "Room"
                                                                                                                                                                            rev_list.departement = 0
                                                                                                                                                                            rev_list.t_day =  to_decimal(t_day)
                                                                                                                                                                            rev_list.mtd =  to_decimal(mtd)
                                                                                                                                                                            rev_list.mtd_budget =  to_decimal(mtd_budget)
                                                                                                                                                                            rev_list.ytd =  to_decimal(ytd)
                                                                                                                                                                            rev_list.ytd_budget =  to_decimal(ytd_budget)
                                                                                                                                                                            rev_list.descr = artikel.bezeich


                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("stat-tot-rm").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.descr = "Total Room"
                                                                                                                                                                            stat_list.flag = "stat-tot-rm"


                                                                                                                                                                            for datum in date_range(datum1,to_date) :

                                                                                                                                                                                zinrstat = db_session.query(Zinrstat).filter(
                                                                                                                                                                                         (Zinrstat.datum == datum) & (func.lower(Zinrstat.zinr) == ("tot-rm").lower())).first()

                                                                                                                                                                                if zinrstat:
                                                                                                                                                                                    anz = zinrstat.zimmeranz
                                                                                                                                                                                else:
                                                                                                                                                                                    anz = anz0
                                                                                                                                                                                d_flag = None ! == zinrstat and (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

                                                                                                                                                                                if zinrstat:

                                                                                                                                                                                    if d_flag:
                                                                                                                                                                                        stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(zinrstat.datum) - 1]) + to_decimal(anz)

                                                                                                                                                                                if datum == to_date:
                                                                                                                                                                                    stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal(anz)

                                                                                                                                                                                if from_date != None:

                                                                                                                                                                                    if (datum < from_date) and (datum >= from_date):
                                                                                                                                                                                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(anz)
                                                                                                                                                                                    else:

                                                                                                                                                                                        if ytd_flag and (datum >= from_date):
                                                                                                                                                                                            stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(anz)
                                                                                                                                                                                else:

                                                                                                                                                                                    if (datum < from_date):
                                                                                                                                                                                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(anz)
                                                                                                                                                                                    else:

                                                                                                                                                                                        if ytd_flag:
                                                                                                                                                                                            stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(anz)


    def fill_tot_avail():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list


                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("stat-act-rm").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.descr = "Room Available"
                                                                                                                                                                            stat_list.flag = "stat-act-rm"

                                                                                                                                                                            for zkstat in db_session.query(Zkstat).filter(
                                                                                                                                                                                     (Zkstat.datum >= datum1) & (Zkstat.datum <= to_date)).order_by(Zkstat._recid).all():

                                                                                                                                                                                if zkstat.datum == to_date:
                                                                                                                                                                                    stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal(zkstat.anz100)

                                                                                                                                                                                if zkstat.datum < from_date:
                                                                                                                                                                                    stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zkstat.anz100)
                                                                                                                                                                                else:

                                                                                                                                                                                    if ytd_flag:
                                                                                                                                                                                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zkstat.anz100)

                                                                                                                                                                                if get_month(zkstat.datum) == get_month(to_date) and get_year(zkstat.datum) == get_year(to_date):
                                                                                                                                                                                    stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(zkstat.datum) - 1]) + to_decimal(zkstat.anz100)


    def fill_inactive():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        tday1:int = 0
        tday2:int = 0
        tday3:int = 0
        mtd1:int = 0
        mtd2:int = 0
        mtd3:int = 0
        ytd1:int = 0
        ytd2:int = 0
        ytd3:int = 0
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("tot-inactive").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.descr = "InactiveRoom"
                                                                                                                                                                            stat_list.flag = "tot-inactive"

                                                                                                                                                                            for b_stat_list in query(b_stat_list_list):

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("tot-rm").lower() :
                                                                                                                                                                                    tday1 = b_stat_list.t_day
                                                                                                                                                                                    mtd1 = b_stat_list.mtd
                                                                                                                                                                                    ytd1 = b_stat_list.ytd

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("tot-rmavail").lower() :
                                                                                                                                                                                    tday2 = b_stat_list.t_day
                                                                                                                                                                                    mtd2 = b_stat_list.mtd
                                                                                                                                                                                    ytd2 = b_stat_list.ytd


                                                                                                                                                                            stat_list.t_day =  to_decimal(tday1) - to_decimal(tday2)
                                                                                                                                                                            stat_list.mtd =  to_decimal(mtd1) - to_decimal(mtd2)
                                                                                                                                                                            stat_list.ytd =  to_decimal(ytd1) - to_decimal(ytd2)


    def fill_rmstat(key_word:str):

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        datum:date = None
        anz:int = 0
        anz0:int = 0
        d_flag:bool = False
        dlmtd_flag:bool = False
        cur_key:str = ""
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == (key_word).lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1

                                                                                                                                                                            if key_word.lower()  == ("ooo").lower() :
                                                                                                                                                                                stat_list.descr = "Out of Order Rooms"
                                                                                                                                                                                stat_list.flag = "stat-ooo"

                                                                                                                                                                            elif key_word.lower()  == ("oos").lower() :
                                                                                                                                                                                stat_list.descr = "Rooms Occupied"
                                                                                                                                                                                stat_list.flag = "stat-ooc"

                                                                                                                                                                            elif key_word.lower()  == ("dayuse").lower() :
                                                                                                                                                                                stat_list.descr = "Day Use"
                                                                                                                                                                                stat_list.flag = "stat-day-use"

                                                                                                                                                                            elif key_word.lower()  == ("No-Show").lower() :
                                                                                                                                                                                stat_list.descr = "No Show"
                                                                                                                                                                                stat_list.flag = "stat-noshow"

                                                                                                                                                                            elif key_word.lower()  == ("arrival-WIG").lower() :
                                                                                                                                                                                stat_list.descr = "Walk in Guest"
                                                                                                                                                                                stat_list.flag = "stat-rm-wig"

                                                                                                                                                                            elif key_word.lower()  == ("NewRes").lower() :
                                                                                                                                                                                stat_list.descr = "Reservation Made Today"
                                                                                                                                                                                stat_list.flag = "stat-newres"

                                                                                                                                                                            elif key_word.lower()  == ("CancRes").lower() :
                                                                                                                                                                                stat_list.descr = "Cancellation For Today"
                                                                                                                                                                                stat_list.flag = "stat-cancel"

                                                                                                                                                                            elif key_word.lower()  == ("Early-CO").lower() :
                                                                                                                                                                                stat_list.descr = "Early Check Out"
                                                                                                                                                                                stat_list.flag = "stat-earco"

                                                                                                                                                                            elif key_word.lower()  == ("arrival").lower() :
                                                                                                                                                                                stat_list.descr = "Room Arrivals"
                                                                                                                                                                                stat_list.flag = "stat-rm-arr"

                                                                                                                                                                            elif key_word.lower()  == ("pers-arrival").lower() :
                                                                                                                                                                                cur_key = "pers-arrival"
                                                                                                                                                                                key_word = "arrival"
                                                                                                                                                                                stat_list.descr = "Person Arrivals"
                                                                                                                                                                                stat_list.flag = "stat-prs-arr"

                                                                                                                                                                            elif key_word.lower()  == ("departure").lower() :
                                                                                                                                                                                stat_list.descr = "Room Departures"
                                                                                                                                                                                stat_list.flag = "stat-rm-dep"

                                                                                                                                                                            elif key_word.lower()  == ("pers-depature").lower() :
                                                                                                                                                                                cur_key = "pers-depature"
                                                                                                                                                                                key_word = "departure"
                                                                                                                                                                                stat_list.descr = "Person Depatures"
                                                                                                                                                                                stat_list.flag = "stat-prs-dep"

                                                                                                                                                                            elif key_word.lower()  == ("ArrTmrw").lower() :
                                                                                                                                                                                stat_list.descr = "Room Arrivals Tomorrow"
                                                                                                                                                                                stat_list.flag = "stat-rm-arrtmr"

                                                                                                                                                                            elif key_word.lower()  == ("pers-ArrTmrw").lower() :
                                                                                                                                                                                cur_key = "pers-ArrTmrw"
                                                                                                                                                                                key_word = "ArrTmrw"
                                                                                                                                                                                stat_list.descr = "Person Arrivals Tomorrow"
                                                                                                                                                                                stat_list.flag = "stat-prs-arrtmr"

                                                                                                                                                                            elif key_word.lower()  == ("DepTmrw").lower() :
                                                                                                                                                                                stat_list.descr = "Room Departures Tomorrow"
                                                                                                                                                                                stat_list.flag = "stat-rm-deptmr"

                                                                                                                                                                            elif key_word.lower()  == ("pers-DepTmrw").lower() :
                                                                                                                                                                                cur_key = "pers-DepTmrw"
                                                                                                                                                                                key_word = "DepTmrw"
                                                                                                                                                                                stat_list.descr = "Person Departures Tomorrow"

                                                                                                                                                                            elif key_word.lower()  == ("arrival-RSV").lower() :
                                                                                                                                                                                stat_list.descr = "Room Arrivals (Resv)"
                                                                                                                                                                                stat_list.flag = "stat-rm-rsv"

                                                                                                                                                                            for zinrstat in db_session.query(Zinrstat).filter(
                                                                                                                                                                                     (Zinrstat.datum >= datum1) & (Zinrstat.datum <= to_date) & (func.lower(Zinrstat.zinr) == (key_word).lower())).order_by(Zinrstat._recid).all():
                                                                                                                                                                                d_flag = (get_month(zinrstat.datum) == get_month(to_date)) and (get_year(zinrstat.datum) == get_year(to_date))

                                                                                                                                                                                if d_flag:

                                                                                                                                                                                    if substring(cur_key, 0, 4) == ("pers").lower() :
                                                                                                                                                                                        stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(zinrstat.datum) - 1]) + to_decimal(zinrstat.personen)
                                                                                                                                                                                    else:
                                                                                                                                                                                        stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(zinrstat.datum) - 1]) + to_decimal(zinrstat.zimmeranz)

                                                                                                                                                                                if zinrstat.datum == to_date:

                                                                                                                                                                                    if substring(cur_key, 0, 4) == ("pers").lower() :
                                                                                                                                                                                        stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal(zinrstat.personen)
                                                                                                                                                                                    else:
                                                                                                                                                                                        stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal(zinrstat.zimmeranz)

                                                                                                                                                                                if zinrstat.datum < from_date:

                                                                                                                                                                                    if substring(cur_key, 0, 4) == ("pers").lower() :
                                                                                                                                                                                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zinrstat.personen)
                                                                                                                                                                                    else:
                                                                                                                                                                                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zinrstat.zimmeranz)
                                                                                                                                                                                else:

                                                                                                                                                                                    if ytd_flag:

                                                                                                                                                                                        if substring(cur_key, 0, 4) == ("pers").lower() :
                                                                                                                                                                                            stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zinrstat.personen)
                                                                                                                                                                                        else:
                                                                                                                                                                                            stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(zinrstat.zimmeranz)


    def fill_rmocc():

        nonlocal mess_result, month_str, chcol, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        curr_date:date = None
        datum1:date = None
        datum2:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:decimal = to_decimal("0.0")

                                                                                                                                                                        if ytd_flag:
                                                                                                                                                                            datum1 = jan1
                                                                                                                                                                        else:
                                                                                                                                                                            datum1 = from_date
                                                                                                                                                                        ct1 = ct1 + 1
                                                                                                                                                                        stat_list = Stat_list()
                                                                                                                                                                        stat_list_list.append(stat_list)

                                                                                                                                                                        stat_list.ct = ct1
                                                                                                                                                                        stat_list.descr = "Rooms Occupied"
                                                                                                                                                                        stat_list.flag = "stat-occ-rm"

                                                                                                                                                                        for genstat in db_session.query(Genstat).filter(
                                                                                                                                                                                 (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.nationnr != 0) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1))]).order_by(Genstat.segmentcode).all():
                                                                                                                                                                            d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

                                                                                                                                                                            if genstat.datum == to_date:
                                                                                                                                                                                stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal("1")

                                                                                                                                                                            if get_month(genstat.datum) == get_month(to_date) and get_year(genstat.datum) == get_year(to_date):
                                                                                                                                                                                stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal("1")

                                                                                                                                                                            if ytd_flag:
                                                                                                                                                                                stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal("1")


    def fill_stat(key_word:str):

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        tday1:int = 0
        tday2:int = 0
        tday3:int = 0
        mtd1:int = 0
        mtd2:int = 0
        mtd3:int = 0
        ytd1:int = 0
        ytd2:int = 0
        ytd3:int = 0
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == (key_word).lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.flag = key_word

                                                                                                                                                                            if key_word.lower()  == ("vacant").lower() :
                                                                                                                                                                                stat_list.descr = "Vacant Rooms"

                                                                                                                                                                            for b_stat_list in query(b_stat_list_list):

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("tot-rmavail").lower() :
                                                                                                                                                                                    tday1 = b_stat_list.t_day
                                                                                                                                                                                    mtd1 = b_stat_list.mtd
                                                                                                                                                                                    ytd1 = b_stat_list.ytd

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("ooo").lower() :
                                                                                                                                                                                    tday2 = b_stat_list.t_day
                                                                                                                                                                                    mtd2 = b_stat_list.mtd
                                                                                                                                                                                    ytd2 = b_stat_list.ytd

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("occ").lower() :
                                                                                                                                                                                    tday3 = b_stat_list.t_day
                                                                                                                                                                                    mtd3 = b_stat_list.mtd
                                                                                                                                                                                    ytd3 = b_stat_list.ytd


                                                                                                                                                                            stat_list.t_day =  to_decimal(tday1) - to_decimal(tday2) - to_decimal(tday3)
                                                                                                                                                                            stat_list.mtd =  to_decimal(mtd1) - to_decimal(mtd2) - to_decimal(mtd3)
                                                                                                                                                                            stat_list.ytd =  to_decimal(ytd1) - to_decimal(ytd2) - to_decimal(ytd3)


    def fill_segm(key_word:str):

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        d_flag:bool = False
        mm:int = 0
        frate1:decimal = to_decimal("0.0")
        comp_tday:int = 0
                                                                                                                                                                        mm = get_month(to_date)
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        if key_word.lower()  == ("HSE").lower() :

                                                                                                                                                                            segment = db_session.query(Segment).filter(
                                                                                                                                                                                     (Segment.betriebsnr == 2)).first()

                                                                                                                                                                        elif key_word.lower()  == ("COM").lower() :

                                                                                                                                                                            segment = db_session.query(Segment).filter(
                                                                                                                                                                                     (Segment.betriebsnr == 1)).first()

                                                                                                                                                                        elif key_word.lower()  == ("COM-GS").lower() :

                                                                                                                                                                            segment = db_session.query(Segment).filter(
                                                                                                                                                                                     (Segment.betriebsnr == 1)).first()

                                                                                                                                                                        if segment:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1

                                                                                                                                                                            if key_word.lower()  == ("HSE").lower() :
                                                                                                                                                                                stat_list.descr = "House Uses"
                                                                                                                                                                                stat_list.flag = "stat-rrom-91"

                                                                                                                                                                            elif key_word.lower()  == ("COM").lower() :
                                                                                                                                                                                stat_list.descr = "Complimentary"
                                                                                                                                                                                stat_list.flag = "stat-rrom-90"

                                                                                                                                                                            elif key_word.lower()  == ("COM-GS").lower() :
                                                                                                                                                                                stat_list.descr = "Complimentary Guest"
                                                                                                                                                                                stat_list.flag = "stat-numcompl"

                                                                                                                                                                            for genstat in db_session.query(Genstat).filter(
                                                                                                                                                                                     (Genstat.segmentcode == segment.segmentcode) & (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1))]).order_by(Genstat._recid).all():

                                                                                                                                                                                if foreign_flag:
                                                                                                                                                                                    find_exrate(genstat.datum)

                                                                                                                                                                                    if exrate:
                                                                                                                                                                                        frate =  to_decimal(exrate.betrag)
                                                                                                                                                                                d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

                                                                                                                                                                                if genstat.datum == to_date:

                                                                                                                                                                                    if key_word.lower()  == ("COM-GS").lower() :
                                                                                                                                                                                        stat_list.t_day =  to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.kind3)
                                                                                                                                                                                    else:
                                                                                                                                                                                        stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal("1")

                                                                                                                                                                                if get_month(genstat.datum) == mm:

                                                                                                                                                                                    if key_word.lower()  == ("COM-GS").lower() :
                                                                                                                                                                                        stat_list.mtd =  to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.kind3)
                                                                                                                                                                                    else:
                                                                                                                                                                                        stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(genstat.datum) - 1]) + to_decimal("1")

                                                                                                                                                                                if key_word.lower()  == ("COM-GS").lower() :
                                                                                                                                                                                    stat_list.mtd =  to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.kind3)
                                                                                                                                                                                else:
                                                                                                                                                                                    stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal("1")


    def fill_comproomnew():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        d_flag:bool = False
        mm:int = 0
        frate1:decimal = to_decimal("0.0")
                                                                                                                                                                        mm = get_month(to_date)
                                                                                                                                                                        ct1 = ct1 + 1
                                                                                                                                                                        stat_list = Stat_list()
                                                                                                                                                                        stat_list_list.append(stat_list)

                                                                                                                                                                        stat_list.ct = ct1
                                                                                                                                                                        stat_list.flag = "Compl"
                                                                                                                                                                        stat_list.descr = "Complimentary Paying Guest"

                                                                                                                                                                        genstat_obj_list = []
                                                                                                                                                                        for genstat, segment in db_session.query(Genstat, Segment).join(Segment,(Segment.segmentcode == Genstat.segmentcode)).filter(
                                                                                                                                                                                 (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.zipreis == 0) & (Genstat.gratis == 0) & (Genstat.resstatus == 6) & (Genstat.res_logic[inc_value(2))]).order_by(Genstat._recid).all():
                                                                                                                                                                            if genstat._recid in genstat_obj_list:
                                                                                                                                                                                continue
                                                                                                                                                                            else:
                                                                                                                                                                                genstat_obj_list.append(genstat._recid)

                                                                                                                                                                            if segment.betriebsnr == 0:

                                                                                                                                                                                if foreign_flag:
                                                                                                                                                                                    find_exrate(genstat.datum)

                                                                                                                                                                                    if exrate:
                                                                                                                                                                                        frate =  to_decimal(exrate.betrag)
                                                                                                                                                                                d_flag = (get_month(genstat.datum) == get_month(to_date)) and (get_year(genstat.datum) == get_year(to_date))

                                                                                                                                                                                if genstat.datum == to_date:
                                                                                                                                                                                    stat_list.t_day =  to_decimal(stat_list.t_day) + to_decimal("1")

                                                                                                                                                                                if get_month(genstat.datum) == mm:
                                                                                                                                                                                    stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(mon_saldo[get_day(genstat.datum) - 1]) + to_decimal("1")
                                                                                                                                                                                stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal("1")


    def fill_roomsold():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        tday1:int = 0
        tday2:int = 0
        tday3:int = 0
        mtd1:int = 0
        mtd2:int = 0
        mtd3:int = 0
        ytd1:int = 0
        ytd2:int = 0
        ytd3:int = 0
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("rmsold").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.flag = "rmsold"
                                                                                                                                                                            stat_list.descr = "Rooms Sold"

                                                                                                                                                                            for b_stat_list in query(b_stat_list_list):

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("stat-rrom-91").lower() :
                                                                                                                                                                                    tday1 = b_stat_list.t_day
                                                                                                                                                                                    mtd1 = b_stat_list.mtd
                                                                                                                                                                                    ytd1 = b_stat_list.ytd

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("stat-rrom-90").lower() :
                                                                                                                                                                                    tday2 = b_stat_list.t_day
                                                                                                                                                                                    mtd2 = b_stat_list.mtd
                                                                                                                                                                                    ytd2 = b_stat_list.ytd

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("stat-occ-rm").lower() :
                                                                                                                                                                                    tday3 = b_stat_list.t_day
                                                                                                                                                                                    mtd3 = b_stat_list.mtd
                                                                                                                                                                                    ytd3 = b_stat_list.ytd


                                                                                                                                                                            stat_list.t_day =  to_decimal(tday1) + to_decimal(tday2) + to_decimal(tday3)
                                                                                                                                                                            stat_list.mtd =  to_decimal(mtd1) + to_decimal(mtd2) + to_decimal(mtd3)
                                                                                                                                                                            stat_list.ytd =  to_decimal(ytd1) + to_decimal(ytd2) + to_decimal(ytd3)


    def fill_occ_pay():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        tday1:int = 0
        tday2:int = 0
        tday3:int = 0
        mtd1:int = 0
        mtd2:int = 0
        mtd3:int = 0
        ytd1:int = 0
        ytd2:int = 0
        ytd3:int = 0
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("occpay").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.flag = "occ-pay"
                                                                                                                                                                            stat_list.descr = "% Occupancy (Paying)"

                                                                                                                                                                            for b_stat_list in query(b_stat_list_list):

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("tot-rm").lower() :
                                                                                                                                                                                    tday1 = b_stat_list.t_day
                                                                                                                                                                                    mtd1 = b_stat_list.mtd
                                                                                                                                                                                    ytd1 = b_stat_list.ytd

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("rmsold").lower() :
                                                                                                                                                                                    tday2 = b_stat_list.t_day
                                                                                                                                                                                    mtd2 = b_stat_list.mtd
                                                                                                                                                                                    ytd2 = b_stat_list.ytd

                                                                                                                                                                            if tday2 != 0 or mtd2 != 0 or ytd2 != 0:
                                                                                                                                                                                stat_list.t_day = ( to_decimal(tday2) / to_decimal(tday1)) * to_decimal("100")
                                                                                                                                                                                stat_list.mtd = ( to_decimal(mtd2) / to_decimal(mtd1)) * to_decimal("100")
                                                                                                                                                                                stat_list.ytd = ( to_decimal(ytd2) / to_decimal(ytd1)) * to_decimal("100")


    def fill_occ_comp_hu():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        tday1:int = 0
        tday2:int = 0
        tday3:int = 0
        mtd1:int = 0
        mtd2:int = 0
        mtd3:int = 0
        ytd1:int = 0
        ytd2:int = 0
        ytd3:int = 0
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("occ-comp-hu").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.flag = "occ-comp-hu"
                                                                                                                                                                            stat_list.descr = "% Occupancy (Comp + HU)"

                                                                                                                                                                            for b_stat_list in query(b_stat_list_list):

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("occ").lower() :
                                                                                                                                                                                    tday1 = b_stat_list.t_day
                                                                                                                                                                                    mtd1 = b_stat_list.mtd
                                                                                                                                                                                    ytd1 = b_stat_list.ytd

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("tot-rm").lower() :
                                                                                                                                                                                    tday2 = b_stat_list.t_day
                                                                                                                                                                                    mtd2 = b_stat_list.mtd
                                                                                                                                                                                    ytd2 = b_stat_list.ytd

                                                                                                                                                                            if tday2 != 0 or mtd2 != 0 or ytd2 != 0:
                                                                                                                                                                                stat_list.t_day = ( to_decimal(tday1) / to_decimal(tday2)) * to_decimal("100")
                                                                                                                                                                                stat_list.mtd = ( to_decimal(mtd1) / to_decimal(mtd2)) * to_decimal("100")
                                                                                                                                                                                stat_list.ytd = ( to_decimal(ytd1) / to_decimal(ytd2)) * to_decimal("100")


    def fill_tot_rev():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        tday1:decimal = to_decimal("0.0")
        tday2:decimal = to_decimal("0.0")
        tday3:decimal = to_decimal("0.0")
        mtd1:decimal = to_decimal("0.0")
        mtd2:decimal = to_decimal("0.0")
        mtd3:decimal = to_decimal("0.0")
        ytd1:decimal = to_decimal("0.0")
        ytd2:decimal = to_decimal("0.0")
        ytd3:decimal = to_decimal("0.0")
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("tot-rev").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.flag = "stat-tot-rev"
                                                                                                                                                                            stat_list.descr = "Total Room Revenue"

                                                                                                                                                                            rev_list = query(rev_list_list, filters=(lambda rev_list: rev_list.flag.lower()  == ("Room").lower()  and re.match(r".*Room Revenue.*",rev_list.descr, re.IGNORECASE)), first=True)

                                                                                                                                                                            if rev_list:
                                                                                                                                                                                stat_list.t_day =  to_decimal(rev_list.t_day)
                                                                                                                                                                                stat_list.mtd =  to_decimal(rev_list.mtd)
                                                                                                                                                                                stat_list.ytd =  to_decimal(rev_list.ytd)
                                                                                                                                                                                stat_list.mtd_budget =  to_decimal(rev_list.mtd_budget)


    def fill_avg_rmrate_rp():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        tday1:decimal = to_decimal("0.0")
        tday2:decimal = to_decimal("0.0")
        tday3:decimal = to_decimal("0.0")
        mtd1:decimal = to_decimal("0.0")
        mtd2:decimal = to_decimal("0.0")
        mtd3:decimal = to_decimal("0.0")
        ytd1:decimal = to_decimal("0.0")
        ytd2:decimal = to_decimal("0.0")
        ytd3:decimal = to_decimal("0.0")
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("avg-rmrate-rp").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.flag = "avg-rmrate-rp"
                                                                                                                                                                            stat_list.descr = "Average Room Rate Rp."

                                                                                                                                                                            for b_stat_list in query(b_stat_list_list):

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("rmsold").lower() :
                                                                                                                                                                                    tday2 =  to_decimal(b_stat_list.t_day)
                                                                                                                                                                                    mtd2 =  to_decimal(b_stat_list.mtd)
                                                                                                                                                                                    ytd2 =  to_decimal(b_stat_list.ytd)

                                                                                                                                                                            b_stat = query(b_stat_list, filters=(lambda b_stat: b_stat.flag.lower()  == ("stat-tot-rev").lower()), first=True)

                                                                                                                                                                            if b_stat:
                                                                                                                                                                                tday1 =  to_decimal(b_stat.t_day)
                                                                                                                                                                                mtd1 =  to_decimal(b_stat.mtd)
                                                                                                                                                                                ytd1 =  to_decimal(b_stat.ytd)

                                                                                                                                                                            if tday2 != 0 or mtd2 != 0 or ytd2 != 0:
                                                                                                                                                                                stat_list.t_day = ( to_decimal(tday1) / to_decimal(tday2) )
                                                                                                                                                                                stat_list.mtd = ( to_decimal(mtd1) / to_decimal(mtd2) )
                                                                                                                                                                                stat_list.ytd = ( to_decimal(ytd1) / to_decimal(ytd2) )


    def fill_avg_rmrate_frg():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        tday1:decimal = to_decimal("0.0")
        tday2:decimal = to_decimal("0.0")
        tday3:decimal = to_decimal("0.0")
        mtd1:decimal = to_decimal("0.0")
        mtd2:decimal = to_decimal("0.0")
        mtd3:decimal = to_decimal("0.0")
        ytd1:decimal = to_decimal("0.0")
        ytd2:decimal = to_decimal("0.0")
        ytd3:decimal = to_decimal("0.0")
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("avg-rmrate-frg").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.flag = "avg-rmrate-frg"
                                                                                                                                                                            stat_list.descr = "Average Room Rate US$"

                                                                                                                                                                            for b_stat_list in query(b_stat_list_list):

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("rmsold").lower() :
                                                                                                                                                                                    tday2 =  to_decimal(b_stat_list.t_day)
                                                                                                                                                                                    mtd2 =  to_decimal(b_stat_list.mtd)
                                                                                                                                                                                    ytd2 =  to_decimal(b_stat_list.ytd)

                                                                                                                                                                            rev_list = query(rev_list_list, first=True)

                                                                                                                                                                            if rev_list:
                                                                                                                                                                                find_exrate(to_date)

                                                                                                                                                                                if exrate:
                                                                                                                                                                                    frate =  to_decimal(exrate.betrag)
                                                                                                                                                                                tday1 =  to_decimal(rev_list.t_day) / to_decimal((fact) * to_decimal(frate) )
                                                                                                                                                                                mtd1 =  to_decimal(rev_list.mtd) / to_decimal((fact) * to_decimal(frate) )
                                                                                                                                                                                ytd1 =  to_decimal(rev_list.ytd) / to_decimal((fact) * to_decimal(frate) )

                                                                                                                                                                            if tday2 != 0 or mtd2 != 0 or ytd2 != 0:
                                                                                                                                                                                stat_list.t_day = ( to_decimal(tday1) / to_decimal(tday2)) / to_decimal(foreign_curr)
                                                                                                                                                                                stat_list.mtd = ( to_decimal(mtd1) / to_decimal(mtd2)) / to_decimal(foreign_curr)
                                                                                                                                                                                stat_list.ytd = ( to_decimal(ytd1) / to_decimal(ytd2)) / to_decimal(foreign_curr)


    def fill_revpar():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        tday1:decimal = to_decimal("0.0")
        tday2:decimal = to_decimal("0.0")
        mtd1:decimal = to_decimal("0.0")
        mtd2:decimal = to_decimal("0.0")
        mtd_budget1:decimal = to_decimal("0.0")
        mtd_budget2:decimal = to_decimal("0.0")
        ytd1:decimal = to_decimal("0.0")
        ytd2:decimal = to_decimal("0.0")
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("revpar").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.flag = "revpar"
                                                                                                                                                                            stat_list.descr = "Revenue Per Available Room / Revpar"

                                                                                                                                                                            for b_stat_list in query(b_stat_list_list):

                                                                                                                                                                                if b_stat_list.flag.lower()  == ("tot-rmav").lower() :
                                                                                                                                                                                    tday2 =  to_decimal(b_stat_list.t_day)
                                                                                                                                                                                    mtd2 =  to_decimal(b_stat_list.mtd)
                                                                                                                                                                                    mtd_budget2 =  to_decimal(b_stat_list.mtd_budget)
                                                                                                                                                                                    ytd2 =  to_decimal(b_stat_list.ytd)

                                                                                                                                                                            rev_list = query(rev_list_list, filters=(lambda rev_list: rev_list.descr.lower()  == ("TOTAL ROOM REVENUE").lower()), first=True)

                                                                                                                                                                            if rev_list:
                                                                                                                                                                                tday1 =  to_decimal(rev_list.t_day)
                                                                                                                                                                                mtd1 =  to_decimal(rev_list.mtd)
                                                                                                                                                                                mtd_budget1 =  to_decimal(rev_list.mtd_budget)
                                                                                                                                                                                ytd1 =  to_decimal(rev_list.ytd)

                                                                                                                                                                            if mtd_budget1 != 0 and mtd_budget2 != 0:
                                                                                                                                                                                stat_list.mtd_budget = ( to_decimal(mtd_budget1) / to_decimal(mtd_budget2))

                                                                                                                                                                            if tday2 != 0 or mtd2 != 0 or ytd2 != 0:
                                                                                                                                                                                stat_list.t_day = ( to_decimal(tday1) / to_decimal(tday2) )
                                                                                                                                                                                stat_list.mtd = ( to_decimal(mtd1) / to_decimal(mtd2) )
                                                                                                                                                                                stat_list.ytd = ( to_decimal(ytd1) / to_decimal(ytd2) )


    def fill_gs_inhouse():

        nonlocal mess_result, month_str, chcol, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, from_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        datum1:date = None
        datum2:date = None
        curr_date:date = None
        ly_currdate:date = None
        d_flag:bool = False
        dbudget_flag:bool = False
        dlmtd_flag:bool = False
        frate1:decimal = to_decimal("0.0")

                                                                                                                                                                        if ytd_flag:
                                                                                                                                                                            datum1 = jan1
                                                                                                                                                                        else:
                                                                                                                                                                            datum1 = from_date
                                                                                                                                                                        ct1 = ct1 + 1

                                                                                                                                                                        stat_list = query(stat_list_list, filters=(lambda stat_list: stat_list.flag.lower()  == ("stat-nguest").lower()), first=True)

                                                                                                                                                                        if not stat_list:
                                                                                                                                                                            stat_list = Stat_list()
                                                                                                                                                                            stat_list_list.append(stat_list)

                                                                                                                                                                            stat_list.ct = ct1
                                                                                                                                                                            stat_list.flag = "stat-nguest"
                                                                                                                                                                            stat_list.descr = "Guest In House"

                                                                                                                                                                            for segmentstat in db_session.query(Segmentstat).filter(
                                                                                                                                                                                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date) & (Segmentstat.segmentcode == segment.segmentcode)).order_by(Segmentstat._recid).all():
                                                                                                                                                                                frate =  to_decimal("1")

                                                                                                                                                                                if foreign_flag:
                                                                                                                                                                                    find_exrate(segmentstat.datum)

                                                                                                                                                                                    if exrate:
                                                                                                                                                                                        frate =  to_decimal(exrate.betrag)
                                                                                                                                                                                d_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))
                                                                                                                                                                                dbudget_flag = (get_month(segmentstat.datum) == get_month(to_date)) and (get_year(segmentstat.datum) == get_year(to_date))

                                                                                                                                                                                if segmentstat.datum == to_date:
                                                                                                                                                                                    stat_list.t_day =  to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

                                                                                                                                                                                if get_month(segmentstat.datum) == get_month(to_date):
                                                                                                                                                                                    stat_list.mtd =  to_decimal(stat_list.mtd) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)

                                                                                                                                                                                if segmentstat.datum < from_date:
                                                                                                                                                                                    stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)
                                                                                                                                                                                else:

                                                                                                                                                                                    if ytd_flag:
                                                                                                                                                                                        stat_list.ytd =  to_decimal(stat_list.ytd) + to_decimal(segmentstat.persanz) + to_decimal(segmentstat.kind1) + to_decimal(segmentstat.kind2) + to_decimal(segmentstat.gratis)


    def calc_cf():

        nonlocal mess_result, month_str, chcol, curr_date, curr_i, curr_row, curr_col, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, gl_year, to_year, foreign_flag, prev_str, cell_val, exrate_betrag, hist_flag, curr_close_year, found_flag, ytd_bal, val_sign, j, i, diff, lmdiff, mtd_betrag, ytd_betrag, start_row, start_col, end_row, end_col, htl_no, datum1, jan1, ljan1, lfrom_date, lto_date, cash_flow, foreign_curr, ct1, mon_saldo, vat2, ytd_flag, d_flag, n_serv, n_tax, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, waehrung, htparam, paramtext, gl_jouhdr, gl_journal, umsatz, genstat, segmentstat, budget, zinrstat, zkstat, segment
        nonlocal briefnr, from_date, to_date, user_init, gl_month, link
        nonlocal b_stat_list, b_stat, buff_exrate, b_param


        nonlocal t_parameters, t_gl_accthis, glacct_list, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, coa_list, t_list, stat_list, rev_list, b_stat_list, b_stat, buff_exrate, b_param
        nonlocal t_parameters_list, t_gl_accthis_list, glacct_list_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, coa_list_list, t_list_list, stat_list_list, rev_list_list

        from_lsyr:date = None
        to_lsyr:date = None
        pfrom_date:date = None
        pto_date:date = None
        from_month:date = None
        from_year:date = None

                                                                                                                                                                        if get_month(from_date) == 1:
                                                                                                                                                                            pfrom_date = date_mdy(12, get_day(from_date) , get_year(from_date) - timedelta(days=1))
                                                                                                                                                                        else:
                                                                                                                                                                            pfrom_date = date_mdy(get_month(from_date) - timedelta(days=1, get_day(from_date) , get_year(from_date)))

                                                                                                                                                                        if get_month(to_date) == 1:
                                                                                                                                                                            pto_date = date_mdy(12, get_day(to_date) , get_year(to_date) - timedelta(days=1))
                                                                                                                                                                        else:
                                                                                                                                                                            pto_date = date_mdy(get_month(to_date) - timedelta(days=1, get_day(to_date) , get_year(to_date)))
                                                                                                                                                                        from_lsyr = date_mdy(get_month(from_date) , get_day(from_date) , get_year(from_date) - timedelta(days=1))

                                                                                                                                                                        if get_month(to_date) == 2 and (get_year(to_date) % 4 == 0):
                                                                                                                                                                            to_lsyr = date_mdy(get_month(to_date) , get_day(to_date) - 1, get_year(to_date) - 1)
                                                                                                                                                                        else:
                                                                                                                                                                            to_lsyr = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - timedelta(days=1))

                                                                                                                                                                        if pfrom_date == None:
                                                                                                                                                                            pfrom_date = date_mdy(get_month(from_date) , 1, get_year(from_date)) - timedelta(days=1)

                                                                                                                                                                        if pto_date == None:
                                                                                                                                                                            pto_date = date_mdy(get_month(to_date) , 1, get_year(to_date)) - timedelta(days=1)

                                                                                                                                                                        if from_lsyr == None:
                                                                                                                                                                            from_lsyr = date_mdy(get_month(from_date) , 1, get_year(from_date) - 1) - 1

                                                                                                                                                                        if to_lsyr == None:
                                                                                                                                                                            to_lsyr = date_mdy(get_month(to_date) , 1, get_year(to_date) - 1) - 1

                                                                                                                                                                        if from_month == None:
                                                                                                                                                                            from_month = date_mdy(get_month(to_date) , 1, get_year(to_date))

                                                                                                                                                                        if from_year == None:
                                                                                                                                                                            from_year = date_mdy(1, 1, get_year(to_date))
                                                                                                                                                                        t_list_list = get_output(glacct_cashflow_1bl(from_date, to_date, from_lsyr, to_lsyr, pfrom_date, pto_date, from_month, from_year, coa_list_list))

    if (get_month(to_date) != 2) or (get_day(to_date) != 29):
        lto_date = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - timedelta(days=1))
    else:
        lto_date = date_mdy(get_month(to_date) , 28, get_year(to_date) - timedelta(days=1))
    jan1 = date_mdy(1, 1, get_year(to_date))
    ljan1 = date_mdy(1, 1, get_year(to_date) - timedelta(days=1))
    lfrom_date = date_mdy(get_month(to_date) , 1, get_year(to_date) - timedelta(days=1))

    waehrung = db_session.query(Waehrung).filter(
             (Waehrung.waehrungsnr == 2)).first()

    if waehrung:
        foreign_curr =  to_decimal(waehrung.ankauf)

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)
    g_list_list.clear()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum).all():

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal.fibukonto).all():
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.datum = gl_jouhdr.datum
            g_list.grecid = gl_journal._recid
            g_list.fibu = gl_journal.fibukonto

    if ytd_flag:
        datum1 = jan1
    else:
        datum1 = from_date
    OS_DELETE VALUE ("/usr1/vhp/tmp/output_" + htl_no + ".txt")
    OUTPUT STREAM s1 TO VALUE ("/usr1/vhp/tmp/output_" + htl_no + ".txt") APPEND UNBUFFERED

    parameters = db_session.query(Parameters).filter(
             (func.lower(Parameters.progname) == ("GL-macro").lower()) & (Parameters.section == to_string(briefnr)) & (Parameters.vstring == "$IN-FORParameters.EIGN")).first()

    if parameters:
        foreign_flag = True
        fill_exrate()

    parameters = db_session.query(Parameters).filter(
             (func.lower(Parameters.progname) == ("GL-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (num_entries(Parameters.varname, "-") == 3) & (entry(2, Parameters.varname, "-") == ("CF").lower())).first()

    if parameters:
        cash_flow = True

    if cash_flow:

        for parameters in db_session.query(Parameters).filter(
                 (func.lower(Parameters.progname) == ("GL-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (num_entries(Parameters.varname, "-") == 3) & (entry(2, Parameters.varname, "-") == ("CF").lower())).order_by(Parameters.varname).all():
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)

            gl_acct = db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto == entry(0, t_parameters.vstring, ":"))).first()

            if gl_acct:

                coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.fibu == gl_acct.fibukonto), first=True)

                if not coa_list:
                    coa_list = Coa_list()
                    coa_list_list.append(coa_list)

                    coa_list.fibu = gl_acct.fibukonto


        calc_cf()

    parameters = db_session.query(Parameters).filter(
             (func.lower(Parameters.progname) == ("GL-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (num_entries(Parameters.varname, "-") == 3) & (entry(2, Parameters.varname, "-") == ("REV").lower())).first()

    if parameters:
        fill_revenue()

    parameters = db_session.query(Parameters).filter(
             (func.lower(Parameters.progname) == ("GL-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (func.lower((Parameters.vstring).op("~")(("*segmrev*".lower().replace("*",".*")))) | (func.lower(Parameters.vstring).op("~")(("*segmpers*".lower().replace("*",".*")))) | (func.lower(Parameters.vstring).op("~")(("*segmroom*".lower().replace("*",".*")))))).first()

    if parameters:
        fill_segment()
    create_rev_list()
    fill_tot_room()
    fill_tot_avail()
    fill_inactive()
    fill_rmstat("ooo")
    fill_rmocc()
    fill_stat("vacant")
    fill_segm("HSE")
    fill_segm("COM")
    fill_segm("COM-GS")
    fill_comproomnew()
    fill_roomsold()
    fill_occ_pay()
    fill_occ_comp_hu()
    fill_tot_rev()
    fill_avg_rmrate_rp()
    fill_avg_rmrate_frg()
    fill_revpar()
    fill_rmstat("dayuse")
    fill_rmstat("No-Show")
    fill_rmstat("arrival-WIG")
    fill_rmstat("NewRes")
    fill_rmstat("CancRes")
    fill_rmstat("Early-CO")
    fill_rmstat("arrival")
    fill_rmstat("pers-arrival")
    fill_rmstat("departure")
    fill_rmstat("pers-depature")
    fill_rmstat("ArrTmrw")
    fill_rmstat("pers-ArrTmrw")
    fill_rmstat("DepTmrw")
    fill_rmstat("pers-DepTmrw")
    fill_rmstat("arrival-RSV")
    fill_gs_inhouse()
    fill_statistic()
    gl_year = get_year(to_date)

    for parameters in db_session.query(Parameters).filter(
             (func.lower(Parameters.progname) == ("GL-macro").lower()) & (Parameters.section == to_string(briefnr))).order_by(Parameters.varname).all():

        if prev_str != parameters.varname:
            debit =  to_decimal("0")
            credit =  to_decimal("0")
            prev_str = parameters.varname


            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)

            if substring(parameters.vstring, 0, 1) != ("$").lower() :

                gl_accthis = db_session.query(Gl_accthis).filter(
                         (Gl_accthis.fibukonto == parameters.vstring) & (Gl_accthis.year == gl_year)).first()

                if gl_accthis:

                    t_gl_accthis = query(t_gl_accthis_list, filters=(lambda t_gl_accthis: t_gl_accthis.fibukonto == gl_accthis.fibukonto and t_gl_accthis.year == gl_accthis.year), first=True)

                    if not t_gl_accthis:
                        t_gl_accthis = T_gl_accthis()
                        t_gl_accthis_list.append(t_gl_accthis)

                        buffer_copy(gl_accthis, t_gl_accthis)

                        if substring(t_gl_accthis.fibukonto, 0, 1) == ("9").lower() :
                            pass
                        else:
                            for curr_i in range(1,12 + 1) :
                                t_gl_accthis.actual[curr_i - 1] = t_gl_accthis.actual[curr_i - 1] / actual_exrate[curr_i - 1]
                                t_gl_accthis.budget[curr_i - 1] = t_gl_accthis.budget[curr_i - 1] / budget_exrate[curr_i - 1]
                                t_gl_accthis.last_yr[curr_i - 1] = t_gl_accthis.last_yr[curr_i - 1] / lyear_exrate[curr_i - 1]
                                t_gl_accthis.ly_budget[curr_i - 1] = t_gl_accthis.ly_budget[curr_i - 1] / blyear_exrate[curr_i - 1]

                gl_acct = db_session.query(Gl_acct).filter(
                         (Gl_acct.fibukonto == parameters.vstring)).first()

                if gl_acct:

                    t_gl_acct = query(t_gl_acct_list, filters=(lambda t_gl_acct: t_gl_acct.fibukonto == gl_acct.fibukonto), first=True)

                    if not t_gl_acct:
                        t_gl_acct = T_gl_acct()
                        t_gl_acct_list.append(t_gl_acct)

                        buffer_copy(gl_acct, t_gl_acct)

                        if substring(t_gl_acct.fibukonto, 0, 1) == ("9").lower() :
                            pass
                        else:
                            for curr_i in range(1,12 + 1) :
                                t_gl_acct.actual[curr_i - 1] = t_gl_acct.actual[curr_i - 1] / actual_exrate[curr_i - 1]
                                t_gl_acct.budget[curr_i - 1] = t_gl_acct.budget[curr_i - 1] / budget_exrate[curr_i - 1]
                                t_gl_acct.last_yr[curr_i - 1] = t_gl_acct.last_yr[curr_i - 1] / lyear_exrate[curr_i - 1]
                                t_gl_acct.ly_budget[curr_i - 1] = t_gl_acct.ly_budget[curr_i - 1] / blyear_exrate[curr_i - 1]

                if parameters.vtype == 25 or parameters.vtype == 26:

                    for g_list in query(g_list_list, filters=(lambda g_list: g_list.fibu == parameters.vstring), sort_by=[("fibu",False),("datum",False)]):
                        pass

                        if g_list.grecid != 0:

                            gl_journal = db_session.query(Gl_journal).filter(
                                     (Gl_journal._recid == g_list.grecid)).first()

                            if gl_journal:
                                debit =  to_decimal(debit) + to_decimal(gl_journal.debit)


                            credit =  to_decimal(credit) + to_decimal(gl_journal.credit)
                    temp_list = Temp_list()
                    temp_list_list.append(temp_list)

                    temp_list.vstring = parameters.vstring
                    temp_list.debit =  to_decimal(debit)
                    temp_list.credit =  to_decimal(credit)

                if parameters.vtype == 23 and num_entries(parameters.varname, "-") == 2:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == to_int(substring(parameters.vstring, 2))) & (Artikel.departement == to_int(substring(parameters.vstring, 0, 2)))).first()

                    if artikel:

                        t_artikel = query(t_artikel_list, filters=(lambda t_artikel: t_artikel.artnr == artikel.artnr and t_artikel.departement == artikel.departement), first=True)

                        if not t_artikel:
                            t_artikel = T_artikel()
                            t_artikel_list.append(t_artikel)

                            buffer_copy(artikel, t_artikel)
                    for curr_date in date_range(date_mdy(01, 01, get_year(to_date)),to_date) :
                        serv =  to_decimal("0")
                        vat =  to_decimal("0")

                        umsatz = db_session.query(Umsatz).filter(
                                 (Umsatz.datum == curr_date) & (Umsatz.artnr == to_int(substring(parameters.vstring, 2))) & (Umsatz.departement == to_int(substring(parameters.vstring, 0, 2)))).first()

                        if umsatz:
                            serv, vat = get_output(calc_servvat(umsatz.departement, umsatz.artnr, umsatz.datum, artikel.service_code, artikel.mwst_code))
                            fact =  to_decimal(1.00) + to_decimal(serv) + to_decimal(vat)
                            n_betrag =  to_decimal("0")

                            if foreign_flag:
                                find_exrate(curr_date)

                                if buff_exrate:
                                    frate =  to_decimal(buff_exrate.betrag)
                            n_betrag =  to_decimal(umsatz.betrag) / to_decimal((fact) * to_decimal(frate))

                            if price_decimal == 0:
                                n_betrag = to_decimal(round(n_betrag , 0))

                        if umsatz:
                            t_umsz = T_umsz()
                            t_umsz_list.append(t_umsz)

                            t_umsz.curr_date = curr_date
                            t_umsz.fact =  to_decimal(fact)
                            t_umsz.betrag =  to_decimal(n_betrag)
                            t_umsz.artnr = umsatz.artnr
                            t_umsz.dept = umsatz.departement


    glacct_list = Glacct_list()
    glacct_list_list.append(glacct_list)


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 795)).first()
    curr_close_year = get_year(htparam.fdate) + 1

    if gl_year < curr_close_year:
        hist_flag = True

    t_parameters = query(t_parameters_list, filters=(lambda t_parameters: t_parameters.progname.lower()  == ("GL-Macro").lower()  and num_entries(t_parameters.varname, "-") == 3 and entry(2, t_parameters.varname, "-") == ("CF").lower()), first=True)

    if t_parameters:

        for t_parameters in query(t_parameters_list, filters=(lambda t_parameters: t_parameters.num_entries(t_parameters.varname, "-") == 3 and entry(2, t_parameters.varname, "-") == ("CF").lower()  and num_entries(t_parameters.vstring, ":") > 1)):
            curr_row = to_int(entry(0, t_parameters.varname, "-"))
            curr_col = to_int(entry(1, t_parameters.varname, "-"))
            end_row = curr_row
            end_col = curr_col

            if num_entries(t_parameters.vstring, ":") > 1:

                t_list = query(t_list_list, filters=(lambda t_list: t_list.fibukonto == entry(0, t_parameters.vstring, ":") and t_list.cf == to_int(entry(1, t_parameters.vstring, ":"))), first=True)

                if t_list:
                    cell_val = ""

                    if t_parameters.vtype == 25:
                        cell_val = to_string(t_list.debit, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 26:
                        cell_val = to_string(t_list.credit, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 79:
                        cell_val = to_string(t_list.debit_lsyear, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 80:
                        cell_val = to_string(t_list.credit_lsyear, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 81:
                        cell_val = to_string(t_list.debit_lsmonth, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 82:
                        cell_val = to_string(t_list.credit_lsmonth, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 1:
                        cell_val = to_string(t_list.balance, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 3:
                        cell_val = to_string(t_list.pm_balance, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 4:
                        cell_val = to_string(t_list.ly_balance, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 90:
                        cell_val = to_string(t_list.debit_today, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 91:
                        cell_val = to_string(t_list.credit_today, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 92:
                        cell_val = to_string(t_list.debit_MTD, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 93:
                        cell_val = to_string(t_list.credit_MTD, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 94:
                        cell_val = to_string(t_list.debit_YTD, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 95:
                        cell_val = to_string(t_list.credit_YTD, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 96:
                        cell_val = to_string(t_list.today_balance, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 97:
                        cell_val = to_string(t_list.MTD_balance, "->,>>>,>>>,>>>,>>>,>>9.99")

                    elif t_parameters.vtype == 98:
                        cell_val = to_string(t_list.YTD_balance, "->,>>>,>>>,>>>,>>>,>>9.99")


                else:
                    cell_val = ""

            if cell_val != "":
                else:

            for t_parameters in query(t_parameters_list, filters=(lambda t_parameters: t_parameters.num_entries(t_parameters.varname, "-") <= 2), sort_by=[("varname",False)]):
                curr_row = to_int(entry(0, t_parameters.varname, "-"))
                curr_col = to_int(entry(1, t_parameters.varname, "-"))
                end_row = curr_row
                end_col = curr_col

            if start_row == 0:
                start_row = curr_row

            if start_col == 0:
                start_col = curr_col

            if t_parameters.vtype == 0:
                cell_val = ""

                if t_parameters.vstring == "$datum":
                    cell_val = "Created: " + to_string(get_current_date()) + " - " + user_init


                elif t_parameters.vstring == "$CLOSE-DATE":
                    cell_val = "Closing Date: " + to_string(to_date, "99/99/9999")


                elif t_parameters.vstring == "$CLOSE-MONTH":
                    cell_val = "Accounting Period: " + month_str[get_month(to_date) - 1] +\
                        " " + to_string(get_year(to_date) , "9999")


                elif t_parameters.vstring == "$CLOSE-MONTH1":
                    cell_val = to_string(get_month(to_date) , "99") + "/" + to_string(get_year(to_date) , "9999")


                elif t_parameters.vstring == "$EXRATE":
                    exrate_betrag, frate = get_output(gl_parxls1_find_exratebl(to_date, foreign_flag))
                    cell_val = "ExchgRate: " + trim(to_string(exrate_betrag, "->>>>>>>>>>>>>9.99"))

                if cell_val != "":
                    else:

                    elif t_parameters.vtype > 0:

                        if hist_flag:

                            t_gl_accthis = query(t_gl_accthis_list, filters=(lambda t_gl_accthis: t_gl_accthis.fibukonto == t_parameters.vstring and t_gl_accthis.year == gl_year), first=True)
                        found_flag = None ! == t_gl_accthis

                        if found_flag:
                            buffer_copy(t_gl_accthis, glacct_list)
                    else:

                        t_gl_acct = query(t_gl_acct_list, filters=(lambda t_gl_acct: t_gl_acct.fibukonto == t_parameters.vstring), first=True)
                        found_flag = None ! == t_gl_acct

                        if found_flag:
                            buffer_copy(t_gl_acct, glacct_list)

                if t_parameters.vtype > 0:
                    cell_val = ""

                    if found_flag and (glacct_list.acc_type == 1 or glacct_list.acc_type == 4):

                        if t_parameters.vtype == 1:

                            if glacct_list.actual[gl_month - 1] == None:
                                glacct_list.actual[gl_month - 1] = 0


                            cell_val = trim(to_string(- glacct_list.actual[gl_month - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 2:
                        ytd_bal =  to_decimal("0")
                        for curr_i in range(1,gl_month + 1) :

                            if glacct_list.actual[curr_i - 1] == None:
                                glacct_list.actual[curr_i - 1] = 0


                            ytd_bal =  to_decimal(ytd_bal) - to_decimal(glacct_list.actual[curr_i - 1])
                        cell_val = trim(to_string(ytd_bal, "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 3:

                        if gl_month == 1:

                            if glacct_list.last_yr[11] == None:
                                glacct_list.last_yr[11] = 0


                            cell_val = trim(to_string(- glacct_list.last_yr[11], "->>>>>>>>>>>>>>>>9.99"))
                        else:

                            if glacct_list.actual[gl_month - 1 - 1] == None:
                                glacct_list.actual[gl_month - 1 - 1] = 0


                            cell_val = trim(to_string(- glacct_list.actual[gl_month - 1 - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 4:

                        if glacct_list.last_yr[gl_month - 1] == None:
                            glacct_list.last_yr[gl_month - 1] = 0


                        cell_val = trim(to_string(- glacct_list.last_yr[gl_month - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 5:
                        ytd_bal =  to_decimal("0")
                        for curr_i in range(1,gl_month + 1) :

                            if glacct_list.last_yr[curr_i - 1] == None:
                                glacct_list.last_yr[curr_i - 1] = 0


                            ytd_bal =  to_decimal(ytd_bal) - to_decimal(glacct_list.last_yr[curr_i - 1])
                        cell_val = trim(to_string(ytd_bal, "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 6:

                        if glacct_list.budget[gl_month - 1] == None:
                            glacct_list.budget[gl_month - 1] = 0


                        cell_val = trim(to_string(- glacct_list.budget[gl_month - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 7:
                        ytd_bal =  to_decimal("0")
                        for curr_i in range(1,gl_month + 1) :

                            if glacct_list.budget[curr_i - 1] == None:
                                glacct_list.budget[curr_i - 1] = 0


                            ytd_bal =  to_decimal(ytd_bal) - to_decimal(glacct_list.budget[curr_i - 1])
                        cell_val = trim(to_string(ytd_bal, "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 8:

                        if gl_month == 1:

                            if glacct_list.ly_budget[11] == None:
                                glacct_list.ly_budget[11] = 0


                            cell_val = trim(to_string(- glacct_list.ly_budget[11], "->>>>>>>>>>>>>>>>9.99"))
                        else:

                            if glacct_list.budget[gl_month - 1 - 1] == None:
                                glacct_list.budget[gl_month - 1 - 1] = 0


                            cell_val = trim(to_string(- glacct_list.budget[gl_month - 1 - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 9:

                        if glacct_list.ly_budget[gl_month - 1] == None:
                            glacct_list.ly_budget[gl_month - 1] = 0


                        cell_val = trim(to_string(- glacct_list.ly_budget[gl_month - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 10:
                        ytd_bal =  to_decimal("0")
                        for curr_i in range(1,gl_month + 1) :

                            if glacct_list.ly_budget[curr_i - 1] == None:
                                glacct_list.ly_budget[curr_i - 1] = 0


                            ytd_bal =  to_decimal(ytd_bal) - to_decimal(glacct_list.ly_budget[curr_i - 1])
                        cell_val = trim(to_string(ytd_bal, "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 11:
                        cell_val = trim(to_string(- glacct_list.actual[0], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 12:
                        cell_val = trim(to_string(- glacct_list.actual[1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 13:
                        cell_val = trim(to_string(- glacct_list.actual[2], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 14:
                        cell_val = trim(to_string(- glacct_list.actual[3], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 15:
                        cell_val = trim(to_string(- glacct_list.actual[4], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 16:
                        cell_val = trim(to_string(- glacct_list.actual[5], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 17:
                        cell_val = trim(to_string(- glacct_list.actual[6], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 18:
                        cell_val = trim(to_string(- glacct_list.actual[7], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 19:
                        cell_val = trim(to_string(- glacct_list.actual[8], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 20:
                        cell_val = trim(to_string(- glacct_list.actual[9], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 21:
                        cell_val = trim(to_string(- glacct_list.actual[10], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 22:
                        cell_val = trim(to_string(- glacct_list.actual[11], "->>>>>>>>>>>>>>>>9.99"))

                    elif found_flag:

                        if t_parameters.vtype == 1:

                            if glacct_list.actual[gl_month - 1] == None:
                                glacct_list.actual[gl_month - 1] = 0


                            cell_val = trim(to_string(glacct_list.actual[gl_month - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 2:
                        ytd_bal =  to_decimal("0")
                        for curr_i in range(1,gl_month + 1) :

                            if glacct_list.actual[curr_i - 1] == None:
                                glacct_list.actual[curr_i - 1] = 0


                            ytd_bal =  to_decimal(ytd_bal) + to_decimal(glacct_list.actual[curr_i - 1])
                        cell_val = trim(to_string(ytd_bal, "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 3:

                        if gl_month == 1:

                            if glacct_list.last_yr[11] == None:
                                glacct_list.last_yr[11] = 0


                            cell_val = trim(to_string(glacct_list.last_yr[11], "->>>>>>>>>>>>>>>>9.99"))
                        else:

                            if glacct_list.actual[gl_month - 1 - 1] == None:
                                glacct_list.actual[gl_month - 1 - 1] = 0


                            cell_val = trim(to_string(glacct_list.actual[gl_month - 1 - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 4:

                        if glacct_list.last_yr[gl_month - 1] == None:
                            glacct_list.last_yr[gl_month - 1] = 0


                        cell_val = trim(to_string(glacct_list.last_yr[gl_month - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 5:
                        ytd_bal =  to_decimal("0")
                        for curr_i in range(1,gl_month + 1) :

                            if glacct_list.last_yr[curr_i - 1] == None:
                                glacct_list.last_yr[curr_i - 1] = 0


                            ytd_bal =  to_decimal(ytd_bal) + to_decimal(glacct_list.last_yr[curr_i - 1])
                        cell_val = trim(to_string(ytd_bal, "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 6:

                        if glacct_list.budget[gl_month - 1] == None:
                            glacct_list.budget[gl_month - 1] = 0


                        cell_val = trim(to_string(glacct_list.budget[gl_month - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 7:
                        ytd_bal =  to_decimal("0")
                        for curr_i in range(1,gl_month + 1) :

                            if glacct_list.budget[curr_i - 1] == None:
                                glacct_list.budget[curr_i - 1] = 0


                            ytd_bal =  to_decimal(ytd_bal) + to_decimal(glacct_list.budget[curr_i - 1])
                        cell_val = trim(to_string(ytd_bal, "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 8:

                        if gl_month == 1:

                            if glacct_list.ly_budget[11] == None:
                                glacct_list.ly_budget[11] = 0


                            cell_val = trim(to_string(glacct_list.ly_budget[11], "->>>>>>>>>>>>>>>>9.99"))
                        else:

                            if glacct_list.budget[gl_month - 1 - 1] == None:
                                glacct_list.budget[gl_month - 1 - 1] = 0


                            cell_val = trim(to_string(glacct_list.budget[gl_month - 1 - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 9:

                        if glacct_list.ly_budget[gl_month - 1] == None:
                            glacct_list.ly_budget[gl_month - 1] = 0


                        cell_val = trim(to_string(glacct_list.ly_budget[gl_month - 1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 10:
                        ytd_bal =  to_decimal("0")
                        for curr_i in range(1,gl_month + 1) :

                            if glacct_list.ly_budget[curr_i - 1] == None:
                                glacct_list.ly_budget[curr_i - 1] = 0


                            ytd_bal =  to_decimal(ytd_bal) + to_decimal(glacct_list.ly_budget[curr_i - 1])
                        cell_val = trim(to_string(ytd_bal, "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 11:
                        cell_val = trim(to_string(glacct_list.actual[0], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 12:
                        cell_val = trim(to_string(glacct_list.actual[1], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 13:
                        cell_val = trim(to_string(glacct_list.actual[2], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 14:
                        cell_val = trim(to_string(glacct_list.actual[3], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 15:
                        cell_val = trim(to_string(glacct_list.actual[4], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 16:
                        cell_val = trim(to_string(glacct_list.actual[5], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 17:
                        cell_val = trim(to_string(glacct_list.actual[6], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 18:
                        cell_val = trim(to_string(glacct_list.actual[7], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 19:
                        cell_val = trim(to_string(glacct_list.actual[8], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 20:
                        cell_val = trim(to_string(glacct_list.actual[9], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 21:
                        cell_val = trim(to_string(glacct_list.actual[10], "->>>>>>>>>>>>>>>>9.99"))
                    elif t_parameters.vtype == 22:
                        cell_val = trim(to_string(glacct_list.actual[11], "->>>>>>>>>>>>>>>>9.99"))

                    if found_flag and (t_parameters.vtype == 25 or t_parameters.vtype == 26):

                        temp_list = query(temp_list_list, filters=(lambda temp_list: temp_list.vstring == t_parameters.vstring), first=True)

                        if temp_list:

                            if t_parameters.vtype == 25:
                                cell_val = trim(to_string(temp_list.debit, "->>>>>>>>>>>>>>>>9.99"))

                            if t_parameters.vtype == 26:
                                cell_val = trim(to_string(temp_list.credit, "->>>>>>>>>>>>>>>>9.99"))

                    if found_flag:

                        if glacct_list.acc_type == 1 or glacct_list.acc_type == 4:
                            val_sign = - 1
                        else:
                            val_sign = 1

                        if t_parameters.vtype >= 31 and t_parameters.vtype <= 42:
                            j = 0
                            for i in range(31,42 + 1) :
                                j = j + 1

                                if t_parameters.vtype == i:
                                    cell_val = trim(to_string(val_sign * glacct_list.budget[j - 1] , "->>>>>>>>>>>>>>>>9.99"))

                        if t_parameters.vtype >= 43 and t_parameters.vtype <= 54:
                            j = 0
                            for i in range(43,54 + 1) :
                                j = j + 1

                                if t_parameters.vtype == i:
                                    cell_val = trim(to_string(val_sign * glacct_list.last_yr[j - 1] , "->>>>>>>>>>>>9.99"))

                        if t_parameters.vtype >= 55 and t_parameters.vtype <= 66:
                            j = 0
                            for i in range(55,66 + 1) :
                                j = j + 1

                                if t_parameters.vtype == i:
                                    cell_val = trim(to_string(val_sign * glacct_list.debit[j - 1] , "->>>>>>>>>>>>>>>>9.99"))

                        if t_parameters.vtype >= 67 and t_parameters.vtype <= 78:
                            j = 0
                            for i in range(67,78 + 1) :
                                j = j + 1

                                if t_parameters.vtype == i:
                                    cell_val = trim(to_string(val_sign * glacct_list.ly_budget[j - 1] , "->>>>>>>>>>>>>>>>9.99"))

                        if t_parameters.vtype == 27:
                            diff =  to_decimal(glacct_list.actual[gl_month - 1] - glacct_list.budget[gl_month - 1])
                            cell_val = trim(to_string(diff, "->>>>>>>>>>>>>>>>9.99"))

                        if t_parameters.vtype == 28:

                            if gl_month == 1:
                                lmdiff =  to_decimal(glacct_list.last_yr[11] - glacct_list.ly_budget[11])
                            else:
                                lmdiff =  to_decimal(glacct_list.actual[gl_month - 1 - 1] - glacct_list.budget[gl_month - 1 - 1])
                            cell_val = trim(to_string(lmdiff, "->>>>>>>>>>>>>>>>9.99"))

                    if t_parameters.vtype == 23:
                        mtd_betrag =  to_decimal("0")
                        ytd_betrag =  to_decimal("0")

                        t_artikel = query(t_artikel_list, filters=(lambda t_artikel: t_artikel.artnr == to_int(substring(t_parameters.vstring, 2)) and t_artikel.departement == to_int(substring(t_parameters.vstring, 0, 2))), first=True)

                        if t_artikel:
                            for curr_date in date_range(date_mdy(01, 01, get_year(to_date)),to_date) :
                                serv =  to_decimal("0")
                                vat =  to_decimal("0")
                                n_betrag =  to_decimal("0")

                                t_umsz = query(t_umsz_list, filters=(lambda t_umsz: t_umsz.curr_date == curr_date and t_umsz.artnr == to_int(substring(t_parameters.vstring, 2)) and t_umsz.dept == to_int(substring(t_parameters.vstring, 0, 2))), first=True)

                                if t_umsz:
                                    n_betrag =  to_decimal(t_umsz.betrag)

                                if curr_date >= date_mdy(get_month(to_date) , 01, get_year(to_date)) and curr_date <= to_date:
                                    mtd_betrag =  to_decimal(mtd_betrag) + to_decimal(n_betrag)
                                ytd_betrag =  to_decimal(ytd_betrag) + to_decimal(n_betrag)
                        cell_val = to_string(mtd_betrag)

                    if t_parameters.vtype == 24:
                        cell_val = to_string(ytd_betrag)

                    if cell_val != "":

                        if cell_val.lower()  == ("0").lower() :
                            else:
                            else:
                        OUTPUT STREAM s1 CLOSE
                    mess_result = "Successfully generate data"
                    OS_COMMAND SILENT VALUE ("php /usr1/vhp/php-script/write-sheet.php /usr1/vhp/tmp/output_" + htl_no + ".txt " + link)
                    OS_DELETE VALUE ("/usr1/vhp/tmp/output_" + htl_no + ".txt")

    return generate_output()