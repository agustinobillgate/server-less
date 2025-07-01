#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.gacct_balance_btn_go_listbl import gacct_balance_btn_go_listbl
from models import Queasy, Paramtext

bill_alert_list, Bill_alert = create_model("Bill_alert", {"rechnr":int})

def gacct_balance_btn_go_list_webbl(pvilanguage:int, bill_alert_list:[Bill_alert], heute:date, billdate:date, ank_flag:bool, sorttype:int, fact1:int, price_decimal:int, short_flag:bool, idflag:string):

    prepare_cache ([Queasy, Paramtext])

    msg_str = ""
    msg_str2 = ""
    i_counter:string = ""
    flag:string = ""
    artnr:string = ""
    dept:string = ""
    ankunft:string = ""
    ankzeit:string = ""
    typebill:string = ""
    bill_datum:string = ""
    guest:string = ""
    roomno:string = ""
    billno:string = ""
    billnr:string = ""
    bezeich:string = ""
    prevbala:string = ""
    debit:string = ""
    credit:string = ""
    balance:string = ""
    depart:string = ""
    counter:int = 0
    str:string = ""
    htl_no:string = ""
    queasy = paramtext = None

    gacct_balance_list = bill_alert = bqueasy = tqueasy = t_list = None

    gacct_balance_list_list, Gacct_balance_list = create_model("Gacct_balance_list", {"i_counter":int, "flag":int, "artnr":int, "dept":int, "ankunft":date, "ankzeit":string, "typebill":string, "billdatum":date, "guest":string, "roomno":string, "billno":int, "billnr":int, "bezeich":string, "prevbala":Decimal, "debit":Decimal, "credit":Decimal, "balance":Decimal, "depart":date})

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)
    T_list = Gacct_balance_list
    t_list_list = gacct_balance_list_list

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, msg_str2, i_counter, flag, artnr, dept, ankunft, ankzeit, typebill, bill_datum, guest, roomno, billno, billnr, bezeich, prevbala, debit, credit, balance, depart, counter, str, htl_no, queasy, paramtext
        nonlocal pvilanguage, heute, billdate, ank_flag, sorttype, fact1, price_decimal, short_flag, idflag
        nonlocal bqueasy, tqueasy, t_list


        nonlocal gacct_balance_list, bill_alert, bqueasy, tqueasy, t_list
        nonlocal gacct_balance_list_list

        return {"msg_str": msg_str, "msg_str2": msg_str2}

    def decode_string(in_str:string):

        nonlocal msg_str, msg_str2, i_counter, flag, artnr, dept, ankunft, ankzeit, typebill, bill_datum, guest, roomno, billno, billnr, bezeich, prevbala, debit, credit, balance, depart, counter, str, htl_no, queasy, paramtext
        nonlocal pvilanguage, heute, billdate, ank_flag, sorttype, fact1, price_decimal, short_flag, idflag
        nonlocal bqueasy, tqueasy, t_list


        nonlocal gacct_balance_list, bill_alert, bqueasy, tqueasy, t_list
        nonlocal gacct_balance_list_list

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
    queasy.char1 = "guest Ledger Report"
    queasy.number1 = 1
    queasy.char2 = idflag


    pass

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 243)]})

    if paramtext and paramtext.ptexte != "":
        htl_no = decode_string(paramtext.ptexte)
    msg_str, msg_str2, gacct_balance_list_list = get_output(gacct_balance_btn_go_listbl(pvilanguage, bill_alert_list, heute, billdate, ank_flag, sorttype, fact1, price_decimal, short_flag))

    gacct_balance_list = query(gacct_balance_list_list, first=True)
    while None != gacct_balance_list:

        if gacct_balance_list.ankunft == None:
            ankunft = ""
        else:
            ankunft = to_string(gacct_balance_list.ankunft)

        if gacct_balance_list.billdatum == None:
            bill_datum = ""
        else:
            bill_datum = to_string(gacct_balance_list.billdatum)

        if gacct_balance_list.depart == None:
            depart = ""
        else:
            depart = to_string(gacct_balance_list.depart)

        if matches(gacct_balance_list.guest,r"*|*"):
            guest = replace_str(gacct_balance_list.guest, "|", "&")
        else:
            guest = gacct_balance_list.guest

        if matches(gacct_balance_list.bezeich,r"*|*"):
            bezeich = replace_str(gacct_balance_list.bezeich, "|", " ")
        else:
            bezeich = gacct_balance_list.bezeich
        queasy = Queasy()
        db_session.add(queasy)

        counter = counter + 1
        queasy.key = 280
        queasy.char1 = "guest Ledger Report"
        queasy.char3 = idflag
        queasy.char2 = to_string(gacct_balance_list.i_counter) + "|" +\
                to_string(gacct_balance_list.flag) + "|" +\
                to_string(gacct_balance_list.artnr) + "|" +\
                to_string(gacct_balance_list.dept) + "|" +\
                ankunft + "|" +\
                gacct_balance_list.ankzeit + "|" +\
                gacct_balance_list.typebill + "|" +\
                bill_datum + "|" +\
                guest + "|" +\
                gacct_balance_list.roomno + "|" +\
                to_string(gacct_balance_list.billno) + "|" +\
                to_string(gacct_balance_list.billnr) + "|" +\
                bezeich + "|" +\
                to_string(gacct_balance_list.prevbala) + "|" +\
                to_string(gacct_balance_list.debit) + "|" +\
                to_string(gacct_balance_list.credit) + "|" +\
                to_string(gacct_balance_list.balance) + "|" +\
                depart


        queasy.number1 = to_int(counter)

        gacct_balance_list = query(gacct_balance_list_list, next=True)

    bqueasy = get_cache (Queasy, {"key": [(eq, 285)],"char1": [(eq, "guest ledger report")],"char2": [(eq, idflag)]})

    if bqueasy:
        pass
        bqueasy.number1 = 0


        pass
        pass

    return generate_output()