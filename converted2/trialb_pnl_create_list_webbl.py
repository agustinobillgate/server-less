#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Gl_jouhdr, Gl_acct, Gl_journal, Gl_department

def trialb_pnl_create_list_webbl(from_depart:int, from_date:date, to_date:date, close_month:int, sorttype:int, from_fibu:string, to_fibu:string, pnl_acct:string, pbal_flag:bool):

    prepare_cache ([Htparam, Gl_jouhdr, Gl_acct, Gl_journal, Gl_department])

    summary_list_data = []
    detail_list_data = []
    sales:Decimal = to_decimal("0.0")
    cost:Decimal = to_decimal("0.0")
    gop_credit:Decimal = to_decimal("0.0")
    gop_debit:Decimal = to_decimal("0.0")
    tot_diff:Decimal = to_decimal("0.0")
    close_date:date = None
    htparam = gl_jouhdr = gl_acct = gl_journal = gl_department = None

    g_list = summary_list = detail_list = None

    g_list_data, G_list = create_model("G_list", {"grecid":int, "fibu":string})
    summary_list_data, Summary_list = create_model("Summary_list", {"acctno":string, "bezeich":string, "beg_balance":Decimal, "t_debit":Decimal, "t_credit":Decimal, "net_change":Decimal, "end_balance":Decimal, "ytd_balance":Decimal})
    detail_list_data, Detail_list = create_model("Detail_list", {"datum":date, "refno":string, "bezeich":string, "t_debit":Decimal, "t_credit":Decimal, "net_change":Decimal, "end_balance":Decimal, "note":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal summary_list_data, detail_list_data, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal from_depart, from_date, to_date, close_month, sorttype, from_fibu, to_fibu, pnl_acct, pbal_flag


        nonlocal g_list, summary_list, detail_list
        nonlocal g_list_data, summary_list_data, detail_list_data

        return {"summary-list": summary_list_data, "detail-list": detail_list_data}

    def get_bemerk(bemerk:string):

        nonlocal summary_list_data, detail_list_data, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal from_depart, from_date, to_date, close_month, sorttype, from_fibu, to_fibu, pnl_acct, pbal_flag


        nonlocal g_list, summary_list, detail_list
        nonlocal g_list_data, summary_list_data, detail_list_data

        n:int = 0
        s1:string = ""
        n = get_index(bemerk, ";&&")

        if n > 0:
            return substring(bemerk, 0, n - 1)
        else:
            return bemerk


    def create_glist():

        nonlocal summary_list_data, detail_list_data, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal from_depart, from_date, to_date, close_month, sorttype, from_fibu, to_fibu, pnl_acct, pbal_flag


        nonlocal g_list, summary_list, detail_list
        nonlocal g_list_data, summary_list_data, detail_list_data


        g_list_data.clear()

        if from_depart > 0:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum).all():

                gl_journal_obj_list = {}
                gl_journal = Gl_journal()
                gl_acct = Gl_acct()
                for gl_journal._recid, gl_journal.fibukonto, gl_journal.jnr, gl_journal.credit, gl_journal.debit, gl_journal.bemerk, gl_acct.fibukonto, gl_acct.bezeich, gl_acct.acc_type, gl_acct.actual, gl_acct.last_yr, gl_acct._recid in db_session.query(Gl_journal._recid, Gl_journal.fibukonto, Gl_journal.jnr, Gl_journal.credit, Gl_journal.debit, Gl_journal.bemerk, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct.acc_type, Gl_acct.actual, Gl_acct.last_yr, Gl_acct._recid).join(Gl_acct,(Gl_acct.deptnr == from_depart)).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                    if gl_journal_obj_list.get(gl_journal._recid):
                        continue
                    else:
                        gl_journal_obj_list[gl_journal._recid] = True


                    g_list = G_list()
                    g_list_data.append(g_list)

                    g_list.grecid = gl_journal._recid
                    g_list.fibu = gl_journal.fibukonto

        else:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                     (Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date)).order_by(Gl_jouhdr.datum).all():

                gl_journal_obj_list = {}
                gl_journal = Gl_journal()
                gl_acct = Gl_acct()
                for gl_journal._recid, gl_journal.fibukonto, gl_journal.jnr, gl_journal.credit, gl_journal.debit, gl_journal.bemerk, gl_acct.fibukonto, gl_acct.bezeich, gl_acct.acc_type, gl_acct.actual, gl_acct.last_yr, gl_acct._recid in db_session.query(Gl_journal._recid, Gl_journal.fibukonto, Gl_journal.jnr, Gl_journal.credit, Gl_journal.debit, Gl_journal.bemerk, Gl_acct.fibukonto, Gl_acct.bezeich, Gl_acct.acc_type, Gl_acct.actual, Gl_acct.last_yr, Gl_acct._recid).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto) & (Gl_acct.acc_type != 3) & (Gl_acct.acc_type != 4)).filter(
                         (Gl_journal.jnr == gl_jouhdr.jnr)).order_by(Gl_journal._recid).all():
                    if gl_journal_obj_list.get(gl_journal._recid):
                        continue
                    else:
                        gl_journal_obj_list[gl_journal._recid] = True


                    g_list = G_list()
                    g_list_data.append(g_list)

                    g_list.grecid = gl_journal._recid
                    g_list.fibu = gl_journal.fibukonto

    def create_trial_list1():

        nonlocal summary_list_data, detail_list_data, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal from_depart, from_date, to_date, close_month, sorttype, from_fibu, to_fibu, pnl_acct, pbal_flag


        nonlocal g_list, summary_list, detail_list
        nonlocal g_list_data, summary_list_data, detail_list_data

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
        diff:Decimal = to_decimal("0.0")
        tt_debit:Decimal = to_decimal("0.0")
        tt_credit:Decimal = to_decimal("0.0")
        tt_pbal:Decimal = to_decimal("0.0")
        tt_bal:Decimal = to_decimal("0.0")
        tt_diff:Decimal = to_decimal("0.0")
        act_flag:int = 0
        n:int = 0
        gl_account = None
        tmp_date:date = None
        Gl_account =  create_buffer("Gl_account",Gl_acct)
        tmp_date = date_mdy(get_month(close_date) , 1, get_year(close_date))
        tmp_date = tmp_date - timedelta(days=1)
        sales =  to_decimal("0")
        cost =  to_decimal("0")
        gop_credit =  to_decimal("0")
        gop_debit =  to_decimal("0")
        tot_diff =  to_decimal("0")

        if to_date <= tmp_date:
            act_flag = 1
        curr_month = close_month

        if sorttype == 1:

            for gl_acct in db_session.query(Gl_acct).filter(
                     (Gl_acct.fibukonto >= (from_fibu).lower()) & (Gl_acct.fibukonto <= (to_fibu).lower()) & (Gl_acct.deptnr == from_depart) & ((Gl_acct.acc_type == 1) | (Gl_acct.acc_type == 2) | (Gl_acct.acc_type == 5))).order_by(Gl_acct.fibukonto).all():
                detail_list = Detail_list()
                detail_list_data.append(detail_list)

                c = convert_fibu(gl_acct.fibukonto)
                detail_list.refno = c
                detail_list.bezeich = gl_acct.bezeich
                t_debit =  to_decimal("0")
                t_credit =  to_decimal("0")
                p_bal =  to_decimal("0")
                t_bal =  to_decimal("0")
                konto = gl_acct.fibukonto

                for g_list in query(g_list_data, filters=(lambda g_list: g_list.fibu == gl_acct.fibukonto)):

                    gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                    gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})
                    g_list_data.remove(g_list)

                    if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                        gop_credit =  to_decimal(gop_credit) + to_decimal(gl_journal.credit)
                        gop_debit =  to_decimal(gop_debit) + to_decimal(gl_journal.debit)

                    if gl_acct.acc_type == 1:
                        sales =  to_decimal(sales) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)

                    elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                        cost =  to_decimal(cost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                    t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                    t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)

                    if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                        t_bal =  to_decimal(t_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                    else:
                        t_bal =  to_decimal(t_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                    tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
                    tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)

                    if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                        tot_bal =  to_decimal(tot_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                    else:
                        tot_bal =  to_decimal(tot_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                    detail_list = Detail_list()
                    detail_list_data.append(detail_list)

                    detail_list.datum = gl_jouhdr.datum
                    detail_list.refno = gl_jouhdr.refno
                    detail_list.t_debit =  to_decimal(gl_journal.debit)
                    detail_list.t_credit =  to_decimal(gl_journal.credit)
                    detail_list.note = get_bemerk (gl_journal.bemerk)

                if p_bal != 0 or t_debit != 0 or t_credit != 0:

                    if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                        diff =  to_decimal(t_credit) - to_decimal(t_debit)
                        tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                    else:
                        diff =  to_decimal(t_debit) - to_decimal(t_credit)
                        tot_diff =  to_decimal(tot_diff) - to_decimal(t_credit) + to_decimal(t_debit)
                    detail_list = Detail_list()
                    detail_list_data.append(detail_list)

                    detail_list.refno = "T O T A L"
                    detail_list.t_debit =  to_decimal(t_debit)
                    detail_list.t_credit =  to_decimal(t_credit)
                    detail_list.net_change =  to_decimal(diff)
                    detail_list.end_balance =  to_decimal(t_bal)


                    detail_list = Detail_list()
                    detail_list_data.append(detail_list)

                else:
                    detail_list_data.remove(detail_list)

            if prev_bal != 0 or tot_debit != 0 or tot_credit != 0:
                detail_list = Detail_list()
                detail_list_data.append(detail_list)

                detail_list.refno = "Grand TOTAL"
                detail_list.t_debit =  to_decimal(tot_debit)
                detail_list.t_credit =  to_decimal(tot_credit)
                detail_list.net_change =  to_decimal(tot_diff)
                detail_list.end_balance =  to_decimal(tot_bal)

        elif sorttype == 2:

            for gl_department in db_session.query(Gl_department).filter(
                     (Gl_department.nr == from_depart)).order_by(Gl_department._recid).all():
                prev_bal =  to_decimal("0")
                tot_debit =  to_decimal("0")
                tot_credit =  to_decimal("0")
                t_ybal =  to_decimal("0")
                tot_bal =  to_decimal("0")
                diff =  to_decimal("0")
                tot_diff =  to_decimal("0")
                summary_list = Summary_list()
                summary_list_data.append(summary_list)

                summary_list.bezeich = to_string(gl_department.nr, ">>9") + " - " + substring(gl_department.bezeich, 0, 32)

                for gl_acct in db_session.query(Gl_acct).filter(
                         (Gl_acct.deptnr == gl_department.nr)).order_by(Gl_acct.fibukonto).all():
                    t_debit =  to_decimal("0")
                    t_credit =  to_decimal("0")
                    p_bal =  to_decimal("0")
                    t_bal =  to_decimal("0")
                    y_bal =  to_decimal("0")
                    konto = gl_acct.fibukonto

                    for g_list in query(g_list_data, filters=(lambda g_list: g_list.fibu == gl_acct.fibukonto)):

                        gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                        gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})
                        g_list_data.remove(g_list)

                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_journal.credit)
                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_journal.debit)

                        if gl_acct.acc_type == 1:
                            sales =  to_decimal(sales) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)

                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                            cost =  to_decimal(cost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                        t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                        t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)
                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)
                        tt_debit =  to_decimal(tt_debit) + to_decimal(gl_journal.debit)
                        tt_credit =  to_decimal(tt_credit) + to_decimal(gl_journal.credit)

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            t_bal =  to_decimal(t_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                        else:
                            t_bal =  to_decimal(t_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                        tot_bal =  to_decimal(tot_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                        tt_bal =  to_decimal(tt_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)

                    if gl_acct.acc_type == 1:

                        if get_year(close_date) == get_year(to_date):
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal =  to_decimal(p_bal) - to_decimal(gl_acct.actual[n - 1])
                                y_bal =  to_decimal(y_bal) - to_decimal(gl_acct.actual[n - 1])

                        elif get_year(close_date) == get_year(to_date) + 1:
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal =  to_decimal(p_bal) - to_decimal(gl_acct.last_yr[n - 1])
                                y_bal =  to_decimal(y_bal) - to_decimal(gl_acct.last_yr[n - 1])
                        t_ybal =  to_decimal(t_ybal) + to_decimal(y_bal)
                        tt_ybal =  to_decimal(tt_ybal) + to_decimal(y_bal)

                    elif (gl_acct.acc_type == 2 or gl_acct.acc_type == 5):

                        if get_year(close_date) == get_year(to_date):
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal =  to_decimal(p_bal) + to_decimal(gl_acct.actual[n - 1])
                                y_bal =  to_decimal(y_bal) + to_decimal(gl_acct.actual[n - 1])

                        elif get_year(close_date) == get_year(to_date) - 1:
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal =  to_decimal(p_bal) + to_decimal(gl_acct.last_yr[n - 1])
                                y_bal =  to_decimal(y_bal) + to_decimal(gl_acct.last_yr[n - 1])
                        t_ybal =  to_decimal(t_ybal) - to_decimal(y_bal)
                        tt_ybal =  to_decimal(tt_ybal) - to_decimal(y_bal)

                    if p_bal != 0 or t_debit != 0 or t_credit != 0 or y_bal != 0:
                        summary_list = Summary_list()
                        summary_list_data.append(summary_list)

                        c = convert_fibu(gl_acct.fibukonto)
                        summary_list.acctno = c
                        summary_list.bezeich = gl_acct.bezeich
                        summary_list.beg_balance =  to_decimal(p_bal)
                        summary_list.t_debit =  to_decimal(t_debit)
                        summary_list.t_credit =  to_decimal(t_credit)

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            diff =  - to_decimal(t_debit) + to_decimal(t_credit)
                        else:
                            diff =  to_decimal(t_debit) - to_decimal(t_credit)
                        tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                        tt_diff =  to_decimal(tt_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                        summary_list.net_change =  to_decimal(diff)
                        summary_list.end_balance =  to_decimal(t_bal)
                        summary_list.ytd_balance =  to_decimal(y_bal)


                summary_list = Summary_list()
                summary_list_data.append(summary_list)

                summary_list.bezeich = " s U B T O T A L"
                summary_list.beg_balance =  to_decimal(prev_bal)
                summary_list.t_debit =  to_decimal(tot_debit)
                summary_list.t_credit =  to_decimal(tot_credit)
                summary_list.net_change =  to_decimal(tot_diff)
                summary_list.end_bal =  to_decimal(tot_bal)
                summary_list.ytd_bal =  to_decimal(t_ybal)


                summary_list = Summary_list()
                summary_list_data.append(summary_list)

            summary_list = Summary_list()
            summary_list_data.append(summary_list)

            summary_list.bezeich = "T O T A L"
            summary_list.beg_bal =  to_decimal(tt_pbal)
            summary_list.t_debit =  to_decimal(tt_debit)
            summary_list.t_credit =  to_decimal(tt_credit)
            summary_list.net_change =  to_decimal(tt_diff)
            summary_list.end_bal =  to_decimal(tt_bal)
            summary_list.ytd_bal =  to_decimal(tt_ybal)


    def create_trial_list2():

        nonlocal summary_list_data, detail_list_data, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal from_depart, from_date, to_date, close_month, sorttype, from_fibu, to_fibu, pnl_acct, pbal_flag


        nonlocal g_list, summary_list, detail_list
        nonlocal g_list_data, summary_list_data, detail_list_data

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
        diff:Decimal = to_decimal("0.0")
        tt_debit:Decimal = to_decimal("0.0")
        tt_credit:Decimal = to_decimal("0.0")
        tt_pbal:Decimal = to_decimal("0.0")
        tt_bal:Decimal = to_decimal("0.0")
        tt_diff:Decimal = to_decimal("0.0")
        act_flag:int = 0
        n:int = 0
        gl_account = None
        tmp_date:date = None
        Gl_account =  create_buffer("Gl_account",Gl_acct)
        tmp_date = date_mdy(get_month(close_date) , 1, get_year(close_date))
        tmp_date = tmp_date - timedelta(days=1)
        sales =  to_decimal("0")
        cost =  to_decimal("0")
        gop_credit =  to_decimal("0")
        gop_debit =  to_decimal("0")
        tot_diff =  to_decimal("0")

        if to_date <= tmp_date:
            act_flag = 1
        curr_month = close_month

        if sorttype == 1:

            for gl_department in db_session.query(Gl_department).filter(
                     (Gl_department.nr > 0)).order_by(Gl_department.nr).all():
                detail_list = Detail_list()
                detail_list_data.append(detail_list)

                detail_list = Detail_list()
                detail_list_data.append(detail_list)

                detail_list.bezeich = gl_department.bezeich

                for gl_acct in db_session.query(Gl_acct).filter(
                         (Gl_acct.fibukonto >= (from_fibu).lower()) & (Gl_acct.fibukonto <= (to_fibu).lower()) & (Gl_acct.deptnr == gl_department.nr) & ((Gl_acct.acc_type == 1) | (Gl_acct.acc_type == 2) | (Gl_acct.acc_type == 5))).order_by(Gl_acct.fibukonto).all():
                    c = convert_fibu(gl_acct.fibukonto)
                    detail_list = Detail_list()
                    detail_list_data.append(detail_list)

                    detail_list.refno = c
                    detail_list.bezeich = gl_acct.bezeich


                    t_debit =  to_decimal("0")
                    t_credit =  to_decimal("0")
                    p_bal =  to_decimal("0")
                    t_bal =  to_decimal("0")
                    konto = gl_acct.fibukonto

                    for g_list in query(g_list_data, filters=(lambda g_list: g_list.fibu == gl_acct.fibukonto)):

                        gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                        gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})
                        g_list_data.remove(g_list)

                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_journal.credit)
                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_journal.debit)

                        if gl_acct.acc_type == 1:
                            sales =  to_decimal(sales) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)

                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                            cost =  to_decimal(cost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                        t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                        t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            t_bal =  to_decimal(t_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                        else:
                            t_bal =  to_decimal(t_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            tot_bal =  to_decimal(tot_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                        else:
                            tot_bal =  to_decimal(tot_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                        detail_list = Detail_list()
                        detail_list_data.append(detail_list)

                        detail_list.datum = gl_jouhdr.datum
                        detail_list.refno = gl_jouhdr.refno
                        detail_list.t_debit =  to_decimal(gl_journal.debit)
                        detail_list.t_credit =  to_decimal(gl_journal.credit)
                        detail_list.note = get_bemerk (gl_journal.bemerk)

                    if p_bal != 0 or t_debit != 0 or t_credit != 0:

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            diff =  to_decimal(t_credit) - to_decimal(t_debit)
                            tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                        else:
                            diff =  to_decimal(t_debit) - to_decimal(t_credit)
                            tot_diff =  to_decimal(tot_diff) - to_decimal(t_credit) + to_decimal(t_debit)
                        detail_list = Detail_list()
                        detail_list_data.append(detail_list)

                        detail_list.refno = "T O T A L"
                        detail_list.t_debit =  to_decimal(t_debit)
                        detail_list.t_credit =  to_decimal(t_credit)
                        detail_list.net_change =  to_decimal(diff)
                        detail_list.end_bal =  to_decimal(t_bal)


                        detail_list = Detail_list()
                        detail_list_data.append(detail_list)

                    else:
                        detail_list_data.remove(detail_list)


        if sorttype == 1 and (prev_bal != 0 or tot_debit != 0 or tot_credit != 0):
            tot_diff =  to_decimal(tot_credit) - to_decimal(tot_debit)
            tot_bal =  to_decimal(tot_diff)
            detail_list = Detail_list()
            detail_list_data.append(detail_list)

            detail_list.refno = "Grand TOTAL"
            detail_list.t_debit =  to_decimal(tot_debit)
            detail_list.t_credit =  to_decimal(tot_credit)
            detail_list.net_change =  to_decimal(tot_diff)
            detail_list.end_bal =  to_decimal(tot_bal)

        if sorttype == 2:

            gl_department_obj_list = {}
            gl_department = Gl_department()
            gl_account = Gl_acct()
            for gl_department.nr, gl_department.bezeich, gl_department._recid, gl_account.fibukonto, gl_account.bezeich, gl_account.acc_type, gl_account.actual, gl_account.last_yr, gl_account._recid in db_session.query(Gl_department.nr, Gl_department.bezeich, Gl_department._recid, Gl_account.fibukonto, Gl_account.bezeich, Gl_account.acc_type, Gl_account.actual, Gl_account.last_yr, Gl_account._recid).join(Gl_account,(Gl_account.deptnr == Gl_department.nr)).filter(
                     (Gl_department.nr > 0)).order_by(Gl_department.nr).all():
                if gl_department_obj_list.get(gl_department._recid):
                    continue
                else:
                    gl_department_obj_list[gl_department._recid] = True


                prev_bal =  to_decimal("0")
                tot_debit =  to_decimal("0")
                tot_credit =  to_decimal("0")
                t_ybal =  to_decimal("0")
                tot_bal =  to_decimal("0")
                diff =  to_decimal("0")
                tot_diff =  to_decimal("0")
                summary_list = Summary_list()
                summary_list_data.append(summary_list)

                summary_list.bezeich = to_string(gl_department.nr, ">>9") + " - " +\
                        substring(gl_department.bezeich, 0, 32)

                for gl_acct in db_session.query(Gl_acct).filter(
                         (Gl_acct.deptnr == gl_department.nr)).order_by(Gl_acct.fibukonto).all():
                    t_debit =  to_decimal("0")
                    t_credit =  to_decimal("0")
                    p_bal =  to_decimal("0")
                    t_bal =  to_decimal("0")
                    y_bal =  to_decimal("0")
                    konto = gl_acct.fibukonto

                    for g_list in query(g_list_data, filters=(lambda g_list: g_list.fibu == gl_acct.fibukonto)):

                        gl_journal = get_cache (Gl_journal, {"_recid": [(eq, g_list.grecid)]})

                        gl_jouhdr = get_cache (Gl_jouhdr, {"jnr": [(eq, gl_journal.jnr)]})
                        g_list_data.remove(g_list)

                        if gl_acct.fibukonto.lower()  == (pnl_acct).lower() :
                            gop_credit =  to_decimal(gop_credit) + to_decimal(gl_journal.credit)
                            gop_debit =  to_decimal(gop_debit) + to_decimal(gl_journal.debit)

                        if gl_acct.acc_type == 1:
                            sales =  to_decimal(sales) + to_decimal(gl_journal.credit) - to_decimal(gl_journal.debit)

                        elif gl_acct.acc_type == 2 or gl_acct.acc_type == 5:
                            cost =  to_decimal(cost) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                        t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
                        t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)
                        tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
                        tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)
                        tt_debit =  to_decimal(tt_debit) + to_decimal(gl_journal.debit)
                        tt_credit =  to_decimal(tt_credit) + to_decimal(gl_journal.credit)

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            t_bal =  to_decimal(t_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                        else:
                            t_bal =  to_decimal(t_bal) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)
                        tot_bal =  to_decimal(tot_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
                        tt_bal =  to_decimal(tt_bal) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)

                    if gl_acct.acc_type == 1:

                        if get_year(close_date) == get_year(to_date):
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal =  to_decimal(p_bal) - to_decimal(gl_acct.actual[n - 1])
                                y_bal =  to_decimal(y_bal) - to_decimal(gl_acct.actual[n - 1])

                        elif get_year(close_date) == get_year(to_date) + 1:
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal =  to_decimal(p_bal) - to_decimal(gl_acct.last_yr[n - 1])
                                y_bal =  to_decimal(y_bal) - to_decimal(gl_acct.last_yr[n - 1])
                        t_ybal =  to_decimal(t_ybal) + to_decimal(y_bal)
                        tt_ybal =  to_decimal(tt_ybal) + to_decimal(y_bal)

                    elif (gl_acct.acc_type == 2 or gl_acct.acc_type == 5):

                        if get_year(close_date) == get_year(to_date):
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal =  to_decimal(p_bal) + to_decimal(gl_acct.actual[n - 1])
                                y_bal =  to_decimal(y_bal) + to_decimal(gl_acct.actual[n - 1])

                        elif get_year(close_date) == get_year(to_date) - 1:
                            for n in range(1,get_month(to_date)  + 1) :

                                if n < get_month(to_date) and pbal_flag:
                                    p_bal =  to_decimal(p_bal) + to_decimal(gl_acct.last_yr[n - 1])
                                y_bal =  to_decimal(y_bal) + to_decimal(gl_acct.last_yr[n - 1])
                        t_ybal =  to_decimal(t_ybal) - to_decimal(y_bal)
                        tt_ybal =  to_decimal(tt_ybal) - to_decimal(y_bal)

                    if p_bal != 0 or t_debit != 0 or t_credit != 0 or y_bal != 0:
                        c = convert_fibu(gl_acct.fibukonto)
                        summary_list = Summary_list()
                        summary_list_data.append(summary_list)

                        summary_list.acctno = c
                        summary_list.bezeich = gl_acct.bezeich
                        summary_list.beg_bal =  to_decimal(p_bal)
                        summary_list.t_debit =  to_decimal(t_debit)
                        summary_list.t_credit =  to_decimal(t_credit)

                        if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                            diff =  - to_decimal(t_debit) + to_decimal(t_credit)
                        else:
                            diff =  to_decimal(t_debit) - to_decimal(t_credit)
                        tot_diff =  to_decimal(tot_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                        tt_diff =  to_decimal(tt_diff) + to_decimal(t_credit) - to_decimal(t_debit)
                        summary_list.net_change =  to_decimal(diff)
                        summary_list.end_bal =  to_decimal(t_bal)
                        summary_list.ytd_bal =  to_decimal(y_bal)


                summary_list = Summary_list()
                summary_list_data.append(summary_list)

                summary_list.bezeich = "s U B T O T A L"
                summary_list.beg_bal =  to_decimal(prev_bal)
                summary_list.t_debit =  to_decimal(tot_debit)
                summary_list.t_credit =  to_decimal(tot_credit)
                summary_list.net_change =  to_decimal(tot_diff)
                summary_list.end_bal =  to_decimal(tot_bal)
                summary_list.ytd_bal =  to_decimal(t_ybal)


                summary_list = Summary_list()
                summary_list_data.append(summary_list)

            summary_list = Summary_list()
            summary_list_data.append(summary_list)

            summary_list.bezeich = "T O T A L"
            summary_list.beg_bal =  to_decimal(tt_pbal)
            summary_list.t_debit =  to_decimal(tt_debit)
            summary_list.t_credit =  to_decimal(tt_credit)
            summary_list.net_change =  to_decimal(tt_diff)
            summary_list.end_bal =  to_decimal(tt_bal)
            summary_list.ytd_bal =  to_decimal(tt_ybal)


    def convert_fibu(konto:string):

        nonlocal summary_list_data, detail_list_data, sales, cost, gop_credit, gop_debit, tot_diff, close_date, htparam, gl_jouhdr, gl_acct, gl_journal, gl_department
        nonlocal from_depart, from_date, to_date, close_month, sorttype, from_fibu, to_fibu, pnl_acct, pbal_flag


        nonlocal g_list, summary_list, detail_list
        nonlocal g_list_data, summary_list_data, detail_list_data

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
        ch = htparam.fchar
        j = 0
        for i in range(1,length(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 597)]})
    close_date = htparam.fdate
    create_glist()

    if from_depart > 0:
        create_trial_list1()
    else:
        create_trial_list2()

    return generate_output()