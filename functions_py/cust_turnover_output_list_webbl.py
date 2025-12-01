#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 1/8/2025
# hasil .p dan endpoint tidak sama
# Rd, 28/11/2025, with_for_update added
#----------------------------------------

from functions.additional_functions import *
from sqlalchemy import func
from decimal import Decimal
from models import Queasy
import time

cust_list_data, Cust_list = create_model("Cust_list", {"gastnr":int, "cust_name":string, "gesamtumsatz":Decimal, "logiernachte":int, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":Decimal, "ly_rev":Decimal, "region":string, "region1":string, "stayno":int, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int})

def cust_turnover_output_list_webbl(idflag:string, cust_list_data:[Cust_list]):
    doneflag = False
    counter:int = 0
    queasy = None

    cust_list = bqueasy = pqueasy = tqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session
    iflag = idflag.strip()

    def generate_output():
        nonlocal doneflag, counter, queasy
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal cust_list, bqueasy, pqueasy, tqueasy
        return {"counter": counter,"idFlag": idflag, "doneflag": doneflag, "cust-list": cust_list_data}

    
    # tunggu sampai proses selesai
    count = retry = tmp_count = 0
    while True:
        count = db_session.query(Queasy).filter(
            (Queasy.key == 280) &
            (Queasy.char1 == "Guest Turnover") &
            (Queasy.char3 == idflag)
        ).count()

        if count >= 1000:
            break

        if tmp_count == 0 and retry > 60:
            break

        if tmp_count > 0 and tmp_count == count:
            break

        tmp_count = count
        retry += 1

        time.sleep(0.3)


    for queasy in db_session.query(Queasy).filter(
            (Queasy.key == 280) & (Queasy.char1 == "Guest Turnover") & (Queasy.char3 == idflag)).order_by(Queasy.number1).yield_per(100):

        counter = counter + 1

        if counter > 1000:
            break
        cust_list = Cust_list()
        cust_list_data.append(cust_list)

        cust_list.gastnr = to_int(entry(0, queasy.char2, "|"))
        cust_list.cust_name = entry(1, queasy.char2, "|")
        cust_list.gesamtumsatz =  to_decimal(to_decimal(entry(2 , queasy.char2 , "|")) )
        cust_list.logiernachte = to_decimal(entry(3, queasy.char2, "|"))
        cust_list.argtumsatz =  to_decimal(to_decimal(entry(4 , queasy.char2 , "|")) )
        cust_list.f_b_umsatz =  to_decimal(to_decimal(entry(5 , queasy.char2 , "|")) )
        cust_list.sonst_umsatz =  to_decimal(to_decimal(entry(6 , queasy.char2 , "|")) )
        cust_list.wohnort = entry(7, queasy.char2, "|")
        cust_list.plz = entry(8, queasy.char2, "|")
        cust_list.land = entry(9, queasy.char2, "|")
        cust_list.sales_id = entry(10, queasy.char2, "|")
        cust_list.ba_umsatz =  to_decimal(to_decimal(entry(11 , queasy.char2 , "|")) )
        cust_list.ly_rev =  to_decimal(to_decimal(entry(12 , queasy.char2 , "|")) )
        cust_list.region = entry(13, queasy.char2, "|")
        cust_list.region1 = entry(14, queasy.char2, "|")
        cust_list.stayno = to_int(entry(15, queasy.char2, "|"))
        cust_list.resnr = entry(16, queasy.char2, "|")
        cust_list.counter = to_int(entry(17, queasy.char2, "|"))
        cust_list.counterall = to_int(entry(18, queasy.char2, "|"))
        cust_list.resno = to_int(entry(19, queasy.char2, "|"))
        cust_list.reslinnr = to_int(entry(20, queasy.char2, "|"))
        cust_list.curr_pos = to_int(entry(21, queasy.char2, "|"))

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).with_for_update().first()
        # Rd 14/8/2025
        if bqueasy:
            db_session.delete(bqueasy)
        pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("Guest Turnover")) & (Pqueasy.char3 == idflag)).first()

    if pqueasy:
        doneflag = False
    else:
        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("Guest Turnover")) & (Tqueasy.number1 == 1) & (Tqueasy.char2 == idflag)).first()

        if tqueasy:
            doneflag = False

        else:
            doneflag = True

    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (Tqueasy.char1 == ("Guest Turnover")) & (Tqueasy.number1 == 0) & (Tqueasy.char2 == idflag)).with_for_update().first()

    if tqueasy:
        db_session.delete(tqueasy)
        pass

    return generate_output()