from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_jhdrhis, Gl_jourhis, Gl_jouhdr, Gl_journal, Gl_acct, Gl_accthis, Htparam

def gl_joulist_1_webbl(from_date:date, to_date:date, last_2yr:date, close_year:date, journaltype:int, excl_other:bool, other_dept:bool, summ_date:bool, from_fibu:str, to_fibu:str, sorttype:int, from_dept:int, journaltype1:int, cashflow:bool, f_note:str, from_main:int):
    out_list_list = []
    datum1:date = None
    datum2:date = None
    gl_jhdrhis = gl_jourhis = gl_jouhdr = gl_journal = gl_acct = gl_accthis = htparam = None

    out_list = g_list = j_list = gl_account = gl_jour1 = gl_jouh1 = hdrbuff = joubuff = None

    out_list_list, Out_list = create_model("Out_list", {"s_recid":int, "marked":str, "fibukonto":str, "jnr":int, "jtype":int, "bemerk":str, "trans_date":date, "bezeich":str, "number1":str, "debit":decimal, "credit":decimal, "balance":decimal, "debit_str":str, "credit_str":str, "balance_str":str, "refno":str, "uid":str, "created":date, "chgid":str, "chgdate":date, "tax_code":str, "tax_amount":str, "tot_amt":str, "approved":bool, "prev_bal":str})
    g_list_list, G_list = create_model("G_list", {"grecid":int, "fibu":str})
    j_list_list, J_list = create_model("J_list", {"grecid":int, "fibu":str, "datum":date})

    Gl_account = Gl_acct
    Gl_jour1 = Gl_journal
    Gl_jouh1 = Gl_jouhdr
    Hdrbuff = Gl_jouhdr
    Joubuff = Gl_journal

    db_session = local_storage.db_session

    def generate_output():
        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff


        nonlocal out_list, g_list, j_list, gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff
        nonlocal out_list_list, g_list_list, j_list_list
        return {"out-list": out_list_list}

    def get_bemerk(bemerk:str):

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff


        nonlocal out_list, g_list, j_list, gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff
        nonlocal out_list_list, g_list_list, j_list_list

        n:int = 0
        s1:str = ""
        bemerk = replace_str(bemerk, chr(10) , " ")
        n = 1 + get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1

    def create_dlist():

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff


        nonlocal out_list, g_list, j_list, gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff
        nonlocal out_list_list, g_list_list, j_list_list


        j_list_list.clear()
        datum1 = date_mdy(12, 31, get_year(last_2yr))
        datum2 = datum1 + 1

        for gl_jhdrhis in db_session.query(Gl_jhdrhis).filter(
                (Gl_jhdrhis.datum >= from_date) &  (Gl_jhdrhis.datum <= datum1)).all():

            if journaltype == 0 and excl_other and gl_jhdrhis.jtype != 0:
                continue

            elif journaltype != 0 and not other_dept and gl_jhdrhis.jtype != journaltype:
                continue

            for gl_jourhis in db_session.query(Gl_jourhis).filter(
                    (Gl_jourhis.jnr == gl_jhdrhis.jnr) &  (func.lower(Gl_jourhis.fibukonto) >= (from_fibu).lower()) &  (func.lower(Gl_jourhis.fibukonto) <= (to_fibu).lower())).all():
                j_list = J_list()
                j_list_list.append(j_list)

                j_list.grecid = gl_jourhis._recid
                j_list.fibu = gl_jourhis.fibukonto
                j_list.datum = gl_jhdrhis.datum

        for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                (Gl_jouhdr.datum >= datum2) &  (Gl_jouhdr.datum <= to_date)).all():

            if journaltype == 0 and excl_other and gl_jouhdr.jtype != 0:
                continue

            elif journaltype != 0 and other_dept and gl_jouhdr.jtype == 0:
                continue

            elif journaltype != 0 and not other_dept and gl_jouhdr.jtype != journaltype and gl_jouhdr.jtype != journaltype1:
                continue

            for gl_journal in db_session.query(Gl_journal).filter(
                    (Gl_journal.jnr == gl_jouhdr.jnr) &  (func.lower(Gl_journal.fibukonto) >= (from_fibu).lower()) &  (func.lower(Gl_journal.fibukonto) <= (to_fibu).lower())).all():
                j_list = J_list()
                j_list_list.append(j_list)

                j_list.grecid = gl_journal._recid
                j_list.fibu = gl_journal.fibukonto
                j_list.datum = gl_jouhdr.datum

    def create_djlist():

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff


        nonlocal out_list, g_list, j_list, gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff
        nonlocal out_list_list, g_list_list, j_list_list

        debit:decimal = 0
        credit:decimal = 0
        balance:decimal = 0
        konto:str = ""
        i:int = 0
        c:str = ""
        bezeich:str = ""
        datum:date = None
        refno:str = ""
        h_bezeich:str = ""
        id:str = ""
        chgdate:date = None
        beg_date:date = None
        beg_day:int = 0
        date1:date = None
        ddebit:decimal = 0
        dcredit:decimal = 0
        dbalance:decimal = 0
        t_debit:decimal = 0
        t_credit:decimal = 0
        tot_debit:decimal = 0
        tot_credit:decimal = 0
        e_bal:decimal = 0
        delta:decimal = 0
        fdate:date = None
        tdate:date = None
        prev_mm:int = 0
        prev_yr:int = 0
        prev_bal:decimal = 0
        end_bal:decimal = 0
        blankchar:str = ""
        acc_bez:str = ""
        Gl_account = Gl_acct
        Gl_jour1 = Gl_jourhis
        Gl_jouh1 = Gl_jhdrhis
        for i in range(1,72 + 1) :
            blankchar = blankchar + " "
        prev_mm = get_month(from_date) - 1
        prev_yr = get_year(from_date)

        if prev_mm == 0:
            prev_mm = 12
            prev_yr = prev_yr - 1


        beg_date = date_mdy(get_month(from_date) , 1, get_year(from_date))
        out_list_list.clear()

        if sorttype == 2:

            for j_list in query(j_list_list):

                gl_jourhis = db_session.query(Gl_jourhis).filter(
                            (Gl_jourhis._recid == j_list.grecid)).first()

                if gl_jourhis:

                    gl_jhdrhis = db_session.query(Gl_jhdrhis).filter(
                                (Gl_jhdrhis.jnr == gl_jourhis.jnr)).first()

                    gl_acct = db_session.query(Gl_acct).filter(
                                (Gl_acct.fibukonto == gl_jourhis.fibukonto)).first()
                    j_list_list.remove(j_list)

                    if gl_jourhis.chgdate == None:
                        chgdate = None
                    else:
                        chgdate = gl_jourhis.chgdate

                    if konto == "":
                        prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        c = convert_fibu(gl_acct.fibukonto)
                        out_list.fibukonto = c
                        out_list.refno = to_string(c, "x(15)")
                        out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                        out_list.bemerk = to_string(gl_acct.bezeich) + " "+ to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

                        if cashflow :
                            out_list.bemerk = to_string(out_list.bemerk, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                        else:
                            out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)) , "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                        konto = gl_acct.fibukonto
                        acc_bez = gl_acct.bezeich

                    if konto != gl_acct.fibukonto:

                        if summ_date:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.s_recid = to_int(gl_journal._recid)
                            out_list.fibukonto = konto
                            out_list.trans_date = date1
                            out_list.bezeich = to_string(acc_bez, "x(40)")
                            out_list.bemerk = to_string(acc_bez, "x(40)")
                            out_list.debit = ddebit
                            out_list.credit = dcredit
                            out_list.balance = dbalance
                            out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                            if gl_journal:

                                if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                    out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                            if gl_acct:

                                if num_entries(gl_acct.bemerk, ";") > 1:
                                    out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                if cashflow :
                                    out_list.bemerk = to_string(out_list.bemerk)
                                else:
                                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                            ddebit = 0
                            dcredit = 0
                            date1 = gl_jhdrhis.datum


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.bezeich = "T O T A L "
                        out_list.debit = t_debit
                        out_list.credit = t_credit
                        out_list.balance = balance
                        out_list.debit_str = to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(t_credit, "->>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        balance = 0
                        t_debit = 0
                        t_credit = 0


                        prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        c = convert_fibu(gl_acct.fibukonto)
                        out_list.refno = to_string(c, "x(15)")
                        out_list.fibukonto = to_string(c, "x(15)")
                        out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                        out_list.bemerk = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                        acc_bez = gl_acct.bezeich
                        konto = gl_acct.fibukonto

                    if summ_date:

                        if date1 != None and date1 != gl_jhdrhis.datum:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.fibukonto = konto
                            out_list.trans_date = date1
                            out_list.bezeich = acc_bez
                            out_list.debit = ddebit
                            out_list.credit = dcredit
                            out_list.balance = dbalance
                            out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                            if gl_acct:

                                if num_entries(gl_acct.bemerk, ";") > 1:
                                    out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                if cashflow :
                                    out_list.bemerk = to_string(out_list.bemerk)
                                else:
                                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                            ddebit = 0
                            dcredit = 0

                    gl_account = db_session.query(Gl_account).filter(
                                (Gl_account.fibukonto == gl_jourhis.fibukonto)).first()

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        balance = balance - gl_jourhis.debit + gl_jourhis.credit


                    else:
                        balance = balance + gl_jourhis.debit - gl_jourhis.credit


                    t_debit = t_debit + gl_jourhis.debit
                    t_credit = t_credit + gl_jourhis.credit
                    tot_debit = tot_debit + gl_jourhis.debit
                    tot_credit = tot_credit + gl_jourhis.credit

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        dbalance = dbalance - gl_jourhis.debit + gl_jourhis.credit


                    else:
                        dbalance = dbalance + gl_jourhis.debit - gl_jourhis.credit


                    ddebit = ddebit + gl_jourhis.debit
                    dcredit = dcredit + gl_jourhis.credit
                    date1 = gl_jhdrhis.datum

                    if not summ_date:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.s_recid = to_int(gl_jourhis._recid)
                        out_list.fibukonto = gl_jourhis.fibukonto
                        out_list.jnr = gl_jhdrhis.jnr
                        out_list.jtype = gl_jhdrhis.jtype
                        out_list.trans_date = gl_jhdrhis.datum
                        out_list.refno = gl_jhdrhis.refno
                        out_list.bezeich = gl_jhdrhis.bezeich
                        out_list.debit = gl_jourhis.debit
                        out_list.credit = gl_jourhis.credit
                        out_list.uid = gl_jourhis.userinit
                        out_list.created = gl_jourhis.sysdate
                        out_list.chgID = gl_jourhis.chginit
                        out_list.chgdate = chgdate
                        out_list.bemerk = to_string(get_bemerk (gl_jourhis.bemerk) , "x(50)")
                        out_list.balance = balance
                        out_list.debit_str = to_string(gl_jourhis.debit, "->>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(gl_jourhis.credit, "->>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")

                        if num_entries(gl_acct.bemerk, ";") > 1:
                            out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                        if cashflow :
                            out_list.bemerk = to_string(out_list.bemerk)
                        else:
                            out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                else:

                    gl_journal = db_session.query(Gl_journal).filter(
                                (Gl_journal._recid == j_list.grecid)).first()

                    if gl_journal:

                        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                                    (Gl_jouhdr.jnr == gl_journal.jnr)).first()

                        gl_acct = db_session.query(Gl_acct).filter(
                                    (Gl_acct.fibukonto == gl_journal.fibukonto)).first()
                        j_list_list.remove(j_list)

                        if gl_journal.chgdate == None:
                            chgdate = None
                        else:
                            chgdate = gl_journal.chgdate

                        if konto == "":
                            prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            c = convert_fibu(gl_acct.fibukonto)
                            out_list.fibukonto = to_string(c, "x(15)")
                            out_list.refno = to_string(c, "x(15)")
                            out_list.bezeich = to_string(gl_acct.bezeich) + " " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                            out_list.bemerk = to_string(gl_acct.bezeich) + " " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                            konto = gl_acct.fibukonto
                            acc_bez = gl_acct.bezeich

                        if konto != gl_acct.fibukonto:

                            if summ_date:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.s_recid = to_int(gl_journal._recid)
                                out_list.fibukonto = konto
                                out_list.trans_date = date1
                                out_list.bezeich = acc_bez
                                out_list.bemerk = acc_bez
                                out_list.debit = ddebit
                                out_list.credit = dcredit
                                out_list.balance = dbalance
                                out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                                out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                                out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                                if gl_journal:

                                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                                if gl_acct:

                                    if num_entries(gl_acct.bemerk, ";") > 1:
                                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                    if cashflow :
                                        out_list.bemerk = to_string(out_list.bemerk)
                                    else:
                                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                                ddebit = 0
                                dcredit = 0
                                date1 = gl_jouhdr.datum


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = to_string("T O T A L ")
                            out_list.debit = t_debit
                            out_list.credit = t_credit
                            out_list.balance = balance
                            out_list.debit_str = to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(t_credit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            balance = 0
                            t_debit = 0
                            t_credit = 0


                            prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            c = convert_fibu(gl_acct.fibukonto)
                            out_list.refno = to_string(c, "x(15)")
                            out_list.fibukonto = to_string(c, "x(15)")
                            out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                            out_list.bemerk = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                            acc_bez = gl_acct.bezeich
                            konto = gl_acct.fibukonto

                        if summ_date:

                            if date1 != None and date1 != gl_jouhdr.datum:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.fibukonto = konto
                                out_list.trans_date = date1
                                out_list.debit = ddebit
                                out_list.credit = dcredit
                                out_list.balance = dbalance
                                out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                                out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                                out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                                if gl_acct:

                                    if num_entries(gl_acct.bemerk, ";") > 1:
                                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                    if cashflow :
                                        out_list.bemerk = to_string(out_list.bemerk)
                                    else:
                                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                                ddebit = 0
                                dcredit = 0

                        gl_account = db_session.query(Gl_account).filter(
                                    (Gl_account.fibukonto == gl_journal.fibukonto)).first()

                        if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                            balance = balance - gl_journal.debit + gl_journal.credit


                        else:
                            balance = balance + gl_journal.debit - gl_journal.credit


                        t_debit = t_debit + gl_journal.debit
                        t_credit = t_credit + gl_journal.credit
                        tot_debit = tot_debit + gl_journal.debit
                        tot_credit = tot_credit + gl_journal.credit

                        if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                            dbalance = dbalance - gl_journal.debit + gl_journal.credit


                        else:
                            dbalance = dbalance + gl_journal.debit - gl_journal.credit


                        ddebit = ddebit + gl_journal.debit
                        dcredit = dcredit + gl_journal.credit
                        date1 = gl_jouhdr.datum

                        if not summ_date:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.s_recid = to_int(gl_journal._recid)
                            out_list.fibukonto = gl_journal.fibukonto
                            out_list.jnr = gl_jouhdr.jnr
                            out_list.jtype = gl_jouhdr.jtype
                            out_list.trans_date = gl_jouhdr.datum
                            out_list.refno = gl_jouhdr.refno
                            out_list.bezeich = gl_jouhdr.bezeich
                            out_list.debit = gl_journal.debit
                            out_list.credit = gl_journal.credit
                            out_list.refno = gl_jouhdr.refno
                            out_list.uid = gl_journal.userinit
                            out_list.created = gl_journal.sysdate
                            out_list.chgID = gl_journal.chginit
                            out_list.chgdate = chgdate
                            out_list.bemerk = to_string(get_bemerk (gl_journal.bemerk) , "x(50)")
                            out_list.balance = balance
                            out_list.debit_str = to_string(gl_journal.debit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(gl_journal.credit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")

                            if gl_journal:

                                if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                    out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk, "x(50)")
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)) , "x(50)")

            if summ_date:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.s_recid = to_int(gl_journal._recid)
                out_list.fibukonto = konto
                out_list.trans_date = date1
                out_list.bezeich = acc_bez
                out_list.debit = ddebit
                out_list.credit = dcredit
                out_list.balance = dbalance
                out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                if gl_journal:

                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))
                ddebit = 0
                dcredit = 0


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "T O T A L "
            out_list.debit = t_debit
            out_list.credit = t_credit
            out_list.balance = balance
            out_list.debit_str = to_string(t_debit, "->>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(t_credit, "->>>,>>>,>>>,>>9.99")
            out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "GRAND T O T A L               "
            out_list.debit = tot_debit
            out_list.credit = tot_credit
            out_list.debit_str = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(tot_credit, "->>>,>>>,>>>,>>9.99")

        elif sorttype == 1:

            for j_list in query(j_list_list):

                gl_jourhis = db_session.query(Gl_jourhis).filter(
                            (Gl_jourhis._recid == j_list.grecid)).first()

                if gl_jourhis:

                    gl_jhdrhis = db_session.query(Gl_jhdrhis).filter(
                                (Gl_jhdrhis.jnr == gl_jourhis.jnr)).first()

                    gl_acct = db_session.query(Gl_acct).filter(
                                (Gl_acct.fibukonto == gl_jourhis.fibukonto) &  (Gl_acct.main_nr == from_main)).first()
                    j_list_list.remove(j_list)

                    if gl_jourhis.chgdate == None:
                        chgdate = None
                    else:
                        chgdate = gl_jourhis.chgdate

                    if konto == "":
                        prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        c = convert_fibu(gl_acct.fibukonto)
                        out_list.fibukonto = to_string(c, "x(15)")
                        out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                        konto = gl_acct.fibukonto
                        acc_bez = gl_acct.bezeich

                    if konto != gl_acct.fibukonto:

                        if summ_date:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.s_recid = to_int(gl_journal._recid)
                            out_list.fibukonto = konto
                            out_list.trans_date = date1
                            out_list.bezeich = acc_bez
                            out_list.debit = ddebit
                            out_list.credit = dcredit
                            out_list.balance = dbalance
                            out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                            if gl_journal:

                                if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                    out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                            if gl_acct:

                                if num_entries(gl_acct.bemerk, ";") > 1:
                                    out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                if cashflow :
                                    out_list.bemerk = to_string(out_list.bemerk)
                                else:
                                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                            ddebit = 0
                            dcredit = 0
                            date1 = gl_jhdrhis.datum


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.bezeich = "T O T A L  "
                        out_list.debit = t_debit
                        out_list.credit = t_credit
                        out_list.balance = balance
                        out_list.debit_str = to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(t_credit, "->>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        balance = 0
                        t_debit = 0
                        t_credit = 0


                        prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        c = convert_fibu(gl_acct.fibukonto)
                        out_list.fibukonto = to_string(c, "x(15)")
                        out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                        acc_bez = gl_acct.bezeich
                        konto = gl_acct.fibukonto

                    if summ_date:

                        if date1 != None and date1 != gl_jhdrhis.datum:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.fibukonto = konto
                            out_list.trans_date = date1
                            out_list.bezeich = acc_bez
                            out_list.debit = ddebit
                            out_list.credit = dcredit
                            out_list.balance = dbalance
                            out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                            if gl_acct:

                                if num_entries(gl_acct.bemerk, ";") > 1:
                                    out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                if cashflow :
                                    out_list.bemerk = to_string(out_list.bemerk)
                                else:
                                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                            ddebit = 0
                            dcredit = 0

                    gl_account = db_session.query(Gl_account).filter(
                                (Gl_account.fibukonto == gl_jourhis.fibukonto)).first()

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        balance = balance - gl_jourhis.debit + gl_jourhis.credit
                    else:
                        balance = balance + gl_jourhis.debit - gl_jourhis.credit
                    t_debit = t_debit + gl_jourhis.debit
                    t_credit = t_credit + gl_jourhis.credit
                    tot_debit = tot_debit + gl_jourhis.debit
                    tot_credit = tot_credit + gl_jourhis.credit

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        dbalance = dbalance - gl_jourhis.debit + gl_jourhis.credit


                    else:
                        dbalance = dbalance + gl_jourhis.debit - gl_jourhis.credit


                    ddebit = ddebit + gl_jourhis.debit
                    dcredit = dcredit + gl_jourhis.credit
                    date1 = gl_jhdrhis.datum

                    if not summ_date:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.s_recid = to_int(gl_journal._recid)
                        out_list.fibukonto = gl_jourhis.fibukonto
                        out_list.jnr = gl_jhdrhis.jnr
                        out_list.jtype = gl_jhdrhis.jtype
                        out_list.trans_date = gl_jhdrhis.datum
                        out_list.refno = gl_jhdrhis.refno
                        out_list.bezeich = gl_jhdrhis.bezeich
                        out_list.debit = gl_jourhis.debit
                        out_list.credit = gl_jourhis.credit
                        out_list.uid = gl_jourhis.userinit
                        out_list.created = gl_jourhis.sysdate
                        out_list.chgID = gl_jourhis.chginit
                        out_list.chgdate = chgdate
                        out_list.bemerk = to_string(get_bemerk (gl_jourhis.bemerk) , "x(50)")
                        out_list.balance = balance
                        out_list.debit_str = to_string(gl_jourhis.debit, "->>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(gl_jourhis.credit, "->>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")

                        if num_entries(gl_acct.bemerk, ";") > 1:
                            out_list.tax_code = entry(1, gl_acct.bemerk, ";")
                else:

                    gl_journal = db_session.query(Gl_journal).filter(
                                (Gl_journal._recid == j_list.grecid)).first()

                    if gl_journal:

                        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                                    (Gl_jouhdr.jnr == gl_journal.jnr)).first()

                        gl_acct = db_session.query(Gl_acct).filter(
                                    (Gl_acct.fibukonto == gl_journal.fibukonto) &  (Gl_acct.main_nr == from_main)).first()
                        j_list_list.remove(j_list)

                        if gl_journal.chgdate == None:
                            chgdate = None
                        else:
                            chgdate = gl_journal.chgdate

                        if konto == "":
                            prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            c = convert_fibu(gl_acct.fibukonto)
                            out_list.fibukonto = to_string(c, "x(15)")
                            out_list.refno = to_string(c, "x(15)")
                            out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                            out_list.bemerk = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                            konto = gl_acct.fibukonto
                            acc_bez = gl_acct.bezeich

                        if konto != gl_acct.fibukonto:

                            if summ_date:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.s_recid = to_int(gl_journal._recid)
                                out_list.fibukonto = konto
                                out_list.trans_date = date1
                                out_list.bezeich = acc_bez
                                out_list.bemerk = acc_bez
                                out_list.debit = ddebit
                                out_list.credit = dcredit
                                out_list.balance = dbalance
                                out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                                out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                                out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")

                                if gl_journal:

                                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                                if gl_acct:

                                    if num_entries(gl_acct.bemerk, ";") > 1:
                                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                    if cashflow :
                                        out_list.bemerk = to_string(out_list.bemerk)
                                    else:
                                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                                ddebit = 0
                                dcredit = 0
                                date1 = gl_jouhdr.datum


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = "T O T A L  "
                            out_list.debit = t_debit
                            out_list.credit = t_credit
                            out_list.balance = balance
                            out_list.debit_str = to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(t_credit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            balance = 0
                            t_debit = 0
                            t_credit = 0


                            prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            c = convert_fibu(gl_acct.fibukonto)
                            out_list.refno = to_string(c, "x(15)")
                            out_list.fibukonto = to_string(c, "x(15)")
                            out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                            out_list.bemerk = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                            acc_bez = gl_acct.bezeich
                            konto = gl_acct.fibukonto

                        if summ_date:

                            if date1 != None and date1 != gl_jouhdr.datum:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.fibukonto = konto
                                out_list.trans_date = date1
                                out_list.bezeich = acc_bez
                                out_list.bemerk = acc_bez
                                out_list.debit = ddebit
                                out_list.credit = dcredit
                                out_list.balance = dbalance
                                out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                                out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                                out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                                if gl_acct:

                                    if num_entries(gl_acct.bemerk, ";") > 1:
                                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                    if cashflow :
                                        out_list.bemerk = to_string(out_list.bemerk)
                                    else:
                                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                                ddebit = 0
                                dcredit = 0

                        gl_account = db_session.query(Gl_account).filter(
                                    (Gl_account.fibukonto == gl_journal.fibukonto)).first()

                        if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                            balance = balance - gl_journal.debit + gl_journal.credit
                        else:
                            balance = balance + gl_journal.debit - gl_journal.credit
                        t_debit = t_debit + gl_journal.debit
                        t_credit = t_credit + gl_journal.credit
                        tot_debit = tot_debit + gl_journal.debit
                        tot_credit = tot_credit + gl_journal.credit

                        if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                            dbalance = dbalance - gl_journal.debit + gl_journal.credit


                        else:
                            dbalance = dbalance + gl_journal.debit - gl_journal.credit


                        ddebit = ddebit + gl_journal.debit
                        dcredit = dcredit + gl_journal.credit
                        date1 = gl_jouhdr.datum

                        if not summ_date:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.s_recid = to_int(gl_journal._recid)
                            out_list.fibukonto = gl_journal.fibukonto
                            out_list.jnr = gl_jouhdr.jnr
                            out_list.jtype = gl_jouhdr.jtype
                            out_list.trans_date = gl_jouhdr.datum
                            out_list.refno = gl_jouhdr.refno
                            out_list.bezeich = gl_jouhdr.bezeich
                            out_list.debit = gl_journal.debit
                            out_list.credit = gl_journal.credit
                            out_list.uid = gl_journal.userinit
                            out_list.created = gl_journal.sysdate
                            out_list.chgID = gl_journal.chginit
                            out_list.chgdate = chgdate
                            out_list.bemerk = to_string(get_bemerk (gl_journal.bemerk) , "x(50)")
                            out_list.balance = balance
                            out_list.debit_str = to_string(gl_journal.debit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(gl_journal.credit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")

                            if gl_journal:

                                if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                    out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk, "x(50)")
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)) , "x(50)")

            if summ_date:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.s_recid = to_int(gl_journal._recid)
                out_list.fibukonto = konto
                out_list.trans_date = date1
                out_list.bezeich = acc_bez
                out_list.debit = ddebit
                out_list.credit = dcredit
                out_list.balance = dbalance
                out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                if gl_journal:

                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                if gl_acct:

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                ddebit = 0
                dcredit = 0


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "T O T A L  "
            out_list.debit = tot_debit
            out_list.credit = tot_credit
            out_list.debit_str = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(tot_credit, "->>>,>>>,>>>,>>9.99")

        elif sorttype == 3:

            for j_list in query(j_list_list):

                gl_jourhis = db_session.query(Gl_jourhis).filter(
                            (Gl_jourhis._recid == j_list.grecid)).first()

                if gl_jourhis:

                    gl_jhdrhis = db_session.query(Gl_jhdrhis).filter(
                                (Gl_jhdrhis.jnr == gl_jourhis.jnr)).first()

                    gl_acct = db_session.query(Gl_acct).filter(
                                (Gl_acct.fibukonto == gl_jourhis.fibukonto) &  (Gl_acct.deptnr == from_dept)).first()
                    j_list_list.remove(j_list)

                    if gl_jourhis.chgdate == None:
                        chgdate = None
                    else:
                        chgdate = gl_jourhis.chgdate

                    if konto == "":
                        prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        c = convert_fibu(gl_acct.fibukonto)
                        out_list.fibukonto = to_string(c, "x(15)")
                        out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                        acc_bez = gl_acct.bezeich
                        konto = gl_acct.fibukonto

                    if konto != gl_acct.fibukonto:

                        if summ_date:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.s_recid = to_int(gl_journal._recid)
                            out_list.fibukonto = konto
                            out_list.trans_date = date1
                            out_list.bezeich = acc_bez
                            out_list.debit = ddebit
                            out_list.credit = dcredit
                            out_list.balance = dbalance
                            out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                            if gl_journal:

                                if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                    out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                            if gl_acct:

                                if num_entries(gl_acct.bemerk, ";") > 1:
                                    out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                if cashflow :
                                    out_list.bemerk = to_string(out_list.bemerk)
                                else:
                                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                            ddebit = 0
                            dcredit = 0
                            date1 = gl_jhdrhis.datum


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.bezeich = "T O T A L  "
                        out_list.debit = t_debit
                        out_list.credit = t_credit
                        out_list.balance = balance
                        out_list.debit_str = to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(t_credit, "->>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")


                        out_list = Out_list()
                        out_list_list.append(out_list)

                        balance = 0
                        t_debit = 0
                        t_credit = 0


                        prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        c = convert_fibu(gl_acct.fibukonto)
                        out_list.fibukonto = to_string(c, "x(15)")
                        out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                        acc_bez = gl_acct.bezeich
                        konto = gl_acct.fibukonto

                    if summ_date:

                        if date1 != None and date1 != gl_jhdrhis.datum:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.fibukonto = konto
                            out_list.trans_date = date1
                            out_list.bezeich = acc_bez
                            out_list.debit = ddebit
                            out_list.credit = dcredit
                            out_list.balance = dbalance
                            out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                            if gl_acct:

                                if num_entries(gl_acct.bemerk, ";") > 1:
                                    out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                if cashflow :
                                    out_list.bemerk = to_string(out_list.bemerk)
                                else:
                                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                            ddebit = 0
                            dcredit = 0

                    gl_account = db_session.query(Gl_account).filter(
                                (Gl_account.fibukonto == gl_jourhis.fibukonto)).first()

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        balance = balance - gl_jourhis.debit + gl_jourhis.credit
                    else:
                        balance = balance + gl_jourhis.debit - gl_jourhis.credit
                    t_debit = t_debit + gl_jourhis.debit
                    t_credit = t_credit + gl_jourhis.credit
                    tot_debit = tot_debit + gl_jourhis.debit
                    tot_credit = tot_credit + gl_jourhis.credit

                    if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                        dbalance = dbalance - gl_jourhis.debit + gl_jourhis.credit


                    else:
                        dbalance = dbalance + gl_jourhis.debit - gl_jourhis.credit


                    ddebit = ddebit + gl_jourhis.debit
                    dcredit = dcredit + gl_jourhis.credit
                    date1 = gl_jhdrhis.datum

                    if not summ_date:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.s_recid = to_int(gl_jourhis._recid)
                        out_list.fibukonto = gl_jourhis.fibukonto
                        out_list.jnr = gl_jhdrhis.jnr
                        out_list.jtype = gl_jhdrhis.jtype
                        out_list.trans_date = gl_jhdrhis.datum
                        out_list.refno = gl_jhdrhis.refno
                        out_list.bezeich = gl_jhdrhis.bezeich
                        out_list.debit = gl_jourhis.debit
                        out_list.credit = gl_jourhis.credit
                        out_list.uid = gl_jourhis.userinit
                        out_list.created = gl_jourhis.sysdate
                        out_list.chgID = gl_jourhis.chginit
                        out_list.chgdate = chgdate
                        out_list.bemerk = to_string(get_bemerk (gl_jourhis.bemerk) , "x(50)")
                        out_list.balance = balance
                        out_list.debit_str = to_string(gl_jourhis.debit, "->>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(gl_jourhis.credit, "->>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")

                        if num_entries(gl_acct.bemerk, ";") > 1:
                            out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                        if cashflow :
                            out_list.bemerk = to_string(out_list.bemerk)
                        else:
                            out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                else:

                    gl_journal = db_session.query(Gl_journal).filter(
                                (Gl_journal._recid == j_list.grecid)).first()

                    if gl_journal:

                        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                                    (Gl_jouhdr.jnr == gl_journal.jnr)).first()

                        gl_acct = db_session.query(Gl_acct).filter(
                                    (Gl_acct.fibukonto == gl_journal.fibukonto) &  (Gl_acct.deptnr == from_dept)).first()
                        j_list_list.remove(j_list)

                        if gl_journal.chgdate == None:
                            chgdate = None
                        else:
                            chgdate = gl_journal.chgdate

                        if konto == "":
                            prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            c = convert_fibu(gl_acct.fibukonto)
                            out_list.refno = to_string(c, "x(15)")
                            out_list.fibukonto = to_string(c, "x(15)")
                            out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                            out_list.bemerk = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                            acc_bez = gl_acct.bezeich
                            konto = gl_acct.fibukonto

                        if konto != gl_acct.fibukonto:

                            if summ_date:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.s_recid = to_int(gl_journal._recid)
                                out_list.fibukonto = konto
                                out_list.trans_date = date1
                                out_list.bezeich = acc_bez
                                out_list.bemerk = acc_bez
                                out_list.debit = ddebit
                                out_list.credit = dcredit
                                out_list.balance = dbalance
                                out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                                out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                                out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                                if gl_journal:

                                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                                if gl_acct:

                                    if num_entries(gl_acct.bemerk, ";") > 1:
                                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                    if cashflow :
                                        out_list.bemerk = to_string(out_list.bemerk)
                                    else:
                                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                                ddebit = 0
                                dcredit = 0
                                date1 = gl_jouhdr.datum


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.bezeich = "T O T A L  "
                            out_list.debit = t_debit
                            out_list.credit = t_credit
                            out_list.balance = balance
                            out_list.debit_str = to_string(t_debit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(t_credit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")


                            out_list = Out_list()
                            out_list_list.append(out_list)

                            balance = 0
                            t_debit = 0
                            t_credit = 0


                            prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            c = convert_fibu(gl_acct.fibukonto)
                            out_list.refno = to_string(c, "x(15)")
                            out_list.fibukonto = to_string(c, "x(15)")
                            out_list.bezeich = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                            out_list.bemerk = to_string(gl_acct.bezeich, "x(40)") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                            acc_bez = gl_acct.bezeich
                            konto = gl_acct.fibukonto

                        if summ_date:

                            if date1 != None and date1 != gl_jouhdr.datum:
                                out_list = Out_list()
                                out_list_list.append(out_list)

                                out_list.fibukonto = konto
                                out_list.trans_date = date1
                                out_list.bezeich = acc_bez
                                out_list.bemerk = acc_bez
                                out_list.debit = ddebit
                                out_list.credit = dcredit
                                out_list.balance = dbalance
                                out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                                out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                                out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                                if gl_acct:

                                    if num_entries(gl_acct.bemerk, ";") > 1:
                                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                                    if cashflow :
                                        out_list.bemerk = to_string(out_list.bemerk)
                                    else:
                                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                                ddebit = 0
                                dcredit = 0

                        gl_account = db_session.query(Gl_account).filter(
                                    (Gl_account.fibukonto == gl_journal.fibukonto)).first()

                        if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                            balance = balance - gl_journal.debit + gl_journal.credit
                        else:
                            balance = balance + gl_journal.debit - gl_journal.credit
                        t_debit = t_debit + gl_journal.debit
                        t_credit = t_credit + gl_journal.credit
                        tot_debit = tot_debit + gl_journal.debit
                        tot_credit = tot_credit + gl_journal.credit

                        if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                            dbalance = dbalance - gl_journal.debit + gl_journal.credit


                        else:
                            dbalance = dbalance + gl_journal.debit - gl_journal.credit


                        ddebit = ddebit + gl_journal.debit
                        dcredit = dcredit + gl_journal.credit
                        date1 = gl_jouhdr.datum

                        if not summ_date:
                            out_list = Out_list()
                            out_list_list.append(out_list)

                            out_list.s_recid = to_int(gl_journal._recid)
                            out_list.fibukonto = gl_journal.fibukonto
                            out_list.jnr = gl_jouhdr.jnr
                            out_list.jtype = gl_jouhdr.jtype
                            out_list.trans_date = gl_jouhdr.datum
                            out_list.refno = gl_jouhdr.refno
                            out_list.bezeich = gl_jouhdr.bezeich
                            out_list.debit = gl_journal.debit
                            out_list.credit = gl_journal.credit
                            out_list.uid = gl_journal.userinit
                            out_list.created = gl_journal.sysdate
                            out_list.chgID = gl_journal.chginit
                            out_list.chgdate = chgdate
                            out_list.bemerk = to_string(get_bemerk (gl_journal.bemerk) , "x(50)")
                            out_list.balance = balance
                            out_list.debit_str = to_string(gl_journal.debit, "->>>,>>>,>>>,>>9.99")
                            out_list.credit_str = to_string(gl_journal.credit, "->>>,>>>,>>>,>>9.99")
                            out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")

                            if gl_journal:

                                if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                    out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk, "x(50)")
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)) , "x(50)")

            if summ_date:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.s_recid = to_int(gl_journal._recid)
                out_list.fibukonto = konto
                out_list.trans_date = date1
                out_list.bezeich = acc_bez
                out_list.debit = ddebit
                out_list.credit = dcredit
                out_list.balance = dbalance
                out_list.debit_str = to_string(ddebit, "->>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(dcredit, "->>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(dbalance, "->>>,>>>,>>>,>>9.99")

                if gl_journal:

                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                if gl_acct:

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                ddebit = 0
                dcredit = 0


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "T O T A L  "
            out_list.debit = t_debit
            out_list.credit = t_credit
            out_list.balance = balance
            out_list.debit_str = to_string(t_debit, "->>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(t_credit, "->>>,>>>,>>>,>>9.99")
            out_list.balance_str = to_string(balance, "->>>,>>>,>>>,>>9.99")


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "GRAND T O T A L               "
            out_list.debit = tot_debit
            out_list.credit = tot_credit
            out_list.debit_str = to_string(tot_debit, "->>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(tot_credit, "->>>,>>>,>>>,>>9.99")

    def create_hglist():

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff


        nonlocal out_list, g_list, j_list, gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff
        nonlocal out_list_list, g_list_list, j_list_list


        g_list_list.clear()

        if f_note != "":

            for gl_jhdrhis in db_session.query(Gl_jhdrhis).filter(
                    (Gl_jhdrhis.datum >= from_date) &  (Gl_jhdrhis.datum <= to_date)).all():

                if journaltype == 0 and excl_other and gl_jhdrhis.jtype != 0:
                    continue

                elif journaltype != 0 and not other_dept and gl_jhdrhis.jtype != journaltype:
                    continue

                for gl_jourhis in db_session.query(Gl_jourhis).filter(
                        (Gl_jourhis.jnr == gl_jhdrhis.jnr) &  (Gl_jourhis.bemerk.op("~")(".*") + f_note + "*") &  (func.lower(Gl_jourhis.fibukonto) >= (from_fibu).lower()) &  (func.lower(Gl_jourhis.fibukonto) <= (to_fibu).lower())).all():
                    g_list = G_list()
                    g_list_list.append(g_list)

                    g_list.grecid = gl_jourhis._recid
                    g_list.fibu = gl_jourhis.fibukonto


        else:

            for gl_jhdrhis in db_session.query(Gl_jhdrhis).filter(
                    (Gl_jhdrhis.datum >= from_date) &  (Gl_jhdrhis.datum <= to_date)).all():

                if journaltype == 0 and excl_other and gl_jhdrhis.jtype != 0:
                    continue

                elif journaltype != 0 and not other_dept and gl_jhdrhis.jtype != journaltype:
                    continue

                for gl_jourhis in db_session.query(Gl_jourhis).filter(
                        (Gl_jourhis.jnr == gl_jhdrhis.jnr) &  (func.lower(Gl_jourhis.fibukonto) >= (from_fibu).lower()) &  (func.lower(Gl_jourhis.fibukonto) <= (to_fibu).lower())).all():
                    g_list = G_list()
                    g_list_list.append(g_list)

                    g_list.grecid = gl_jourhis._recid
                    g_list.fibu = gl_jourhis.fibukonto

    def create_hlist():

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff


        nonlocal out_list, g_list, j_list, gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff
        nonlocal out_list_list, g_list_list, j_list_list

        debit:decimal = 0
        credit:decimal = 0
        balance:decimal = 0
        konto:str = ""
        i:int = 0
        c:str = ""
        bezeich:str = ""
        datum:date = None
        refno:str = ""
        h_bezeich:str = ""
        id:str = ""
        chgdate:date = None
        beg_date:date = None
        beg_day:int = 0
        date1:date = None
        ddebit:decimal = 0
        dcredit:decimal = 0
        dbalance:decimal = 0
        t_debit:decimal = 0
        t_credit:decimal = 0
        tot_debit:decimal = 0
        tot_credit:decimal = 0
        e_bal:decimal = 0
        delta:decimal = 0
        fdate:date = None
        tdate:date = None
        prev_mm:int = 0
        prev_yr:int = 0
        prev_bal:decimal = 0
        end_bal:decimal = 0
        blankchar:str = ""
        acc_bez:str = ""
        Gl_account = Gl_acct
        Gl_jour1 = Gl_jourhis
        Gl_jouh1 = Gl_jhdrhis
        for i in range(1,72 + 1) :
            blankchar = blankchar + " "
        prev_mm = get_month(from_date) - 1
        prev_yr = get_year(from_date)

        if prev_mm == 0:
            prev_mm = 12
            prev_yr = prev_yr - 1


        beg_date = date_mdy(get_month(from_date) , 1, get_year(from_date))
        out_list_list.clear()

        if sorttype == 2:

            for g_list in query(g_list_list):
                gl_jourhis = db_session.query(Gl_jourhis).filter((Gl_jourhis._recid == g_list.grecid)).first()
                if not gl_jourhis:
                    continue

                gl_jhdrhis = db_session.query(Gl_jhdrhis).filter((Gl_jhdrhis.jnr == gl_jourhis.jnr)).first()
                if not gl_jhdrhis:
                    continue

                gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == gl_jourhis.fibukonto)).first()
                if not gl_acct:
                    continue

                g_list_list.remove(g_list)

                if gl_jourhis.chgdate == None:
                    chgdate = None
                else:
                    chgdate = gl_jourhis.chgdate

                if konto == "":
                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)

                    if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                        prev_bal = - prev_bal
                    else:
                        balance = prev_bal
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.fibukonto = c
                    out_list.refno = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.bemerk = to_string(gl_acct.bezeich)
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk, "x(40)")
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)) , "x(40)")
                    konto = gl_acct.fibukonto
                    acc_bez = gl_acct.bezeich

                if konto != gl_acct.fibukonto:

                    if summ_date:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.s_recid = to_int(gl_journal._recid)
                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = to_string(acc_bez, "x(40)")
                        out_list.bemerk = to_string(acc_bez, "x(40)")
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_journal:

                            if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0
                        date1 = gl_jhdrhis.datum


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.bezeich = "T O T A L "
                    out_list.debit = t_debit
                    out_list.credit = t_credit
                    out_list.balance = balance
                    out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    balance = 0
                    t_debit = 0
                    t_credit = 0


                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.refno = to_string(c, "x(15)")
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.bemerk = to_string(gl_acct.bezeich, "x(40)")
                    acc_bez = gl_acct.bezeich
                    konto = gl_acct.fibukonto
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

                if summ_date:

                    if date1 != None and date1 != gl_jhdrhis.datum:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = acc_bez
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0

                gl_account = db_session.query(Gl_account).filter(
                            (Gl_account.fibukonto == gl_jourhis.fibukonto)).first()

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    balance = balance - gl_jourhis.debit + gl_jourhis.credit


                else:
                    balance = balance + gl_jourhis.debit - gl_jourhis.credit


                t_debit = t_debit + gl_jourhis.debit
                t_credit = t_credit + gl_jourhis.credit
                tot_debit = tot_debit + gl_jourhis.debit
                tot_credit = tot_credit + gl_jourhis.credit

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    dbalance = dbalance - gl_jourhis.debit + gl_jourhis.credit


                else:
                    dbalance = dbalance + gl_jourhis.debit - gl_jourhis.credit


                ddebit = ddebit + gl_jourhis.debit
                dcredit = dcredit + gl_jourhis.credit
                date1 = gl_jhdrhis.datum

                if not summ_date:
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.s_recid = to_int(gl_jourhis._recid)
                    out_list.fibukonto = gl_jourhis.fibukonto
                    out_list.jnr = gl_jhdrhis.jnr
                    out_list.jtype = gl_jhdrhis.jtype
                    out_list.trans_date = gl_jhdrhis.datum
                    out_list.refno = gl_jhdrhis.refno
                    out_list.bezeich = gl_jhdrhis.bezeich
                    out_list.debit = gl_jourhis.debit
                    out_list.credit = gl_jourhis.credit
                    out_list.uid = gl_jourhis.userinit
                    out_list.created = gl_jourhis.sysdate
                    out_list.chgID = gl_jourhis.chginit
                    out_list.chgdate = chgdate
                    out_list.bemerk = to_string(get_bemerk (gl_jourhis.bemerk) , "x(100)")
                    out_list.balance = balance
                    out_list.debit_str = to_string(gl_jourhis.debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(gl_jourhis.credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))

            if summ_date:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.s_recid = to_int(gl_journal._recid)
                out_list.fibukonto = konto
                out_list.trans_date = date1
                out_list.bezeich = acc_bez
                out_list.debit = ddebit
                out_list.credit = dcredit
                out_list.balance = dbalance
                out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                if gl_journal:

                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))
                ddebit = 0
                dcredit = 0


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "T O T A L " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
            out_list.debit = t_debit
            out_list.credit = t_credit
            out_list.balance = balance
            out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
            out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
            out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "GRAND T O T A L               "
            out_list.debit = tot_debit
            out_list.credit = tot_credit
            out_list.debit_str = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(tot_credit, "->,>>>,>>>,>>>,>>9.99")

        elif sorttype == 1:

            for g_list in query(g_list_list):
                gl_jourhis = db_session.query(Gl_jourhis).filter((Gl_jourhis._recid == g_list.grecid)).first()
                if not gl_jourhis:
                    continue

                gl_jhdrhis = db_session.query(Gl_jhdrhis).filter((Gl_jhdrhis.jnr == gl_jourhis.jnr)).first()
                if not gl_jhdrhis:
                    continue

                gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == gl_jourhis.fibukonto) &  (Gl_acct.main_nr == from_main)).first()
                if not gl_acct:
                    continue

                g_list_list.remove(g_list)

                if gl_jourhis.chgdate == None:
                    chgdate = None
                else:
                    chgdate = gl_jourhis.chgdate

                if konto == "":
                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    konto = gl_acct.fibukonto
                    acc_bez = gl_acct.bezeich

                if konto != gl_acct.fibukonto:

                    if summ_date:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.s_recid = to_int(gl_journal._recid)
                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = acc_bez
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_journal:

                            if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0
                        date1 = gl_jhdrhis.datum


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.bezeich = "T O T A L  " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                    out_list.debit = t_debit
                    out_list.credit = t_credit
                    out_list.balance = balance
                    out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    balance = 0
                    t_debit = 0
                    t_credit = 0


                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    acc_bez = gl_acct.bezeich
                    konto = gl_acct.fibukonto

                if summ_date:

                    if date1 != None and date1 != gl_jhdrhis.datum:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = acc_bez
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0

                gl_account = db_session.query(Gl_account).filter(
                            (Gl_account.fibukonto == gl_jourhis.fibukonto)).first()

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    balance = balance - gl_jourhis.debit + gl_jourhis.credit
                else:
                    balance = balance + gl_jourhis.debit - gl_jourhis.credit
                t_debit = t_debit + gl_jourhis.debit
                t_credit = t_credit + gl_jourhis.credit
                tot_debit = tot_debit + gl_jourhis.debit
                tot_credit = tot_credit + gl_jourhis.credit

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    dbalance = dbalance - gl_jourhis.debit + gl_jourhis.credit


                else:
                    dbalance = dbalance + gl_jourhis.debit - gl_jourhis.credit


                ddebit = ddebit + gl_jourhis.debit
                dcredit = dcredit + gl_jourhis.credit
                date1 = gl_jhdrhis.datum

                if not summ_date:
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.s_recid = to_int(gl_journal._recid)
                    out_list.fibukonto = gl_jourhis.fibukonto
                    out_list.jnr = gl_jhdrhis.jnr
                    out_list.jtype = gl_jhdrhis.jtype
                    out_list.trans_date = gl_jhdrhis.datum
                    out_list.refno = gl_jhdrhis.refno
                    out_list.bezeich = gl_jhdrhis.bezeich
                    out_list.debit = gl_jourhis.debit
                    out_list.credit = gl_jourhis.credit
                    out_list.uid = gl_jourhis.userinit
                    out_list.created = gl_jourhis.sysdate
                    out_list.chgID = gl_jourhis.chginit
                    out_list.chgdate = chgdate
                    out_list.bemerk = to_string(get_bemerk (gl_jourhis.bemerk) , "x(100)")
                    out_list.balance = balance
                    out_list.debit_str = to_string(gl_jourhis.debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(gl_jourhis.credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

            if summ_date:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.s_recid = to_int(gl_journal._recid)
                out_list.fibukonto = konto
                out_list.trans_date = date1
                out_list.bezeich = acc_bez
                out_list.debit = ddebit
                out_list.credit = dcredit
                out_list.balance = dbalance
                out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                if gl_journal:

                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                if gl_acct:

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                ddebit = 0
                dcredit = 0


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "T O T A L  " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
            out_list.debit = tot_debit
            out_list.credit = tot_credit
            out_list.debit_str = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(tot_credit, "->,>>>,>>>,>>>,>>9.99")
            out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

        elif sorttype == 3:

            for g_list in query(g_list_list):
                gl_jourhis = db_session.query(Gl_jourhis).filter((Gl_jourhis._recid == g_list.grecid)).first()
                if not gl_jourhis:
                    continue

                gl_jhdrhis = db_session.query(Gl_jhdrhis).filter((Gl_jhdrhis.jnr == gl_jourhis.jnr)).first()
                if not gl_jhdrhis:
                    continue

                gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == gl_jourhis.fibukonto) &  (Gl_acct.deptnr == from_dept)).first()
                if not gl_acct:
                    continue

                g_list_list.remove(g_list)

                if gl_jourhis.chgdate == None:
                    chgdate = None
                else:
                    chgdate = gl_jourhis.chgdate

                if konto == "":
                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    acc_bez = gl_acct.bezeich
                    konto = gl_acct.fibukonto

                if konto != gl_acct.fibukonto:

                    if summ_date:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.s_recid = to_int(gl_journal._recid)
                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = acc_bez
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->,>>>,>>>,>>>,>>9.99")

                        if gl_journal:

                            if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0
                        date1 = gl_jhdrhis.datum


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.bezeich = "T O T A L  " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                    out_list.debit = t_debit
                    out_list.credit = t_credit
                    out_list.balance = balance
                    out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    balance = 0
                    t_debit = 0
                    t_credit = 0


                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    ASSIGN
                    acc_bez = gl_acct.bezeich
                    konto = gl_acct.fibukonto

                if summ_date:

                    if date1 != None and date1 != gl_jhdrhis.datum:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = acc_bez
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0

                gl_account = db_session.query(Gl_account).filter(
                            (Gl_account.fibukonto == gl_jourhis.fibukonto)).first()

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    balance = balance - gl_jourhis.debit + gl_jourhis.credit
                else:
                    balance = balance + gl_jourhis.debit - gl_jourhis.credit
                t_debit = t_debit + gl_jourhis.debit
                t_credit = t_credit + gl_jourhis.credit
                tot_debit = tot_debit + gl_jourhis.debit
                tot_credit = tot_credit + gl_jourhis.credit

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    dbalance = dbalance - gl_jourhis.debit + gl_jourhis.credit


                else:
                    dbalance = dbalance + gl_jourhis.debit - gl_jourhis.credit


                ddebit = ddebit + gl_jourhis.debit
                dcredit = dcredit + gl_jourhis.credit
                date1 = gl_jhdrhis.datum

                if not summ_date:
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.s_recid = to_int(gl_jourhis._recid)
                    out_list.fibukonto = gl_jourhis.fibukonto
                    out_list.jnr = gl_jhdrhis.jnr
                    out_list.jtype = gl_jhdrhis.jtype
                    out_list.trans_date = gl_jhdrhis.datum
                    out_list.refno = gl_jhdrhis.refno
                    out_list.bezeich = gl_jhdrhis.bezeich
                    out_list.debit = gl_jourhis.debit
                    out_list.credit = gl_jourhis.credit
                    out_list.uid = gl_jourhis.userinit
                    out_list.created = gl_jourhis.sysdate
                    out_list.chgID = gl_jourhis.chginit
                    out_list.chgdate = chgdate
                    out_list.bemerk = to_string(get_bemerk (gl_jourhis.bemerk) , "x(100)")
                    out_list.balance = balance
                    out_list.debit_str = to_string(gl_jourhis.debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(gl_jourhis.credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))

            if summ_date:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.s_recid = to_int(gl_journal._recid)
                out_list.fibukonto = konto
                out_list.trans_date = date1
                out_list.bezeich = acc_bez
                out_list.debit = ddebit
                out_list.credit = dcredit
                out_list.balance = dbalance
                out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                if gl_journal:

                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                if gl_acct:

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                ddebit = 0
                dcredit = 0


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "T O T A L  " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
            out_list.debit = t_debit
            out_list.credit = t_credit
            out_list.balance = balance
            out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
            out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
            out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "GRAND T O T A L               "
            out_list.debit = tot_debit
            out_list.credit = tot_credit
            out_list.debit_str = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(tot_credit, "->,>>>,>>>,>>>,>>9.99")

    def create_glist():

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff


        nonlocal out_list, g_list, j_list, gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff
        nonlocal out_list_list, g_list_list, j_list_list


        g_list_list.clear()

        if f_note != "":

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                    (Gl_jouhdr.datum >= from_date) &  (Gl_jouhdr.datum <= to_date)).all():

                if journaltype == 0 and excl_other and gl_jouhdr.jtype != 0:
                    continue

                elif journaltype != 0 and other_dept and gl_jouhdr.jtype == 0:
                    continue

                elif journaltype != 0 and not other_dept and gl_jouhdr.jtype != journaltype and gl_jouhdr.jtype != journaltype1:
                    continue

                for gl_journal in db_session.query(Gl_journal).filter(
                        (Gl_journal.jnr == gl_jouhdr.jnr) \
                            and  (Gl_journal.bemerk.op("~")(".*" + f_note + ".*")) \
                            and  (func.lower(Gl_journal.fibukonto) >= from_fibu.lower()) \
                            and  (func.lower(Gl_journal.fibukonto) <= to_fibu.lower())).all():
                    g_list = G_list()
                    g_list_list.append(g_list)

                    g_list.grecid = gl_journal._recid
                    g_list.fibu = gl_journal.fibukonto


        else:

            for gl_jouhdr in db_session.query(Gl_jouhdr).filter(
                    (Gl_jouhdr.datum >= from_date) &  (Gl_jouhdr.datum <= to_date)).all():

                if journaltype == 0 and excl_other and gl_jouhdr.jtype != 0:
                    continue

                elif journaltype != 0 and other_dept and gl_jouhdr.jtype == 0:
                    continue

                elif journaltype != 0 and not other_dept and gl_jouhdr.jtype != journaltype and gl_jouhdr.jtype != journaltype1:
                    continue

                for gl_journal in db_session.query(Gl_journal).filter(
                        (Gl_journal.jnr == gl_jouhdr.jnr) &  (func.lower(Gl_journal.fibukonto) >= (from_fibu).lower()) &  (func.lower(Gl_journal.fibukonto) <= (to_fibu).lower())).all():
                    g_list = G_list()
                    g_list_list.append(g_list)

                    g_list.grecid = gl_journal._recid
                    g_list.fibu = gl_journal.fibukonto

    def create_list():

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff


        nonlocal out_list, g_list, j_list, gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff
        nonlocal out_list_list, g_list_list, j_list_list

        debit:decimal = 0
        credit:decimal = 0
        balance:decimal = 0
        i:int = 0
        c:str = ""
        bezeich:str = ""
        refno:str = ""
        datum:date = None
        h_bezeich:str = ""
        id:str = ""
        chgdate:date = None
        beg_date:date = None
        beg_day:int = 0
        date1:date = None
        fdate:date = None
        tdate:date = None
        ddebit:decimal = 0
        dcredit:decimal = 0
        dbalance:decimal = 0
        e_bal:decimal = 0
        delta:decimal = 0
        prev_mm:int = 0
        prev_yr:int = 0
        prev_bal:decimal = 0
        end_bal:decimal = 0
        blankchar:str = ""
        acc_bez:str = ""
        t_debit:decimal = 0
        t_credit:decimal = 0
        tot_debit:decimal = 0
        tot_credit:decimal = 0
        konto:str = ""
        Gl_account = Gl_acct
        Gl_jour1 = Gl_journal
        Gl_jouh1 = Gl_jouhdr
        for i in range(1,72 + 1) :
            blankchar = blankchar + " "
        prev_mm = get_month(from_date) - 1
        prev_yr = get_year(from_date)

        if prev_mm == 0:
            prev_mm = 12
            prev_yr = prev_yr - 1


        beg_date = date_mdy(get_month(from_date) , 1, get_year(from_date))
        out_list_list.clear()

        if sorttype == 2:

            for g_list in query(g_list_list):
                gl_journal = db_session.query(Gl_journal).filter((Gl_journal._recid == g_list.grecid)).first()
                if not gl_journal:
                    continue

                gl_jouhdr = db_session.query(Gl_jouhdr).filter((Gl_jouhdr.jnr == gl_journal.jnr)).first()
                if not gl_jouhdr:
                    continue

                gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == gl_journal.fibukonto)).first()
                if not gl_acct:
                    continue

                g_list_list.remove(g_list)

                if gl_journal.chgdate == None:
                    chgdate = None
                else:
                    chgdate = gl_journal.chgdate

                if konto == "":
                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.refno = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich)
                    out_list.bemerk = to_string(gl_acct.bezeich)


                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                    konto = gl_acct.fibukonto
                    acc_bez = gl_acct.bezeich

                if konto != gl_acct.fibukonto:

                    if summ_date:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.s_recid = to_int(gl_journal._recid)
                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = acc_bez
                        out_list.bemerk = acc_bez
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_journal:

                            if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0
                        date1 = gl_jouhdr.datum


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.bezeich = to_string("T O T A L ") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                    out_list.debit = t_debit
                    out_list.credit = t_credit
                    out_list.balance = balance
                    out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    balance = 0
                    t_debit = 0
                    t_credit = 0


                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.refno = to_string(c, "x(15)")
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.bemerk = to_string(gl_acct.bezeich, "x(40)")
                    acc_bez = gl_acct.bezeich
                    konto = gl_acct.fibukonto


                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

                if summ_date:

                    if date1 != None and date1 != gl_jouhdr.datum:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0

                gl_account = db_session.query(Gl_account).filter(
                            (Gl_account.fibukonto == gl_journal.fibukonto)).first()

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    balance = balance - gl_journal.debit + gl_journal.credit


                else:
                    balance = balance + gl_journal.debit - gl_journal.credit


                t_debit = t_debit + gl_journal.debit
                t_credit = t_credit + gl_journal.credit
                tot_debit = tot_debit + gl_journal.debit
                tot_credit = tot_credit + gl_journal.credit

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    dbalance = dbalance - gl_journal.debit + gl_journal.credit


                else:
                    dbalance = dbalance + gl_journal.debit - gl_journal.credit


                ddebit = ddebit + gl_journal.debit
                dcredit = dcredit + gl_journal.credit
                date1 = gl_jouhdr.datum

                if not summ_date:
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.s_recid = to_int(gl_journal._recid)
                    out_list.fibukonto = gl_journal.fibukonto
                    out_list.jnr = gl_jouhdr.jnr
                    out_list.jtype = gl_jouhdr.jtype
                    out_list.trans_date = gl_jouhdr.datum
                    out_list.refno = gl_jouhdr.refno
                    out_list.bezeich = gl_jouhdr.bezeich
                    out_list.debit = gl_journal.debit
                    out_list.credit = gl_journal.credit
                    out_list.refno = gl_jouhdr.refno
                    out_list.uid = gl_journal.userinit
                    out_list.created = gl_journal.sysdate
                    out_list.chgID = gl_journal.chginit
                    out_list.chgdate = chgdate
                    out_list.bemerk = to_string(get_bemerk (gl_journal.bemerk) , "x(100)")
                    out_list.balance = balance
                    out_list.debit_str = to_string(gl_journal.debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(gl_journal.credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")

                    if gl_journal:

                        if num_entries(gl_journal.bemerk, chr(2)) > 1:
                            out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk, "x(100)")
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)) , "x(100)")

            if summ_date:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.s_recid = to_int(gl_journal._recid)
                out_list.fibukonto = konto
                out_list.trans_date = date1
                out_list.bezeich = acc_bez
                out_list.bemerk = acc_bez
                out_list.debit = ddebit
                out_list.credit = dcredit
                out_list.balance = dbalance
                out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                if gl_journal:

                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                if gl_acct:

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                ddebit = 0
                dcredit = 0


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "T O T A L  " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
            out_list.debit = t_debit
            out_list.credit = t_credit
            out_list.balance = balance
            out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
            out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
            out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "GRAND T O T A L               "
            out_list.debit = tot_debit
            out_list.credit = tot_credit
            out_list.debit_str = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(tot_credit, "->,>>>,>>>,>>>,>>9.99")

        elif sorttype == 1:

            for g_list in query(g_list_list):
                gl_journal = db_session.query(Gl_journal).filter((Gl_journal._recid == g_list.grecid)).first()
                if not gl_journal:
                    continue

                gl_jouhdr = db_session.query(Gl_jouhdr).filter((Gl_jouhdr.jnr == gl_journal.jnr)).first()
                if not gl_jouhdr:
                    continue

                gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == gl_journal.fibukonto) &  (Gl_acct.main_nr == from_main)).first()
                if not gl_acct:
                    continue

                g_list_list.remove(g_list)

                if gl_journal.chgdate == None:
                    chgdate = None
                else:
                    chgdate = gl_journal.chgdate

                if konto == "":
                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.refno = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.bemerk = to_string(gl_acct.bezeich, "x(40)")


                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                    konto = gl_acct.fibukonto
                    acc_bez = gl_acct.bezeich

                if konto != gl_acct.fibukonto:

                    if summ_date:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.s_recid = to_int(gl_journal._recid)
                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = acc_bez
                        out_list.bemerk = acc_bez
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_journal:

                            if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0
                        date1 = gl_jouhdr.datum


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.bezeich = "T O T A L  " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                    out_list.debit = t_debit
                    out_list.credit = t_credit
                    out_list.balance = balance
                    out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    balance = 0
                    t_debit = 0
                    t_credit = 0


                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.refno = to_string(c, "x(15)")
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.bemerk = to_string(gl_acct.bezeich, "x(40)")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    acc_bez = gl_acct.bezeich
                    konto = gl_acct.fibukonto

                if summ_date:

                    if date1 != None and date1 != gl_jouhdr.datum:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = acc_bez
                        out_list.bemerk = acc_bez
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0

                gl_account = db_session.query(Gl_account).filter(
                            (Gl_account.fibukonto == gl_journal.fibukonto)).first()

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    balance = balance - gl_journal.debit + gl_journal.credit
                else:
                    balance = balance + gl_journal.debit - gl_journal.credit
                t_debit = t_debit + gl_journal.debit
                t_credit = t_credit + gl_journal.credit
                tot_debit = tot_debit + gl_journal.debit
                tot_credit = tot_credit + gl_journal.credit

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    dbalance = dbalance - gl_journal.debit + gl_journal.credit


                else:
                    dbalance = dbalance + gl_journal.debit - gl_journal.credit


                ddebit = ddebit + gl_journal.debit
                dcredit = dcredit + gl_journal.credit
                date1 = gl_jouhdr.datum

                if not summ_date:
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.s_recid = to_int(gl_journal._recid)
                    out_list.fibukonto = gl_journal.fibukonto
                    out_list.jnr = gl_jouhdr.jnr
                    out_list.jtype = gl_jouhdr.jtype
                    out_list.trans_date = gl_jouhdr.datum
                    out_list.refno = gl_jouhdr.refno
                    out_list.bezeich = gl_jouhdr.bezeich
                    out_list.debit = gl_journal.debit
                    out_list.credit = gl_journal.credit
                    out_list.uid = gl_journal.userinit
                    out_list.created = gl_journal.sysdate
                    out_list.chgID = gl_journal.chginit
                    out_list.chgdate = chgdate
                    out_list.bemerk = to_string(get_bemerk (gl_journal.bemerk) , "x(100)")
                    out_list.balance = balance
                    out_list.debit_str = to_string(gl_journal.debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(gl_journal.credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")

                    if gl_journal:

                        if num_entries(gl_journal.bemerk, chr(2)) > 1:
                            out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk, "x(100)")
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)) , "x(100)")

            if summ_date:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.s_recid = to_int(gl_journal._recid)
                out_list.fibukonto = konto
                out_list.trans_date = date1
                out_list.bezeich = acc_bez
                out_list.bemerk = acc_bez
                out_list.debit = ddebit
                out_list.credit = dcredit
                out_list.balance = dbalance
                out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                if gl_journal:

                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                if gl_acct:

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                ddebit = 0
                dcredit = 0


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "T O T A L  " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
            out_list.debit = t_debit
            out_list.credit = t_credit
            out_list.balance = balance
            out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
            out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
            out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "GRAND T O T A L               "
            out_list.debit = tot_debit
            out_list.credit = tot_credit
            out_list.debit_str = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(tot_credit, "->,>>>,>>>,>>>,>>9.99")

        elif sorttype == 3:

            for g_list in query(g_list_list):
                gl_journal = db_session.query(Gl_journal).filter((Gl_journal._recid == g_list.grecid)).first()
                if not gl_journal:
                    continue

                gl_jouhdr = db_session.query(Gl_jouhdr).filter((Gl_jouhdr.jnr == gl_journal.jnr)).first()
                if not gl_jouhdr:
                    continue

                gl_acct = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == gl_journal.fibukonto) &  (Gl_acct.deptnr == from_dept)).first()
                if not gl_acct:
                    continue

                g_list_list.remove(g_list)

                if gl_journal.chgdate == None:
                    chgdate = None
                else:
                    chgdate = gl_journal.chgdate

                if konto == "":
                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.refno = to_string(c, "x(15)")
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.bemerk = to_string(gl_acct.bezeich, "x(40)")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    acc_bez = gl_acct.bezeich
                    konto = gl_acct.fibukonto

                if konto != gl_acct.fibukonto:

                    if summ_date:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.s_recid = to_int(gl_journal._recid)
                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = acc_bez
                        out_list.bemerk = acc_bez
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_journal:

                            if num_entries(gl_journal.bemerk, chr(2)) > 1:
                                out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0
                        date1 = gl_jouhdr.datum


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.bezeich = "T O T A L  " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                    out_list.debit = t_debit
                    out_list.credit = t_credit
                    out_list.balance = balance
                    out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    out_list = Out_list()
                    out_list_list.append(out_list)

                    balance = 0
                    t_debit = 0
                    t_credit = 0


                    prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    c = convert_fibu(gl_acct.fibukonto)
                    out_list.refno = to_string(c, "x(15)")
                    out_list.fibukonto = to_string(c, "x(15)")
                    out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                    out_list.bemerk = to_string(gl_acct.bezeich, "x(40)")
                    out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


                    acc_bez = gl_acct.bezeich
                    konto = gl_acct.fibukonto

                if summ_date:

                    if date1 != None and date1 != gl_jouhdr.datum:
                        out_list = Out_list()
                        out_list_list.append(out_list)

                        out_list.fibukonto = konto
                        out_list.trans_date = date1
                        out_list.bezeich = acc_bez
                        out_list.bemerk = acc_bez
                        out_list.debit = ddebit
                        out_list.credit = dcredit
                        out_list.balance = dbalance
                        out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                        out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                        if gl_acct:

                            if num_entries(gl_acct.bemerk, ";") > 1:
                                out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                            if cashflow :
                                out_list.bemerk = to_string(out_list.bemerk)
                            else:
                                out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                        ddebit = 0
                        dcredit = 0

                gl_account = db_session.query(Gl_account).filter(
                            (Gl_account.fibukonto == gl_journal.fibukonto)).first()

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    balance = balance - gl_journal.debit + gl_journal.credit
                else:
                    balance = balance + gl_journal.debit - gl_journal.credit
                t_debit = t_debit + gl_journal.debit
                t_credit = t_credit + gl_journal.credit
                tot_debit = tot_debit + gl_journal.debit
                tot_credit = tot_credit + gl_journal.credit

                if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                    dbalance = dbalance - gl_journal.debit + gl_journal.credit


                else:
                    dbalance = dbalance + gl_journal.debit - gl_journal.credit


                ddebit = ddebit + gl_journal.debit
                dcredit = dcredit + gl_journal.credit
                date1 = gl_jouhdr.datum

                if not summ_date:
                    out_list = Out_list()
                    out_list_list.append(out_list)

                    out_list.s_recid = to_int(gl_journal._recid)
                    out_list.fibukonto = gl_journal.fibukonto
                    out_list.jnr = gl_jouhdr.jnr
                    out_list.jtype = gl_jouhdr.jtype
                    out_list.trans_date = gl_jouhdr.datum
                    out_list.refno = gl_jouhdr.refno
                    out_list.bezeich = gl_jouhdr.bezeich
                    out_list.debit = gl_journal.debit
                    out_list.credit = gl_journal.credit
                    out_list.uid = gl_journal.userinit
                    out_list.created = gl_journal.sysdate
                    out_list.chgID = gl_journal.chginit
                    out_list.chgdate = chgdate
                    out_list.bemerk = to_string(get_bemerk (gl_journal.bemerk) , "x(100)")
                    out_list.balance = balance
                    out_list.debit_str = to_string(gl_journal.debit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(gl_journal.credit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")

                    if gl_journal:

                        if num_entries(gl_journal.bemerk, chr(2)) > 1:
                            out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk, "x(100)")
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)) , "x(100)")

            if summ_date:
                out_list = Out_list()
                out_list_list.append(out_list)

                out_list.s_recid = to_int(gl_journal._recid)
                out_list.fibukonto = konto
                out_list.trans_date = date1
                out_list.bezeich = acc_bez
                out_list.bemerk = acc_bez
                out_list.debit = ddebit
                out_list.credit = dcredit
                out_list.balance = dbalance
                out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

                if gl_journal:

                    if num_entries(gl_journal.bemerk, chr(2)) > 1:
                        out_list.number1 = entry(1, gl_journal.bemerk, chr(2))

                if gl_acct:

                    if num_entries(gl_acct.bemerk, ";") > 1:
                        out_list.tax_code = entry(1, gl_acct.bemerk, ";")

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))
                ddebit = 0
                dcredit = 0


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "T O T A L  " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
            out_list.debit = t_debit
            out_list.credit = t_credit
            out_list.balance = balance
            out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
            out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
            out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")


            out_list = Out_list()
            out_list_list.append(out_list)

            out_list = Out_list()
            out_list_list.append(out_list)

            out_list.bezeich = "GRAND T O T A L               "
            out_list.debit = tot_debit
            out_list.credit = tot_credit
            out_list.debit_str = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(tot_credit, "->,>>>,>>>,>>>,>>9.99")

    def calc_prev_bal(fibu:str, prev_mm:int, prev_yr:int):

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff


        nonlocal out_list, g_list, j_list, gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff
        nonlocal out_list_list, g_list_list, j_list_list

        prev_bal = 0
        balance = 0
        dbalance = 0
        curr_datum:date = None

        def generate_inner_output():
            return prev_bal, balance, dbalance
        Gl_account = Gl_acct
        Hdrbuff = Gl_jouhdr
        Joubuff = Gl_journal
        prev_bal = 0

        gl_account = db_session.query(Gl_account).filter(
                (func.lower(Gl_account.fibukonto) == (fibu).lower())).first()

        if prev_yr < get_year(close_year):

            gl_accthis = db_session.query(Gl_accthis).filter(
                    (Gl_accthis.fibukonto == gl_account.fibukonto) &  (Gl_accthis.YEAR == prev_yr)).first()

            if gl_accthis:
                prev_bal = gl_accthis.actual[prev_mm - 1]

        elif prev_yr == get_year(close_year):
            prev_bal = gl_account.actual[prev_mm - 1]

        if (gl_account.acc_type == 3 or gl_account.acc_type == 4) and get_day(from_date) > 1:
            for curr_datum in range(date_mdy(get_month(from_date) , 1, get_year(from_date)),date_mdy(get_month(from_date) , get_day(from_date) - 1, get_year(from_date))  + 1) :

                for hdrbuff in db_session.query(Hdrbuff).filter(
                            (Hdrbuff.datum == curr_datum) &  (Hdrbuff.activeflag <= 1)).all():

                    for joubuff in db_session.query(Joubuff).filter(
                                (Joubuff.jnr == hdrbuff.jnr) &  (func.lower(Joubuff.fibukonto) == (fibu).lower())).all():
                        prev_bal = prev_bal + joubuff.debit - joubuff.credit

        if gl_account.acc_type == 1 or gl_account.acc_type == 4:
            prev_bal = - prev_bal

        if gl_account.acc_type == 3 or gl_account.acc_type == 4:
            balance = prev_bal
            dbalance = prev_bal


        else:
            balance = 0
            dbalance = 0


        return generate_inner_output()

    def convert_fibu(konto:str):

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff


        nonlocal out_list, g_list, j_list, gl_account, gl_jour1, gl_jouh1, hdrbuff, joubuff
        nonlocal out_list_list, g_list_list, j_list_list

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

    if get_year(to_date) <= get_year(last_2yr):
        create_hglist()
        create_hlist()
    else:
        create_glist()
        create_list()

    return generate_output()