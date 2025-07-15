#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Htparam, Guest, Mc_guest, Bill

def ts_table_check_creditlimitbl(resrecid:int):

    prepare_cache ([Res_line, Htparam, Guest, Mc_guest, Bill])

    klimit = to_decimal("0.0")
    ksaldo = to_decimal("0.0")
    remark = ""
    i:int = 0
    str:string = ""
    child_age:string = ""
    res_line = htparam = guest = mc_guest = bill = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal klimit, ksaldo, remark, i, str, child_age, res_line, htparam, guest, mc_guest, bill
        nonlocal resrecid

        return {"klimit": klimit, "ksaldo": ksaldo, "remark": remark}

    def check_creditlimit():

        nonlocal klimit, ksaldo, remark, i, str, child_age, res_line, htparam, guest, mc_guest, bill
        nonlocal resrecid

        answer:bool = True

        htparam = get_cache (Htparam, {"paramnr": [(eq, 68)]})

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, guest.gastnr)],"activeflag": [(eq, True)]})

        if mc_guest:
            remark = "Membership No: "+ mc_guest.cardnum + chr_unicode(10)

        if guest.kreditlimit != 0:
            klimit =  to_decimal(guest.kreditlimit)
        else:

            if htparam.fdecimal != 0:
                klimit =  to_decimal(htparam.fdecimal)
            else:
                klimit =  to_decimal(htparam.finteger)
        ksaldo =  to_decimal("0")

        bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"flag": [(eq, 0)],"zinr": [(eq, res_line.zinr)]})

        if bill:
            ksaldo =  to_decimal(bill.saldo)
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 5) == ("ChAge").lower() :
                child_age = substring(str, 5)

        if child_age != "":
            remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr_unicode(10) + "A:" + to_string(res_line.erwachs + res_line.gratis) + " Ch:" + to_string(res_line.kind1) + " " + "(" + child_age + ")" + " - " + res_line.arrangement + chr_unicode(10) + res_line.bemerk
        else:
            remark = remark + to_string(res_line.ankunft) + " - " + to_string(res_line.abreise) + chr_unicode(10) + "A:" + to_string(res_line.erwachs + res_line.gratis) + " Ch:" + to_string(res_line.kind1) + " - " + res_line.arrangement + chr_unicode(10) + res_line.bemerk

    res_line = get_cache (Res_line, {"_recid": [(eq, resrecid)]})
    check_creditlimit()

    return generate_output()