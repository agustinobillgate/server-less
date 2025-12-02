#using conversion tools version: 1.0.0.117
#---------------------------------------------------------------------
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#---------------------------------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Gl_acct, L_op, Gl_jouhdr, Htparam, L_kredit, L_lieferant, Ap_journal, Counters, Gl_journal
from functions.next_counter_for_update import next_counter_for_update

s_list_data, S_list = create_model("S_list", {"fibukonto":string, "debit":Decimal, "credit":Decimal, "flag":bool, "bezeich":string, "remark":string}, {"fibukonto": "000000000000"})

def mk_ap_btn_ok_1bl(s_list_data:[S_list], pvilanguage:int, invoice:string, journ_flag:bool, balance:Decimal, avail_sbuff:bool, 
                     docu_nr:string, rgdatum:date, lief_nr:int, disc:Decimal, saldo:Decimal, d_amount:Decimal, ziel:int, nr:int, 
                     comments:string, netto:Decimal, userinit:string, ap_other:string, user_init:string, firma:string, 
                     s_list_fibukonto:string, s_list_debit:Decimal, tax_code:string, tax_amt:string):

    prepare_cache ([L_op, Gl_jouhdr, Htparam, L_kredit, L_lieferant, Ap_journal, Counters, Gl_journal])

    msg_str = ""
    fl_code = 0
    avail_gl = True
    return_flag:bool = False
    lvcarea:string = "mk-ap"
    gl_close_month:date = None
    ch:string = ""
    gl_acct = l_op = gl_jouhdr = htparam = l_kredit = l_lieferant = ap_journal = counters = gl_journal = None

    s_list = sbuff = None

    Sbuff = S_list
    sbuff_data = s_list_data

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    invoice = invoice.strip()
    docu_nr = docu_nr.strip()
    comments = comments.strip()
    userinit = userinit.strip()
    user_init = user_init.strip()
    ap_other = ap_other.strip()
    firma = firma.strip()
    s_list_fibukonto = s_list_fibukonto.strip()
    tax_code = tax_code.strip()
    tax_amt = tax_amt.strip()

    def generate_output():
        nonlocal msg_str, fl_code, avail_gl, return_flag, lvcarea, gl_close_month, ch, gl_acct, l_op, gl_jouhdr, htparam, l_kredit, l_lieferant, ap_journal, counters, gl_journal
        nonlocal pvilanguage, invoice, journ_flag, balance, avail_sbuff, docu_nr, rgdatum, lief_nr, disc, saldo, d_amount, ziel, nr, comments, netto, userinit, ap_other, user_init, firma, s_list_fibukonto, s_list_debit, tax_code, tax_amt
        nonlocal sbuff

        nonlocal s_list, sbuff

        return {"s-list": s_list_data, "msg_str": msg_str, "fl_code": fl_code, "avail_gl": avail_gl}

    for s_list in query(s_list_data):

        if s_list.debit != 0:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, s_list.fibukonto)]})

            if not gl_acct:
                avail_gl = False

        if to_decimal(s_list.fibukonto) != 0:

            gl_acct = get_cache (Gl_acct, {"fibukonto": [(eq, s_list.fibukonto)]})

            if not gl_acct:
                avail_gl = False

        if not avail_gl:
            s_list.flag = True
            return_flag = True

            break

    if return_flag:

        return generate_output()

    l_op = get_cache (L_op, {"op_art": [(eq, 1)],"loeschflag": [(le, 1)],"lscheinnr": [(eq, invoice)]})

    if l_op:
        msg_str = msg_str + chr_unicode(2) + translateExtended ("Same Delivery No exists in Receiving Record, date =", lvcarea, "") + " " + to_string(l_op.datum) + " - " + l_op.docu_nr
        fl_code = 1

        return generate_output()

    if journ_flag:

        if balance != 0:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Journal Transaction NOT balanced.", lvcarea, "")
            fl_code = 2

            return generate_output()

        if not avail_sbuff:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Journal record NOT found.", lvcarea, "")
            fl_code = 3

            return generate_output()

        gl_jouhdr = get_cache (Gl_jouhdr, {"refno": [(eq, docu_nr)]})

        if gl_jouhdr:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("Same G/L RefNo exists, date =", lvcarea, "") + " " + to_string(gl_jouhdr.datum)
            fl_code = 4

            return generate_output()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 558)]})

        if rgdatum <= htparam.fdate:
            msg_str = msg_str + chr_unicode(2) + translateExtended ("A/P transaction date too old.", lvcarea, "")
            fl_code = 5

            return generate_output()
    else:

        l_kredit = get_cache (L_kredit, {"lief_nr": [(ne, lief_nr)],"name": [(eq, docu_nr)],"zahlkonto": [(eq, 0)]})

        if l_kredit:

            l_lieferant = get_cache (L_lieferant, {"lief_nr": [(eq, lief_nr)]})

            if l_lieferant:
                ch = l_lieferant.firma
            msg_str = msg_str + chr_unicode(2) + translateExtended ("A/P with same RefNo exists:", lvcarea, "") + " " + to_string(l_kredit.rgdatum) + " " + ch
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
        l_kredit.saldo =  to_decimal(saldo)
        l_kredit.rabatt =  to_decimal(disc)
        l_kredit.rabattbetrag =  to_decimal(d_amount)
        l_kredit.ziel = ziel
        l_kredit.netto =  to_decimal(netto)
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
        ap_journal.saldo =  to_decimal(saldo)
        ap_journal.netto =  to_decimal(netto)
        ap_journal.userinit = userinit
        ap_journal.zeit = get_current_time_in_seconds()
        ap_journal.betriebsnr = to_int(journ_flag)

        if journ_flag:

            # counters = get_cache (Counters, {"counter_no": [(eq, 25)]})
            counters = db_session.query(Counters).filter(
                     (Counters.counter_no == 25)).with_for_update().first()

            if not counters:
                counters = Counters()
                db_session.add(counters)

                counters.counter_no = 25
                counters.counter_bez = translateExtended ("G/L Transaction Journal", lvcarea, "")
            counters.counter = counters.counter + 1
            gl_jouhdr = Gl_jouhdr()
            db_session.add(gl_jouhdr)

            gl_jouhdr.jnr = counters.counter

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
                gl_journal.credit =  to_decimal(netto)
            else:
                gl_journal.debit =  - to_decimal(netto)

            if l_kredit.bemerk != "":

                if num_entries(l_kredit.bemerk, ";") > 1:
                    gl_journal.bemerk = gl_journal.bemerk + " - " + entry(0, l_kredit.bemerk, ";")
                else:
                    gl_journal.bemerk = gl_journal.bemerk + " - " + l_kredit.bemerk
            gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) + to_decimal(gl_journal.credit)
            gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) + to_decimal(gl_journal.debit)

            for sbuff in query(sbuff_data, filters=(lambda sbuff: to_decimal(sbuff.fibukonto) != 0)):
                gl_journal = Gl_journal()
                db_session.add(gl_journal)

                gl_journal.jnr = gl_jouhdr.jnr
                gl_journal.fibukonto = sbuff.fibukonto
                gl_journal.userinit = user_init
                gl_journal.zeit = get_current_time_in_seconds()
                gl_journal.bemerk = sbuff.remark
                gl_journal.debit =  to_decimal(sbuff.debit)
                gl_journal.credit =  to_decimal(sbuff.credit)
                gl_jouhdr.credit =  to_decimal(gl_jouhdr.credit) + to_decimal(gl_journal.credit)
                gl_jouhdr.debit =  to_decimal(gl_jouhdr.debit) + to_decimal(gl_journal.debit)
                pass
            pass

    return generate_output()