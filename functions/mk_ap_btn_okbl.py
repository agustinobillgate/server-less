from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Gl_acct, L_op, Gl_jouhdr, Htparam, L_kredit, L_lieferant, Ap_journal, Counters, Gl_journal

def mk_ap_btn_okbl(s_list:[S_list], pvilanguage:int, invoice:str, journ_flag:bool, balance:decimal, avail_sbuff:bool, docu_nr:str, rgdatum:date, lief_nr:int, disc:decimal, saldo:decimal, d_amount:decimal, ziel:int, nr:int, comments:str, netto:decimal, userinit:str, ap_other:str, user_init:str, firma:str, s_list_fibukonto:str, s_list_debit:decimal, tax_code:str, tax_amt:str):
    msg_str = ""
    fl_code = 0
    avail_gl = False
    return_flag:bool = False
    lvcarea:str = "mk_ap"
    gl_close_month:date = None
    ch:str = ""
    gl_acct = l_op = gl_jouhdr = htparam = l_kredit = l_lieferant = ap_journal = counters = gl_journal = None

    s_list = sbuff = None

    s_list_list, S_list = create_model("S_list", {"fibukonto":str, "debit":decimal, "credit":decimal, "flag":bool, "bezeich":str}, {"fibukonto": "000000000000"})

    Sbuff = S_list
    sbuff_list = s_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, fl_code, avail_gl, return_flag, lvcarea, gl_close_month, ch, gl_acct, l_op, gl_jouhdr, htparam, l_kredit, l_lieferant, ap_journal, counters, gl_journal
        nonlocal sbuff


        nonlocal s_list, sbuff
        nonlocal s_list_list
        return {"msg_str": msg_str, "fl_code": fl_code, "avail_gl": avail_gl}

    for s_list in query(s_list_list):

        if s_list.debit != 0:

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == s_list.fibukonto)).first()

            if not gl_acct:
                avail_gl = False

        if decimal.Decimal(s_list.fibukonto) != 0:

            gl_acct = db_session.query(Gl_acct).filter(
                    (Gl_acct.fibukonto == s_list.fibukonto)).first()

            if not gl_acct:
                avail_gl = False

        if not avail_gl:
            s_list.flag = True
            return_flag = True


            break

    if return_flag:

        return generate_output()

    l_op = db_session.query(L_op).filter(
            (L_op.op_art == 1) &  (L_op.loeschflag <= 1) &  (func.lower(L_op.lscheinnr) == (invoice).lower())).first()

    if l_op:
        msg_str = msg_str + chr(2) + translateExtended ("Same Delivery No exists in Receiving Record, date  == ", lvcarea, "") + " " + to_string(l_op.datum) + " - " + l_op.docu_nr
        fl_code = 1

        return generate_output()

    if journ_flag:

        if balance != 0:
            msg_str = msg_str + chr(2) + translateExtended ("Journal Transaction NOT balanced.", lvcarea, "")
            fl_code = 2

            return generate_output()

        if not avail_sbuff:
            msg_str = msg_str + chr(2) + translateExtended ("Journal record NOT found.", lvcarea, "")
            fl_code = 3

            return generate_output()

        gl_jouhdr = db_session.query(Gl_jouhdr).filter(
                (func.lower(Gl_jouhdr.refno) == (docu_nr).lower())).first()

        if gl_jouhdr:
            msg_str = msg_str + chr(2) + translateExtended ("Same G/L RefNo exists, date  == ", lvcarea, "") + " " + to_string(gl_jouhdr.datum)
            fl_code = 4

            return generate_output()

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 558)).first()

        if rgdatum <= htparam.fdate:
            msg_str = msg_str + chr(2) + translateExtended ("A/P transaction date too old.", lvcarea, "")
            fl_code = 5

            return generate_output()
    else:

        l_kredit = db_session.query(L_kredit).filter(
                (L_kredit.lief_nr != lief_nr) &  (func.lower(L_kredit.name) == (docu_nr).lower()) &  (L_kredit.zahlkonto == 0)).first()

        if l_kredit:

            l_lieferant = db_session.query(L_lieferant).filter(
                    (L_lieferant.lief_nr == lief_nr)).first()

            if l_lieferant:
                ch = l_lieferant.firma
            msg_str = msg_str + chr(2) + translateExtended ("A/P with same RefNo exists:", lvcarea, "") + " " + to_string(l_kredit.rgdatum) + " " + ch
            fl_code = 6

            return generate_output()

    if netto != 0:

        if tax_code != " ":

            if tax_amt != " ":
                comments = comments + ";" + tax_code + ";" + tax_amt
            else:
                comments = comments + ";" + tax_code
    l_kredit = L_kredit()
    db_session.add(l_kredit)

    l_kredit.name = docu_nr
    l_kredit.lief_nr = lief_nr
    l_kredit.lscheinnr = invoice
    l_kredit.rgdatum = rgdatum
    l_kredit.datum = None
    l_kredit.saldo = saldo
    l_kredit.rabatt = disc
    l_kredit.rabattbetrag = d_amount
    l_kredit.ziel = ziel
    l_kredit.netto = netto
    l_kredit.bediener_nr = nr
    l_kredit.bemerk = comments
    l_kredit.steuercode = 1
    l_kredit.betriebsnr = to_int(journ_flag)


    ap_journal = Ap_journal()
    db_session.add(ap_journal)

    ap_journal.lief_nr = lief_nr
    ap_journal.docu_nr = docu_nr
    ap_journal.lscheinnr = invoice
    ap_journal.rgdatum = rgdatum
    ap_journal.saldo = saldo
    ap_journal.netto = netto
    ap_journal.userinit = userinit
    ap_journal.zeit = get_current_time_in_seconds()
    ap_journal.betriebsnr = to_int(journ_flag)

    if journ_flag:

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 25)).first()

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 25
            counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")
        counters = counters + 1

        counters = db_session.query(Counters).first()
        gl_jouhdr = Gl_jouhdr()
        db_session.add(gl_jouhdr)

        gl_jouhdr.jnr = counters
        gl_jouhdr.refno = docu_nr
        gl_jouhdr.datum = rgdatum
        gl_jouhdr.bezeich = firma
        gl_jouhdr.batch = True
        gl_jouhdr.jtype = 4


        gl_journal = Gl_journal()
        db_session.add(gl_journal)

        gl_journal.jnr = gl_jouhdr.jnr
        gl_journal.fibukonto = ap_other
        gl_journal.userinit = user_init
        gl_journal.zeit = get_current_time_in_seconds()
        gl_journal.bemerk = invoice

        if netto > 0:
            gl_journal.credit = netto
        else:
            gl_journal.debit = - netto

        if l_kredit.bemerk != "":

            if num_entries(l_kredit.bemerk, ";") > 1:
                gl_journal.bemerk = gl_journal.bemerk + " - " + entry(0, l_kredit.bemerk, ";")
            else:
                gl_journal.bemerk = gl_journal.bemerk + " - " + l_kredit.bemerk
        gl_jouhdr.credit = gl_jouhdr.credit + gl_journal.credit
        gl_jouhdr.debit = gl_jouhdr.debit + gl_journal.debit

        for sbuff in query(sbuff_list, filters=(lambda sbuff :decimal.Decimal(sbuff.fibukonto) != 0)):
            gl_journal = Gl_journal()
            db_session.add(gl_journal)

            gl_journal.jnr = gl_jouhdr.jnr
            gl_journal.fibukonto = sbuff.fibukonto
            gl_journal.userinit = user_init
            gl_journal.zeit = get_current_time_in_seconds()
            gl_journal.bemerk = invoice
            gl_journal.debit = sbuff.debit
            gl_journal.credit = sbuff.credit

            if l_kredit.bemerk != "":

                if num_entries(l_kredit.bemerk, ";") > 1:
                    gl_journal.bemerk = gl_journal.bemerk + " - " + entry(0, l_kredit.bemerk, ";")
                else:
                    gl_journal.bemerk = gl_journal.bemerk + " - " + l_kredit.bemerk
            gl_jouhdr.credit = gl_jouhdr.credit + gl_journal.credit
            gl_jouhdr.debit = gl_jouhdr.debit + gl_journal.debit

            gl_journal = db_session.query(Gl_journal).first()

        gl_jouhdr = db_session.query(Gl_jouhdr).first()

    return generate_output()