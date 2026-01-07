#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 14/8/2025
# if available bqueasy
# Rd, 25/11/2025, with_for_update added
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Queasy, Paramtext
from sqlalchemy import func, and_, or_


out_list_data, Out_list = create_model("Out_list", {"s_recid":int, "marked":string, "fibukonto":string, "jnr":int, "jtype":int, "bemerk":string, "trans_date":date, "bezeich":string, "number1":string, "debit":Decimal, "credit":Decimal, "balance":Decimal, "debit_str":string, "credit_str":string, "balance_str":string, "refno":string, "uid":string, "created":date, "chgid":string, "chgdate":date, "tax_code":string, "tax_amount":string, "tot_amt":string, "approved":bool, "prev_bal":string, "dept_code":int, "coa_bezeich":string})

def gl_joulist2_create_output_web_1bl(idflag:string, out_list_data:[Out_list]):

    prepare_cache ([Paramtext])

    doneflag = False
    counter:int = 0
    htl_no:string = ""
    temp_char:string = ""
    curr_time:int = 0
    queasy = paramtext = None

    out_list = bqueasy = pqueasy = tqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, counter, htl_no, temp_char, curr_time, queasy, paramtext
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal out_list, bqueasy, pqueasy, tqueasy

        return {"doneflag": doneflag, "out-list": out_list_data}

    def decode_string(in_str:string):

        nonlocal doneflag, counter, htl_no, temp_char, curr_time, queasy, paramtext
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal out_list, bqueasy, pqueasy, tqueasy

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

    # Oscar - disable time sleep (not needed)
    # count = retry = tmp_count = 0
    # while True:
    #     count = db_session.query(Queasy).filter((Queasy.key == 280) & (func.lower(Queasy.char1) == "general ledger") & (Queasy.char3 == (idflag))).count()

    #     if count >= 500:
    #         break

    #     if tmp_count == 0 and retry > 1:
    #         break

    #     if tmp_count > 0 and tmp_count == count:
    #         break

    #     tmp_count = count
    #     retry += 1

    #     time.sleep(0.5)

    # paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})
    paramtext = db_session.query(Paramtext).filter((Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)
        
    curr_time = get_current_time_in_seconds()

    # queasy = get_cache (Queasy, {"key": [(eq, 280)],"char1": [(eq, "general ledger")],"char3": [(eq, idflag)]})
    # while None != queasy:

    queasy = Queasy()
    for queasy_char2, queasy_recid in db_session.query(Queasy.char2, Queasy._recid).filter((Queasy.key == 280) & (func.lower(Queasy.char1) == 'general ledger') & (Queasy.char3 == idflag)).order_by(Queasy._recid).yield_per(100):
        counter = counter + 1

        if counter > 500:
            break

        out_list = Out_list()
        out_list_data.append(out_list)

        out_list.s_recid = to_int(entry(0, queasy_char2, "|"))
        out_list.marked = entry(1, queasy_char2, "|")
        out_list.fibukonto = entry(2, queasy_char2, "|")
        out_list.jnr = to_int(entry(3, queasy_char2, "|"))
        out_list.jtype = to_int(entry(4, queasy_char2, "|"))
        out_list.bemerk = entry(5, queasy_char2, "|")
        out_list.bezeich = entry(7, queasy_char2, "|")
        out_list.number1 = entry(8, queasy_char2, "|")
        out_list.debit =  to_decimal(to_decimal(entry(9 , queasy_char2 , "|")) )
        out_list.credit =  to_decimal(to_decimal(entry(10 , queasy_char2 , "|")) )
        out_list.balance =  to_decimal(to_decimal(entry(11 , queasy_char2 , "|")) )
        out_list.debit_str = entry(12, queasy_char2, "|")
        out_list.credit_str = entry(13, queasy_char2, "|")
        out_list.balance_str = entry(14, queasy_char2, "|")
        out_list.refno = entry(15, queasy_char2, "|")
        out_list.uid = entry(16, queasy_char2, "|")
        out_list.chgid = entry(18, queasy_char2, "|")
        out_list.tax_code = entry(20, queasy_char2, "|")
        out_list.tax_amount = entry(21, queasy_char2, "|")
        out_list.tot_amt = entry(22, queasy_char2, "|")
        out_list.prev_bal = entry(24, queasy_char2, "|")
        out_list.dept_code = to_int(entry(25, queasy_char2, "|"))
        out_list.coa_bezeich = entry(26, queasy_char2, "|")

        if entry(23, (queasy_char2).lower(), "|") == ("no").lower() :
            out_list.approved = False

        elif entry(23, (queasy_char2).lower(), "|") == ("yes").lower() :
            out_list.approved = True

        if entry(6, queasy_char2, "|") != "":
            out_list.trans_date = entry(6, queasy_char2, "|")

        if entry(17, queasy_char2, "|") != "":
            out_list.created = entry(17, queasy_char2, "|")

        if entry(19, queasy_char2, "|") != "":
            out_list.chgdate = entry(19, queasy_char2, "|")

        # Rd 25/11/2025, with_for_update added
        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy_recid)).with_for_update().first()
        
        # Rd 14/8/2025
        if bqueasy:
            db_session.delete(bqueasy)
        

        # curr_recid = queasy._recid
        # queasy = db_session.query(Queasy).filter(
        #          (Queasy.key == 280) & (func.lower(Queasy.char1) == ("General Ledger").lower()) & (Queasy.char3 == idflag) & (Queasy._recid > curr_recid)).first()

    pqueasy = db_session.query(Pqueasy).filter((Pqueasy.key == 280) & (func.lower(Pqueasy.char1) == "general ledger") & (Pqueasy.char3 == idflag)).first()

    if pqueasy:
        doneflag = False
    else:
        tqueasy = db_session.query(Tqueasy).filter((Tqueasy.key == 285) & (func.lower(Tqueasy.char1) == "general ledger") & (Tqueasy.number1 == 1) & (Tqueasy.char2 == idflag)).first()

        if tqueasy:
            doneflag = False
        else:
            doneflag = True

    # Rd, 25/11/2025, with_for_update added
    tqueasy = db_session.query(Tqueasy).filter((Tqueasy.key == 285) & (func.lower(Tqueasy.char1) == "general ledger") & (Tqueasy.number1 == 0) & (Tqueasy.char2 == idflag)).with_for_update().first()

    if tqueasy:
        db_session.delete(tqueasy)

    return generate_output()