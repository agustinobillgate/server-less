#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 21/8/20225
# data tidak tampil semua
#-----------------------------------------
from functions.additional_functions import *
from functions.more_additional_functions import format_fixed_length, handling_negative
from sqlalchemy import func, literal, select, union_all
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import sessionmaker
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from functions.htpchar import htpchar
from models import Gl_acct, Gl_jouhdr, Gl_journal, Gl_jhdrhis, Gl_jourhis, Gl_department, Gl_main, Htparam, Gl_accthis

from functions import log_program as lp
from itertools import islice

import time
import traceback

def trialbalance_btn_go_cld_1bl(acct_type:int, from_fibu:string, to_fibu:string, sorttype:int, from_dept:int, from_date:date, to_date:date, close_month:int, close_date:date, pnl_acct:string, close_year:date, prev_month:int, show_longbal:bool, pbal_flag:bool, asremoteflag:bool):

    prepare_cache ([Gl_acct, Gl_jouhdr, Gl_journal, Gl_jhdrhis, Gl_jourhis, Gl_department, Gl_main, Htparam, Gl_accthis])

    output_list_data = []
    num_acctype:int = 0
    sales:Decimal = to_decimal("0.0")
    cost:Decimal = to_decimal("0.0")
    gop_credit:Decimal = to_decimal("0.0")
    gop_debit:Decimal = to_decimal("0.0")
    tot_diff:Decimal = to_decimal("0.0")
    curr_i:int = 0
    in_procedure:bool = False
    numsend:int = 30
    last_acct_close_priod:date = None
    t_from_date:date = None
    t_to_date:date = None
    t_strgrp:string = ""
    t_str:string = ""
    t_int:int = 0
    t_date:date = None
    from_datehis:date = None
    to_datehis:date = None
    readflag:int = 0
    coa_format:string = ""
    counter:int = 0
    lastprevmonthdate:date = None
    firstmonthdate:date = None
    tt_pbal2:Decimal = to_decimal("0.0")
    gl_acct = gl_jouhdr = gl_journal = gl_jhdrhis = gl_jourhis = gl_department = gl_main = htparam = gl_accthis = None

    output_list = output_listhis = result_list = t_res_list = t_res_listhis = g_list = g_listpre = g_listhis = None

    gl_accthis_map = {}
    gl_journal_map = {}
    gl_jourhis_map = {}
    gl_department_map = {}
    htparam_map = {}
    tmp_glist = {}

    tmp_gl_acct_actual = 0
    tmp_gl_acct_fibukonto = ""
    tmp_gl_acct_acc_type = 0

    output_list_data, Output_list = create_model("Output_list", {"gop_flag":bool, "nr":int, "str":string, "budget":Decimal, "proz":Decimal, "mark":bool, "ch":string, "ref_no":string, "begin_bal":string, "tot_debit":string, "tot_credit":string, "net_change":string, "ending_bal":string, "ytd_bal":string, "dept_nr":int, "dept_name":string, "is_show_depart":bool, "note":string})
    output_listhis_data, Output_listhis = create_model_like(Output_list)
    result_list_data, Result_list = create_model_like(Output_list)
    t_res_list_data, T_res_list = create_model("T_res_list", {"grp_nr":string, "acc_no":string, "t_date":date, "f1":string, "f2":string, "f3":int, "f4":int, "f5":int, "f6":int, "f7":int, "f8":int, "f9":int, "f10":int, "note":string})
    t_res_listhis_data, T_res_listhis = create_model_like(T_res_list)
    g_list_data, G_list = create_model("G_list", {"datum":date, "grecid":int, "fibu":string, "table_name":string}, {"datum": None})
    g_listpre_data, G_listpre = create_model_like(G_list)
    g_listhis_data, G_listhis = create_model_like(G_list)

    db_session = local_storage.db_session

    sql = text("""
    SELECT n.nspname AS full_name
    FROM pg_class c
    JOIN pg_namespace n ON n.oid = c.relnamespace
    WHERE c.oid = CAST(:tbl AS regclass) 
    LIMIT 1
    """)

    search_path = db_session.execute(sql, {"tbl": "htparam"}).scalar()

    localBind = db_session.get_bind()
    localEngine = localBind.engine if isinstance(localBind, Connection) else localBind

    # Oscar - start - create new session with same search_path for looping operation and stream result
    LoopingSessionOnly = sessionmaker(bind=localEngine)

    looping_session_only = LoopingSessionOnly()

    looping_session_only.execute(
        text(f"SET search_path TO {search_path}")
    )
    # Oscar - end - create new session with same search_path for looping operation and stream result

    def generate_output():
        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        return {"output-list": output_list_data}

    def format_fixed_length(text: str, length: int) -> str:
        if len(text) > length:
            return text[:length]   # trim
        else:
            return text.ljust(length)

    def get_bemerk(bemerk:string):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        n:int = 0
        s1:string = ""
        bemerk = replace_str(bemerk, chr_unicode(10) , " ")
        n = get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk

        return s1

    def lastday(d:date):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        lastmonthdate:date = None
        nextmonth:int = 0
        firstdate:date = None

        if get_month(d) == 12:
            lastmonthdate = date_mdy(1, 1, get_year(d) + 1) - timedelta(days=1)
        else:
            lastmonthdate = date_mdy(get_month(d) + 1, 1, get_year(d)) - timedelta(days=1)

        return lastmonthdate

    def prepare_cache_custom():
        nonlocal g_list_data, gl_journal_map, gl_jourhis_map, gl_department_map, gl_accthis_map, htparam_map

        rows = (
            db_session.query(Gl_department).join(Gl_acct, Gl_acct.deptnr == Gl_department.nr).distinct().all()
        )
        gl_department_map = {j.nr: j for j in rows}

        if get_year(from_date) != None:
            years_needed = {get_year(t_from_date), get_year(t_from_date) - 1, get_year(t_to_date), get_year(from_date)}
        else:
            years_needed = {get_year(t_from_date), get_year(t_from_date) - 1, get_year(t_to_date)}

        stmt = (
            select(
                Gl_accthis.fibukonto,
                Gl_accthis.year,
                Gl_accthis.actual,
            )
            .where(Gl_accthis.year.in_(years_needed))
        )
        rows = db_session.execute(stmt).all()
        gl_accthis_map = {(j[0], j[1]): j for j in rows}

        param_nr_group = {795,977}
        rows = (
            db_session.query(Htparam).filter(Htparam.paramnr.in_(param_nr_group)).all()
        )
        htparam_map = {j.paramnr: j for j in rows}

    # def create_glist():

    #     nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
    #     nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag

    #     nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
    #     nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

    #     # Oscar - Optimasi query
    #     # for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
    #     #          (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum).all():

    #     #     for gl_journal in db_session.query(Gl_journal).filter((Gl_journal.jnr == gl_jouhdr.jnr) & (Gl_journal.fibukonto >= (from_fibu).lower()) & (Gl_journal.fibukonto <= (to_fibu).lower())).order_by(Gl_journal.fibukonto).all():

    #     # datum = Gl_jouhdr.datum
    #     # _recid = Gl_journal._recid
    #     # fibukonto = Gl_journal.fibukonto
    #     stmt = (
    #         select(
    #             Gl_jouhdr.datum,
    #             Gl_journal._recid,
    #             Gl_journal.fibukonto,
    #         )
    #         .select_from(Gl_jouhdr)
    #         .join(
    #             Gl_journal,
    #             Gl_journal.jnr == Gl_jouhdr.jnr
    #         )
    #         .where(
    #             Gl_jouhdr.datum >= from_date,
    #             Gl_jouhdr.datum <= to_date,
    #             Gl_journal.fibukonto >= from_fibu,
    #             Gl_journal.fibukonto <= to_fibu,
    #         )
    #         .order_by(
    #             Gl_jouhdr.datum,
    #             Gl_journal.fibukonto,
    #         )
    #     )
        
    #     for row in looping_session_only.execute(stmt.execution_options(stream_results=True)):

    #         (
    #             datum,
    #             _recid,
    #             fibukonto
    #         ) = row

    #         g_list = G_list()
    #         g_list_data.append(g_list)

    #         g_list.datum = datum
    #         g_list.grecid = _recid
    #         g_list.fibu = fibukonto
    #         g_list.table_name = "gl_journal"


    # def create_glisthis():

    #     nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
    #     nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


    #     nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
    #     nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

    #     # Oscar - Optimasi query
    #     # for gl_jhdrhis in db_session.query(Gl_jhdrhis).filter((Gl_jhdrhis.datum >= from_datehis) & (Gl_jhdrhis.datum <= to_datehis)).order_by(Gl_jhdrhis.datum).all():

    #     #     for gl_jourhis in db_session.query(Gl_jourhis).filter((Gl_jourhis.jnr == gl_jhdrhis.jnr) & (Gl_jourhis.fibukonto >= (from_fibu).lower()) & (Gl_jourhis.fibukonto <= (to_fibu).lower())).order_by(Gl_jourhis.fibukonto).all():

    #     # datum = Gl_jhdrhis.datum
    #     # _recid = Gl_jourhis._recid
    #     # fibukonto = Gl_jourhis.fibukonto      
    #     stmt = (
    #         select(
    #             Gl_jhdrhis.datum,
    #             Gl_jourhis._recid,
    #             Gl_jourhis.fibukonto,
    #         )
    #         .select_from(Gl_jhdrhis)
    #         .join(Gl_jourhis, Gl_jourhis.jnr == Gl_jhdrhis.jnr)
    #         .where(
    #             Gl_jhdrhis.datum >= from_datehis,
    #             Gl_jhdrhis.datum <= to_datehis,
    #             Gl_jourhis.fibukonto >= from_fibu,
    #             Gl_jourhis.fibukonto <= to_fibu
    #         )
    #         .order_by(Gl_jhdrhis.datum, Gl_jourhis.fibukonto)
    #     )

    #     for row in looping_session_only.execute(stmt.execution_options(stream_results=True)):
    #         (
    #             datum,
    #             _recid,
    #             fibukonto
    #         ) = row
            
    #         g_list = G_list()
    #         g_list_data.append(g_list)

    #         g_list.datum = datum
    #         g_list.grecid = _recid
    #         g_list.fibu = fibukonto
    #         g_list.table_name = "gl_jourhis"

    def create_list1():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag

        nonlocal gl_journal_map, gl_jourhis_map,  gl_department_map, tmp_gl_acct_fibukonto, tmp_gl_acct_actual, tmp_gl_acct_acc_type, tmp_glist

        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        konto:string = ""
        i:int = 0
        c:string = ""
        ind:int = 0
        curr_month:int = 0
        t_debit:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        p_bal:Decimal = to_decimal("0.0")
        t_bal:Decimal = to_decimal("0.0")
        y_bal:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        t_ybal:Decimal = to_decimal("0.0")
        tt_ybal:Decimal = to_decimal("0.0")
        prev_bal:Decimal = to_decimal("0.0")
        tot_bal:Decimal = to_decimal("0.0")
        tot_budget:Decimal = to_decimal("0.0")
        diff:Decimal = to_decimal("0.0")
        tt_debit:Decimal = to_decimal("0.0")
        tt_credit:Decimal = to_decimal("0.0")
        tt_pbal:Decimal = to_decimal("0.0")
        tt_bal:Decimal = to_decimal("0.0")
        tt_diff:Decimal = to_decimal("0.0")
        act_flag:int = 0
        n:int = 0
        to_bal:Decimal = to_decimal("0.0")
        curr_tbal:Decimal = to_decimal("0.0")
        curr_totbal:Decimal = to_decimal("0.0")
        curr_ttbal:Decimal = to_decimal("0.0")
        gl_account = None
        Gl_account =  create_buffer("Gl_account",Gl_acct)
        in_procedure = True
        sales =  to_decimal("0")
        cost =  to_decimal("0")
        gop_credit =  to_decimal("0")
        gop_debit =  to_decimal("0")
        tot_diff =  to_decimal("0")
        act_flag = 0

        if to_date <= lastprevmonthdate:
            act_flag = 1

        output_list_data.clear()
        curr_month = close_month

        gl_main_obj_list = {}
        gl_main = Gl_main()
        gl_account = Gl_acct()

        txn_selects = []

        if from_date is not None:
            txn_selects.append(
                select(
                    Gl_journal.fibukonto.label("fibukonto"),
                    Gl_journal.debit.label("debit"),
                    Gl_journal.credit.label("credit"),
                    Gl_journal.bemerk.label("bemerk"),
                    Gl_journal._recid.label("recid"),
                    Gl_jouhdr.datum.label("datum"),
                    Gl_jouhdr.refno.label("refno"),
                    literal("gl_journal").label("source"),
                )
                .join(Gl_jouhdr, Gl_jouhdr.jnr == Gl_journal.jnr)
                .where(
                    Gl_jouhdr.datum.between(from_date, to_date),
                    Gl_journal.fibukonto.between(from_fibu, to_fibu),
                )
            )

        if from_datehis is not None:
            txn_selects.append(
                select(
                    Gl_jourhis.fibukonto.label("fibukonto"),
                    Gl_jourhis.debit.label("debit"),
                    Gl_jourhis.credit.label("credit"),
                    Gl_jourhis.bemerk.label("bemerk"),
                    Gl_jhdrhis._recid.label("recid"),
                    Gl_jhdrhis.datum.label("datum"),
                    Gl_jhdrhis.refno.label("refno"),
                    literal("gl_jourhis").label("source"),
                )
                .join(Gl_jhdrhis, Gl_jhdrhis.jnr == Gl_jourhis.jnr)
                .where(
                    Gl_jhdrhis.datum.between(from_datehis, to_datehis),
                    Gl_jourhis.fibukonto.between(from_fibu, to_fibu),
                )
            )

        if len(txn_selects) > 1:
            txn_union = union_all(*txn_selects).subquery("txn")
        elif len(txn_selects) == 1:
            txn_union = txn_selects[0].subquery("txn")

        stmt = (
            select(txn_union.c.fibukonto)
            .distinct()
        )

        tmp_glist = set(
            looping_session_only.execute(
                stmt.execution_options(stream_results=True)
            ).scalars()
        )

        stmt = (
            select(
                Gl_account.fibukonto,
                Gl_account.acc_type,
                Gl_account.deptnr,
                Gl_account.bezeich,
                Gl_account.budget,
                Gl_account.ly_budget,
                Gl_account.actual,
                txn_union.c.fibukonto,
                txn_union.c.debit,
                txn_union.c.credit,
                txn_union.c.bemerk,
                txn_union.c.datum,
                txn_union.c.refno,
                txn_union.c.source,
            )
            .select_from(Gl_account)
            .outerjoin(
                txn_union,
                txn_union.c.fibukonto == Gl_account.fibukonto
            )
            .order_by(
                Gl_account.fibukonto,
                txn_union.c.fibukonto,
                txn_union.c.datum,
                txn_union.c.recid,
            )
        )

        if acct_type != 0:
            stmt = stmt.where(Gl_account.acc_type == acct_type)

        if from_dept != 0:
            stmt = stmt.where(Gl_account.deptnr == from_dept)


        # for gl_main, gl_acct in looping_session_only.query(Gl_main, Gl_account).outerjoin(Gl_account, (Gl_account.main_nr == Gl_main.nr)).filter((Gl_account.fibukonto >= from_fibu) & (Gl_account.fibukonto <= to_fibu)).order_by(Gl_main.code, Gl_account.fibukonto).yield_per(1000).execution_options(stream_result=True):

        prev_gl_main_code = None

        prev_gl_acct_fibukonto = None
        prev_gl_acct_deptnr = None
        prev_gl_acct_acc_type = None
        prev_gl_acct_actual = None
        prev_gl_acct_bezeich = None
        prev_gl_acct_budget = None
        prev_gl_acct_ly_budget = None

        # Oscar - optimize query
        for row in looping_session_only.execute(stmt.execution_options(stream_results=True)):

            (
                gl_acct_fibukonto,
                gl_acct_acc_type,
                gl_acct_deptnr,
                gl_acct_bezeich,
                gl_acct_budget,
                gl_acct_ly_budget,
                gl_acct_actual,
                glist_fibukonto,
                glist_debit,
                glist_credit,
                glist_bemerk,
                glist_datum,
                glist_refno,
                glist_source
            ) = row

            # PREVIOUS GL ACCT DATA
            if prev_gl_acct_fibukonto != None and prev_gl_acct_fibukonto != gl_acct_fibukonto:
                tmp_gl_acct_acc_type = prev_gl_acct_acc_type
                tmp_gl_acct_fibukonto = prev_gl_acct_fibukonto
                tmp_gl_acct_actual = prev_gl_acct_actual

                p_bal, y_bal = calcrevcost(t_bal, p_bal, y_bal)

                if prev_gl_acct_acc_type != 3 and prev_gl_acct_acc_type != 4:
                    prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)

                if p_bal != 0 or t_debit != 0 or t_credit != 0:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    counter = counter + 1
                    output_list.nr = counter

                    output_list.str = to_string("", "x(8)")  + "T O T A L "
                    c = convert_balance(p_bal)
                    # output_list.str = output_list.str + to_string(c, "x(22)")
                    output_list.str = output_list.str + format_fixed_length(c, 22)
                    output_list.ref_no = "T O T A L"
                    output_list.begin_bal = c
                    output_list.is_show_depart = False

                    if t_debit >= 0:
                        output_list.str = output_list.str + to_string(t_debit, ">>>,>>>,>>>,>>>,>>9.99")
                        output_list.tot_debit = to_string(t_debit, ">>>,>>>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                        output_list.tot_debit = to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")

                    if t_credit >= 0:
                        output_list.str = output_list.str + to_string(t_credit, ">>>,>>>,>>>,>>>,>>9.99")
                        output_list.tot_credit = to_string(t_credit, ">>>,>>>,>>>,>>>,>>9.99")
                    else:
                        output_list.str = output_list.str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                        output_list.tot_credit = to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")

                    if gl_acct_acc_type == 1 or gl_acct_acc_type == 4:
                        diff =  to_decimal(t_credit) - to_decimal(t_debit)
                        tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                    else:
                        diff =  to_decimal(t_debit) - to_decimal(t_credit)
                        tot_diff =  to_decimal(tot_diff) - to_decimal(t_credit) + to_decimal(t_debit)

                    c = convert_balance(diff)
                    # output_list.str = output_list.str + to_string(c, "x(22)")
                    output_list.str = output_list.str + format_fixed_length(c, 22)
                    output_list.net_change = to_string(c, "x(22)")
                    t_bal = to_decimal(p_bal) + to_decimal(tot_diff)

                    c = convert_balance(t_bal)
                    # output_list.str = output_list.str + to_string(c, "x(22)")
                    output_list.str = output_list.str + format_fixed_length(c, 22)
                    output_list.ending_bal = to_string(c, "x(22)")
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    counter = counter + 1
                    output_list.nr = counter

                else:
                    output_list_data.remove(output_list)
                    
            # CURRENT GL ACCT DATA
            if prev_gl_acct_fibukonto != gl_acct_fibukonto:
                konto = gl_acct_fibukonto
                do_it = True
                prev_bal =  to_decimal("0")
                tot_bal =  to_decimal("0")

                if from_dept > 0 and gl_acct_deptnr != from_dept:
                    do_it = False

                if do_it:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    counter = counter + 1
                    output_list.nr = counter

                    c = convert_fibu(gl_acct_fibukonto)
                    output_list.str = to_string(" ", "x(8)") + format_fixed_length(c, 16) + substring(gl_acct_bezeich.replace("\\n", "\n"), 0, 20)
                    output_list.ref_no = format_fixed_length(c, 32)
                    output_list.begin_bal = gl_acct_bezeich.replace("\\n", "\n")
                    output_list.tot_debit = ""
                    output_list.is_show_depart = True
                    
                    gl_department = gl_department_map.get(gl_acct_deptnr)

                    if gl_department:
                        output_list.dept_name = gl_department.bezeich
                        output_list.dept_nr = gl_department.nr
                    else:
                        output_list.dept_name = ""
                        output_list.dept_nr = 0

                    if length(gl_acct_bezeich) > 20:
                        output_list.str = output_list.str + substring(gl_acct_bezeich.replace("\\n", "\n"), 20, 18)

                    t_debit =  to_decimal("0")
                    t_credit =  to_decimal("0")
                    p_bal =  to_decimal("0")
                    t_bal =  to_decimal("0")
                    curr_tbal =  to_decimal("0")
                    curr_totbal =  to_decimal("0")
                    curr_ttbal =  to_decimal("0")
                    tot_bal = to_decimal("0")

                    if gl_acct_acc_type == 3 or gl_acct_acc_type == 4:
                        tmp_gl_acct_acc_type = gl_acct_acc_type
                        tmp_gl_acct_fibukonto = gl_acct_fibukonto
                        tmp_gl_acct_actual = gl_acct_actual
                        
                        p_bal, to_bal = calc_prevbalance(konto)

                        if p_bal == None:
                            p_bal =  to_decimal("0")

                        if to_bal == None:
                            to_bal =  to_decimal("0")

                        prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)
                        t_bal =  to_decimal(p_bal) + to_decimal(to_bal)
                        tot_bal =  to_decimal(tot_bal) + to_decimal(p_bal) + to_decimal(to_bal)

                prev_gl_acct_fibukonto = gl_acct_fibukonto
                prev_gl_acct_acc_type = gl_acct_acc_type
                prev_gl_acct_actual = gl_acct_actual


            if glist_fibukonto != None and do_it == True:
                t_date = glist_datum
        
                if from_datehis != None and to_datehis != None:

                    if t_date >= from_datehis and t_date <= to_datehis and glist_source == "gl_jourhis":

                        # gl_jourhis = get_cache (Gl_jourhis, {"_recid": [(eq, g_list.grecid)]})

                        # gl_jourhis = gl_jourhis_map.get(g_list.grecid)

                        # gl_jhdrhis = get_cache (Gl_jhdrhis, {"jnr": [(eq, gl_jourhis.jnr)]})
                        # g_list_data.remove(g_list)


                        if gl_acct_fibukonto.lower()  == (pnl_acct).lower() :
                            gop_credit =  (gop_credit) + (glist_credit)
                            gop_debit =  (gop_debit) + (glist_debit)

                        if gl_acct_acc_type == 1:
                            sales =  (sales) + (glist_credit) - (glist_debit)
                        elif gl_acct_acc_type == 2 or gl_acct_acc_type == 5:
                            cost =  (cost) + (glist_debit) - (glist_credit)

                        t_debit =  (t_debit) + (glist_debit)
                        t_credit =  (t_credit) + (glist_credit)
                        tot_debit =  (tot_debit) + (glist_debit)
                        tot_credit =  (tot_credit) + (glist_credit)
                        tt_debit =  (tt_debit) + (glist_debit)
                        tt_credit =  (tt_credit) + (glist_credit)

                        if gl_acct_acc_type == 1 or gl_acct_acc_type == 4:
                            t_bal =  (t_bal) - (glist_debit) + (glist_credit)
                            tot_bal =  (tot_bal) - (glist_debit) + (glist_credit)
                            tt_bal =  (tt_bal) - (glist_debit) + (glist_credit)
                        else:
                            t_bal =  (t_bal) + (glist_debit) - (glist_credit)
                            tot_bal =  (tot_bal) + (glist_debit) - (glist_credit)
                            tt_bal =  (tt_bal) + (glist_debit) - (glist_credit)

                        output_list = Output_list()
                        output_list_data.append(output_list)

                        counter = counter + 1
                        output_list.nr = counter

                        output_list.str = format_fixed_length(glist_datum.strftime("%m/%d/%y"), 8) + format_fixed_length(glist_refno, 13)
                        output_list.ref_no = format_fixed_length(glist_refno, 32)
                        output_list.begin_bal = handling_negative((tot_bal - glist_debit + glist_credit), "->>,>>>,>>>,>>>,>>9.99")
                        output_list.net_change = handling_negative((glist_debit - glist_credit) , "->>,>>>,>>>,>>>,>>9.99")
                        output_list.ending_bal = handling_negative((tot_bal) , "->>,>>>,>>>,>>>,>>9.99")
                        output_list.is_show_depart = False

                        gl_department = gl_department_map.get(gl_acct_deptnr)
                        if gl_department:
                            output_list.dept_name = gl_department.bezeich
                            output_list.dept_nr = gl_department.nr
                        else:
                            output_list.dept_name = ""
                            output_list.dept_nr = 0

                        output_list.str = output_list.str + " "

                        if glist_debit >= 0:
                            output_list.str = output_list.str + to_string(glist_debit, ">>>,>>>,>>>,>>>,>>9.99")
                            output_list.tot_debit = to_string(glist_debit, ">>>,>>>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + to_string(glist_debit, "->>,>>>,>>>,>>>,>>9.99")
                            output_list.tot_debit = to_string(glist_debit, "->>,>>>,>>>,>>>,>>9.99")

                        if glist_credit >= 0:
                            output_list.str = output_list.str + to_string(glist_credit, ">>>,>>>,>>>,>>>,>>9.99")
                            output_list.tot_credit = to_string(glist_credit, ">>>,>>>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + to_string(glist_credit, "->>,>>>,>>>,>>>,>>9.99")
                            output_list.tot_credit = to_string(glist_credit, "->>,>>>,>>>,>>>,>>9.99")

                        # output_list.str = output_list.str + to_string("", "x(44)") + to_string(get_bemerk (gl_jourhis.bemerk) , "x(62)")
                        output_list.str = output_list.str + to_string("", "x(44)") + format_fixed_length(get_bemerk(glist_bemerk) , 62)
                        output_list.note = format_fixed_length(get_bemerk(glist_bemerk) , 62)

                if from_date != None and t_date != None:

                    if t_date >= from_date and t_date <= to_date and glist_source == "gl_journal":

                        # gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                        # gl_journal = gl_journal_map.get(g_list.grecid)

                        # gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})

                        # g_list_data.remove(g_list)

                        if gl_acct_fibukonto.lower()  == (pnl_acct).lower() :
                            gop_credit =  (gop_credit) + (glist_credit)
                            gop_debit =  (gop_debit) + (glist_debit)

                        if gl_acct_acc_type == 1:
                            sales =  (sales) + (glist_credit) - (glist_debit)

                        elif gl_acct_acc_type == 2 or gl_acct_acc_type == 5:
                            cost =  (cost) + (glist_debit) - (glist_credit)

                        t_debit =  (t_debit) + (glist_debit)
                        t_credit =  (t_credit) + (glist_credit)
                        tot_debit =  (tot_debit) + (glist_debit)
                        tot_credit =  (tot_credit) + (glist_credit)
                        tt_debit =  (tt_debit) + (glist_debit)
                        tt_credit =  (tt_credit) + (glist_credit)

                        if gl_acct_acc_type == 1 or gl_acct_acc_type == 4:
                            t_bal =  (t_bal) - (glist_debit) + (glist_credit)
                            tot_bal =  (tot_bal) - (glist_debit) + (glist_credit)
                            tt_bal =  (tt_bal) - (glist_debit) + (glist_credit)
                        else:
                            t_bal =  (t_bal) + (glist_debit) - (glist_credit)
                            tot_bal =  (tot_bal) + (glist_debit) - (glist_credit)
                            tt_bal =  (tt_bal) + (glist_debit) - (glist_credit)

                        output_list = Output_list()
                        output_list_data.append(output_list)

                        counter = counter + 1
                        output_list.nr = counter

                        output_list.str = format_fixed_length(glist_datum.strftime("%m/%d/%y"), 8) + format_fixed_length(glist_refno, 13)
                        output_list.ref_no = format_fixed_length(glist_refno, 32)
                        output_list.begin_bal = handling_negative((tot_bal - glist_debit + glist_credit), "->>,>>>,>>>,>>>,>>9.99")
                        output_list.net_change = handling_negative((glist_debit - glist_credit) , "->>,>>>,>>>,>>>,>>9.99")
                        output_list.ending_bal = handling_negative((tot_bal) , "->>,>>>,>>>,>>>,>>9.99")
                        output_list.is_show_depart = False

                        gl_department = gl_department_map.get(gl_acct_deptnr)
                        if gl_department:
                            output_list.dept_name = gl_department.bezeich
                            output_list.dept_nr = gl_department.nr
                        else:
                            output_list.dept_name = ""
                            output_list.dept_nr = 0

                        output_list.str = output_list.str + " "

                        if glist_debit >= 0:
                            output_list.str = output_list.str + to_string(glist_debit, ">>>,>>>,>>>,>>>,>>9.99")
                            output_list.tot_debit = to_string(glist_debit, ">>>,>>>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + to_string(glist_debit, "->>,>>>,>>>,>>>,>>9.99")
                            output_list.tot_debit = to_string(glist_debit, "->>,>>>,>>>,>>>,>>9.99")

                        if glist_credit >= 0:
                            output_list.str = output_list.str + to_string(glist_credit, ">>>,>>>,>>>,>>>,>>9.99")
                            output_list.tot_credit = to_string(glist_credit, ">>>,>>>,>>>,>>>,>>9.99")
                        else:
                            output_list.str = output_list.str + to_string(glist_credit, "->>,>>>,>>>,>>>,>>9.99")
                            output_list.tot_credit = to_string(glist_credit, "->>,>>>,>>>,>>>,>>9.99")

                        # output_list.str = output_list.str + to_string("", "x(44)") + to_string(get_bemerk (gl_jourhis.bemerk) , "x(62)")
                        output_list.str = output_list.str + to_string("", "x(44)") + format_fixed_length(get_bemerk(glist_bemerk) , 62)
                        output_list.note = format_fixed_length(get_bemerk(glist_bemerk) , 62)
        
        # PREVIOUS GL ACCT DATA
        if prev_gl_acct_fibukonto != None:
            tmp_gl_acct_acc_type = prev_gl_acct_acc_type
            tmp_gl_acct_fibukonto = prev_gl_acct_fibukonto
            tmp_gl_acct_actual = prev_gl_acct_actual

            p_bal, y_bal = calcrevcost(t_bal, p_bal, y_bal)

            if prev_gl_acct_acc_type != 3 and prev_gl_acct_acc_type != 4:
                prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)

            if p_bal != 0 or t_debit != 0 or t_credit != 0:
                output_list = Output_list()
                output_list_data.append(output_list)

                counter = counter + 1
                output_list.nr = counter

                output_list.str = to_string("", "x(8)")  + "T O T A L "
                c = convert_balance(p_bal)
                # output_list.str = output_list.str + to_string(c, "x(22)")
                output_list.str = output_list.str + format_fixed_length(c, 22)
                output_list.ref_no = "T O T A L"
                output_list.begin_bal = c
                output_list.is_show_depart = False

                if t_debit >= 0:
                    output_list.str = output_list.str + to_string(t_debit, ">>>,>>>,>>>,>>>,>>9.99")
                    output_list.tot_debit = to_string(t_debit, ">>>,>>>,>>>,>>>,>>9.99")
                else:
                    output_list.str = output_list.str + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                    output_list.tot_debit = to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")

                if t_credit >= 0:
                    output_list.str = output_list.str + to_string(t_credit, ">>>,>>>,>>>,>>>,>>9.99")
                    output_list.tot_credit = to_string(t_credit, ">>>,>>>,>>>,>>>,>>9.99")
                else:
                    output_list.str = output_list.str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                    output_list.tot_credit = to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")

                if gl_acct_acc_type == 1 or gl_acct_acc_type == 4:
                    diff =  to_decimal(t_credit) - to_decimal(t_debit)
                    tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                else:
                    diff =  to_decimal(t_debit) - to_decimal(t_credit)
                    tot_diff =  to_decimal(tot_diff) - to_decimal(t_credit) + to_decimal(t_debit)

                c = convert_balance(diff)
                # output_list.str = output_list.str + to_string(c, "x(22)")
                output_list.str = output_list.str + format_fixed_length(c, 22)
                output_list.net_change = to_string(c, "x(22)")
                t_bal = to_decimal(p_bal) + to_decimal(tot_diff)

                c = convert_balance(t_bal)
                # output_list.str = output_list.str + to_string(c, "x(22)")
                output_list.str = output_list.str + format_fixed_length(c, 22)
                output_list.ending_bal = to_string(c, "x(22)")
                output_list = Output_list()
                output_list_data.append(output_list)

                counter = counter + 1
                output_list.nr = counter

            else:
                output_list_data.remove(output_list)
                

        if prev_bal != 0 or tot_debit != 0 or tot_credit != 0:
            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter

            output_list.str = to_string("", "x(8)") + "Grand TOTAL "
            c = convert_balance(prev_bal)
            # output_list.str = output_list.str + to_string(c, "x(22)")
            output_list.str = output_list.str + format_fixed_length(c, 22)
            output_list.ref_no = "Grand TOTAL"
            output_list.begin_bal = c
            output_list.is_show_depart = False

            if tot_debit >= 0:
                output_list.str = output_list.str + to_string(tot_debit, ">>>,>>>,>>>,>>>,>>9.99")
                output_list.tot_debit = to_string(tot_debit, ">>>,>>>,>>>,>>>,>>9.99")
            else:
                output_list.str = output_list.str + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
                output_list.tot_debit = to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")

            if tot_credit >= 0:
                output_list.str = output_list.str + to_string(tot_credit, ">>>,>>>,>>>,>>>,>>9.99")
                output_list.tot_credit = to_string(tot_credit, ">>>,>>>,>>>,>>>,>>9.99")
            else:
                output_list.str = output_list.str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                output_list.tot_credit = to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")

            c = convert_balance(tot_diff)
            # output_list.str = output_list.str + to_string(c, "x(22)")
            output_list.str = output_list.str + format_fixed_length(c, 22)
            output_list.net_change = to_string(c, "x(22)")
            tot_bal =  to_decimal(prev_bal) + to_decimal(tot_diff)

            c = convert_balance(tot_bal)
            # output_list.str = output_list.str + to_string(c, "x(22)")
            output_list.str = output_list.str + format_fixed_length(c, 22)
            output_list.ending_bal = to_string(c, "x(22)")

        if to_date == close_date:
            prof_loss_acct11()


    def create_list2():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag

        nonlocal gl_journal_map, gl_jourhis_map,  gl_department_map, tmp_gl_acct_fibukonto, tmp_gl_acct_actual, tmp_gl_acct_acc_type, tmp_glist

        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        konto:string = ""
        i:int = 0
        c:string = ""
        ind:int = 0
        curr_month:int = 0
        t_debit:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        p_bal:Decimal = to_decimal("0.0")
        t_bal:Decimal = to_decimal("0.0")
        y_bal:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        t_ybal:Decimal = to_decimal("0.0")
        tt_ybal:Decimal = to_decimal("0.0")
        prev_bal:Decimal = to_decimal("0.0")
        tot_bal:Decimal = to_decimal("0.0")
        tot_budget:Decimal = to_decimal("0.0")
        diff:Decimal = to_decimal("0.0")
        tt_debit:Decimal = to_decimal("0.0")
        tt_credit:Decimal = to_decimal("0.0")
        tt_pbal:Decimal = to_decimal("0.0")
        tt_bal:Decimal = to_decimal("0.0")
        tt_diff:Decimal = to_decimal("0.0")
        act_flag:int = 0
        n:int = 0
        to_bal:Decimal = to_decimal("0.0")
        curr_tbal:Decimal = to_decimal("0.0")
        curr_totbal:Decimal = to_decimal("0.0")
        curr_ttbal:Decimal = to_decimal("0.0")
        gl_account = None
        Gl_account =  create_buffer("Gl_account",Gl_acct)
        in_procedure = True
        sales =  to_decimal("0")
        cost =  to_decimal("0")
        gop_credit =  to_decimal("0")
        gop_debit =  to_decimal("0")
        tot_diff =  to_decimal("0")
        act_flag = 0

        if to_date <= lastprevmonthdate:
            act_flag = 1

        output_list_data.clear()
        curr_month = close_month

        gl_main_obj_list = {}
        gl_main = Gl_main()
        gl_account = Gl_acct()

        txn_selects = []

        if from_date is not None:
            txn_selects.append(
                select(
                    Gl_journal.fibukonto.label("fibukonto"),
                    Gl_journal.debit.label("debit"),
                    Gl_journal.credit.label("credit"),
                    Gl_jouhdr.datum.label("datum"),
                    literal("gl_journal").label("source"),
                )
                .join(Gl_jouhdr, Gl_jouhdr.jnr == Gl_journal.jnr)
                .where(
                    Gl_jouhdr.datum.between(from_date, to_date),
                    Gl_journal.fibukonto.between(from_fibu, to_fibu),
                )
            )

        if from_datehis is not None:
            txn_selects.append(
                select(
                    Gl_jourhis.fibukonto.label("fibukonto"),
                    Gl_jourhis.debit.label("debit"),
                    Gl_jourhis.credit.label("credit"),
                    Gl_jhdrhis.datum.label("datum"),
                    literal("gl_jourhis").label("source"),
                )
                .join(Gl_jhdrhis, Gl_jhdrhis.jnr == Gl_jourhis.jnr)
                .where(
                    Gl_jhdrhis.datum.between(from_datehis, to_datehis),
                    Gl_jourhis.fibukonto.between(from_fibu, to_fibu),
                )
            )

        if len(txn_selects) > 1:
            txn_union = union_all(*txn_selects).subquery("txn")
        elif len(txn_selects) == 1:
            txn_union = txn_selects[0].subquery("txn")

        stmt = (
            select(txn_union.c.fibukonto)
            .distinct()
        )

        tmp_glist = set(
            looping_session_only.execute(
                stmt.execution_options(stream_results=True)
            ).scalars()
        )

        stmt = (
            select(
                Gl_main.nr,
                Gl_main.code,
                Gl_main.bezeich,
                Gl_account.fibukonto,
                Gl_account.acc_type,
                Gl_account.deptnr,
                Gl_account.bezeich,
                Gl_account.budget,
                Gl_account.ly_budget,
                Gl_account.actual,
                txn_union.c.fibukonto,
                txn_union.c.debit,
                txn_union.c.credit,
                txn_union.c.datum,
                txn_union.c.source,
            )
            .select_from(Gl_main)
            .join(
                Gl_account,
                (Gl_account.main_nr == Gl_main.nr) &
                (Gl_account.fibukonto.between(from_fibu, to_fibu))
            )
            .outerjoin(
                txn_union,
                txn_union.c.fibukonto == Gl_account.fibukonto
            )
            .order_by(
                Gl_main.code, 
                Gl_account.fibukonto,
                txn_union.c.source,
                txn_union.c.datum,
                txn_union.c.fibukonto,
            )
        )

        if acct_type != 0:
            stmt = stmt.where(Gl_account.acc_type == acct_type)

        if from_dept != 0:
            stmt = stmt.where(Gl_account.deptnr == from_dept)


        # for gl_main, gl_acct in looping_session_only.query(Gl_main, Gl_account).outerjoin(Gl_account, (Gl_account.main_nr == Gl_main.nr)).filter((Gl_account.fibukonto >= from_fibu) & (Gl_account.fibukonto <= to_fibu)).order_by(Gl_main.code, Gl_account.fibukonto).yield_per(1000).execution_options(stream_result=True):

        prev_gl_main_code = None

        prev_gl_acct_fibukonto = None
        prev_gl_acct_deptnr = None
        prev_gl_acct_acc_type = None
        prev_gl_acct_actual = None
        prev_gl_acct_bezeich = None
        prev_gl_acct_budget = None
        prev_gl_acct_ly_budget = None

        # Oscar - optimize query
        for row in looping_session_only.execute(stmt.execution_options(stream_results=True)):

            (
                gl_main_nr,
                gl_main_code,
                gl_main_bezeich,
                gl_acct_fibukonto,
                gl_acct_acc_type,
                gl_acct_deptnr,
                gl_acct_bezeich,
                gl_acct_budget,
                gl_acct_ly_budget,
                gl_acct_actual,
                glist_fibukonto,
                glist_debit,
                glist_credit,
                glist_datum,
                glist_source
            ) = row

            # PREVIOUS GL ACCT DATA
            if prev_gl_acct_fibukonto != None and prev_gl_acct_fibukonto != gl_acct_fibukonto:
                tmp_gl_acct_acc_type = prev_gl_acct_acc_type
                tmp_gl_acct_fibukonto = prev_gl_acct_fibukonto
                tmp_gl_acct_actual = prev_gl_acct_actual

                p_bal, y_bal = calcrevcost(t_bal, p_bal, y_bal)

                if prev_gl_acct_acc_type != 3 and prev_gl_acct_acc_type != 4:
                    prev_bal =  (prev_bal) + (p_bal)

                if p_bal != 0 or t_debit != 0 or t_credit != 0 or y_bal != 0:
                    output_list = Output_list()
                    output_list_data.append(output_list)

                    # gl_department = get_cache (Gl_department, {"nr": [(eq, gl_acct_deptnr)]})
                    gl_department = gl_department_map.get(prev_gl_acct_deptnr)

                    if gl_department:
                        output_list.dept_name = gl_department.bezeich
                        output_list.dept_nr = gl_department.nr
                    else:
                        output_list.dept_name = ""
                        output_list.dept_nr = 0

                    output_list.is_show_depart = True
                    counter = counter + 1
                    output_list.nr = counter

                    c = convert_fibu(prev_gl_acct_fibukonto)
                    # output_list.str = to_string(c, "x(16)") + to_string(gl_acct_bezeich, "x(38)")
                    output_list.str = format_fixed_length(c, 16) + format_fixed_length(prev_gl_acct_bezeich, 38)
                    c = convert_balance(p_bal)

                    if t_debit >= 0:
                        # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                        tmp_t_debit = format_fixed_length(to_string(t_debit, ">>,>>>,>>>,>>>,>>9.99"), 22)
                        output_list.str = output_list.str + format_fixed_length(c, 22) + tmp_t_debit
                    else:
                        # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                        tmp_t_debit = to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                        output_list.str = output_list.str + format_fixed_length(c, 22) + tmp_t_debit

                    if t_credit >= 0:
                        # output_list.str = output_list.str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                        tmp_t_credit = format_fixed_length(to_string(t_credit, ">>,>>>,>>>,>>>,>>9.99"), 22)
                        output_list.str = output_list.str  + tmp_t_credit
                    else:
                        # output_list.str = output_list.str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                        tmp_t_credit = to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                        output_list.str = output_list.str  + tmp_t_credit

                    if prev_gl_acct_acc_type == 1 or prev_gl_acct_acc_type == 4:
                        diff =  - (t_debit) + (t_credit)
                        tot_diff =  (tot_diff) + (t_credit) - (t_debit)
                        tt_diff =  (tt_diff) + (t_credit) - (t_debit)
                    else:
                        diff =  (t_debit) - (t_credit)
                        tot_diff =  (tot_diff) - (t_credit) + (t_debit)
                        tt_diff =  (tt_diff) - (t_credit) + (t_debit)

                    c = convert_balance(diff)
                    # output_list.str = output_list.str + to_string(c, "x(22)")
                    output_list.str = output_list.str + format_fixed_length(c, 22)
                    c = convert_balance(t_bal)
                    # output_list.str = output_list.str + to_string(c, "x(22)")
                    output_list.str = output_list.str + format_fixed_length(c, 22)
                    c = convert_balance(y_bal)
                    # output_list.str = output_list.str + to_string(c, "x(22)")
                    output_list.str = output_list.str + format_fixed_length(c, 22)

                    t_ybal =  (t_ybal) + (y_bal)
                    tt_ybal =  (tt_ybal) + (y_bal)

                    if get_year(close_year) == get_year(to_date):

                        if prev_gl_acct_acc_type == 1:
                            output_list.budget =  (prev_gl_acct_budget[get_month(to_date) - 1]) * -1
                        elif prev_gl_acct_acc_type == 2 or prev_gl_acct_acc_type == 5:
                            output_list.budget =  (prev_gl_acct_budget[get_month(to_date) - 1])

                    elif get_year(close_year) == get_year(to_date) + 1:

                        if prev_gl_acct_acc_type == 1:
                            output_list.budget =  (prev_gl_acct_ly_budget[get_month(to_date) - 1]) * -1
                        elif prev_gl_acct_acc_type == 2 or prev_gl_acct_acc_type == 5:
                            output_list.budget =  (prev_gl_acct_ly_budget[get_month(to_date) - 1])

                    if output_list.budget != 0 and output_list.budget != None:
                        output_list.proz =  (t_bal) / (output_list.budget) * (100)
                        tot_budget =  (tot_budget) + (output_list.budget)

            # PREVIOUS GL MAIN DATA
            if prev_gl_main_code != None and prev_gl_main_code != gl_main_code:

                output_list = Output_list()
                output_list_data.append(output_list)

                counter = counter + 1
                output_list.nr = counter

                # output_list.str = to_string("", "x(16)")  + to_string("S U B T O T A L", "x(38)")
                output_list.str = to_string("", "x(16)")  + format_fixed_length("S U B T O T A L", 38)
                c = convert_balance(prev_bal)
                tt_pbal2 =  (tt_pbal2) + (prev_bal)
                output_list.is_show_depart = False

                if tot_debit >= 0:
                    # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
                    tmp_tot_debit = format_fixed_length(to_string(tot_debit, ">>,>>>,>>>,>>>,>>9.99"), 22)
                    output_list.str = output_list.str + to_string(c, "x(22)") + tmp_tot_debit
                else:
                    # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
                    tmp_tot_debit = to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
                    output_list.str = output_list.str + to_string(c, "x(22)") + tmp_tot_debit

                if tot_credit >= 0:
                    # output_list.str = output_list.str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                    tmp_tot_credit = format_fixed_length(to_string(tot_credit, ">>,>>>,>>>,>>>,>>9.99"), 22)
                    output_list.str = output_list.str + tmp_tot_credit
                else:
                    # output_list.str = output_list.str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                    tmp_tot_credit = to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                    output_list.str = output_list.str + tmp_tot_credit

                c = convert_balance(tot_diff)
                # output_list.str = output_list.str + to_string(c, "x(22)")
                output_list.str = output_list.str + format_fixed_length(c, 22)
                c = convert_balance(tot_bal)
                # output_list.str = output_list.str + to_string(c, "x(22)")
                output_list.str = output_list.str + format_fixed_length(c, 22)
                c = convert_balance(t_ybal)
                # output_list.str = output_list.str + to_string(c, "x(22)")
                output_list.str = output_list.str + format_fixed_length(c, 22)
                output_list.budget =  (tot_budget)

                if output_list.budget != 0 and output_list.budget != None:
                    output_list.proz =  (tot_bal) / (output_list.budget) * 100

                output_list = Output_list()
                output_list_data.append(output_list)

                counter = counter + 1
                output_list.nr = counter

            # CURRENT GL MAIN DATA
            if prev_gl_main_code != gl_main_code:

                # if gl_main_obj_list.get(gl_main._recid):
                #     continue
                # else:
                #     gl_main_obj_list[gl_main._recid] = True 

                prev_bal =  to_decimal("0")
                tot_debit =  to_decimal("0")
                tot_credit =  to_decimal("0")
                t_ybal =  to_decimal("0")
                tot_bal =  to_decimal("0")
                tot_budget =  to_decimal("0")
                diff =  to_decimal("0")
                tot_diff =  to_decimal("0")
                curr_tbal =  to_decimal("0")
                curr_totbal =  to_decimal("0")
                curr_ttbal =  to_decimal("0")

                output_list = Output_list()
                output_list_data.append(output_list)

                counter = counter + 1
                output_list.nr = counter

                # output_list.str = to_string(to_string(gl_main.code) , "x(16)") + substring(gl_main.bezeich, 0, 38)
                output_list.str = format_fixed_length(to_string(gl_main_code) , 16) + substring(gl_main_bezeich, 0, 38)

                prev_gl_main_code = gl_main_code

            # CURRENT GL ACCT DATA
            if prev_gl_acct_fibukonto != gl_acct_fibukonto:
                konto = gl_acct_fibukonto
                t_debit =  to_decimal("0")
                t_credit =  to_decimal("0")
                p_bal =  to_decimal("0")
                t_bal =  to_decimal("0")
                y_bal =  to_decimal("0")

                if gl_acct_acc_type == 3 or gl_acct_acc_type == 4:
                    tmp_gl_acct_acc_type = gl_acct_acc_type
                    tmp_gl_acct_fibukonto = gl_acct_fibukonto
                    tmp_gl_acct_actual = gl_acct_actual

                    p_bal, to_bal = calc_prevbalance(konto)

                    prev_bal =  (prev_bal) + (p_bal)
                    t_bal =  (p_bal) + (to_bal)
                    tot_bal =  (tot_bal) + (p_bal) + (to_bal)

                    tt_pbal =  (tt_pbal) + (p_bal)
                    tt_bal =  (tt_bal) + (p_bal) + (to_bal)

                prev_gl_acct_fibukonto = gl_acct_fibukonto
                prev_gl_acct_deptnr = gl_acct_deptnr
                prev_gl_acct_acc_type = gl_acct_acc_type
                prev_gl_acct_actual = gl_acct_actual
                prev_gl_acct_bezeich = gl_acct_bezeich
                prev_gl_acct_budget = gl_acct_budget
                prev_gl_acct_ly_budget = gl_acct_ly_budget


            if glist_fibukonto != None:
                t_date = glist_datum
        
                if from_datehis != None and to_datehis != None:

                    if t_date >= from_datehis and t_date <= to_datehis and glist_source == "gl_jourhis":

                        # gl_jourhis = get_cache (Gl_jourhis, {"_recid": [(eq, g_list.grecid)]})

                        # gl_jourhis = gl_jourhis_map.get(g_list.grecid)

                        # gl_jhdrhis = get_cache (Gl_jhdrhis, {"jnr": [(eq, gl_jourhis.jnr)]})
                        # g_list_data.remove(g_list)


                        if gl_acct_fibukonto.lower()  == (pnl_acct).lower() :
                            gop_credit =  (gop_credit) + (glist_credit)
                            gop_debit =  (gop_debit) + (glist_debit)

                        if gl_acct_acc_type == 1:
                            sales =  (sales) + (glist_credit) - (glist_debit)

                        elif gl_acct_acc_type == 2 or gl_acct_acc_type == 5:
                            cost =  (cost) + (glist_debit) - (glist_credit)

                        t_debit =  (t_debit) + (glist_debit)
                        t_credit =  (t_credit) + (glist_credit)
                        tot_debit =  (tot_debit) + (glist_debit)
                        tot_credit =  (tot_credit) + (glist_credit)
                        tt_debit =  (tt_debit) + (glist_debit)
                        tt_credit =  (tt_credit) + (glist_credit)

                        if gl_acct_acc_type == 1 or gl_acct_acc_type == 4:
                            t_bal =  (t_bal) - (glist_debit) + (glist_credit)
                            tot_bal =  (tot_bal) - (glist_debit) + (glist_credit)
                            tt_bal =  (tt_bal) - (glist_debit) + (glist_credit)
                        else:
                            t_bal =  (t_bal) + (glist_debit) - (glist_credit)
                            tot_bal =  (tot_bal) + (glist_debit) - (glist_credit)
                            tt_bal =  (tt_bal) + (glist_debit) - (glist_credit)

                if from_date != None and t_date != None:

                    if t_date >= from_date and t_date <= to_date and glist_source == "gl_journal":

                        # gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                        # gl_journal = gl_journal_map.get(g_list.grecid)

                        # gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})

                        # g_list_data.remove(g_list)

                        if gl_acct_fibukonto.lower()  == (pnl_acct).lower() :
                            gop_credit =  (gop_credit) + (glist_credit)
                            gop_debit =  (gop_debit) + (glist_debit)

                        if gl_acct_acc_type == 1:
                            sales =  (sales) + (glist_credit) - (glist_debit)

                        elif gl_acct_acc_type == 2 or gl_acct_acc_type == 5:
                            cost =  (cost) + (glist_debit) - (glist_credit)

                        t_debit =  (t_debit) + (glist_debit)
                        t_credit =  (t_credit) + (glist_credit)
                        tot_debit =  (tot_debit) + (glist_debit)
                        tot_credit =  (tot_credit) + (glist_credit)
                        tt_debit =  (tt_debit) + (glist_debit)
                        tt_credit =  (tt_credit) + (glist_credit)

                        if gl_acct_acc_type == 1 or gl_acct_acc_type == 4:
                            t_bal =  (t_bal) - (glist_debit) + (glist_credit)
                            tot_bal =  (tot_bal) - (glist_debit) + (glist_credit)
                            tt_bal =  (tt_bal) - (glist_debit) + (glist_credit)
                        else:
                            t_bal =  (t_bal) + (glist_debit) - (glist_credit)
                            tot_bal =  (tot_bal) + (glist_debit) - (glist_credit)
                            tt_bal =  (tt_bal) + (glist_debit) - (glist_credit)
        
        # PREVIOUS GL ACCT DATA
        if prev_gl_acct_fibukonto != None:
            tmp_gl_acct_acc_type = prev_gl_acct_acc_type
            tmp_gl_acct_fibukonto = prev_gl_acct_fibukonto
            tmp_gl_acct_actual = prev_gl_acct_actual

            p_bal, y_bal = calcrevcost(t_bal, p_bal, y_bal)

            if prev_gl_acct_acc_type != 3 and prev_gl_acct_acc_type != 4:
                prev_bal =  (prev_bal) + (p_bal)

            if p_bal != 0 or t_debit != 0 or t_credit != 0 or y_bal != 0:
                output_list = Output_list()
                output_list_data.append(output_list)

                # gl_department = get_cache (Gl_department, {"nr": [(eq, gl_acct_deptnr)]})
                gl_department = gl_department_map.get(prev_gl_acct_deptnr)

                if gl_department:
                    output_list.dept_name = gl_department.bezeich
                    output_list.dept_nr = gl_department.nr
                else:
                    output_list.dept_name = ""
                    output_list.dept_nr = 0

                output_list.is_show_depart = True
                counter = counter + 1
                output_list.nr = counter

                c = convert_fibu(prev_gl_acct_fibukonto)
                # output_list.str = to_string(c, "x(16)") + to_string(gl_acct_bezeich, "x(38)")
                output_list.str = format_fixed_length(c, 16) + format_fixed_length(prev_gl_acct_bezeich, 38)
                c = convert_balance(p_bal)

                if t_debit >= 0:
                    # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                    tmp_t_debit = format_fixed_length(to_string(t_debit, ">>,>>>,>>>,>>>,>>9.99"), 22)
                    output_list.str = output_list.str + format_fixed_length(c, 22) + tmp_t_debit
                else:
                    # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                    tmp_t_debit = to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
                    output_list.str = output_list.str + format_fixed_length(c, 22) + tmp_t_debit

                if t_credit >= 0:
                    # output_list.str = output_list.str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                    tmp_t_credit = format_fixed_length(to_string(t_credit, ">>,>>>,>>>,>>>,>>9.99"), 22)
                    output_list.str = output_list.str  + tmp_t_credit
                else:
                    # output_list.str = output_list.str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                    tmp_t_credit = to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
                    output_list.str = output_list.str  + tmp_t_credit

                if prev_gl_acct_acc_type == 1 or prev_gl_acct_acc_type == 4:
                    diff =  - (t_debit) + (t_credit)
                    tot_diff =  (tot_diff) + (t_credit) - (t_debit)
                    tt_diff =  (tt_diff) + (t_credit) - (t_debit)
                else:
                    diff =  (t_debit) - (t_credit)
                    tot_diff =  (tot_diff) - (t_credit) + (t_debit)
                    tt_diff =  (tt_diff) - (t_credit) + (t_debit)

                c = convert_balance(diff)
                # output_list.str = output_list.str + to_string(c, "x(22)")
                output_list.str = output_list.str + format_fixed_length(c, 22)
                c = convert_balance(t_bal)
                # output_list.str = output_list.str + to_string(c, "x(22)")
                output_list.str = output_list.str + format_fixed_length(c, 22)
                c = convert_balance(y_bal)
                # output_list.str = output_list.str + to_string(c, "x(22)")
                output_list.str = output_list.str + format_fixed_length(c, 22)

                t_ybal =  (t_ybal) + (y_bal)
                tt_ybal =  (tt_ybal) + (y_bal)

                if get_year(close_year) == get_year(to_date):

                    if prev_gl_acct_acc_type == 1:
                        output_list.budget =  (prev_gl_acct_budget[get_month(to_date) - 1]) * -1
                    elif prev_gl_acct_acc_type == 2 or prev_gl_acct_acc_type == 5:
                        output_list.budget =  (prev_gl_acct_budget[get_month(to_date) - 1])

                elif get_year(close_year) == get_year(to_date) + 1:

                    if prev_gl_acct_acc_type == 1:
                        output_list.budget =  (prev_gl_acct_ly_budget[get_month(to_date) - 1]) * -1
                    elif prev_gl_acct_acc_type == 2 or prev_gl_acct_acc_type == 5:
                        output_list.budget =  (prev_gl_acct_ly_budget[get_month(to_date) - 1])

                if output_list.budget != 0 and output_list.budget != None:
                    output_list.proz =  (t_bal) / (output_list.budget) * (100)
                    tot_budget =  (tot_budget) + (output_list.budget)

        # PREVIOUS GL MAIN DATA
        if prev_gl_main_code != None:

            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter

            # output_list.str = to_string("", "x(16)")  + to_string("S U B T O T A L", "x(38)")
            output_list.str = to_string("", "x(16)")  + format_fixed_length("S U B T O T A L", 38)
            c = convert_balance(prev_bal)
            tt_pbal2 =  (tt_pbal2) + (prev_bal)
            output_list.is_show_depart = False

            if tot_debit >= 0:
                # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
                tmp_tot_debit = format_fixed_length(to_string(tot_debit, ">>,>>>,>>>,>>>,>>9.99"), 22)
                output_list.str = output_list.str + to_string(c, "x(22)") + tmp_tot_debit
            else:
                # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
                tmp_tot_debit = to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
                output_list.str = output_list.str + to_string(c, "x(22)") + tmp_tot_debit

            if tot_credit >= 0:
                # output_list.str = output_list.str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                tmp_tot_credit = format_fixed_length(to_string(tot_credit, ">>,>>>,>>>,>>>,>>9.99"), 22)
                output_list.str = output_list.str + tmp_tot_credit
            else:
                # output_list.str = output_list.str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                tmp_tot_credit = to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
                output_list.str = output_list.str + tmp_tot_credit

            c = convert_balance(tot_diff)
            # output_list.str = output_list.str + to_string(c, "x(22)")
            output_list.str = output_list.str + format_fixed_length(c, 22)
            c = convert_balance(tot_bal)
            # output_list.str = output_list.str + to_string(c, "x(22)")
            output_list.str = output_list.str + format_fixed_length(c, 22)
            c = convert_balance(t_ybal)
            # output_list.str = output_list.str + to_string(c, "x(22)")
            output_list.str = output_list.str + format_fixed_length(c, 22)
            output_list.budget =  (tot_budget)

            if output_list.budget != 0 and output_list.budget != None:
                output_list.proz =  (tot_bal) / (output_list.budget) * 100

            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter

        
        output_list = Output_list()
        output_list_data.append(output_list)

        counter = counter + 1
        output_list.nr = counter

        output_list.str = to_string("", "x(16)")  + to_string("T O T A L", "x(38)")
        c = convert_balance(tt_pbal2)
        output_list.is_show_depart = False

        if tt_debit >= 0:
            # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(tt_debit, "->>,>>>,>>>,>>>,>>9.99")
            tmp_tt_debit = format_fixed_length(to_string(tt_debit, ">>,>>>,>>>,>>>,>>9.99"), 22)
            output_list.str = output_list.str + format_fixed_length(c, 22) + tmp_tt_debit
        else:
            # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(tt_debit, "->>,>>>,>>>,>>>,>>9.99")
            tmp_tt_debit = to_string(tt_debit, "->>,>>>,>>>,>>>,>>9.99")
            output_list.str = output_list.str + format_fixed_length(c, 22) + tmp_tt_debit

        if tt_credit >= 0:
            # output_list.str = output_list.str + to_string(tt_credit, "->>,>>>,>>>,>>>,>>9.99")
            tmp_tt_credit = format_fixed_length(to_string(tt_credit, ">>,>>>,>>>,>>>,>>9.99"), 22)
            output_list.str = output_list.str  + tmp_tt_credit
        else:
            # output_list.str = output_list.str + to_string(tt_credit, "->>,>>>,>>>,>>>,>>9.99")
            tmp_tt_credit = to_string(tt_credit, "->>,>>>,>>>,>>>,>>9.99")
            output_list.str = output_list.str  + tmp_tt_credit

        c = convert_balance(tt_diff)
        output_list.str = output_list.str + to_string(c, "x(22)")
        c = convert_balance(tt_bal)
        output_list.str = output_list.str + to_string(c, "x(22)")

        if from_dept == 0:
            prof_loss_acct21()


    # def create_list2d():

    #     nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
    #     nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


    #     nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
    #     nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

    #     konto:string = ""
    #     i:int = 0
    #     c:string = ""
    #     ind:int = 0
    #     curr_month:int = 0
    #     t_debit:Decimal = to_decimal("0.0")
    #     t_credit:Decimal = to_decimal("0.0")
    #     p_bal:Decimal = to_decimal("0.0")
    #     t_bal:Decimal = to_decimal("0.0")
    #     y_bal:Decimal = to_decimal("0.0")
    #     tot_debit:Decimal = to_decimal("0.0")
    #     tot_credit:Decimal = to_decimal("0.0")
    #     t_ybal:Decimal = to_decimal("0.0")
    #     tt_ybal:Decimal = to_decimal("0.0")
    #     prev_bal:Decimal = to_decimal("0.0")
    #     tot_bal:Decimal = to_decimal("0.0")
    #     tot_budget:Decimal = to_decimal("0.0")
    #     diff:Decimal = to_decimal("0.0")
    #     tt_debit:Decimal = to_decimal("0.0")
    #     tt_credit:Decimal = to_decimal("0.0")
    #     tt_pbal:Decimal = to_decimal("0.0")
    #     tt_bal:Decimal = to_decimal("0.0")
    #     tt_diff:Decimal = to_decimal("0.0")
    #     act_flag:int = 0
    #     n:int = 0
    #     to_bal:Decimal = to_decimal("0.0")
    #     curr_tbal:Decimal = to_decimal("0.0")
    #     curr_totbal:Decimal = to_decimal("0.0")
    #     curr_ttbal:Decimal = to_decimal("0.0")
    #     gl_account = None
    #     Gl_account =  create_buffer("Gl_account",Gl_acct)
    #     in_procedure = True
    #     sales =  to_decimal("0")
    #     cost =  to_decimal("0")
    #     gop_credit =  to_decimal("0")
    #     gop_debit =  to_decimal("0")
    #     tot_diff =  to_decimal("0")
    #     act_flag = 0

    #     if to_date <= lastprevmonthdate:
    #         act_flag = 1

    #     output_list_data.clear()
    #     curr_month = close_month

    #     if sorttype == 2:

    #         gl_main_obj_list = {}
    #         gl_main = Gl_main()
    #         gl_account = Gl_acct()

    #         for gl_main.code, gl_main.bezeich, gl_main.nr, gl_main._recid, gl_account.fibukonto, gl_account.bezeich, gl_account.deptnr, gl_account.acc_type, gl_account.budget, gl_account.ly_budget, gl_account.actual, gl_account.last_yr, gl_account._recid in db_session.query(Gl_main.code, Gl_main.bezeich, Gl_main.nr, Gl_main._recid, Gl_account.fibukonto, Gl_account.bezeich, Gl_account.deptnr, Gl_account.acc_type, Gl_account.budget, Gl_account.ly_budget, Gl_account.actual, Gl_account.last_yr, Gl_account._recid).join(Gl_account,(Gl_account.main_nr == Gl_main.nr) & (Gl_account.fibukonto >= (from_fibu).lower()) & (Gl_account.fibukonto <= (to_fibu).lower()) & (Gl_account.deptnr == from_dept)).order_by(Gl_main.code).all():
               
    #             if gl_main_obj_list.get(gl_main._recid):
    #                 continue
    #             else:
    #                 gl_main_obj_list[gl_main._recid] = True


    #             prev_bal =  to_decimal("0")
    #             tot_debit =  to_decimal("0")
    #             tot_credit =  to_decimal("0")
    #             t_ybal =  to_decimal("0")
    #             tot_bal =  to_decimal("0")
    #             tot_budget =  to_decimal("0")
    #             diff =  to_decimal("0")
    #             tot_diff =  to_decimal("0")
    #             curr_tbal =  to_decimal("0")
    #             curr_totbal =  to_decimal("0")
    #             curr_ttbal =  to_decimal("0")

    #             output_list = Output_list()
    #             output_list_data.append(output_list)

    #             counter = counter + 1
    #             output_list.nr = counter

    #             # output_list.str = to_string(to_string(gl_main.code) , "x(16)") + substring(gl_main.bezeich, 0, 38)
    #             output_list.str = format_fixed_length(to_string(gl_main.code) , 16) + substring(gl_main.bezeich, 0, 38)

    #             for gl_acct in db_session.query(Gl_acct).filter((Gl_acct.main_nr == gl_main.nr) & (Gl_acct.fibukonto >= (from_fibu).lower()) & (Gl_acct.fibukonto <= (to_fibu).lower()) & (Gl_acct.deptnr == from_dept)).order_by(Gl_acct.fibukonto).all():

    #                 konto = gl_acct.fibukonto
    #                 t_debit =  to_decimal("0")
    #                 t_credit =  to_decimal("0")
    #                 p_bal =  to_decimal("0")
    #                 t_bal =  to_decimal("0")
    #                 y_bal =  to_decimal("0")

    #                 if gl_acct.acc_type == 3 or gl_acct.acc_type == 4:
    #                     p_bal, to_bal = calc_prevbalance(konto)
    #                     prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)
    #                     t_bal =  to_decimal(p_bal) + to_decimal(to_bal)
    #                     tot_bal =  to_decimal(tot_bal) + to_decimal(p_bal) + to_decimal(to_bal)


    #                     tt_pbal =  to_decimal(tt_pbal) + to_decimal(p_bal)
    #                     tt_bal =  to_decimal(tt_bal) + to_decimal(p_bal) + to_decimal(to_bal)

    #                 for g_list in query(g_list_data, filters=(lambda g_list: g_list.fibu == gl_acct.fibukonto)):
    #                     t_date = g_list.datum
    #                     pass

    #                     if g_list.grecid != 0:

    #                         if from_datehis != None and to_datehis != None:

    #                             if t_date >= from_datehis and t_date <= to_datehis:

    #                                 gl_jourhis = get_cache (Gl_jourhis, {"_recid": [(eq, g_list.grecid)]})

    #                                 gl_jhdrhis = get_cache (Gl_jhdrhis, {"jnr": [(eq, gl_jourhis.jnr)]})
    #                                 g_list_data.remove(g_list)

    #                                 if gl_jourhis:

    #                                     if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
    #                                         gop_credit =  to_decimal(gop_credit) + to_decimal(gl_jourhis.credit)
    #                                         gop_debit =  to_decimal(gop_debit) + to_decimal(gl_jourhis.debit)

    #                                     if gl_acct.acc_type == 1:
    #                                         sales =  to_decimal(sales) + to_decimal(gl_jourhis.credit) - to_decimal(gl_jourhis.debit)

    #                                     elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
    #                                         cost =  to_decimal(cost) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)

    #                                     t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
    #                                     t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)
    #                                     tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
    #                                     tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)
    #                                     tt_debit =  to_decimal(tt_debit) + to_decimal(gl_jourhis.debit)
    #                                     tt_credit =  to_decimal(tt_credit) + to_decimal(gl_jourhis.credit)

    #                                     if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
    #                                         t_bal =  to_decimal(t_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
    #                                         tot_bal =  to_decimal(tot_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
    #                                         tt_bal =  to_decimal(tt_bal) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
    #                                     else:
    #                                         t_bal =  to_decimal(t_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
    #                                         tot_bal =  to_decimal(tot_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)
    #                                         tt_bal =  to_decimal(tt_bal) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)

    #                         if from_date != None and to_date != None:

    #                             if t_date >= from_date and t_date <= to_date:

    #                                 gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

    #                                 gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})
    #                                 g_list_data.remove(g_list)

    #                                 if gl_journal:

    #                                     if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
    #                                         gop_credit =  to_decimal(gop_credit) + to_decimal(gl_journal.credit)
    #                                         gop_debit =  to_decimal(gop_debit) + to_decimal(gl_journal.debit)

    #                                     if gl_acct.acc_type == 1:
    #                                         sales =  to_decimal(sales) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)

    #                                     elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
    #                                         cost =  to_decimal(cost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

    #                                     t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
    #                                     t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)
    #                                     tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
    #                                     tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)
    #                                     tt_debit =  to_decimal(tt_debit) + to_decimal(gl_journal.debit)
    #                                     tt_credit =  to_decimal(tt_credit) + to_decimal(gl_journal.credit)

    #                                     if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
    #                                         t_bal =  to_decimal(t_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
    #                                         tot_bal =  to_decimal(tot_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
    #                                         tt_bal =  to_decimal(tt_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
    #                                     else:
    #                                         t_bal =  to_decimal(t_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
    #                                         tot_bal =  to_decimal(tot_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
    #                                         tt_bal =  to_decimal(tt_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

    #                 p_bal, y_bal = calcrevcost(t_bal, p_bal, y_bal)

    #                 if gl_acct.acc_type != 3 and gl_acct.acc_type != 4:
    #                     prev_bal =  to_decimal(prev_bal) + to_decimal(p_bal)

    #                 if p_bal != 0 or t_debit != 0 or t_credit != 0 or y_bal != 0:
    #                     output_list = Output_list()
    #                     output_list_data.append(output_list)
    #                     gl_department = get_cache (Gl_department, {"nr": [(eq, gl_acct.deptnr)]})

    #                     if gl_department:
    #                         output_list.dept_name = gl_department.bezeich
    #                         output_list.dept_nr = gl_department.nr
    #                     else:
    #                         output_list.dept_name = ""
    #                         output_list.dept_nr = 0

    #                     output_list.is_show_depart = True
    #                     counter = counter + 1
    #                     output_list.nr = counter


    #                     c = convert_fibu(gl_acct.fibukonto)
    #                     # output_list.str = to_string(c, "x(16)") + to_string(gl_acct.bezeich, "x(38)")
    #                     output_list.str = format_fixed_length(c, 16) + format_fixed_length(gl_acct.bezeich, 38)
    #                     c = convert_balance(p_bal)

    #                     if t_debit >= 0:
    #                         # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
    #                         tmp_t_debit = format_fixed_length(to_string(t_debit, ">>,>>>,>>>,>>>,>>9.99"), 22)
    #                         output_list.str = output_list.str + format_fixed_length(c, 22) + tmp_t_debit
    #                     else:
    #                         # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
    #                         tmp_t_debit = to_string(t_debit, "->>,>>>,>>>,>>>,>>9.99")
    #                         output_list.str = output_list.str + format_fixed_length(c, 22) + tmp_t_debit

    #                     if t_credit >= 0:
    #                         # output_list.str = output_list.str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
    #                         tmp_t_credit = format_fixed_length(to_string(t_credit, ">>,>>>,>>>,>>>,>>9.99"), 22)
    #                         output_list.str = output_list.str  + tmp_t_credit
    #                     else:
    #                         # output_list.str = output_list.str + to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
    #                         tmp_t_credit = to_string(t_credit, "->>,>>>,>>>,>>>,>>9.99")
    #                         output_list.str = output_list.str  + tmp_t_credit

    #                     if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
    #                         diff =  - to_decimal(t_debit) + to_decimal(t_credit)
    #                         tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
    #                         tt_diff =  to_decimal(tt_diff) + to_decimal(t_credit) - to_decimal(t_debit)
    #                     else:
    #                         diff =  to_decimal(t_debit) - to_decimal(t_credit)
    #                         tot_diff =  to_decimal(tot_diff) - to_decimal(t_credit) + to_decimal(t_debit)
    #                         tt_diff =  to_decimal(tt_diff) - to_decimal(t_credit) + to_decimal(t_debit)

    #                     c = convert_balance(diff)
    #                     # output_list.str = output_list.str + to_string(c, "x(22)")
    #                     output_list.str = output_list.str + format_fixed_length(c, 22)
    #                     c = convert_balance(t_bal)
    #                     # output_list.str = output_list.str + to_string(c, "x(22)")
    #                     output_list.str = output_list.str + format_fixed_length(c, 22)
    #                     c = convert_balance(y_bal)
    #                     # output_list.str = output_list.str + to_string(c, "x(22)")
    #                     output_list.str = output_list.str + format_fixed_length(c, 22)

    #                     t_ybal =  to_decimal(t_ybal) + to_decimal(y_bal)
    #                     tt_ybal =  to_decimal(tt_ybal) + to_decimal(y_bal)

    #                     if get_year(close_year) == get_year(to_date):

    #                         if gl_acct.acc_type == 1:
    #                             output_list.budget =  to_decimal(gl_acct.budget[get_month(to_date) - 1]) * -1
    #                         elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
    #                             output_list.budget =  to_decimal(gl_acct.budget[get_month(to_date) - 1])

    #                     elif get_year(close_year) == get_year(to_date) + 1:

    #                         if gl_acct.acc_type == 1:
    #                             output_list.budget =  to_decimal(gl_acct.ly_budget[get_month(to_date) - 1]) * -1
    #                         elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
    #                             output_list.budget =  to_decimal(gl_acct.ly_budget[get_month(to_date) - 1])

    #                     if output_list.budget != 0 and output_list.budget != None:
    #                         output_list.proz =  to_decimal(t_bal) / to_decimal(output_list.budget) * to_decimal("100")
    #                         tot_budget =  to_decimal(tot_budget) + to_decimal(output_list.budget)

    #             output_list = Output_list()
    #             output_list_data.append(output_list)

    #             counter = counter + 1
    #             output_list.nr = counter

    #             # output_list.str = " " + to_string("S U B T O T A L", "x(38)")
    #             output_list.str = to_string("", "x(16)") + to_string("S U B T O T A L", "x(38)")
    #             c = convert_balance(prev_bal)
    #             output_list.is_show_depart = False

    #             if tot_debit >= 0:
    #                 # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
    #                 tmp_tot_debit = format_fixed_length(to_string(tot_debit, ">>,>>>,>>>,>>>,>>9.99"), 22)
    #                 output_list.str = output_list.str + to_string(c, "x(22)") + tmp_tot_debit
    #             else:
    #                 # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
    #                 tmp_tot_debit = to_string(tot_debit, "->>,>>>,>>>,>>>,>>9.99")
    #                 output_list.str = output_list.str + to_string(c, "x(22)") + tmp_tot_debit

    #             if tot_credit >= 0:
    #                 # output_list.str = output_list.str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
    #                 tmp_tot_credit = format_fixed_length(to_string(tot_credit, ">>,>>>,>>>,>>>,>>9.99"), 22)
    #                 output_list.str = output_list.str + tmp_tot_credit
    #             else:
    #                 # output_list.str = output_list.str + to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
    #                 tmp_tot_credit = to_string(tot_credit, "->>,>>>,>>>,>>>,>>9.99")
    #                 output_list.str = output_list.str + tmp_tot_credit

    #             c = convert_balance(tot_diff)
    #             # output_list.str = output_list.str + to_string(c, "x(22)")
    #             output_list.str = output_list.str + format_fixed_length(c, 22)
    #             c = convert_balance(tot_bal)
    #             # output_list.str = output_list.str + to_string(c, "x(22)")
    #             output_list.str = output_list.str + format_fixed_length(c, 22)
    #             c = convert_balance(t_ybal)
    #             # output_list.str = output_list.str + to_string(c, "x(22)")
    #             output_list.str = output_list.str + format_fixed_length(c, 22)
    #             output_list.budget =  to_decimal(tot_budget)

    #             if output_list.budget != 0 and output_list.budget != None:
    #                 output_list.proz =  to_decimal(tot_bal) / to_decimal(output_list.budget) * to_decimal("100")

    #             output_list = Output_list()
    #             output_list_data.append(output_list)

    #             counter = counter + 1
    #             output_list.nr = counter

    #         output_list = Output_list()
    #         output_list_data.append(output_list)

    #         counter = counter + 1
    #         output_list.nr = counter

    #         output_list.str = to_string("", "x(16)")  + to_string("T O T A L", "x(38)")
    #         c = convert_balance(tt_pbal)
    #         output_list.is_show_depart = False

    #         if tt_debit >= 0:
    #             # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(tt_debit, "->>,>>>,>>>,>>>,>>9.99")
    #             tmp_tt_debit = format_fixed_length(to_string(tt_debit, ">>,>>>,>>>,>>>,>>9.99"), 22)
    #             output_list.str = output_list.str + format_fixed_length(c, 22) + tmp_tt_debit
    #         else:
    #             # output_list.str = output_list.str + to_string(c, "x(22)") + to_string(tt_debit, "->>,>>>,>>>,>>>,>>9.99")
    #             tmp_tt_debit = to_string(tt_debit, "->>,>>>,>>>,>>>,>>9.99")
    #             output_list.str = output_list.str + format_fixed_length(c, 22) + tmp_tt_debit

    #         if tt_credit >= 0:
    #             # output_list.str = output_list.str + to_string(tt_credit, "->>,>>>,>>>,>>>,>>9.99")
    #             tmp_tt_credit = format_fixed_length(to_string(tt_credit, ">>,>>>,>>>,>>>,>>9.99"), 22)
    #             output_list.str = output_list.str  + tmp_tt_credit
    #         else:
    #             # output_list.str = output_list.str + to_string(tt_credit, "->>,>>>,>>>,>>>,>>9.99")
    #             tmp_tt_credit = to_string(tt_credit, "->>,>>>,>>>,>>>,>>9.99")
    #             output_list.str = output_list.str  + tmp_tt_credit

    #         c = convert_balance(tt_diff)
    #         output_list.str = output_list.str + to_string(c, "x(22)")
    #         c = convert_balance(tt_bal)
    #         output_list.str = output_list.str + to_string(c, "x(22)")


    def convert_fibu(konto:string):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag

        nonlocal htparam_map

        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)

        # htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
        htparam = htparam_map.get(977)
        ch = htparam.fchar
        j = 0
        for i in range(1,length(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()


    def calc_prevbalance(fibu:string):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag

        nonlocal gl_accthis_map, tmp_gl_acct_actual, tmp_gl_acct_fibukonto, tmp_gl_acct_acc_type, tmp_glist

        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        p_bal = to_decimal("0.0")
        to_bal = to_decimal("0.0")
        lastyear:int = 0
        tmp_date:int = 0
        tmp_todate:date = None
        gbuff = None

        def generate_inner_output():
            return (p_bal, to_bal)
        
        Gbuff =  create_buffer("Gbuff",Gl_acct)
        lastyear = get_year(t_from_date) - 1

        # gbuff = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})
        # gbuff = gl_acct

        if tmp_gl_acct_acc_type != 3 and tmp_gl_acct_acc_type != 4:

            return generate_inner_output()

        if get_year(close_year) == get_year(t_from_date) and get_month(t_from_date) >= 2:
            p_bal =  to_decimal(tmp_gl_acct_actual[prev_month - 1])
        else:
            gl_accthis = None
            if get_month(t_from_date) >= 2:
                # gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, fibu)],"year": [(eq, get_year(t_from_date))]})
                if (fibu, get_year(t_from_date)) in gl_accthis_map:
                    gl_accthis = gl_accthis_map.get((fibu, get_year(t_from_date)))
            else:
                # gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, fibu)],"year": [(eq, lastyear)]})
                if (fibu, lastyear) in gl_accthis_map:
                    gl_accthis = gl_accthis_map.get((fibu, lastyear))

            if gl_accthis:
                p_bal =  to_decimal(gl_accthis[2][prev_month - 1])

        if tmp_gl_acct_acc_type == 4:
            p_bal =  -1 * to_decimal(p_bal)

        if p_bal != 0:
            return generate_inner_output()

        tmp_todate = t_to_date + timedelta(days=1)
        tmp_date = get_day(tmp_todate)

        if tmp_date != 1:
            return generate_inner_output()

        # g_list = query(g_list_data, filters=(lambda g_list: g_list.fibu.lower()  == (fibu).lower()), first=True)

        if fibu in tmp_glist:
            return generate_inner_output()

        if get_year(t_to_date) == get_year(close_date):
            to_bal =  to_decimal(tmp_gl_acct_actual[get_month(t_to_date) - 1])
        else:
            gl_accthis = None
            # gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, fibu)],"year": [(eq, get_year(t_to_date))]})
            if (fibu, get_year(t_to_date)) in gl_accthis_map:
                gl_accthis = gl_accthis_map.get((fibu, get_year(t_to_date)))

            if gl_accthis:
                to_bal =  to_decimal(gl_accthis[2][get_month(t_to_date) - 1])

        if tmp_gl_acct_acc_type == 4:
            to_bal =  -1 * to_decimal(to_bal)

        return generate_inner_output()


    def convert_balance(balance:Decimal):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        if balance >= 0:

            if not show_longbal:
                s = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
            else:
                s = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
        else:
            balance =  - to_decimal(balance)

            if balance >= 0:

                if not show_longbal:
                    ch = trim(to_string(balance, "->>,>>>,>>>,>>>,>>9.99"))
                else:
                    ch = trim(to_string(balance, "->>,>>>,>>>,>>>,>>9.99"))
            else:

                if not show_longbal:
                    ch = trim(to_string(balance, "->>,>>>,>>>,>>>,>>9.99"))
                else:
                    ch = trim(to_string(balance, "->>,>>>,>>>,>>>,>>9.99"))
            s = "(" + ch + ")"
            for i in range(1,20 - length(ch)  + 1) :
                s = " " + s

        return generate_inner_output()


    def prof_loss_acct11():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        m:int = 0
        p_bal:Decimal = to_decimal("0.0")
        t_bal:Decimal = to_decimal("0.0")
        diff:Decimal = to_decimal("0.0")
        c:string = ""

        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, pnl_acct)]})
        gl_acct = db_session.query(Gl_acct).filter(Gl_acct.fibukonto == pnl_acct).first()

        if gl_acct:

            if get_year(close_year) == get_year(t_to_date):
                m = close_month - 1

                if m >= 1:
                    p_bal =  - to_decimal(gl_acct.actual[m - 1])
                else:
                    p_bal =  - to_decimal(gl_acct.last_yr[11])

            elif get_year(close_year) == (get_year(t_to_date) + 1):
                m = close_month - 1

                if m >= 1:
                    p_bal =  - to_decimal(gl_acct.last_yr[m - 1])

            t_bal =  to_decimal(p_bal) + to_decimal(sales) - to_decimal(cost) + to_decimal(gop_credit) - to_decimal(gop_debit)
            diff =  to_decimal(gop_credit) + to_decimal(sales) - to_decimal(gop_debit) - to_decimal(cost)
            
            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter

            output_list.str = to_string("", "x(8)") + "Expected GOP "
            c = convert_balance(p_bal)
            output_list.str = output_list.str + to_string(c, "x(22)")

            if (gop_credit + sales) >= 0:
                output_list.str = output_list.str + to_string((gop_debit + cost) , "->>,>>>,>>>,>>>,>>9.99") + to_string((gop_credit + sales) , "->>,>>>,>>>,>>>,>>9.99")
            else:
                output_list.str = output_list.str + to_string((gop_debit + cost) , "->>,>>>,>>>,>>>,>>9.99") + to_string((gop_credit + sales) , "->>,>>>,>>>,>>>,>>9.99")
            c = convert_balance(diff)
            output_list.str = output_list.str + to_string(c, "x(22)")
            c = convert_balance(t_bal)
            output_list.str = output_list.str + to_string(c, "x(22)")


    def calcrevcost(t_bal:Decimal, p_bal:Decimal, y_bal:Decimal):

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag

        nonlocal gl_accthis_map, tmp_gl_acct_actual, tmp_gl_acct_fibukonto, tmp_gl_acct_acc_type

        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        p_sign:int = 1
        n:int = 0
        lastmonth:int = 0

        def generate_inner_output():
            return (p_bal, y_bal)

        lastmonth = get_month(from_date) - 1

        if tmp_gl_acct_acc_type == 3 or tmp_gl_acct_acc_type == 4:
            y_bal =  to_decimal(t_bal)

            return generate_inner_output()

        if tmp_gl_acct_acc_type == 1:
            p_sign = -1

        if pbal_flag and get_month(from_date) > 1:

            if get_year(close_year) == get_year(from_date):
                for n in range(1,lastmonth  + 1) :
                    p_bal =  to_decimal(p_bal) + to_decimal(p_sign) * to_decimal(tmp_gl_acct_actual[n - 1])
            else:

                # gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, tmp_gl_acct_fibukonto)],"year": [(eq, get_year(from_date))]})

                gl_accthis = None
                if (tmp_gl_acct_fibukonto, get_year(from_date)) in gl_accthis_map:
                    gl_accthis = gl_accthis_map.get((tmp_gl_acct_fibukonto, get_year(from_date)))

                if gl_accthis:
                    for n in range(1,lastmonth  + 1) :
                        p_bal =  to_decimal(p_bal) + to_decimal(p_sign) * to_decimal(gl_accthis[2][n - 1])

        if get_year(close_year) == get_year(from_date):
            for n in range(1,get_month(to_date)  + 1) :
                y_bal =  to_decimal(y_bal) + to_decimal(p_sign) * to_decimal(tmp_gl_acct_actual[n - 1])
        else:

            # gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, tmp_gl_acct_fibukonto)],"year": [(eq, get_year(from_date))]})

            gl_accthis = None
            if (tmp_gl_acct_fibukonto, get_year(from_date)) in gl_accthis_map:
                gl_accthis = gl_accthis_map.get((tmp_gl_acct_fibukonto, get_year(from_date)))

            if gl_accthis:
                for n in range(1,get_month(to_date)  + 1) :
                    y_bal =  to_decimal(y_bal) + to_decimal(p_sign) * to_decimal(gl_accthis[2][n - 1])
                
        return generate_inner_output()


    def prof_loss_acct21():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        m:int = 0
        p_bal:Decimal = to_decimal("0.0")
        t_bal:Decimal = to_decimal("0.0")
        diff:Decimal = to_decimal("0.0")
        c:string = ""
        lastyear:int = 0
        hbuff = None
        Hbuff =  create_buffer("Hbuff",Gl_accthis)
        lastyear = get_year(t_to_date) - 1

        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, pnl_acct)]})
        gl_acct = db_session.query(Gl_acct).filter(Gl_acct.fibukonto == pnl_acct).first()

        if gl_acct:

            # gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, pnl_acct)],"year": [(eq, lastyear)]})
            gl_accthis = db_session.query(Gl_accthis).filter((Gl_accthis.fibukonto == pnl_acct) & (Gl_accthis.year == lastyear)).first()

            if get_year(close_year) == get_year(t_to_date):
                m = close_month - 1

                if m >= 1:
                    p_bal =  - to_decimal(gl_acct.actual[m - 1])
                else:

                    if gl_accthis:
                        p_bal =  - to_decimal(gl_accthis.actual[11])
                    else:
                        p_bal =  - to_decimal(gl_acct.last_yr[11])
            else:

                # hbuff = get_cache (Gl_accthis, {"fibukonto": [(eq, pnl_acct)],"year": [(eq, get_year(t_to_date))]})
                hbuff = db_session.query(Hbuff).filter((Hbuff.fibukonto == pnl_acct) & (Hbuff.year == get_year(t_to_date))).first()

                if hbuff:
                    m = close_month - 1

                    if m >= 1:
                        p_bal =  - to_decimal(hbuff.actual[m - 1])
                    else:

                        if gl_accthis:
                            p_bal =  - to_decimal(gl_accthis.actual[11])
                        else:
                            p_bal =  - to_decimal(hbuff.last_yr[11])

            t_bal =  to_decimal(p_bal) + to_decimal(sales) - to_decimal(cost) + to_decimal(gop_credit) - to_decimal(gop_debit)
            diff =  to_decimal(gop_credit) + to_decimal(sales) - to_decimal(gop_debit) - to_decimal(cost)

            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


            output_list.str = to_string("", "x(16)")  + format_fixed_length("Balance - " + gl_acct.bezeich, 38)
            c = convert_balance(p_bal)
            output_list.str = output_list.str + to_string(c, "x(22)")
            
            if (gop_debit + cost) >= 0:
                output_list.str = output_list.str + handling_negative((gop_debit + cost) , "->>,>>>,>>>,>>>,>>9.99")
            else:
                output_list.str = output_list.str + handling_negative((gop_debit + cost) , "->>,>>>,>>>,>>>,>>9.99")

            if (gop_credit + sales) >= 0:
                output_list.str = output_list.str + handling_negative((gop_credit + sales) , "->>,>>>,>>>,>>>,>>9.99")
            else:
                output_list.str = output_list.str + handling_negative((gop_credit + sales) , "->>,>>>,>>>,>>>,>>9.99")

            c = convert_balance(diff)
            output_list.str = output_list.str + format_fixed_length(c, 22)
            c = convert_balance(t_bal)
            output_list.str = output_list.str + format_fixed_length(c, 22)

            output_list = Output_list()
            output_list_data.append(output_list)

            counter = counter + 1
            output_list.nr = counter


    def sendnextrecords():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

        def generate_inner_output():
            return (result_list_data)

        result_list_data.clear()
        curr_i = 1

        output_list = query(output_list_data, next=True)
        while None != output_list and curr_i <= numsend:
            result_list = Result_list()
            result_list_data.append(result_list)

            buffer_copy(output_list, result_list)
            curr_i = curr_i + 1

            if curr_i <= numsend:

                output_list = query(output_list_data, next=True)

        return generate_inner_output()


    def delete_procedure():

        nonlocal output_list_data, num_acctype, sales, cost, gop_credit, gop_debit, tot_diff, curr_i, in_procedure, numsend, last_acct_close_priod, t_from_date, t_to_date, t_strgrp, t_str, t_int, t_date, from_datehis, to_datehis, readflag, coa_format, counter, lastprevmonthdate, firstmonthdate, tt_pbal2, gl_acct, gl_jouhdr, gl_journal, gl_jhdrhis, gl_jourhis, gl_department, gl_main, htparam, gl_accthis
        nonlocal acct_type, from_fibu, to_fibu, sorttype, from_dept, from_date, to_date, close_month, close_date, pnl_acct, close_year, prev_month, show_longbal, pbal_flag, asremoteflag


        nonlocal output_list, output_listhis, result_list, t_res_list, t_res_listhis, g_list, g_listpre, g_listhis
        nonlocal output_list_data, output_listhis_data, result_list_data, t_res_list_data, t_res_listhis_data, g_list_data, g_listpre_data, g_listhis_data

    try:
        # last_acct_close_priod = get_output(htpdate(795))
        last_acct_close_priod = htparam_map.get(795)
        # coa_format = get_output(htpchar(977))
        coa_format = htparam_map.get(977)
        num_acctype = 0

        gl_acct = db_session.query(Gl_acct).filter(
                (Gl_acct.fibukonto >= (from_fibu).lower()) & (Gl_acct.fibukonto <= (to_fibu).lower()) & ((Gl_acct.acc_type == 1) | (Gl_acct.acc_type == 2) | (Gl_acct.acc_type == 5))).first()

        if gl_acct:
            num_acctype = 1

        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(ge, from_fibu),(le, to_fibu)],"acc_type": [(eq, 3)]})
        gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto >= from_fibu) & (Gl_acct.fibukonto <= to_fibu) & (Gl_acct.acc_type == 3)).first()

        if gl_acct:
            num_acctype = num_acctype + 1

        # gl_acct = get_cache (Gl_acct, {"fibukonto": [(ge, from_fibu),(le, to_fibu)],"acc_type": [(eq, 4)]})
        gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto >= from_fibu) & (Gl_acct.fibukonto <= to_fibu) & (Gl_acct.acc_type == 4)).first()

        if gl_acct:
            num_acctype = num_acctype + 1

        t_from_date = from_date
        t_to_date = to_date
        from_date = None
        t_date = None
        firstmonthdate = date_mdy(get_month(close_date) , 1, get_year(close_date))
        lastprevmonthdate = firstmonthdate - timedelta(days=1)

        g_list_data.clear()

        # gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(le, lastday (t_from_date))]})
        gl_jouhdr = db_session.query(Gl_jouhdr).filter(Gl_jouhdr.datum <= lastday(t_from_date)).first()

        if gl_jouhdr:
            from_date = t_from_date
            to_date = t_to_date
            # create_glist()
        else:
            # gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(le, t_to_date)]})
            gl_jouhdr = db_session.query(Gl_jouhdr).filter(Gl_jouhdr.datum <= t_to_date).first()

            if gl_jouhdr:
                # for t_date in date_range(t_from_date,t_to_date) :

                #     gl_jouhdr = get_cache (Gl_jouhdr, {"datum": [(le, t_date)]})

                gl_jouhdr = db_session.query(Gl_jouhdr).filter((Gl_jouhdr.datum >= t_from_date) & (Gl_jouhdr.datum <= t_to_date)).first()

                if gl_jouhdr:
                    from_datehis = t_from_date
                    to_datehis = t_date - timedelta(days=1)

                    # create_glisthis()
                    from_date = t_date
                    to_date = t_to_date

                    # create_glist()
            else:
                from_datehis = t_from_date
                to_datehis = t_to_date

                # create_glisthis()

        prepare_cache_custom()

        if sorttype == 1:
            create_list1()
        else:
            create_list2()

    except Exception as e:
        lp.write_log("error", f"error: {traceback.format_exc()}")

    looping_session_only.close()

    return generate_output()