#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 14/8/2025
# if available bqueasy
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Paramtext

gacct_balance_list_data, Gacct_balance_list = create_model("Gacct_balance_list", {"i_counter":int, "flag":int, "artnr":int, "dept":int, "ankunft":string, "ankzeit":string, "typebill":string, "billdatum":string, "guest":string, "roomno":string, "billno":int, "billnr":int, "bezeich":string, "prevbala":Decimal, "debit":Decimal, "credit":Decimal, "balance":Decimal, "depart":string})

def gacct_balance_btn_go_list_create_output_webbl(idflag:string, gacct_balance_list_data:[Gacct_balance_list]):

    prepare_cache ([Paramtext])

    doneflag = False
    counter:int = 0
    htl_no:string = ""
    temp_char:string = ""
    ankunft:string = ""
    bill_datum:string = ""
    depart:string = ""
    queasy = paramtext = None

    gacct_balance_list = bqueasy = pqueasy = tqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, counter, htl_no, temp_char, ankunft, bill_datum, depart, queasy, paramtext
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal gacct_balance_list, bqueasy, pqueasy, tqueasy

        return {"doneflag": doneflag, "gacct-balance-list": gacct_balance_list_data}

    def decode_string(in_str:string):

        nonlocal doneflag, counter, htl_no, temp_char, ankunft, bill_datum, depart, queasy, paramtext
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal gacct_balance_list, bqueasy, pqueasy, tqueasy

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


    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 280) & (Queasy.char1 == ("Guest Ledger Report").lower()) & (Queasy.char3 == idflag)).order_by(Queasy.number1).all():
        counter = counter + 1

        if counter > 1000:
            break
        gacct_balance_list = Gacct_balance_list()
        gacct_balance_list_data.append(gacct_balance_list)

        gacct_balance_list.i_counter = to_int(entry(0, queasy.char2, "|"))
        gacct_balance_list.flag = to_int(entry(1, queasy.char2, "|"))
        gacct_balance_list.artnr = to_int(entry(2, queasy.char2, "|"))
        gacct_balance_list.dept = to_int(entry(3, queasy.char2, "|"))
        gacct_balance_list.ankunft = entry(4, queasy.char2, "|")
        gacct_balance_list.ankzeit = entry(5, queasy.char2, "|")
        gacct_balance_list.typebill = entry(6, queasy.char2, "|")
        gacct_balance_list.billdatum = entry(7, queasy.char2, "|")
        gacct_balance_list.guest = entry(8, queasy.char2, "|")
        gacct_balance_list.roomno = entry(9, queasy.char2, "|")
        gacct_balance_list.billno = to_int(entry(10, queasy.char2, "|"))
        gacct_balance_list.billnr = to_int(entry(11, queasy.char2, "|"))
        gacct_balance_list.bezeich = entry(12, queasy.char2, "|")
        gacct_balance_list.prevbala =  to_decimal(to_decimal(entry(13 , queasy.char2 , "|")) )
        gacct_balance_list.debit =  to_decimal(to_decimal(entry(14 , queasy.char2 , "|")) )
        gacct_balance_list.credit =  to_decimal(to_decimal(entry(15 , queasy.char2 , "|")) )
        gacct_balance_list.balance =  to_decimal(to_decimal(entry(16 , queasy.char2 , "|")) )
        gacct_balance_list.depart = entry(17, queasy.char2, "|")

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).first()
        # Rd 14/8/2025
        if bqueasy:
            db_session.delete(bqueasy)
        pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("Guest Ledger Report").lower()) & (Pqueasy.char3 == idflag)).first()

    if pqueasy:
        doneflag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("Guest Ledger Report").lower()) & (Tqueasy.number1 == 1) & (Tqueasy.char2 == idflag)).first()

        if tqueasy:
            doneflag = False


        else:
            doneflag = True

    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (Tqueasy.char1 == ("Guest Ledger Report").lower()) & (Tqueasy.number1 == 0) & (Tqueasy.char2 == idflag)).first()

    if tqueasy:
        pass
        db_session.delete(tqueasy)
        pass

    return generate_output()