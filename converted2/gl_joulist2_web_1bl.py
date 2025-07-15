#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gl_joulist_2_webbl import gl_joulist_2_webbl
from models import Queasy, Paramtext

def gl_joulist2_web_1bl(from_date:date, to_date:date, last_2yr:date, close_year:date, journaltype:int, excl_other:bool, other_dept:bool, summ_date:bool, from_fibu:string, to_fibu:string, sorttype:int, from_dept:int, journaltype1:int, cashflow:bool, f_note:string, from_main:int, idflag:string):

    prepare_cache ([Queasy, Paramtext])

    str:string = ""
    htl_no:string = ""
    tdate:string = ""
    crdate:string = ""
    cgdate:string = ""
    counter:int = 0
    curr_time:int = 0
    queasy = paramtext = None

    out_list = g_list = j_list = bqueasy = tqueasy = None

    out_list_data, Out_list = create_model("Out_list", {"s_recid":int, "marked":string, "fibukonto":string, "jnr":int, "jtype":int, "bemerk":string, "trans_date":date, "bezeich":string, "number1":string, "debit":Decimal, "credit":Decimal, "balance":Decimal, "debit_str":string, "credit_str":string, "balance_str":string, "refno":string, "uid":string, "created":date, "chgid":string, "chgdate":date, "tax_code":string, "tax_amount":string, "tot_amt":string, "approved":bool, "prev_bal":string, "dept_code":int, "coa_bezeich":string})
    g_list_data, G_list = create_model("G_list", {"grecid":int, "fibu":string})
    j_list_data, J_list = create_model("J_list", {"grecid":int, "fibu":string, "datum":date})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal str, htl_no, tdate, crdate, cgdate, counter, curr_time, queasy, paramtext
        nonlocal from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main, idflag
        nonlocal bqueasy, tqueasy


        nonlocal out_list, g_list, j_list, bqueasy, tqueasy
        nonlocal out_list_data, g_list_data, j_list_data

        return {}

    def decode_string(in_str:string):

        nonlocal str, htl_no, tdate, crdate, cgdate, counter, curr_time, queasy, paramtext
        nonlocal from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main, idflag
        nonlocal bqueasy, tqueasy


        nonlocal out_list, g_list, j_list, bqueasy, tqueasy
        nonlocal out_list_data, g_list_data, j_list_data

        out_str = ""
        s:string = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = length(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,length(s)  + 1) :
            out_str = out_str + chr_unicode(asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()

    queasy = Queasy()
    db_session.add(queasy)

    queasy.key = 285
    queasy.char1 = "General Ledger"
    queasy.number1 = 1
    queasy.char2 = idflag


    pass
    curr_time = get_current_time_in_seconds()

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)
    out_list_data = get_output(gl_joulist_2_webbl(from_date, to_date, last_2yr, close_year, journaltype, excl_other, other_dept, summ_date, from_fibu, to_fibu, sorttype, from_dept, journaltype1, cashflow, f_note, from_main))
    curr_time = get_current_time_in_seconds()

    out_list = query(out_list_data, first=True)
    while None != out_list:

        if length(out_list.bemerk) > 100:
            out_list.bemerk = substring(out_list.bemerk, 0, 100)

        if length(out_list.bezeich) > 100:
            out_list.bezeich = substring(out_list.bezeich, 0, 100)

        if length(out_list.refno) > 100:
            out_list.refno = substring(out_list.refno, 0, 100)


        out_list.bezeich = replace_str(out_list.bezeich, chr_unicode(10) , "")
        out_list.bezeich = replace_str(out_list.bezeich, chr_unicode(13) , "")
        out_list.refno = replace_str(out_list.refno, chr_unicode(10) , "")
        out_list.refno = replace_str(out_list.refno, chr_unicode(13) , "")
        out_list.bemerk = replace_str(out_list.bemerk, chr_unicode(10) , "")
        out_list.bemerk = replace_str(out_list.bemerk, chr_unicode(13) , "")
        out_list.bemerk = replace_str(out_list.bemerk, "|", " ")
        out_list.bezeich = replace_str(out_list.bezeich, "|", " ")
        out_list.refno = replace_str(out_list.refno, "|", " ")
        counter = counter + 1

        if out_list.uid == None:
            out_list.uid = ""

        if out_list.trans_date == None:
            tdate = ""


        else:
            tdate = to_string(out_list.trans_date)

        if out_list.created == None:
            crdate = ""


        else:
            crdate = to_string(out_list.created)

        if out_list.chgDate == None:
            cgdate = ""


        else:
            cgdate = to_string(out_list.chgDate)


        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 280
        queasy.char1 = "General Ledger"
        queasy.char3 = idflag
        queasy.char2 = to_string(out_list.s_recid) + "|" +\
                out_list.marked + "|" +\
                out_list.fibukonto + "|" +\
                to_string(out_list.jnr) + "|" +\
                to_string(out_list.jtype) + "|" +\
                out_list.bemerk + "|" +\
                tdate + "|" +\
                out_list.bezeich + "|" +\
                out_list.number1 + "|" +\
                to_string(out_list.debit) + "|" +\
                to_string(out_list.credit) + "|" +\
                to_string(out_list.balance) + "|" +\
                out_list.debit_str + "|" +\
                out_list.credit_str + "|" +\
                out_list.balance_str + "|" +\
                out_list.refno + "|" +\
                out_list.uid + "|" +\
                crdate + "|" +\
                out_list.chgID + "|" +\
                cgdate + "|" +\
                out_list.tax_code + "|" +\
                out_list.tax_amount + "|" +\
                out_list.tot_amt + "|" +\
                to_string(out_list.approved) + "|" +\
                out_list.prev_bal + "|" +\
                to_string(out_list.dept_code) + "|" +\
                to_string(out_list.coa_bezeich)
        queasy.number1 = counter

        out_list = query(out_list_data, next=True)

    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "general ledger")],"char2": [(eq, idflag)]})

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()