from functions.additional_functions import *
import decimal
from datetime import date
from functions.fo_journal_1bl import fo_journal_1bl

def fo_journal_list_webbl(from_art:int, to_art:int, from_dept:int, to_dept:int, from_date:date, to_date:date, sorttype:int, exclude_artrans:bool, long_digit:bool, foreign_flag:bool, onlyjournal:bool, excljournal:bool, mi_post:bool, mi_showrelease:bool):
    fo_journal_list_list = []
    gtot:decimal = 0

    output_list = fo_journal_list = None

    output_list_list, Output_list = create_model("Output_list", {"bezeich":str, "c":str, "ns":str, "mb":str, "shift":str, "dept":str, "str":str, "remark":str, "gname":str, "descr":str, "voucher":str, "checkin":date, "checkout":date, "guestname":str})
    fo_journal_list_list, Fo_journal_list = create_model("Fo_journal_list", {"datum":date, "c":str, "roomnumber":str, "nsflag":str, "mbflag":str, "shift":str, "billno":int, "artno":int, "bezeich":str, "voucher":str, "depart":str, "outlet":str, "qty":int, "amount":decimal, "guestname":str, "billrcvr":str, "zeit":str, "id":str, "sysdate":date, "remark":str, "checkin":date, "checkout":date})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal fo_journal_list_list, gtot


        nonlocal output_list, fo_journal_list
        nonlocal output_list_list, fo_journal_list_list
        return {"fo-journal-list": fo_journal_list_list}

    gtot, output_list_list = get_output(fo_journal_1bl(from_art, to_art, from_dept, to_dept, from_date, to_date, sorttype, exclude_artrans, long_digit, foreign_flag, onlyjournal, excljournal, mi_post, mi_showrelease))
    fo_journal_list_list.clear()

    for output_list in query(output_list_list):
        fo_journal_list = Fo_journal_list()
        fo_journal_list_list.append(fo_journal_list)

        fo_journal_list.datum = date_mdy(substring(output_list.str, 0, 8))
        fo_journal_list.c = output_list.c
        fo_journal_list.roomnumber = substring(output_list.STR, 8, 6)
        fo_journal_list.nsflag = output_list.ns
        fo_journal_list.mbflag = output_list.mb
        fo_journal_list.shift = output_list.shift
        fo_journal_list.billno = to_int(substring(output_list.STR, 14, 9))
        fo_journal_list.artno = to_int(substring(output_list.STR, 23, 4))
        fo_journal_list.bezeich = output_list.descr
        fo_journal_list.voucher = output_list.voucher
        fo_journal_list.depart = substring(output_list.STR, 77, 12)
        fo_journal_list.outlet = substring(output_list.STR, 89, 6)
        fo_journal_list.qty = to_int(substring(output_list.STR, 95, 5))
        fo_journal_list.amount = decimal.Decimal(substring(output_list.STR, 100, 22))
        fo_journal_list.guestname = output_list.guestname
        fo_journal_list.billrcvr = output_list.gname
        fo_journal_list.zeit = substring(output_list.STR, 122, 8)
        fo_journal_list.id = substring(output_list.STR, 130, 4)
        fo_journal_list.sysdate = date_mdy(substring(output_list.STR, 134, 8))
        fo_journal_list.remark = output_list.remark
        fo_journal_list.checkin = output_list.checkin
        fo_journal_list.checkout = output_list.checkout

    return generate_output()