#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.glacct_cashflowbl import glacct_cashflowbl
from functions.calc_servvat import calc_servvat
from models import Parameters, Gl_accthis, Gl_acct, Artikel, Exrate, Htparam, Gl_jouhdr, Gl_journal, Waehrung, Genstat, Segmentstat, Umsatz, Budget

def gl_parxls1_2bl(briefnr:int, gl_year:int, from_date:date, to_date:date, foreign_flag:bool):

    prepare_cache ([Artikel, Exrate, Htparam, Gl_jouhdr, Gl_journal, Waehrung, Genstat, Segmentstat, Umsatz, Budget])

    combo_pf_file1 = ""
    combo_pf_file2 = ""
    t_parameters_list = []
    t_gl_accthis_list = []
    t_gl_acct_list = []
    t_artikel_list = []
    t_umsz_list = []
    temp_list_list = []
    t_list_list = []
    w1_list = []
    curr_date:date = None
    curr_i:int = 0
    serv:Decimal = to_decimal("0.0")
    vat:Decimal = to_decimal("0.0")
    fact:Decimal = to_decimal("0.0")
    n_betrag:Decimal = to_decimal("0.0")
    credit:Decimal = to_decimal("0.0")
    debit:Decimal = to_decimal("0.0")
    frate:Decimal = 1
    price_decimal:int = 0
    from_year:Decimal = to_decimal("0.0")
    to_year:Decimal = to_decimal("0.0")
    cash_flow:bool = False
    prev_str:string = ""
    done_segment:bool = False
    datum1:date = None
    jan1:date = None
    ljan1:date = None
    lfrom_date:date = None
    lto_date:date = None
    do_it:bool = True
    actual_exrate:List[Decimal] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    budget_exrate:List[Decimal] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    lyear_exrate:List[Decimal] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    blyear_exrate:List[Decimal] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    bnyear_exrate:List[Decimal] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    parameters = gl_accthis = gl_acct = artikel = exrate = htparam = gl_jouhdr = gl_journal = waehrung = genstat = segmentstat = umsatz = budget = None

    coa_list = t_list = t_parameters = t_gl_accthis = t_gl_acct = t_artikel = t_umsz = g_list = temp_list = w1 = buff_exrate = w_rev = w_pers = w_room = w4 = None

    coa_list_list, Coa_list = create_model("Coa_list", {"fibu":string})
    t_list_list, T_list = create_model("T_list", {"cf":int, "fibukonto":string, "debit":Decimal, "credit":Decimal, "debit_lsyear":Decimal, "credit_lsyear":Decimal, "debit_lsmonth":Decimal, "credit_lsmonth":Decimal, "balance":Decimal, "ly_balance":Decimal, "pm_balance":Decimal})
    t_parameters_list, T_parameters = create_model_like(Parameters)
    t_gl_accthis_list, T_gl_accthis = create_model_like(Gl_accthis)
    t_gl_acct_list, T_gl_acct = create_model_like(Gl_acct)
    t_artikel_list, T_artikel = create_model_like(Artikel)
    t_umsz_list, T_umsz = create_model("T_umsz", {"curr_date":date, "artnr":int, "dept":int, "fact":Decimal, "betrag":Decimal})
    g_list_list, G_list = create_model("G_list", {"datum":date, "grecid":int, "fibu":string}, {"datum": None})
    temp_list_list, Temp_list = create_model("Temp_list", {"vstring":string, "debit":Decimal, "credit":Decimal})
    w1_list, W1 = create_model("W1", {"nr":int, "varname":string, "main_code":int, "s_artnr":string, "artnr":int, "dept":int, "grpflag":int, "done":bool, "bezeich":string, "int_flag":bool, "tday":Decimal, "tday_serv":Decimal, "tday_tax":Decimal, "mtd_serv":Decimal, "mtd_tax":Decimal, "ytd_serv":Decimal, "ytd_tax":Decimal, "yesterday":Decimal, "saldo":Decimal, "lastmon":Decimal, "pmtd_serv":Decimal, "pmtd_tax":Decimal, "lmtd_serv":Decimal, "lmtd_tax":Decimal, "lastyr":Decimal, "lytoday":Decimal, "ytd_saldo":Decimal, "lytd_saldo":Decimal, "year_saldo":[Decimal,12], "mon_saldo":[Decimal,31], "mon_budget":[Decimal,31], "mon_lmtd":[Decimal,31], "tbudget":Decimal, "budget":Decimal, "lm_budget":Decimal, "lm_today":Decimal, "lm_today_serv":Decimal, "lm_today_tax":Decimal, "lm_mtd":Decimal, "lm_ytd":Decimal, "ly_budget":Decimal, "ny_budget":Decimal, "ytd_budget":Decimal, "nytd_budget":Decimal, "nmtd_budget":Decimal, "lytd_budget":Decimal})

    Buff_exrate = create_buffer("Buff_exrate",Exrate)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal combo_pf_file1, combo_pf_file2, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, temp_list_list, t_list_list, w1_list, curr_date, curr_i, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, from_year, to_year, cash_flow, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, htparam, gl_jouhdr, gl_journal, waehrung, genstat, segmentstat, umsatz, budget
        nonlocal briefnr, gl_year, from_date, to_date, foreign_flag
        nonlocal buff_exrate


        nonlocal coa_list, t_list, t_parameters, t_gl_accthis, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, w1, buff_exrate, w_rev, w_pers, w_room, w4
        nonlocal coa_list_list, t_list_list, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, w1_list

        return {"combo_pf_file1": combo_pf_file1, "combo_pf_file2": combo_pf_file2, "t-parameters": t_parameters_list, "t-gl-accthis": t_gl_accthis_list, "t-gl-acct": t_gl_acct_list, "t-artikel": t_artikel_list, "t-umsz": t_umsz_list, "temp-list": temp_list_list, "t-list": t_list_list, "w1": w1_list}

    def fill_exrate():

        nonlocal combo_pf_file1, combo_pf_file2, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, temp_list_list, t_list_list, w1_list, curr_i, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, from_year, to_year, cash_flow, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, htparam, gl_jouhdr, gl_journal, waehrung, genstat, segmentstat, umsatz, budget
        nonlocal briefnr, gl_year, from_date, to_date, foreign_flag
        nonlocal buff_exrate


        nonlocal coa_list, t_list, t_parameters, t_gl_accthis, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, w1, buff_exrate, w_rev, w_pers, w_room, w4
        nonlocal coa_list_list, t_list_list, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, w1_list

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


        for ind in range(1,12 + 1) :

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

            exrate = get_cache (Exrate, {"artnr": [(eq, 99999)],"datum": [(eq, curr_date)]})

            if exrate:
                actual_exrate[ind - 1] = exrate.betrag

            exrate = get_cache (Exrate, {"artnr": [(eq, 99999)],"datum": [(eq, lyear_date)]})

            if exrate:
                lyear_exrate[ind - 1] = exrate.betrag

            exrate = get_cache (Exrate, {"artnr": [(eq, 99998)],"datum": [(eq, curr_date)]})

            if exrate:
                budget_exrate[ind - 1] = exrate.betrag

            exrate = get_cache (Exrate, {"artnr": [(eq, 99998)],"datum": [(eq, lyear_date)]})

            if exrate:
                blyear_exrate[ind - 1] = exrate.betrag

            exrate = get_cache (Exrate, {"artnr": [(eq, 99998)],"datum": [(eq, nyear_date)]})

            if exrate:
                bnyear_exrate[ind - 1] = exrate.betrag


    def calc_cf():

        nonlocal combo_pf_file1, combo_pf_file2, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, temp_list_list, t_list_list, w1_list, curr_date, curr_i, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, from_year, to_year, cash_flow, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, htparam, gl_jouhdr, gl_journal, waehrung, genstat, segmentstat, umsatz, budget
        nonlocal briefnr, gl_year, from_date, to_date, foreign_flag
        nonlocal buff_exrate


        nonlocal coa_list, t_list, t_parameters, t_gl_accthis, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, w1, buff_exrate, w_rev, w_pers, w_room, w4
        nonlocal coa_list_list, t_list_list, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, w1_list

        from_lsyr:date = None
        to_lsyr:date = None
        pfrom_date:date = None
        pto_date:date = None

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
        t_list_list = get_output(glacct_cashflowbl(from_date, to_date, from_lsyr, to_lsyr, pfrom_date, pto_date, coa_list_list))


    def find_exrate(curr_date:date):

        nonlocal combo_pf_file1, combo_pf_file2, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, temp_list_list, t_list_list, w1_list, curr_i, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, from_year, to_year, cash_flow, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, htparam, gl_jouhdr, gl_journal, waehrung, genstat, segmentstat, umsatz, budget
        nonlocal briefnr, gl_year, from_date, to_date, foreign_flag
        nonlocal buff_exrate


        nonlocal coa_list, t_list, t_parameters, t_gl_accthis, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, w1, buff_exrate, w_rev, w_pers, w_room, w4
        nonlocal coa_list_list, t_list_list, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, w1_list

        foreign_nr:int = 0

        if foreign_flag:

            buff_exrate = get_cache (Exrate, {"artnr": [(eq, 99999)],"datum": [(eq, curr_date)]})

            if buff_exrate:

                return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        if htparam.fchar != "":

            waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

            if waehrung:
                foreign_nr = waehrung.waehrungsnr

        if foreign_nr != 0:

            buff_exrate = get_cache (Exrate, {"artnr": [(eq, foreign_nr)],"datum": [(eq, curr_date)]})
        else:

            buff_exrate = get_cache (Exrate, {"datum": [(eq, curr_date)]})


    def fill_segment():

        nonlocal combo_pf_file1, combo_pf_file2, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, temp_list_list, t_list_list, w1_list, curr_date, curr_i, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, from_year, to_year, cash_flow, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, htparam, gl_jouhdr, gl_journal, waehrung, genstat, segmentstat, umsatz, budget
        nonlocal briefnr, gl_year, from_date, to_date, foreign_flag
        nonlocal buff_exrate


        nonlocal coa_list, t_list, t_parameters, t_gl_accthis, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, w1, buff_exrate, w_rev, w_pers, w_room, w4
        nonlocal coa_list_list, t_list_list, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, w1_list

        s_param = None
        prev_param:string = ""
        ytd_flag:bool = False
        lytd_flag:bool = False
        lmtd_flag:bool = False
        ytd_budget_flag:bool = False
        mtd_budget_flag:bool = False
        nr:int = 0
        segm:int = 0
        mm:int = 0
        prev_segm:int = 0
        S_param =  create_buffer("S_param",Parameters)
        W_rev = W1
        w_rev_list = w1_list
        W_pers = W1
        w_pers_list = w1_list
        W_room = W1
        w_room_list = w1_list

        for s_param in db_session.query(S_param).filter(
                 (S_param.progname == ("GL-macro").lower()) & (S_param.section == to_string(briefnr)) & (num_entries(S_param.vstring, ":") == 1) & (num_entries(S_param.varname, "-") == 3) & (entry(2, S_param.varname, "-") == ("FO").lower()) & (substring(S_param.vstring, 0, 4) == ("segm").lower())).order_by(S_param.varname).all():

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

                w1 = query(w1_list, filters=(lambda w1: w1.nr == nr and w1.artnr == segm), first=True)

                if not w1:
                    w1 = W1()
                    w1_list.append(w1)

                    w1.nr = nr
                    w1.artnr = segm


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

        for genstat in db_session.query(Genstat).filter(
                 (Genstat.datum >= datum1) & (Genstat.datum <= to_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():

            if prev_segm != genstat.segmentcode:
                prev_segm = genstat.segmentcode

                w_rev = query(w_rev_list, filters=(lambda w_rev: w_rev.nr == 1 and w_rev.artnr == genstat.segmentcode), first=True)

                w_pers = query(w_pers_list, filters=(lambda w_pers: w_pers.nr == 2 and w_pers.artnr == genstat.segmentcode), first=True)

                w_room = query(w_room_list, filters=(lambda w_room: w_room.nr == 3 and w_room.artnr == genstat.segmentcode), first=True)

            if genstat.datum == to_date:

                if w_rev:
                    w_rev.tday =  to_decimal(w_rev.tday) + to_decimal(genstat.logis)

                if w_pers:
                    w_pers.tday =  to_decimal(w_pers.tday) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if w_room:
                    w_room.tday =  to_decimal(w_room.tday) + to_decimal("1")

            if get_month(genstat.datum) == mm:

                if w_rev:
                    w_rev.saldo =  to_decimal(w_rev.saldo) + to_decimal(genstat.logis)

                if w_pers:
                    w_pers.saldo =  to_decimal(w_pers.saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if w_room:
                    w_room.saldo =  to_decimal(w_room.saldo) + to_decimal("1")

            if w_rev:
                w_rev.ytd_saldo =  to_decimal(w_rev.ytd_saldo) + to_decimal(genstat.logis)

            if w_pers:
                w_pers.ytd_saldo =  to_decimal(w_pers.ytd_saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

            if w_room:
                w_room.ytd_saldo =  to_decimal(w_room.ytd_saldo) + to_decimal("1")

        if lmtd_flag or lytd_flag:

            if lytd_flag:
                datum1 = ljan1
            else:
                datum1 = lfrom_date
            mm = get_month(lto_date)
            prev_segm = 0

            for genstat in db_session.query(Genstat).filter(
                     (Genstat.datum >= datum1) & (Genstat.datum <= lto_date) & (Genstat.resstatus != 13) & (Genstat.segmentcode != 0) & (Genstat.nationnr != 0) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.segmentcode).all():

                if prev_segm != genstat.segmentcode:
                    prev_segm = genstat.segmentcode

                    w_rev = query(w_rev_list, filters=(lambda w_rev: w_rev.nr == 1 and w_rev.artnr == genstat.segmentcode), first=True)

                    w_pers = query(w_pers_list, filters=(lambda w_pers: w_pers.nr == 2 and w_pers.artnr == genstat.segmentcode), first=True)

                    w_room = query(w_room_list, filters=(lambda w_room: w_room.nr == 3 and w_room.artnr == genstat.segmentcode), first=True)

                if genstat.datum == to_date:

                    if w_rev:
                        w_rev.lytoday =  to_decimal(w_rev.lytoday) + to_decimal(genstat.logis)

                    if w_pers:
                        w_pers.lytoday =  to_decimal(w_pers.lytoday) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                    if w_room:
                        w_room.lytoday =  to_decimal(w_room.lytoday) + to_decimal("1")

                if get_month(genstat.datum) == mm:

                    if w_rev:
                        w_rev.lastyr =  to_decimal(w_rev.lastyr) + to_decimal(genstat.logis)

                    if w_pers:
                        w_pers.lastyr =  to_decimal(w_pers.lastyr) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                    if w_room:
                        w_room.lastyr =  to_decimal(w_room.lastyr) + to_decimal("1")

                if w_rev:
                    w_rev.lytd_saldo =  to_decimal(w_rev.lytd_saldo) + to_decimal(genstat.logis)

                if w_pers:
                    w_pers.lytd_saldo =  to_decimal(w_pers.lytd_saldo) + to_decimal(genstat.erwachs) + to_decimal(genstat.kind1) + to_decimal(genstat.kind2) + to_decimal(genstat.gratis)

                if w_room:
                    w_room.lytd_saldo =  to_decimal(w_room.lytd_saldo) + to_decimal("1")

        if mtd_budget_flag or ytd_budget_flag:

            if ytd_budget_flag:
                datum1 = jan1
            else:
                datum1 = from_date
            mm = get_month(to_date)
            prev_segm = 0

            for segmentstat in db_session.query(Segmentstat).filter(
                     (Segmentstat.datum >= datum1) & (Segmentstat.datum <= to_date)).order_by(Segmentstat.segmentcode).all():

                if prev_segm != segmentstat.segmentcode:
                    prev_segm = segmentstat.segmentcode

                    w_rev = query(w_rev_list, filters=(lambda w_rev: w_rev.nr == 1 and w_rev.artnr == segmentstat.segmentcode), first=True)

                    w_pers = query(w_pers_list, filters=(lambda w_pers: w_pers.nr == 2 and w_pers.artnr == segmentstat.segmentcode), first=True)

                    w_room = query(w_room_list, filters=(lambda w_room: w_room.nr == 3 and w_room.artnr == segmentstat.segmentcode), first=True)

                if segmentstat.datum == to_date:

                    if w_rev:
                        w_rev.tbudget =  to_decimal(w_rev.tbudget) + to_decimal(segmentstat.budlogis)

                    if w_pers:
                        w_pers.tbudget =  to_decimal(w_pers.tbudget) + to_decimal(segmentstat.budpersanz)

                    if w_room:
                        w_room.tbudget =  to_decimal(w_room.tbudget) + to_decimal("1")

                if get_month(segmentstat.datum) == mm:

                    if w_rev:
                        w_rev.budget =  to_decimal(w_rev.budget) + to_decimal(segmentstat.budlogis)

                    if w_pers:
                        w_pers.budget =  to_decimal(w_pers.budget) + to_decimal(segmentstat.budpersanz)

                    if w_room:
                        w_room.budget =  to_decimal(w_room.budget) + to_decimal("1")

                if w_rev:
                    w_rev.ytd_budget =  to_decimal(w_rev.ytd_budget) + to_decimal(segmentstat.budlogis)

                if w_pers:
                    w_pers.ytd_budget =  to_decimal(w_pers.ytd_budget) + to_decimal(segmentstat.budpersanz)

                if w_room:
                    w_room.ytd_budget =  to_decimal(w_room.ytd_budget) + to_decimal("1")


    def fill_revenue():

        nonlocal combo_pf_file1, combo_pf_file2, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, temp_list_list, t_list_list, w1_list, curr_date, curr_i, serv, vat, fact, n_betrag, credit, debit, frate, price_decimal, from_year, to_year, cash_flow, prev_str, done_segment, datum1, jan1, ljan1, lfrom_date, lto_date, do_it, actual_exrate, budget_exrate, lyear_exrate, blyear_exrate, bnyear_exrate, parameters, gl_accthis, gl_acct, artikel, exrate, htparam, gl_jouhdr, gl_journal, waehrung, genstat, segmentstat, umsatz, budget
        nonlocal briefnr, gl_year, from_date, to_date, foreign_flag
        nonlocal buff_exrate


        nonlocal coa_list, t_list, t_parameters, t_gl_accthis, t_gl_acct, t_artikel, t_umsz, g_list, temp_list, w1, buff_exrate, w_rev, w_pers, w_room, w4
        nonlocal coa_list_list, t_list_list, t_parameters_list, t_gl_accthis_list, t_gl_acct_list, t_artikel_list, t_umsz_list, g_list_list, temp_list_list, w1_list

        s_param = None
        prev_param:string = ""
        ytd_flag:bool = False
        lytd_flag:bool = False
        lmtd_flag:bool = False
        ytd_budget_flag:bool = False
        mtd_budget_flag:bool = False
        mm:int = 0
        S_param =  create_buffer("S_param",Parameters)
        W4 = W1
        w4_list = w1_list

        for s_param in db_session.query(S_param).filter(
                 (S_param.progname == ("GL-macro").lower()) & (S_param.section == to_string(briefnr)) & (num_entries(S_param.vstring, ":") == 1) & (num_entries(S_param.varname, "-") == 3) & (entry(2, S_param.varname, "-") == ("REV").lower())).order_by(S_param.varname).all():

            if prev_param != s_param.varname:
                prev_param = s_param.varname

                w1 = query(w1_list, filters=(lambda w1: w1.nr == 4 and w1.s_artnr == s_param.vstring), first=True)

                if not w1:
                    w1 = W1()
                    w1_list.append(w1)

                    w1.nr = 4
                    w1.s_artnr = s_param.vstring


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

        for w1 in query(w1_list, filters=(lambda w1: w1.nr == 4), sort_by=[("s_artnr",False)]):

            artikel = get_cache (Artikel, {"artnr": [(eq, to_int(substring(w1.s_artnr, 2)))],"departement": [(eq, to_int(substring(w1.s_artnr, 0, 2)))]})

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
                        w1.tday =  to_decimal(w1.tday) + to_decimal(n_betrag)

                    if get_month(umsatz.datum) == mm:
                        w1.saldo =  to_decimal(w1.saldo) + to_decimal(n_betrag)
                    w1.ytd_saldo =  to_decimal(w1.ytd_saldo) + to_decimal(n_betrag)

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
                            w1.lastyr =  to_decimal(w1.lastyr) + to_decimal(n_betrag)
                        w1.lytd_saldo =  to_decimal(w1.lytd_saldo) + to_decimal(n_betrag)

                if mtd_budget_flag or ytd_budget_flag:

                    if ytd_budget_flag:
                        datum1 = jan1
                    else:
                        datum1 = from_date
                    mm = get_month(to_date)

                    for budget in db_session.query(Budget).filter(
                             (Budget.artnr == artikel.artnr) & (Budget.departement == artikel.departement) & (Budget.datum >= datum1) & (Budget.datum <= to_date)).order_by(Budget._recid).all():

                        if budget.datum == to_date:
                            w1.tbudget =  to_decimal(w1.tbudget) + to_decimal(budget.betrag)

                        if get_month(budget.datum) == mm:
                            w1.budget =  to_decimal(w1.budget) + to_decimal(budget.betrag)
                        w1.ytd_budget =  to_decimal(w1.ytd_budget) + to_decimal(budget.betrag)

    if (get_month(to_date) != 2) or (get_day(to_date) != 29):
        lto_date = date_mdy(get_month(to_date) , get_day(to_date) , get_year(to_date) - timedelta(days=1))
    else:
        lto_date = date_mdy(get_month(to_date) , 28, get_year(to_date) - timedelta(days=1))
    jan1 = date_mdy(1, 1, get_year(to_date))
    ljan1 = date_mdy(1, 1, get_year(to_date) - timedelta(days=1))
    lfrom_date = date_mdy(get_month(to_date) , 1, get_year(to_date) - timedelta(days=1))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = 2

    htparam = get_cache (Htparam, {"paramnr": [(eq, 339)]})
    combo_pf_file1 = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 340)]})
    combo_pf_file2 = htparam.fchar
    g_list_list.clear()

    parameters = db_session.query(Parameters).filter(
             (Parameters.progname == ("GL-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (num_entries(Parameters.varname, "-") == 3) & (entry(2, Parameters.varname, "-") == ("CF").lower())).first()

    if parameters:
        cash_flow = True

    parameters = db_session.query(Parameters).filter(
             (Parameters.progname == ("GL-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (num_entries(Parameters.varname, "-") == 3) & (entry(2, Parameters.varname, "-") == ("REV").lower())).first()

    if parameters:
        fill_revenue()

    parameters = db_session.query(Parameters).filter(
             (Parameters.progname == ("GL-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (matches((Parameters.vstring,"*segmrev*")) | (matches(Parameters.vstring,"*segmpers*")) | (matches(Parameters.vstring,"*segmroom*")))).first()

    if parameters:
        fill_segment()

    if cash_flow:

        for parameters in db_session.query(Parameters).filter(
                 (Parameters.progname == ("GL-Macro").lower()) & (Parameters.section == to_string(briefnr)) & (num_entries(Parameters.varname, "-") == 3) & (entry(2, Parameters.varname, "-") == ("CF").lower())).order_by(Parameters.varname).all():
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, entry(0, t_parameters.vstring, ":"))]})

            if gl_acct:

                coa_list = query(coa_list_list, filters=(lambda coa_list: coa_list.fibu == gl_acct.fibukonto), first=True)

                if not coa_list:
                    coa_list = Coa_list()
                    coa_list_list.append(coa_list)

                    coa_list.fibu = gl_acct.fibukonto


        calc_cf()

    for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
             (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum).all():

        for gl_journal in db_session.query(Gl_journal).filter(
                 (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal.fibukonto).all():
            g_list = G_list()
            g_list_list.append(g_list)

            g_list.datum = gl_jouhdr.datum
            g_list.grecid = gl_journal._recid
            g_list.fibu = gl_journal.fibukonto

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("GL-macro").lower()) & (Parameters.section == to_string(briefnr)) & (matches(Parameters.varname,"*combo*"))).order_by(Parameters.varname).all():

        if prev_str != parameters.varname:
            prev_str = parameters.varname
            t_parameters = T_parameters()
            t_parameters_list.append(t_parameters)

            buffer_copy(parameters, t_parameters)
    prev_str = ""

    for parameters in db_session.query(Parameters).filter(
             (Parameters.progname == ("GL-macro").lower()) & (Parameters.section == to_string(briefnr)) & (num_entries(PARAMETERS.vstring, ":") == 1) & (num_entries(Parameters.varname, "-") == 2)).order_by(Parameters.varname).all():

        if prev_str != parameters.varname:
            prev_str = parameters.varname

            if parameters.vstring.lower()  == ("$IN-FOREIGN").lower() :
                t_parameters = T_parameters()
                t_parameters_list.append(t_parameters)

                buffer_copy(parameters, t_parameters)
                fill_exrate()

            if substring(parameters.vstring, 0, 1) == ("$").lower() :
                t_parameters = T_parameters()
                t_parameters_list.append(t_parameters)

                buffer_copy(parameters, t_parameters)

            if substring(parameters.vstring, 0, 1) != ("$").lower() :
                t_parameters = T_parameters()
                t_parameters_list.append(t_parameters)

                buffer_copy(parameters, t_parameters)
                debit =  to_decimal("0")
                credit =  to_decimal("0")

                gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, parameters.vstring)],"year": [(eq, gl_year)]})

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

                gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, parameters.vstring)]})

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

                            gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                            if gl_journal:
                                debit =  to_decimal(debit) + to_decimal(gl_journal.debit)


                            credit =  to_decimal(credit) + to_decimal(gl_journal.credit)
                    temp_list = Temp_list()
                    temp_list_list.append(temp_list)

                    temp_list.vstring = parameters.vstring
                    temp_list.debit =  to_decimal(debit)
                    temp_list.credit =  to_decimal(credit)

    return generate_output()