from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Queasy, Paramtext

out_list_list, Out_list = create_model("Out_list", {"s_recid":int, "marked":str, "fibukonto":str, "jnr":int, "jtype":int, "bemerk":str, "trans_date":date, "bezeich":str, "number1":str, "debit":decimal, "credit":decimal, "balance":decimal, "debit_str":str, "credit_str":str, "balance_str":str, "refno":str, "uid":str, "created":date, "chgid":str, "chgdate":date, "tax_code":str, "tax_amount":str, "tot_amt":str, "approved":bool, "prev_bal":str})

def gl_joulist2_create_output_webbl(out_list_list:[Out_list]):
    doneflag = False
    counter:int = 0
    htl_no:str = ""
    temp_char:str = ""
    queasy = paramtext = None

    out_list = bqueasy = pqueasy = tqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, counter, htl_no, temp_char, queasy, paramtext
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal out_list, bqueasy, pqueasy, tqueasy
        nonlocal out_list_list
        return {"doneflag": doneflag, "out-list": out_list_list}

    def decode_string(in_str:str):

        nonlocal doneflag, counter, htl_no, temp_char, queasy, paramtext
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal out_list, bqueasy, pqueasy, tqueasy
        nonlocal out_list_list

        out_str = ""
        s:str = ""
        j:int = 0
        len_:int = 0

        def generate_inner_output():
            return (out_str)

        s = in_str
        j = asc(substring(s, 0, 1)) - 70
        len_ = len(in_str) - 1
        s = substring(in_str, 1, len_)
        for len_ in range(1,len(s)  + 1) :
            out_str = out_str + chr (asc(substring(s, len_ - 1, 1)) - j)

        return generate_inner_output()


    paramtext = db_session.query(Paramtext).filter(
             (Paramtext.txtnr == 243)).first()

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 280) & (func.lower(Queasy.char1) == ("General Ledger").lower())).order_by(Queasy.number1).all():
        counter = counter + 1

        if counter > 700:
            break
        out_list = Out_list()
        out_list_list.append(out_list)

        out_list.s_recid = to_int(entry(0, queasy.char2, "|"))
        out_list.marked = entry(1, queasy.char2, "|")
        out_list.fibukonto = entry(2, queasy.char2, "|")
        out_list.jnr = to_int(entry(3, queasy.char2, "|"))
        out_list.jtype = to_int(entry(4, queasy.char2, "|"))
        out_list.bemerk = entry(5, queasy.char2, "|")
        out_list.bezeich = entry(7, queasy.char2, "|")
        out_list.number1 = entry(8, queasy.char2, "|")
        out_list.debit =  to_decimal(to_decimal(entry(9 , queasy.char2 , "|")) )
        out_list.credit =  to_decimal(to_decimal(entry(10 , queasy.char2 , "|")) )
        out_list.balance =  to_decimal(to_decimal(entry(11 , queasy.char2 , "|")) )
        out_list.debit_str = entry(12, queasy.char2, "|")
        out_list.credit_str = entry(13, queasy.char2, "|")
        out_list.balance_str = entry(14, queasy.char2, "|")
        out_list.refno = entry(15, queasy.char2, "|")
        out_list.uid = entry(16, queasy.char2, "|")
        out_list.chgid = entry(18, queasy.char2, "|")
        out_list.tax_code = entry(20, queasy.char2, "|")
        out_list.tax_amount = entry(21, queasy.char2, "|")
        out_list.tot_amt = entry(22, queasy.char2, "|")
        out_list.prev_bal = entry(24, queasy.char2, "|")

        if entry(23, queasy.char2, "|") == ("no").lower() :
            out_list.approved = False

        elif entry(23, queasy.char2, "|") == ("yes").lower() :
            out_list.approved = True

        if entry(6, queasy.char2, "|") != "":
            out_list.trans_date = date_mdy(to_int(entry(1, entry(6, queasy.char2, "|") , "/")) , to_int(entry(0, entry(6, queasy.char2, "|") , "/")) , to_int(entry(2, entry(6, queasy.char2, "|") , "/")))

        if entry(17, queasy.char2, "|") != "" and entry(17, queasy.char2, "|re.match(r".*","), re.IGNORECASE):
            out_list.created = date_mdy(to_int(entry(1, entry(17, queasy.char2, "|") , "/")) , to_int(entry(0, entry(17, queasy.char2, "|") , "/")) , to_int(entry(2, entry(17, queasy.char2, "|") , "/")))

        if entry(19, queasy.char2, "|") != "":
            out_list.chgdate = date_mdy(to_int(entry(1, entry(19, queasy.char2, "|") , "/")) , to_int(entry(0, entry(19, queasy.char2, "|") , "/")) , to_int(entry(2, entry(19, queasy.char2, "|") , "/")))

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).first()
        bqueasy_list.remove(bqueasy)
        pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (func.lower(Pqueasy.char1) == ("General Ledger").lower()) & (func.lower(Pqueasy.char3) == ("PROCESS").lower())).first()

    if pqueasy:
        doneflag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (func.lower(Tqueasy.char1) == ("General Ledger").lower()) & (Tqueasy.number1 == 1)).first()

        if tqueasy:
            doneflag = False


        else:
            doneflag = True

    return generate_output()