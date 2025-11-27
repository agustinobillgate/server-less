#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Artikel, Bill_line, Bill, Billjournal, Debitor

def fo_inv_update_voucher_webbl(new_voucher:string, bline_recid:int, bline_desc:string, art_num:int, dept_num:int, bill_num:int, bill_date:date):

    prepare_cache ([Artikel, Bill_line, Bill, Billjournal, Debitor])

    error_msg = ""
    curr_voucher:string = ""
    desc_str:string = ""
    room_num:string = ""
    art_type:int = 0
    found_it:bool = False
    resno:int = 0
    reslinno:int = 0
    i:int = 0
    str:string = ""
    artikel = bill_line = bill = billjournal = debitor = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal error_msg, curr_voucher, desc_str, room_num, art_type, found_it, resno, reslinno, i, str, artikel, bill_line, bill, billjournal, debitor
        nonlocal new_voucher, bline_recid, bline_desc, art_num, dept_num, bill_num, bill_date

        return {"error_msg": error_msg}


    artikel = get_cache (Artikel, {"artnr": [(eq, art_num)],"departement": [(eq, dept_num)]})

    if artikel:
        art_type = artikel.artart

    if art_type == 5 or art_type == 8 or art_type == 9:
        error_msg = "Article Type is not support."
        
        return generate_output()

    bill_line = db_session.query(Bill_line).filter(Bill_line._recid == bline_recid).first()

    if not bill_line:
        error_msg = "Selected bill not found."

        return generate_output()

    if num_entries(bline_desc, "/") > 1:
        desc_str = entry(0, bline_desc, "/")
        curr_voucher = trim(entry(1, bline_desc, "/"))

    bill = get_cache (Bill, {"rechnr": [(eq, bill_num)]})

    if bill:
        resno = bill.resnr
        reslinno = bill.reslinnr

    db_session.refresh(bill_line, with_for_update=True)

    if num_entries(bill_line.bezeich, "/") > 1:
        bill_line.bezeich = entry(1, bill_line.bezeich, "/", new_voucher)
    
    room_num = bill_line.zinr
    
    for billjournal in db_session.query(Billjournal).filter(
        (Billjournal.rechnr == bill_num) & (Billjournal.artnr == art_num) & (Billjournal.departement == dept_num) & (Billjournal.bill_datum == bill_date) & (Billjournal.zinr == (room_num).lower())).with_for_update().order_by(Billjournal._recid).yield_per(100):
        
        if num_entries(billjournal.bezeich, "/") > 1:
            if entry(1, billjournal.bezeich, "/") == (curr_voucher).lower() :
                billjournal.bezeich = entry(1, billjournal.bezeich, "/", new_voucher)
                found_it = True

        if found_it:
            found_it = False
            break

    if art_type == 2 or art_type == 7:
        for debitor in db_session.query(Debitor).filter(
            (Debitor.rechnr == bill_num) & (Debitor.rgdatum == bill_date) & (Debitor.artnr == art_num) & (Debitor.zinr == (room_num).lower())).with_for_update().order_by(Debitor._recid).yield_per(100):
            
            if resno != 0 and reslinno != 0:
                if num_entries(debitor.vesrcod, ";") > 1:
                    if entry(1, debitor.vesrcod, ";") == (curr_voucher).lower() :
                        debitor.vesrcod = entry(1, debitor.vesrcod, ";", new_voucher)
                        found_it = True
            else:
                if num_entries(debitor.vesrcod, ";") > 1:
                    for i in range(1,num_entries(debitor.vesrcod, ";")  + 1) :
                        str = entry(i - 1, debitor.vesrcod, ";")

                        if str.lower()  == (curr_voucher).lower() :
                            debitor.vesrcod = entry(i - 1, debitor.vesrcod, ";", new_voucher)
                            found_it = True
                            break
                else:
                    debitor.vesrcod = new_voucher
                    found_it = True

            if found_it:
                found_it = False
                break

    return generate_output()