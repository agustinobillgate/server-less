from functions.additional_functions import *
import decimal
from datetime import date, timedelta
from sqlalchemy import func
from models import Htparam, Gl_jouhdr, Gl_acct, Gl_journal, Gl_department

def trialb_pnl_create_list_webbl(from_depart:int, from_date:date, to_date:date, close_month:int, sorttype:int, from_fibu:str, to_fibu:str, pnl_acct:str, pbal_flag:bool):
    summary_list_list = []
    detail_list_list = []
    sales:decimal = 0
    cost:decimal = 0
    gop_credit:decimal = 0
    gop_debit:decimal = 0
    tot_diff:decimal = 0
    close_date:date = None
    htparam = gl_jouhdr = gl_acct = gl_journal = gl_department = None

    g_list = summary_list = detail_list = gl_account = None

    g_list_list, G_list = create_model("G_list", {"grecid":int, "fibu":str})
    summary_list_list, Summary_list = create_model("Summary_list", {"acctno":str, "bezeich":str, "beg_balance":decimal, "t_debit":decimal, "t_credit":decimal, "net_change":decimal, "end_balance":decimal, "ytd_balance":decimal})
    detail_list_list, Detail_list = create_model("Detail_list", {"datum":date, "refno":str, "bezeich":str, "t_debit":decimal, "t_credit":decimal, "net_change":decimal, "end_balance":decimal, "note":str})

    Gl_account = Gl_acct

    db_session = local_storage.db_session

    def generate_output():
        nonlocal summary_list_list, detail_list_list, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal gl_account


        nonlocal g_list, summary_list, detail_list, gl_account
        nonlocal g_list_list, summary_list_list, detail_list_list
        return {"summary-list": summary_list_list, "detail-list": detail_list_list}

    def get_bemerk(bemerk:str):

        nonlocal summary_list_list, detail_list_list, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal gl_account


        nonlocal g_list, summary_list, detail_list, gl_account
        nonlocal g_list_list, summary_list_list, detail_list_list

        n:int = 0
        s1:str = ""
        n = 1 + get_index(bemerk, ";&&")

        if n > 0:
            return substring(bemerk, 0, n - 1)
        else:
            return bemerk

    def create_glist():

        nonlocal summary_list_list, detail_list_list, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal gl_account


        nonlocal g_list, summary_list, detail_list, gl_account
        nonlocal g_list_list, summary_list_list, detail_list_list


        g_list_list.clear()

        if from_depart > 0:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                    (Gl_jouhdr.datum >= from_date) &  (Gl_jouhdr.datum <= to_date)).all():

                gl_journal_obj_list = []
                for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.deptnr == from_depart)).filter(
                        (Gl_journal.jnr == gl_jouhdr.jnr)).all():
                    if gl_journal._recid in gl_journal_obj_list:
                        continue
                    else:
                        gl_journal_obj_list.append(gl_journal._recid)


                    g_list = G_list()
                    g_list_list.append(g_list)

                    g_list.grecid = gl_journal._recid
                    g_list.fibu = gl_journal.fibukonto

        else:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                    (Gl_jouhdr.datum >= from_date) &  (Gl_jouhdr.datum <= to_date)).all():

                gl_journal_obj_list = []
                for gl_journal, gl_acct in db_session.query(Gl_journal, Gl_acct).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto) &  (Gl_acct.acc_type != 3) &  (Gl_acct.acc_type != 4)).filter(
                        (Gl_journal.jnr == gl_jouhdr.jnr)).all():
                    if gl_journal._recid in gl_journal_obj_list:
                        continue
                    else:
                        gl_journal_obj_list.append(gl_journal._recid)


                    g_list = G_list()
                    g_list_list.append(g_list)

                    g_list.grecid = gl_journal._recid
                    g_list.fibu = gl_journal.fibukonto


    def create_trial_list1():

        nonlocal summary_list_list, detail_list_list, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal gl_account


        nonlocal g_list, summary_list, detail_list, gl_account
        nonlocal g_list_list, summary_list_list, detail_list_list

        konto:str = ""
        i:int = 0
        c:str = ""
        ind:int = 0
        curr_month:int = 0
        t_debit:decimal = 0
        t_credit:decimal = 0
        p_bal:decimal = 0
        t_bal:decimal = 0
        y_bal:decimal = 0
        tot_debit:decimal = 0
        tot_credit:decimal = 0
        t_ybal:decimal = 0
        tt_ybal:decimal = 0
        prev_bal:decimal = 0
        tot_bal:decimal = 0
        diff:decimal = 0
        tt_debit:decimal = 0
        tt_credit:decimal = 0
        tt_pbal:decimal = 0
        tt_bal:decimal = 0
        tt_diff:decimal = 0
        act_flag:int = 0
        n:int = 0
        Gl_account = Gl_acct
        sales = 0
        cost = 0
        gop_credit = 0
        gop_debit = 0
        tot_diff = 0

        if to_date <= date_mdy(get_month(close_date) , 1, get_year(close_date)) - timedelta(days=1):
            act_flag = 1
        curr_month = close_month

        if sorttype == 1:

            for gl_acct in db_session.query(Gl_acct).filter(
                    (func.lower(Gl_acct.fibukonto) >= (from_fibu).lower()) &  (func.lower(Gl_acct.fibukonto) <= (to_fibu).lower()) &  (Gl_acct.deptnr == from_depart) &  ((Gl_acct.acc_type == 1) |  (Gl_acct.acc_type == 2) |  (Gl_acct.acc_type == 5))).all():
                detail_list = Detail_list()
                detail_list_list.append(detail_list)

                c = convert_fibu(gl_acct.fibukonto)
                detail_list.refno = c
                detail_list.bezeich = gl_acct.bezeich
                t_debit = 0
                t_credit = 0
                p_bal = 0
                t_bal = 0
                konto = gl_acct.fibukonto

                for g_list in query(g_list_list, filters=(lambda g_list :g_list.fibu == gl_acct.fibukonto)):

                    gl_journal = db_session.query(Gl_journal).filter(
                            (Gl_journal._recid == g_list.grecid)).first()

                    gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                            (Gl_jouhdr.jnr == gl_journal.jnr)).first()
                    g_list_list.remove(g_list)

                    if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                        gop_credit = gop_credit + gl_journal.credit
                        gop_debit = gop_debit + gl_journal.debit

                    if gl_acct.acc_type == 1:
                        sales = sales + gl_journal.credit - gl_journal.debit

                    elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                        cost = cost + gl_journal.debit - gl_journal.credit
                    t_debit = t_debit + gl_journal.debit
                    t_credit = t_credit + gl_journal.credit

                    if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                        t_bal = t_bal - gl_journal.debit + gl_journal.credit
                    else:
                        t_bal = t_bal + gl_journal.debit - gl_journal.credit
                    tot_debit = tot_debit + gl_journal.debit
                    tot_credit = tot_credit + gl_journal.credit

                    if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                        tot_bal = tot_bal - gl_journal.debit + gl_journal.credit
                    else:
                        tot_bal = tot_bal + gl_journal.debit - gl_journal.credit
                    detail_list = Detail_list()
                    detail_list_list.append(detail_list)

                    detail_list.datum = gl_jouhdr.datum
                    detail_list.refno = gl_jouhdr.refno
                    detail_list.t_debit = gl_journal.debit
                    detail_list.t_credit = gl_journal.credit
                    detail_list.note = get_bemerk (gl_journal.bemerk)

                if p_bal != 0 or t_debit != 0 or t_credit != 0:

                    if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                        diff = t_credit - t_debit
                        tot_diff = tot_diff + t_credit - t_debit
                    else:
                        diff = t_debit - t_credit
                        tot_diff = tot_diff - t_credit + t_debit
                    detail_list = Detail_list()
                    detail_list_list.append(detail_list)

                    detail_list.refno = "T O T A L"
                    detail_list.t_debit = t_debit
                    detail_list.t_credit = t_credit
                    detail_list.net_change = diff
                    detail_list.end_balance = t_bal


                    detail_list = Detail_list()
                    detail_list_list.append(detail_list)

                else:
                    detail_list_list.remove(detail_list)

            if prev_bal != 0 or tot_debit != 0 or tot_credit != 0:
                detail_list = Detail_list()
                detail_list_list.append(detail_list)

                detail_list.refno = "Grand TOTAL"
                detail_list.t_debit = tot_debit
                detail_list.t_credit = tot_credit
                detail_list.net_change = tot_diff
                detail_list.end_balance = tot_bal

        elif sorttype == 2:

            for gl_department in db_session.query(Gl_department).filter(
                    (Gl_department.nr == from_depart)).all():
                prev_bal = 0
                tot_debit = 0
                tot_credit = 0
                t_ybal = 0
                tot_bal = 0
                diff = 0
                tot_diff = 0
                summary_list = Summary_list()
                summary_list_list.append(summary_list)
                print("Dept:", gl_department.bezeich)
                summary_list.bezeich = to_string(gl_department.nr, ">>9") + " - " + substring(gl_department.bezeich, 0, 32)

                for gl_acct in db_session.query(Gl_acct).filter(
                        (Gl_acct.deptnr == Gl_department.nr)).all():
                    t_debit = 0
                    t_credit = 0
                    p_bal = 0
                    t_bal = 0
                    y_bal = 0
                    konto = gl_acct.fibukonto

                    for g_list in query(g_list_list, filters=(lambda g_list :g_list.fibu == gl_acct.fibukonto)):

                        gl_journal = db_session.query(Gl_journal).filter(
                                (Gl_journal._recid == g_list.grecid)).first()

                        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                                (Gl_jouhdr.jnr == gl_journal.jnr)).first()
                        g_list_list.remove(g_list)

                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                            gop_credit = gop_credit + gl_journal.credit
                            gop_debit = gop_debit + gl_journal.debit

                        if gl_acct.acc_type == 1:
                            sales = sales + gl_journal.credit - gl_journal.debit

                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                            cost = cost + gl_journal.debit - gl_journal.credit
                        t_debit = t_debit + gl_journal.debit
                        t_credit = t_credit + gl_journal.credit
                        tot_debit = tot_debit + gl_journal.debit
                        tot_credit = tot_credit + gl_journal.credit
                        tt_debit = tt_debit + gl_journal.debit
                        tt_credit = tt_credit + gl_journal.credit

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            t_bal = t_bal - gl_journal.debit + gl_journal.credit
                        else:
                            t_bal = t_bal + gl_journal.debit - gl_journal.credit
                        tot_bal = tot_bal - gl_journal.debit + gl_journal.credit
                        tt_bal = tt_bal - gl_journal.debit + gl_journal.credit

                    if gl_acct.acc_type == 1:

                        if get_year(close_date) == get_year(to_date):
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal = p_bal - gl_acct.actual[n - 1]
                                y_bal = y_bal - gl_acct.actual[n - 1]

                        elif get_year(close_date) == get_year(to_date) + 1:
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal = p_bal - gl_acct.last_yr[n - 1]
                                y_bal = y_bal - gl_acct.last_yr[n - 1]
                        t_ybal = t_ybal + y_bal
                        tt_ybal = tt_ybal + y_bal

                    elif (gl_acct.acc_type == 2 or gl_acct.acc_type == 5):

                        if get_year(close_date) == get_year(to_date):
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal = p_bal + gl_acct.actual[n - 1]
                                y_bal = y_bal + gl_acct.actual[n - 1]

                        elif get_year(close_date) == get_year(to_date) - 1:
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal = p_bal + gl_acct.last_yr[n - 1]
                                y_bal = y_bal + gl_acct.last_yr[n - 1]
                        t_ybal = t_ybal - y_bal
                        tt_ybal = tt_ybal - y_bal

                    if p_bal != 0 or t_debit != 0 or t_credit != 0 or y_bal != 0:
                        summary_list = Summary_list()
                        summary_list_list.append(summary_list)

                        c = convert_fibu(gl_acct.fibukonto)
                        summary_list.acctno = c
                        summary_list.bezeich = gl_acct.bezeich
                        summary_list.beg_balance = p_bal
                        summary_list.t_debit = t_debit
                        summary_list.t_credit = t_credit

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            diff = - t_debit + t_credit
                        else:
                            diff = t_debit - t_credit
                        tot_diff = tot_diff + t_credit - t_debit
                        tt_diff = tt_diff + t_credit - t_debit
                        summary_list.net_change = diff
                        summary_list.end_balance = t_bal
                        summary_list.ytd_balance = y_bal


                summary_list = Summary_list()
                summary_list_list.append(summary_list)

                summary_list.bezeich = " s U B T O T A L"
                summary_list.beg_balance = prev_bal
                summary_list.t_debit = tot_debit
                summary_list.t_credit = tot_credit
                summary_list.net_change = tot_diff
                summary_list.end_bal = tot_bal
                summary_list.ytd_bal = t_ybal


                summary_list = Summary_list()
                summary_list_list.append(summary_list)

            summary_list = Summary_list()
            summary_list_list.append(summary_list)

            summary_list.bezeich = "T O T A L"
            summary_list.beg_bal = tt_pbal
            summary_list.t_debit = tt_debit
            summary_list.t_credit = tt_credit
            summary_list.net_change = tt_diff
            summary_list.end_bal = tt_bal
            summary_list.ytd_bal = tt_ybal

    def create_trial_list2():

        nonlocal summary_list_list, detail_list_list, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal gl_account


        nonlocal g_list, summary_list, detail_list, gl_account
        nonlocal g_list_list, summary_list_list, detail_list_list

        konto:str = ""
        i:int = 0
        c:str = ""
        ind:int = 0
        curr_month:int = 0
        t_debit:decimal = 0
        t_credit:decimal = 0
        p_bal:decimal = 0
        t_bal:decimal = 0
        y_bal:decimal = 0
        tot_debit:decimal = 0
        tot_credit:decimal = 0
        t_ybal:decimal = 0
        tt_ybal:decimal = 0
        prev_bal:decimal = 0
        tot_bal:decimal = 0
        diff:decimal = 0
        tt_debit:decimal = 0
        tt_credit:decimal = 0
        tt_pbal:decimal = 0
        tt_bal:decimal = 0
        tt_diff:decimal = 0
        act_flag:int = 0
        n:int = 0
        Gl_account = Gl_acct
        sales = 0
        cost = 0
        gop_credit = 0
        gop_debit = 0
        tot_diff = 0

        if to_date <= date_mdy(get_month(close_date) , 1, get_year(close_date)) - timedelta(days=1):
            act_flag = 1
        curr_month = close_month

        if sorttype == 1:

            for gl_department in db_session.query(Gl_department).filter(
                    (Gl_department.nr > 0)).all():
                detail_list = Detail_list()
                detail_list_list.append(detail_list)

                detail_list = Detail_list()
                detail_list_list.append(detail_list)

                detail_list.bezeich = gl_department.bezeich

                for gl_acct in db_session.query(Gl_acct).filter(
                        (func.lower(Gl_acct.fibukonto) >= (from_fibu).lower()) &  (func.lower(Gl_acct.fibukonto) <= (to_fibu).lower()) &  (Gl_acct.deptnr == gl_department.nr) &  ((Gl_acct.acc_type == 1) |  (Gl_acct.acc_type == 2) |  (Gl_acct.acc_type == 5))).all():
                    c = convert_fibu(gl_acct.fibukonto)
                    detail_list = Detail_list()
                    detail_list_list.append(detail_list)

                    detail_list.refno = c
                    detail_list.bezeich = gl_acct.bezeich


                    t_debit = 0
                    t_credit = 0
                    p_bal = 0
                    t_bal = 0
                    konto = gl_acct.fibukonto

                    for g_list in query(g_list_list, filters=(lambda g_list :g_list.fibu == gl_acct.fibukonto)):

                        gl_journal = db_session.query(Gl_journal).filter(
                                (Gl_journal._recid == g_list.grecid)).first()

                        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                                (Gl_jouhdr.jnr == gl_journal.jnr)).first()
                        g_list_list.remove(g_list)

                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                            gop_credit = gop_credit + gl_journal.credit
                            gop_debit = gop_debit + gl_journal.debit

                        if gl_acct.acc_type == 1:
                            sales = sales + gl_journal.credit - gl_journal.debit

                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                            cost = cost + gl_journal.debit - gl_journal.credit
                        t_debit = t_debit + gl_journal.debit
                        t_credit = t_credit + gl_journal.credit

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            t_bal = t_bal - gl_journal.debit + gl_journal.credit
                        else:
                            t_bal = t_bal + gl_journal.debit - gl_journal.credit
                        tot_debit = tot_debit + gl_journal.debit
                        tot_credit = tot_credit + gl_journal.credit

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            tot_bal = tot_bal - gl_journal.debit + gl_journal.credit
                        else:
                            tot_bal = tot_bal + gl_journal.debit - gl_journal.credit
                        detail_list = Detail_list()
                        detail_list_list.append(detail_list)

                        detail_list.datum = gl_jouhdr.datum
                        detail_list.refno = gl_jouhdr.refno
                        detail_list.t_debit = gl_journal.debit
                        detail_list.t_credit = gl_journal.credit
                        detail_list.note = get_bemerk (gl_journal.bemerk)

                    if p_bal != 0 or t_debit != 0 or t_credit != 0:

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            diff = t_credit - t_debit
                            tot_diff = tot_diff + t_credit - t_debit
                        else:
                            diff = t_debit - t_credit
                            tot_diff = tot_diff - t_credit + t_debit
                        detail_list = Detail_list()
                        detail_list_list.append(detail_list)

                        detail_list.refno = "T O T A L"
                        detail_list.t_debit = t_debit
                        detail_list.t_credit = t_credit
                        detail_list.net_change = diff
                        detail_list.end_bal = t_bal


                        detail_list = Detail_list()
                        detail_list_list.append(detail_list)

                    else:
                        detail_list_list.remove(detail_list)


        if sorttype == 1 and (prev_bal != 0 or tot_debit != 0 or tot_credit != 0):
            tot_diff = tot_credit - tot_debit
            tot_bal = tot_diff
            detail_list = Detail_list()
            detail_list_list.append(detail_list)

            detail_list.refno = "Grand TOTAL"
            detail_list.t_debit = tot_debit
            detail_list.t_credit = tot_credit
            detail_list.net_change = tot_diff
            detail_list.end_bal = tot_bal

        if sorttype == 2:

            gl_department_obj_list = []
            for gl_department, gl_account in db_session.query(Gl_department, Gl_account).join(Gl_account,(Gl_account.deptnr == Gl_department.nr)).filter(
                    (Gl_department.nr > 0)).all():
                if gl_department._recid in gl_department_obj_list:
                    continue
                else:
                    gl_department_obj_list.append(gl_department._recid)


                prev_bal = 0
                tot_debit = 0
                tot_credit = 0
                t_ybal = 0
                tot_bal = 0
                diff = 0
                tot_diff = 0
                summary_list = Summary_list()
                summary_list_list.append(summary_list)

                summary_list.bezeich = to_string(gl_department.nr, ">>9") + " - " +\
                        substring(gl_department.bezeich, 0, 32)

                for gl_acct in db_session.query(Gl_acct).filter(
                        (Gl_acct.deptnr == gl_department.nr)).all():
                    t_debit = 0
                    t_credit = 0
                    p_bal = 0
                    t_bal = 0
                    y_bal = 0
                    konto = gl_acct.fibukonto

                    for g_list in query(g_list_list, filters=(lambda g_list :g_list.fibu == gl_acct.fibukonto)):

                        gl_journal = db_session.query(Gl_journal).filter(
                                (Gl_journal._recid == g_list.grecid)).first()

                        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                                (Gl_jouhdr.jnr == gl_journal.jnr)).first()
                        g_list_list.remove(g_list)

                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                            gop_credit = gop_credit + gl_journal.credit
                            gop_debit = gop_debit + gl_journal.debit

                        if gl_acct.acc_type == 1:
                            sales = sales + gl_journal.credit - gl_journal.debit

                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                            cost = cost + gl_journal.debit - gl_journal.credit
                        t_debit = t_debit + gl_journal.debit
                        t_credit = t_credit + gl_journal.credit
                        tot_debit = tot_debit + gl_journal.debit
                        tot_credit = tot_credit + gl_journal.credit
                        tt_debit = tt_debit + gl_journal.debit
                        tt_credit = tt_credit + gl_journal.credit

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            t_bal = t_bal - gl_journal.debit + gl_journal.credit
                        else:
                            t_bal = t_bal + gl_journal.debit - gl_journal.credit
                        tot_bal = tot_bal - gl_journal.debit + gl_journal.credit
                        tt_bal = tt_bal - gl_journal.debit + gl_journal.credit

                    if gl_acct.acc_type == 1:

                        if get_year(close_date) == get_year(to_date):
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal = p_bal - gl_acct.actual[n - 1]
                                y_bal = y_bal - gl_acct.actual[n - 1]

                        elif get_year(close_date) == get_year(to_date) + 1:
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal = p_bal - gl_acct.last_yr[n - 1]
                                y_bal = y_bal - gl_acct.last_yr[n - 1]
                        t_ybal = t_ybal + y_bal
                        tt_ybal = tt_ybal + y_bal

                    elif (gl_acct.acc_type == 2 or gl_acct.acc_type == 5):

                        if get_year(close_date) == get_year(to_date):
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal = p_bal + gl_acct.actual[n - 1]
                                y_bal = y_bal + gl_acct.actual[n - 1]

                        elif get_year(close_date) == get_year(to_date) - 1:
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal = p_bal + gl_acct.last_yr[n - 1]
                                y_bal = y_bal + gl_acct.last_yr[n - 1]
                        t_ybal = t_ybal - y_bal
                        tt_ybal = tt_ybal - y_bal

                    if p_bal != 0 or t_debit != 0 or t_credit != 0 or y_bal != 0:
                        c = convert_fibu(gl_acct.fibukonto)
                        summary_list = Summary_list()
                        summary_list_list.append(summary_list)

                        summary_list.acctno = c
                        summary_list.bezeich = gl_acct.bezeich
                        summary_list.beg_bal = p_bal
                        summary_list.t_debit = t_debit
                        summary_list.t_credit = t_credit

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            diff = - t_debit + t_credit
                        else:
                            diff = t_debit - t_credit
                        tot_diff = tot_diff + t_credit - t_debit
                        tt_diff = tt_diff + t_credit - t_debit
                        summary_list.net_change = diff
                        summary_list.end_bal = t_bal
                        summary_list.ytd_bal = y_bal


                summary_list = Summary_list()
                summary_list_list.append(summary_list)

                summary_list.bezeich = "s U B T O T A L"
                summary_list.beg_bal = prev_bal
                summary_list.t_debit = tot_debit
                summary_list.t_credit = tot_credit
                summary_list.net_change = tot_diff
                summary_list.end_bal = tot_bal
                summary_list.ytd_bal = t_ybal


                summary_list = Summary_list()
                summary_list_list.append(summary_list)

            summary_list = Summary_list()
            summary_list_list.append(summary_list)

            summary_list.bezeich = "T O T A L"
            summary_list.beg_bal = tt_pbal
            summary_list.t_debit = tt_debit
            summary_list.t_credit = tt_credit
            summary_list.net_change = tt_diff
            summary_list.end_bal = tt_bal
            summary_list.ytd_bal = tt_ybal

    def convert_fibu(konto:str):

        nonlocal summary_list_list, detail_list_list, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal gl_account


        nonlocal g_list, summary_list, detail_list, gl_account
        nonlocal g_list_list, summary_list_list, detail_list_list

        s = ""
        ch:str = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return s

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 977)).first()
        ch = htparam.fchar
        j = 0
        for i in range(1,len(ch)  + 1) :

            if substring(ch, i - 1, 1) >= "0" and substring(ch, i - 1, 1) <= "9":
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)


        return generate_inner_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 597)).first()
    close_date = htparam.fdate
    create_glist()

    if from_depart > 0:
        create_trial_list1()
    else:
        create_trial_list2()

    return generate_output()