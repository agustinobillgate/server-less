#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Htparam, Artikel, Billjournal, Bill_line, Bill

def prepare_guest_depositpay_webbl(pvilanguage:int, user_init:string, guest_number:int, guest_name:string):

    prepare_cache ([Htparam, Artikel, Bill_line])

    deposit_balance = to_decimal("0.0")
    error_desc = ""
    guest_deposit_list_data = []
    lvcarea:string = "prepare-guest-depositPay-web"
    depoart_guest:int = 0
    depobez_guest:string = ""
    depoart_rsv:int = 0
    depoart_bqt:int = 0
    depoart_pos:int = 0
    str:string = ""
    uniq_str:string = ""
    htparam = artikel = billjournal = bill_line = bill = None

    guest_deposit_list = None

    guest_deposit_list_data, Guest_deposit_list = create_model("Guest_deposit_list", {"guest_number":int, "article_number":int, "article_desc":string, "trans_amount":Decimal, "trans_date":string, "trans_remark":string, "res_number":string, "bill_number":int, "bill_type":string, "user_init":string, "flag":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal deposit_balance, error_desc, guest_deposit_list_data, lvcarea, depoart_guest, depobez_guest, depoart_rsv, depoart_bqt, depoart_pos, str, uniq_str, htparam, artikel, billjournal, bill_line, bill
        nonlocal pvilanguage, user_init, guest_number, guest_name


        nonlocal guest_deposit_list
        nonlocal guest_deposit_list_data

        return {"deposit_balance": deposit_balance, "error_desc": error_desc, "guest-deposit-list": guest_deposit_list_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1068)],"finteger": [(ne, 0)]})

    if htparam:

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if not artikel or artikel.artart != 5:
            error_desc = translateExtended ("Deposit article not defined.", lvcarea, "")

            return generate_output()
        depoart_guest = artikel.artnr
        depobez_guest = artikel.bezeich


    else:

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

    if htparam:
        depoart_rsv = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 117)]})

    if htparam:
        depoart_bqt = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1361)]})

    if htparam:
        depoart_pos = htparam.finteger

    billjournal = db_session.query(Billjournal).filter(
             (Billjournal.billjou_ref == guest_number) & (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & (Billjournal.artnr != depoart_pos) & (num_entries(Billjournal.bezeich, "[") > 1) & (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit").lower())).first()
    while None != billjournal:
        guest_deposit_list = Guest_deposit_list()
        guest_deposit_list_data.append(guest_deposit_list)

        guest_deposit_list.guest_number = guest_number
        guest_deposit_list.article_number = billjournal.artnr
        guest_deposit_list.trans_amount =  - to_decimal(billjournal.betrag)
        guest_deposit_list.trans_date = to_string(billjournal.bill_datum) + " " + to_string(billjournal.zeit, "HH:MM:SS")
        guest_deposit_list.trans_remark = entry(1, billjournal.bezeich, "]")
        guest_deposit_list.user_init = billjournal.userinit
        guest_deposit_list.flag = "*"


        deposit_balance =  to_decimal(deposit_balance) + to_decimal(guest_deposit_list.trans_amount)

        artikel = get_cache (Artikel, {"artnr": [(eq, billjournal.artnr)],"departement": [(eq, 0)]})

        if artikel:
            guest_deposit_list.article_desc = artikel.bezeich

        curr_recid = billjournal._recid
        billjournal = db_session.query(Billjournal).filter(
                 (Billjournal.billjou_ref == guest_number) & (Billjournal.artnr != 0) & (Billjournal.artnr != depoart_guest) & (Billjournal.artnr != depoart_rsv) & (Billjournal.artnr != depoart_bqt) & (Billjournal.artnr != depoart_pos) & (num_entries(Billjournal.bezeich, "[") > 1) & (substring(entry(1, Billjournal.bezeich, "[") , 0, 13) == ("Guest Deposit").lower()) & (Billjournal._recid > curr_recid)).first()

    for bill, bill_line in db_session.query(Bill, Bill_line).join(Bill_line,(Bill_line.rechnr == Bill.rechnr) & (Bill_line.artnr == depoart_guest)).filter(
             (Bill.rechnr > 0) & (Bill.gastnr == guest_number)).order_by(Bill._recid).all():
        guest_deposit_list = Guest_deposit_list()
        guest_deposit_list_data.append(guest_deposit_list)

        guest_deposit_list.guest_number = guest_number
        guest_deposit_list.article_number = bill_line.artnr
        guest_deposit_list.article_desc = bill_line.bezeich
        guest_deposit_list.trans_amount =  to_decimal(bill_line.betrag)
        guest_deposit_list.trans_date = to_string(bill_line.bill_datum) + " " + to_string(bill_line.zeit, "HH:MM:SS")
        guest_deposit_list.bill_number = bill.rechnr
        guest_deposit_list.user_init = bill_line.userinit
        guest_deposit_list.flag = "**"
        guest_deposit_list.trans_remark = "BillNumber:" + " " + to_string(bill.rechnr)


        deposit_balance =  to_decimal(deposit_balance) + to_decimal(guest_deposit_list.trans_amount)

        if bill.resnr > 0 and bill.reslinnr > 0:
            guest_deposit_list.bill_type = "GuestBill"
            guest_deposit_list.res_number = to_string(bill.resnr) + "/" + to_string(bill.reslinnr)
            guest_deposit_list.trans_remark = guest_deposit_list.trans_remark + "|" +\
                    "BillType:" + " " + guest_deposit_list.bill_type + "|" +\
                    "ResNumber:" + " " + guest_deposit_list.res_number

        elif bill.resnr > 0 and bill.reslinnr == 0:
            guest_deposit_list.bill_type = "MasterBill"
            guest_deposit_list.trans_remark = guest_deposit_list.trans_remark + "|" +\
                    "BillType:" + " " + guest_deposit_list.bill_type

        elif bill.resnr == 0 and bill.reslinnr > 0:
            guest_deposit_list.bill_type = "NonstayBill"
            guest_deposit_list.trans_remark = guest_deposit_list.trans_remark + "|" +\
                    "BillType:" + " " + guest_deposit_list.bill_type

    return generate_output()