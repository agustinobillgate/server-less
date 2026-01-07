#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from sqlalchemy.engine import Engine, Connection
from sqlalchemy.orm import sessionmaker
from models import Gl_jhdrhis, Gl_jourhis, Gl_jouhdr, Gl_journal, Gl_acct, Gl_accthis, Htparam, Queasy
from functions.more_additional_functions import format_fixed_length
from functions import log_program as lp

from types import SimpleNamespace

import traceback


# Oscar - add new input idflag for directly create queasy on main loop
# note: diff from VHPCloud version
def gl_joulist_2_webbl(from_date:date, to_date:date, last_2yr:date, close_year:date, journaltype:int, excl_other:bool, other_dept:bool, summ_date:bool, from_fibu:string, to_fibu:string, sorttype:int, from_dept:int, journaltype1:int, cashflow:bool, f_note:string, from_main:int, idflag:str): 

    prepare_cache ([Gl_jhdrhis, Gl_jourhis, Gl_jouhdr, Gl_journal, Gl_acct, Gl_accthis, Htparam])

    out_list_list = []
    datum1:date = None
    datum2:date = None
    f_note = f_note.strip()

    gl_jhdrhis = gl_jourhis = gl_jouhdr = gl_journal = gl_acct = gl_accthis = htparam = None
    out_list = g_list = j_list = None

    out_list_list, Out_list = create_model("Out_list", {"s_recid":int, "marked":string, "fibukonto":string, "jnr":int, "jtype":int, "bemerk":string, "trans_date":date, "bezeich":string, "number1":string, "debit":Decimal, "credit":Decimal, "balance":Decimal, "debit_str":string, "credit_str":string, "balance_str":string, "refno":string, "uid":string, "created":date, "chgid":string, "chgdate":date, "tax_code":string, "tax_amount":string, "tot_amt":string, "approved":bool, "prev_bal":string, "dept_code":int, "coa_bezeich":string})
    g_list_list, G_list = create_model("G_list", {"grecid":int, "fibu":string})
    j_list_list, J_list = create_model("J_list", {"grecid":int, "fibu":string, "datum":date})

    db_session = local_storage.db_session

    # Oscar - start - create new session with same search_path for write operation to db and maintain yield__per connection still active
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

    WriteSessionOnly = sessionmaker(bind=localEngine)

    write_session_only = WriteSessionOnly()

    write_session_only.execute(
        text(f"SET search_path TO {search_path}")
    )
    # Oscar - end - create new session with same search_path for write operation to db and maintain yield__per connection still active
    
    # Oscar - start - create new session with same search_path for looping operation and stream result
    LoopingSessionOnly = sessionmaker(bind=localEngine)

    looping_session_only = LoopingSessionOnly()

    looping_session_only.execute(
        text(f"SET search_path TO {search_path}")
    )
    # Oscar - end - create new session with same search_path for looping operation and stream result

    def generate_output():
        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main


        nonlocal out_list, g_list, j_list
        nonlocal out_list_list, g_list_list, j_list_list

        return {"out-list": out_list_list}

    def get_bemerk(bemerk:string):

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main


        nonlocal out_list, g_list, j_list
        nonlocal out_list_list, g_list_list, j_list_list

        n:int = 0
        s1:string = ""
        bemerk = replace_str(bemerk, chr_unicode(10) , " ")
        n = get_index(bemerk, ";&&")

        if n > 0:
            s1 = substring(bemerk, 0, n - 1)
        else:
            s1 = bemerk
        return s1
    
    def handle_null_date(inp_date:date):
        if inp_date == None:
            return "" * 10
        else:
            # return f"{gl_jouhdr.datum.strftime("%m/%d/%y")}"
            return f"{gl_jouhdr.datum.strftime("%y").zfill(4)}-{gl_jouhdr.datum.strftime("%m-%d")}"
    
    def handle_null_char(inp_char:string):
        if inp_char == None:
            return ""
        else:
            if num_entries(inp_char, "|") > 1:
                inp_char = replace_str(inp_char, "|", "-")
            return inp_char

    def generate_new_queasy(out_list, counter):
        queasy = Queasy()

        queasy.key = 280
        queasy.char1 = "General Ledger"
        queasy.char3 = idflag
        queasy.char2 = to_string(out_list.s_recid) + "|" +\
                handle_null_char(out_list.marked) + "|" +\
                handle_null_char(out_list.fibukonto) + "|" +\
                to_string(out_list.jnr) + "|" +\
                to_string(out_list.jtype) + "|" +\
                handle_null_char(out_list.bemerk) + "|" +\
                handle_null_date(out_list.trans_date) + "|" +\
                handle_null_char(out_list.bezeich) + "|" +\
                handle_null_char(out_list.number1) + "|" +\
                to_string(out_list.debit) + "|" +\
                to_string(out_list.credit) + "|" +\
                to_string(out_list.balance) + "|" +\
                handle_null_char(out_list.debit_str) + "|" +\
                handle_null_char(out_list.credit_str) + "|" +\
                handle_null_char(out_list.balance_str) + "|" +\
                handle_null_char(out_list.refno) + "|" +\
                handle_null_char(out_list.uid) + "|" +\
                handle_null_date(out_list.created) + "|" +\
                handle_null_char(out_list.chgid) + "|" +\
                handle_null_date(out_list.chgdate) + "|" +\
                handle_null_char(out_list.tax_code) + "|" +\
                handle_null_char(out_list.tax_amount) + "|" +\
                handle_null_char(out_list.tot_amt) + "|" +\
                to_string(out_list.approved) + "|" +\
                handle_null_char(out_list.prev_bal) + "|" +\
                to_string(out_list.dept_code) + "|" +\
                to_string(out_list.coa_bezeich)
        queasy.number1 = counter

        write_session_only.add(queasy)
        
        if counter % 200 == 0:
            write_session_only.commit()

    def create_hglist():

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main


        nonlocal out_list, g_list, j_list
        nonlocal out_list_list, g_list_list, j_list_list

        g_list_list.clear()

        query = looping_session_only.query(
            Gl_jhdrhis._recid, 
            Gl_jourhis.fibukonto,
            Gl_jourhis._recid).join(Gl_jourhis, Gl_jourhis.jnr == Gl_jhdrhis.jnr).filter((Gl_jhdrhis.datum >= from_date) & (Gl_jhdrhis.datum <= to_date) & (Gl_jourhis.fibukonto >= (from_fibu).lower()) & (Gl_jourhis.fibukonto <= (to_fibu).lower())).order_by(Gl_jhdrhis.datum, Gl_jourhis.fibukonto)

        if f_note != "":
            query = query.filter((matches(Gl_jourhis.bemerk,"*" + f_note + "*")))

        if journaltype == 0 and excl_other:
            query = query.filter(Gl_jhdrhis.jtype != 0)
        elif journaltype != 0 and not other_dept:
            query = query.filter(Gl_jhdrhis.jtype != journaltype)

        gl_jhdrhis = SimpleNamespace()
        gl_jourhis = SimpleNamespace()

        for row in query.yield_per(100).execution_options(stream_results=True):

            (
                gl_jhdrhis._recid,
                gl_jourhis.fibukonto,
                gl_jourhis._recid
            ) = row

            g_list = G_list()
            g_list_list.append(g_list)

            g_list.grecid = gl_jourhis._recid
            g_list.fibu = gl_jourhis.fibukonto

    def create_hlist():

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main

        nonlocal out_list, g_list, j_list
        nonlocal out_list_list, g_list_list, j_list_list

        debit:Decimal = to_decimal("0.0")
        credit:Decimal = to_decimal("0.0")
        balance:Decimal = to_decimal("0.0")
        konto:string = ""
        i:int = 0
        c:string = ""
        bezeich:string = ""
        datum:date = None
        refno:string = ""
        h_bezeich:string = ""
        id:string = ""
        chgdate:date = None
        beg_date:date = None
        beg_day:int = 0
        date1:date = None
        ddebit:Decimal = to_decimal("0.0")
        dcredit:Decimal = to_decimal("0.0")
        dbalance:Decimal = to_decimal("0.0")
        t_debit:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        e_bal:Decimal = to_decimal("0.0")
        delta:Decimal = to_decimal("0.0")
        fdate:date = None
        tdate:date = None
        gl_account = None
        gl_jour1 = None
        gl_jouh1 = None
        prev_mm:int = 0
        prev_yr:int = 0
        prev_bal:Decimal = to_decimal("0.0")
        end_bal:Decimal = to_decimal("0.0")
        blankchar:string = ""
        acc_bez:string = ""
        Gl_account =  create_buffer("Gl_account",Gl_acct)
        Gl_jour1 =  create_buffer("Gl_jour1",Gl_jourhis)
        Gl_jouh1 =  create_buffer("Gl_jouh1",Gl_jhdrhis)
        for i in range(1,72 + 1) :
            blankchar = blankchar + " "
        prev_mm = get_month(from_date) - 1
        prev_yr = get_year(from_date)

        if prev_mm == 0:
            prev_mm = 12
            prev_yr = prev_yr - 1


        beg_date = date_mdy(get_month(from_date) , 1, get_year(from_date))
        out_list_list.clear()

        counter = 1

        main_q = looping_session_only.query(Gl_jourhis, Gl_jhdrhis, Gl_acct).join(Gl_jhdrhis,(Gl_jhdrhis.jnr == Gl_jourhis.jnr)).join(Gl_acct,(Gl_acct.fibukonto == Gl_jourhis.fibukonto)).filter((Gl_jourhis._recid.in_(list(set([g_list.grecid for g_list in g_list_list]))))).order_by(Gl_jourhis.fibukonto, Gl_jourhis.datum, Gl_jourhis.zeit, Gl_jhdrhis.refno, Gl_jourhis.bemerk)

        if sorttype == 2:
            pass
        elif sorttype == 1:
            main_q = main_q.filter(Gl_acct.main_nr == from_main)
        elif sorttype == 3:
            main_q = main_q.filter(Gl_acct.deptnr == from_dept)

        final_gl_jourhis = None
        final_gl_acct = None

        gl_jourhis_obj_list = {}

        for gl_jourhis, gl_jhdrhis, gl_acct in main_q.yield_per(100).execution_options(stream_results=True):
            final_gl_jourhis = gl_jourhis
            final_gl_acct = gl_acct
            
            # if gl_jourhis_obj_list.get(gl_jourhis._recid):
            #     continue
            # else:
            #     gl_jourhis_obj_list[gl_jourhis._recid] = True

            # g_list = query(g_list_list, (lambda g_list: (gl_jourhis._recid == g_list.grecid)), first=True)
            # g_list_list.remove(g_list)

            if gl_jourhis.chgdate == None:
                chgdate = None
            else:
                chgdate = gl_jourhis.chgdate

            if konto == "":
                prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)

                if gl_acct.acc_type == 1 or gl_acct.acc_type == 4:
                    prev_bal =  - to_decimal(prev_bal)
                else:
                    balance =  to_decimal(prev_bal)


                c = convert_fibu(gl_acct.fibukonto)

                out_list = Out_list()
                out_list.fibukonto = c
                out_list.refno = to_string(c, "x(15)")
                out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                out_list.bemerk = to_string(gl_acct.bezeich)
                out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

                if cashflow :
                    out_list.bemerk = to_string(out_list.bemerk, "x(40)")
                else:
                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr_unicode(2)) , "x(40)")

                generate_new_queasy(out_list, counter)
                counter = counter + 1

                konto = gl_acct.fibukonto
                acc_bez = gl_acct.bezeich

            if konto != gl_acct.fibukonto:

                if summ_date:
                    out_list = Out_list()
                    out_list.s_recid = to_int(gl_jourhis._recid)
                    out_list.fibukonto = konto
                    out_list.trans_date = date1
                    out_list.bezeich = to_string(acc_bez, "x(40)")
                    out_list.bemerk = to_string(acc_bez, "x(40)")
                    out_list.debit =  to_decimal(ddebit)
                    out_list.credit =  to_decimal(dcredit)
                    out_list.balance =  to_decimal(dbalance)
                    out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")
                    out_list.dept_code = gl_acct.deptnr

                    
                    # if num_entries(gl_jourhis.bemerk, chr_unicode(2)) > 1:
                    #     out_list.number1 = entry(1, gl_jourhis.bemerk, chr_unicode(2))
                    if gl_jourhis.bemerk:
                        if len(gl_jourhis.bemerk.split(chr(2))) > 1:
                            out_list.number1 = gl_jourhis.bemerk.split(chr(2))[1]

                    # if num_entries(gl_acct.bemerk, ";") > 1:
                    #     out_list.number1 = entry(1, gl_acct.bemerk, ";")
                    if gl_acct.bemerk:
                        if len(gl_acct.bemerk.split(";")) > 1:
                            out_list.number1 = gl_acct.bemerk.split(";")[1]

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr_unicode(2)))

                    generate_new_queasy(out_list, counter)
                    counter = counter + 1

                    ddebit =  to_decimal("0")
                    dcredit =  to_decimal("0")
                    date1 = gl_jhdrhis.datum

                out_list = Out_list()
                out_list.bezeich = "T O T A L "
                out_list.debit =  to_decimal(t_debit)
                out_list.credit =  to_decimal(t_credit)
                out_list.balance =  to_decimal(balance)
                out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

                generate_new_queasy(out_list, counter)
                counter = counter + 1


                out_list = Out_list()

                generate_new_queasy(out_list, counter)
                counter = counter + 1

                balance =  to_decimal("0")
                t_debit =  to_decimal("0")
                t_credit =  to_decimal("0")

                c = convert_fibu(gl_acct.fibukonto)
                acc_bez = gl_acct.bezeich
                konto = gl_acct.fibukonto

                prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)

                out_list = Out_list()
                out_list.refno = to_string(c, "x(15)")
                out_list.fibukonto = to_string(c, "x(15)")
                out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                out_list.bemerk = to_string(gl_acct.bezeich, "x(40)")
                out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

                generate_new_queasy(out_list, counter)
                counter = counter + 1

            if summ_date:

                if date1 != None and date1 != gl_jhdrhis.datum:
                    out_list = Out_list()
                    out_list.fibukonto = konto
                    out_list.trans_date = date1
                    out_list.bezeich = acc_bez
                    out_list.debit =  to_decimal(ddebit)
                    out_list.credit =  to_decimal(dcredit)
                    out_list.balance =  to_decimal(dbalance)
                    out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")
                    out_list.dept_code = gl_acct.deptnr

                    # if num_entries(gl_acct.bemerk, ";") > 1:
                    #     out_list.tax_code = entry(1, gl_acct.bemerk, ";")
                    if gl_jourhis.bemerk:
                        if len(gl_jourhis.bemerk.split(chr(2))) > 1:
                            out_list.number1 = gl_jourhis.bemerk.split(chr(2))[1]

                    # if num_entries(gl_acct.bemerk, ";") > 1:
                    #     out_list.tax_code = entry(1, gl_acct.bemerk, ";")
                    if gl_acct.bemerk:
                        if len(gl_acct.bemerk.split(";")) > 1:
                            out_list.tax_code = gl_acct.bemerk.split(";")[1]

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr_unicode(2)))

                    generate_new_queasy(out_list, counter)
                    counter = counter + 1

                    ddebit =  to_decimal("0")
                    dcredit =  to_decimal("0")

            # gl_account = get_cache (Gl_acct, {"fibukonto": [(eq, gl_jourhis.fibukonto)]})
            gl_account = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == gl_jourhis.fibukonto)).first()

            if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                balance =  to_decimal(balance) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
            else:
                balance =  to_decimal(balance) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)

            t_debit =  to_decimal(t_debit) + to_decimal(gl_jourhis.debit)
            t_credit =  to_decimal(t_credit) + to_decimal(gl_jourhis.credit)
            tot_debit =  to_decimal(tot_debit) + to_decimal(gl_jourhis.debit)
            tot_credit =  to_decimal(tot_credit) + to_decimal(gl_jourhis.credit)

            if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                dbalance =  to_decimal(dbalance) - to_decimal(gl_jourhis.debit) + to_decimal(gl_jourhis.credit)
            else:
                dbalance =  to_decimal(dbalance) + to_decimal(gl_jourhis.debit) - to_decimal(gl_jourhis.credit)

            ddebit =  to_decimal(ddebit) + to_decimal(gl_jourhis.debit)
            dcredit =  to_decimal(dcredit) + to_decimal(gl_jourhis.credit)
            date1 = gl_jhdrhis.datum

            if not summ_date:
                out_list = Out_list()
                out_list.s_recid = to_int(gl_jourhis._recid)
                out_list.fibukonto = gl_jourhis.fibukonto
                out_list.jnr = gl_jhdrhis.jnr
                out_list.jtype = gl_jhdrhis.jtype
                out_list.trans_date = gl_jhdrhis.datum
                out_list.refno = gl_jhdrhis.refno
                out_list.bezeich = gl_jhdrhis.bezeich
                out_list.debit =  to_decimal(gl_jourhis.debit)
                out_list.credit =  to_decimal(gl_jourhis.credit)
                out_list.uid = gl_jourhis.userinit
                out_list.created = gl_jourhis.sysdate
                out_list.chgid = gl_jourhis.chginit
                out_list.chgdate = chgdate
                out_list.bemerk = to_string(get_bemerk (gl_jourhis.bemerk) , "x(100)")
                out_list.balance =  to_decimal(balance)
                out_list.debit_str = to_string(gl_jourhis.debit, "->,>>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(gl_jourhis.credit, "->,>>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                out_list.dept_code = gl_acct.deptnr
                out_list.coa_bezeich = gl_acct.bezeich

                # if num_entries(gl_jourhis.bemerk, chr_unicode(2)) > 1:
                #     out_list.number1 = entry(1, gl_jourhis.bemerk, chr_unicode(2))
                if gl_jourhis.bemerk:
                    if len(gl_jourhis.bemerk.split(chr(2))) > 1:
                        out_list.number1 = gl_jourhis.bemerk.split(chr(2))[1]

                # if num_entries(gl_acct.bemerk, ";") > 1:
                #     out_list.tax_code = entry(1, gl_acct.bemerk, ";")
                if gl_acct.bemerk:
                    if len(gl_acct.bemerk.split(";")) > 1:
                        out_list.tax_code = gl_acct.bemerk.split(";")[1]

                if cashflow :
                    out_list.bemerk = to_string(out_list.bemerk)
                else:
                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr_unicode(2)))

                generate_new_queasy(out_list, counter)
                counter = counter + 1

        if summ_date:
            out_list = Out_list()
            out_list.s_recid = to_int(final_gl_jourhis._recid)
            out_list.fibukonto = konto
            out_list.trans_date = date1
            out_list.bezeich = acc_bez
            out_list.debit =  to_decimal(ddebit)
            out_list.credit =  to_decimal(dcredit)
            out_list.balance =  to_decimal(dbalance)
            out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
            out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")
            out_list.dept_code = final_gl_acct.deptnr

            if final_gl_jourhis:
                # if num_entries(gl_journal.bemerk, chr_unicode(2)) > 1:
                #     out_list.number1 = entry(1, gl_journal.bemerk, chr_unicode(2))
                if final_gl_jourhis.bemerk:
                    if len(final_gl_jourhis.bemerk.split(chr(2))) > 1:
                        out_list.number1 = final_gl_jourhis.bemerk.split(chr(2))[1]

            if final_gl_acct:
                out_list.dept_code = final_gl_acct.deptnr

                # if num_entries(gl_acct.bemerk, ";") > 1:
                #     out_list.tax_code = entry(1, gl_acct.bemerk, ";")
                if final_gl_acct.bemerk:
                    if len(final_gl_acct.bemerk.split(";")) > 1:
                        out_list.tax_code = final_gl_acct.bemerk.split(";")[1]

                if cashflow :
                    out_list.bemerk = to_string(out_list.bemerk)
                else:
                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))

            generate_new_queasy(out_list, counter)
            counter = counter + 1

            ddebit =  to_decimal("0")
            dcredit =  to_decimal("0")

        out_list = Out_list()
        out_list.bezeich = "T O T A L " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
        out_list.debit =  to_decimal(t_debit)
        out_list.credit =  to_decimal(t_credit)
        out_list.balance =  to_decimal(balance)
        out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
        out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
        out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
        out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

        generate_new_queasy(out_list, counter)
        counter = counter + 1

        out_list = Out_list()

        generate_new_queasy(out_list, counter)
        counter = counter + 1

        out_list = Out_list()
        out_list.bezeich = "GRAND T O T A L "
        out_list.debit =  to_decimal(tot_debit)
        out_list.credit =  to_decimal(tot_credit)
        out_list.debit_str = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        out_list.credit_str = to_string(tot_credit, "->,>>>,>>>,>>>,>>9.99")

        generate_new_queasy(out_list, counter)
        counter = counter + 1

    def create_glist():

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main


        nonlocal out_list, g_list, j_list
        nonlocal out_list_list, g_list_list, j_list_list


        g_list_list.clear()

        query = looping_session_only.query(
            Gl_jouhdr._recid,
            Gl_journal.fibukonto,
            Gl_journal._recid)\
        .join(Gl_journal, Gl_journal.jnr == Gl_jouhdr.jnr).filter((Gl_jouhdr.datum >= from_date) & (Gl_jouhdr.datum <= to_date) & (Gl_journal.fibukonto >= (from_fibu).lower()) & (Gl_journal.fibukonto <= (to_fibu).lower())).order_by(Gl_jouhdr.datum, Gl_journal.fibukonto)

        if f_note != "":
            query = query.filter((matches(Gl_journal.bemerk,"*" + f_note + "*")))

        if journaltype == 0 and excl_other:
            query = query.filter(Gl_jouhdr.jtype == 0)
        elif journaltype != 0 and other_dept:
            query = query.filter(Gl_jouhdr.jtype != 0)
        elif journaltype != 0 and not other_dept:
            query = query.filter(Gl_jouhdr.jtype.in_([journaltype, journaltype1]))
        
        gl_jouhdr = SimpleNamespace()
        gl_journal = SimpleNamespace()

        for row in query.yield_per(100).execution_options(stream_results=True):

            (
                gl_jouhdr._recid,
                gl_journal.fibukonto,
                gl_journal._recid
            ) = row

            g_list = G_list()
            g_list_list.append(g_list)

            g_list.grecid = gl_journal._recid
            g_list.fibu = gl_journal.fibukonto


    def create_list():

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main

        nonlocal out_list, g_list, j_list
        nonlocal out_list_list, g_list_list, j_list_list

        debit:Decimal = to_decimal("0.0")
        credit:Decimal = to_decimal("0.0")
        balance:Decimal = to_decimal("0.0")
        i:int = 0
        c:string = ""
        bezeich:string = ""
        refno:string = ""
        datum:date = None
        h_bezeich:string = ""
        id:string = ""
        chgdate:date = None
        beg_date:date = None
        beg_day:int = 0
        date1:date = None
        fdate:date = None
        tdate:date = None
        ddebit:Decimal = to_decimal("0.0")
        dcredit:Decimal = to_decimal("0.0")
        dbalance:Decimal = to_decimal("0.0")
        e_bal:Decimal = to_decimal("0.0")
        delta:Decimal = to_decimal("0.0")
        prev_mm:int = 0
        prev_yr:int = 0
        prev_bal:Decimal = to_decimal("0.0")
        end_bal:Decimal = to_decimal("0.0")
        blankchar:string = ""
        acc_bez:string = ""
        t_debit:Decimal = to_decimal("0.0")
        t_credit:Decimal = to_decimal("0.0")
        tot_debit:Decimal = to_decimal("0.0")
        tot_credit:Decimal = to_decimal("0.0")
        konto:string = ""
        curr_recid:int = 0
        gl_account = None
        gl_jour1 = None
        gl_jouh1 = None
        Gl_account =  create_buffer("Gl_account",Gl_acct)
        Gl_jour1 =  create_buffer("Gl_jour1",Gl_journal)
        Gl_jouh1 =  create_buffer("Gl_jouh1",Gl_jouhdr)
        for i in range(1,72 + 1) :
            blankchar = blankchar + " "
        prev_mm = get_month(from_date) - 1
        prev_yr = get_year(from_date)

        if prev_mm == 0:
            prev_mm = 12
            prev_yr = prev_yr - 1


        beg_date = date_mdy(get_month(from_date) , 1, get_year(from_date))
        out_list_list.clear()

        counter = 1

        main_q = looping_session_only.query(Gl_journal, Gl_jouhdr, Gl_acct).join(Gl_jouhdr,(Gl_jouhdr.jnr == Gl_journal.jnr)).join(Gl_acct,(Gl_acct.fibukonto == Gl_journal.fibukonto)).filter((Gl_journal._recid.in_(list(set([g_list.grecid for g_list in g_list_list]))))).order_by(Gl_journal.fibukonto, Gl_jouhdr.datum, Gl_jouhdr.refno, Gl_journal.bemerk)

        if sorttype == 2:
            pass
        elif sorttype == 1:
            main_q = main_q.filter(Gl_acct.main_nr == from_main)
        elif sorttype == 3:
            main_q = main_q.filter(Gl_acct.deptnr == from_dept)

        final_gl_journal = None
        final_gl_acct = None

        gl_journal_obj_list = {}

        for gl_journal, gl_jouhdr, gl_acct in main_q.yield_per(100).execution_options(stream_results=True):
            
            final_gl_journal = gl_journal
            final_gl_acct = gl_acct
            # if gl_journal_obj_list.get(gl_journal._recid):
            #     continue
            # else:
            #     gl_journal_obj_list[gl_journal._recid] = True

            curr_recid = g_list.grecid

            if gl_journal.chgdate == None:
                chgdate = None
            else:
                chgdate = gl_journal.chgdate

            if konto == "":
                prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)

                c = convert_fibu(gl_acct.fibukonto)

                out_list = Out_list()
                out_list.fibukonto = to_string(c, "x(15)")
                out_list.refno = to_string(c, "x(15)")
                out_list.bezeich = to_string(gl_acct.bezeich)
                out_list.bemerk = to_string(gl_acct.bezeich)
                out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

                generate_new_queasy(out_list, counter)
                counter = counter + 1

                konto = gl_acct.fibukonto
                acc_bez = gl_acct.bezeich

            if konto != gl_acct.fibukonto:

                if summ_date:
                    out_list = Out_list()
                    out_list.s_recid = curr_recid
                    out_list.fibukonto = konto
                    out_list.trans_date = date1
                    out_list.bezeich = acc_bez
                    out_list.bemerk = acc_bez
                    out_list.debit =  to_decimal(ddebit)
                    out_list.credit =  to_decimal(dcredit)
                    out_list.balance =  to_decimal(dbalance)
                    out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")
                    out_list.dept_code = gl_acct.deptnr


                    # if num_entries(gl_journal.bemerk, chr_unicode(2)) > 1:
                    #     out_list.number1 = entry(1, gl_journal.bemerk, chr_unicode(2))
                    if gl_journal.bemerk:
                        if len(gl_journal.bemerk.split(chr(2))) > 1:
                            out_list.number1 = gl_journal.bemerk.split(chr(2))[1]

                    # if num_entries(gl_acct.bemerk, ";") > 1:
                    #     out_list.tax_code = entry(1, gl_acct.bemerk, ";")
                    if gl_acct.bemerk:
                        if len(gl_acct.bemerk.split(";")) > 1:
                            out_list.tax_code = gl_acct.bemerk.split(";")[1]

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))

                    generate_new_queasy(out_list, counter)
                    counter = counter + 1

                    ddebit =  to_decimal("0")
                    dcredit =  to_decimal("0")
                    date1 = gl_jouhdr.datum

                out_list = Out_list()
                out_list.bezeich = to_string("T O T A L ") + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
                out_list.debit =  to_decimal(t_debit)
                out_list.credit =  to_decimal(t_credit)
                out_list.balance =  to_decimal(balance)
                out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

                generate_new_queasy(out_list, counter)
                counter = counter + 1

                out_list = Out_list()

                generate_new_queasy(out_list, counter)
                counter = counter + 1

                balance =  to_decimal("0")
                t_debit =  to_decimal("0")
                t_credit =  to_decimal("0")

                c = convert_fibu(gl_acct.fibukonto)
                acc_bez = gl_acct.bezeich
                konto = gl_acct.fibukonto

                prev_bal, balance, dbalance = calc_prev_bal(gl_acct.fibukonto, prev_mm, prev_yr)

                out_list = Out_list()
                out_list.refno = to_string(c, "x(15)")
                out_list.fibukonto = to_string(c, "x(15)")
                out_list.bezeich = to_string(gl_acct.bezeich, "x(40)")
                out_list.bemerk = to_string(gl_acct.bezeich, "x(40)")
                out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

                generate_new_queasy(out_list, counter)
                counter = counter + 1

            if summ_date:

                if date1 != None and date1 != gl_jouhdr.datum:
                    out_list = Out_list()
                    out_list.fibukonto = konto
                    out_list.trans_date = date1
                    out_list.debit =  to_decimal(ddebit)
                    out_list.credit =  to_decimal(dcredit)
                    out_list.balance =  to_decimal(dbalance)
                    out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
                    out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")
                    out_list.dept_code = gl_acct.deptnr

                    # if num_entries(gl_journal.bemerk, chr_unicode(2)) > 1:
                    #     out_list.number1 = entry(1, gl_journal.bemerk, chr_unicode(2))
                    if gl_journal.bemerk:
                        if len(gl_journal.bemerk.split(chr(2))) > 1:
                            out_list.number1 = gl_journal.bemerk.split(chr(2))[1]

                    # if num_entries(gl_acct.bemerk, ";") > 1:
                    #     out_list.tax_code = entry(1, gl_acct.bemerk, ";")
                    if gl_acct.bemerk:
                        if len(gl_acct.bemerk.split(";")) > 1:
                            out_list.tax_code = gl_acct.bemerk.split(";")[1]

                    if cashflow :
                        out_list.bemerk = to_string(out_list.bemerk)
                    else:
                        out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))

                    generate_new_queasy(out_list, counter)
                    counter = counter + 1

                    ddebit =  to_decimal("0")
                    dcredit =  to_decimal("0")

            # gl_account = get_cache (Gl_acct, {"fibukonto": [(eq, gl_journal.fibukonto)]})
            gl_account = db_session.query(Gl_acct).filter((Gl_acct.fibukonto == gl_journal.fibukonto)).first()

            if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                balance =  to_decimal(balance) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
            else:
                balance =  to_decimal(balance) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

            t_debit =  to_decimal(t_debit) + to_decimal(gl_journal.debit)
            t_credit =  to_decimal(t_credit) + to_decimal(gl_journal.credit)
            tot_debit =  to_decimal(tot_debit) + to_decimal(gl_journal.debit)
            tot_credit =  to_decimal(tot_credit) + to_decimal(gl_journal.credit)

            if gl_account.acc_type == 1 or gl_account.acc_type == 4:
                dbalance =  to_decimal(dbalance) - to_decimal(gl_journal.debit) + to_decimal(gl_journal.credit)
            else:
                dbalance =  to_decimal(dbalance) + to_decimal(gl_journal.debit) - to_decimal(gl_journal.credit)

            ddebit =  to_decimal(ddebit) + to_decimal(gl_journal.debit)
            dcredit =  to_decimal(dcredit) + to_decimal(gl_journal.credit)
            date1 = gl_jouhdr.datum

            if not summ_date:
                out_list = Out_list()
                out_list.s_recid = curr_recid
                out_list.fibukonto = gl_journal.fibukonto
                out_list.jnr = gl_jouhdr.jnr
                out_list.jtype = gl_jouhdr.jtype
                out_list.trans_date = gl_jouhdr.datum
                out_list.refno = gl_jouhdr.refno
                out_list.bezeich = gl_jouhdr.bezeich
                out_list.debit =  to_decimal(gl_journal.debit)
                out_list.credit =  to_decimal(gl_journal.credit)
                out_list.refno = gl_jouhdr.refno
                out_list.uid = gl_journal.userinit
                out_list.created = gl_journal.sysdate
                out_list.chgid = gl_journal.chginit
                out_list.chgdate = chgdate
                out_list.bemerk = to_string(get_bemerk (gl_journal.bemerk) , "x(100)")
                out_list.balance =  to_decimal(balance)
                out_list.debit_str = to_string(gl_journal.debit, "->,>>>,>>>,>>>,>>9.99")
                out_list.credit_str = to_string(gl_journal.credit, "->,>>>,>>>,>>>,>>9.99")
                out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
                out_list.dept_code = gl_acct.deptnr
                out_list.coa_bezeich = gl_acct.bezeich

                # if num_entries(gl_journal.bemerk, chr_unicode(2)) > 1:
                #     out_list.number1 = entry(1, gl_journal.bemerk, chr_unicode(2))
                if gl_journal.bemerk:
                    if len(gl_journal.bemerk.split(chr(2))) > 1:
                        out_list.number1 = gl_journal.bemerk.split(chr(2))[1]

                # if num_entries(gl_acct.bemerk, ";") > 1:
                #     out_list.tax_code = entry(1, gl_acct.bemerk, ";")
                if gl_acct.bemerk:
                    if len(gl_acct.bemerk.split(";")) > 1:
                        out_list.tax_code = gl_acct.bemerk.split(";")[1]

                if cashflow :
                    out_list.bemerk = to_string(out_list.bemerk, "x(100)")
                else:
                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)) , "x(100)")

                generate_new_queasy(out_list, counter)
                counter = counter + 1
            
        if summ_date:
            out_list = Out_list()
            out_list.s_recid = curr_recid
            out_list.fibukonto = konto
            out_list.trans_date = date1
            out_list.bezeich = acc_bez
            out_list.bemerk = acc_bez
            out_list.debit =  to_decimal(ddebit)
            out_list.credit =  to_decimal(dcredit)
            out_list.balance =  to_decimal(dbalance)
            out_list.debit_str = to_string(ddebit, "->,>>>,>>>,>>>,>>9.99")
            out_list.credit_str = to_string(dcredit, "->,>>>,>>>,>>>,>>9.99")
            out_list.balance_str = to_string(dbalance, "->>,>>>,>>>,>>>,>>9.99")

            if final_gl_journal:
                # if num_entries(gl_journal.bemerk, chr_unicode(2)) > 1:
                #     out_list.number1 = entry(1, gl_journal.bemerk, chr_unicode(2))
                if final_gl_journal.bemerk:
                    if len(final_gl_journal.bemerk.split(chr(2))) > 1:
                        out_list.number1 = final_gl_journal.bemerk.split(chr(2))[1]

            if final_gl_acct:
                out_list.dept_code = final_gl_acct.deptnr

                # if num_entries(gl_acct.bemerk, ";") > 1:
                #     out_list.tax_code = entry(1, gl_acct.bemerk, ";")
                if final_gl_acct.bemerk:
                    if len(final_gl_acct.bemerk.split(";")) > 1:
                        out_list.tax_code = final_gl_acct.bemerk.split(";")[1]

                if cashflow :
                    out_list.bemerk = to_string(out_list.bemerk)
                else:
                    out_list.bemerk = to_string(entry(0, out_list.bemerk, chr(2)))

            generate_new_queasy(out_list, counter)
            counter = counter + 1

            ddebit =  to_decimal("0")
            dcredit =  to_decimal("0")

        out_list = Out_list()
        out_list.bezeich = "T O T A L " + to_string(prev_bal, "->>>,>>>,>>>,>>9.99")
        out_list.debit =  to_decimal(t_debit)
        out_list.credit =  to_decimal(t_credit)
        out_list.balance =  to_decimal(balance)
        out_list.debit_str = to_string(t_debit, "->,>>>,>>>,>>>,>>9.99")
        out_list.credit_str = to_string(t_credit, "->,>>>,>>>,>>>,>>9.99")
        out_list.balance_str = to_string(balance, "->>,>>>,>>>,>>>,>>9.99")
        out_list.prev_bal = to_string(prev_bal, "->>>,>>>,>>>,>>9.99")

        generate_new_queasy(out_list, counter)
        counter = counter + 1

        out_list = Out_list()

        generate_new_queasy(out_list, counter)
        counter = counter + 1

        out_list = Out_list()
        out_list.bezeich = "GRAND T O T A L "
        out_list.debit =  to_decimal(tot_debit)
        out_list.credit =  to_decimal(tot_credit)
        out_list.debit_str = to_string(tot_debit, "->,>>>,>>>,>>>,>>9.99")
        out_list.credit_str = to_string(tot_credit, "->,>>>,>>>,>>>,>>9.99")

        generate_new_queasy(out_list, counter)
        counter = counter + 1
        
       
    def calc_prev_bal(fibu:string, prev_mm:int, prev_yr:int):

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main


        nonlocal out_list, g_list, j_list
        nonlocal out_list_list, g_list_list, j_list_list

        prev_bal = to_decimal("0.0")
        balance = to_decimal("0.0")
        dbalance = to_decimal("0.0")
        curr_datum:date = None
        gl_account = None
        hdrbuff = None
        joubuff = None

        def generate_inner_output():
            return (prev_bal, balance, dbalance)

        Gl_account =  create_buffer("Gl_account",Gl_acct)
        Hdrbuff =  create_buffer("Hdrbuff",Gl_jouhdr)
        Joubuff =  create_buffer("Joubuff",Gl_journal)
        prev_bal =  to_decimal("0")

        # gl_account = get_cache (Gl_acct, {"fibukonto": [(eq, fibu)]})
        gl_account = db_session.query(Gl_acct).filter(Gl_acct.fibukonto == fibu).first()

        if prev_yr < get_year(close_year):

            # gl_accthis = get_cache (Gl_accthis, {"fibukonto": [(eq, gl_account.fibukonto)],"year": [(eq, prev_yr)]})
            gl_accthis = db_session.query(Gl_accthis).filter((Gl_accthis.fibukonto == gl_account.fibukonto) & (Gl_accthis.year == prev_yr)).first()

            if gl_accthis:
                prev_bal =  to_decimal(gl_accthis.actual[prev_mm - 1])

        elif prev_yr == get_year(close_year):
            prev_bal =  to_decimal(gl_account.actual[prev_mm - 1])

        if (gl_account.acc_type == 3 or gl_account.acc_type == 4) and get_day(from_date) > 1:
            hdrbuff = Gl_jouhdr()
            joubuff = Gl_journal()

            tmp_from_date = date_mdy(get_month(from_date) , 1, get_year(from_date))
            tmp_to_date = date_mdy(get_month(from_date) , get_day(from_date) - 1, get_year(from_date))

            for hdrbuff, joubuff in looping_session_only.query(Hdrbuff, Joubuff).join(Joubuff, (Joubuff.jnr == Hdrbuff.jnr)).filter((Hdrbuff.datum >= tmp_from_date) & (Hdrbuff.datum <= tmp_to_date) & (Hdrbuff.activeflag <= 1) & (Joubuff.fibukonto == (fibu).lower())).order_by(Hdrbuff._recid, Joubuff._recid).yield_per(100).execution_options(stream_results=True):
                prev_bal =  to_decimal(prev_bal) + to_decimal(joubuff.debit) - to_decimal(joubuff.credit)

        if gl_account.acc_type == 1 or gl_account.acc_type == 4:
            prev_bal =  - to_decimal(prev_bal)

        if gl_account.acc_type == 3 or gl_account.acc_type == 4:
            balance =  to_decimal(prev_bal)
            dbalance =  to_decimal(prev_bal)
        else:
            balance =  to_decimal("0")
            dbalance =  to_decimal("0")

        return generate_inner_output()


    def convert_fibu(konto:string):

        nonlocal out_list_list, datum1, datum2, gl_jhdrhis, gl_jourhis, gl_jouhdr, gl_journal, gl_acct, gl_accthis, htparam
        nonlocal from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main


        nonlocal out_list, g_list, j_list
        nonlocal out_list_list, g_list_list, j_list_list

        s = ""
        ch:string = ""
        i:int = 0
        j:int = 0

        def generate_inner_output():
            return (s)


        # htparam = get_cache (Htparam, {"paramnr": [(eq, 977)]})
        htparam = db_session.query(Htparam).filter(Htparam.paramnr == 977).first()
        ch = htparam.fchar
        j = 0
        for i in range(1,length(ch)  + 1) :

            if substring(ch, i - 1, 1) >= ("0").lower()  and substring(ch, i - 1, 1) <= ("9").lower() :
                j = j + 1
                s = s + substring(konto, j - 1, 1)
            else:
                s = s + substring(ch, i - 1, 1)

        return generate_inner_output()

    try:
        if get_year(to_date) < get_year(last_2yr):
            create_hglist()
            create_hlist()
        else:
            create_glist()
            create_list()

    except Exception as e:
        tb = traceback.format_exc()
        lp.write_log("error",f"Exception occurred:\n{tb}\n")

    write_session_only.commit()
    write_session_only.close()

    looping_session_only.close()

    return generate_output()