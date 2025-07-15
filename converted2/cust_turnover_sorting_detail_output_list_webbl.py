#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy

b_list_data, B_list = create_model("B_list", {"gastnr":int, "cust_name":string, "gname":string, "gesamtumsatz":Decimal, "logiernachte":Decimal, "argtumsatz":Decimal, "f_b_umsatz":Decimal, "sonst_umsatz":Decimal, "wohnort":string, "plz":string, "land":string, "sales_id":string, "ba_umsatz":Decimal, "ly_rev":Decimal, "region":string, "region1":string, "stayno":int, "resnr":string, "counter":int, "counterall":int, "resno":int, "reslinnr":int, "curr_pos":int, "count_room":string, "rm_sharer":string, "arrival":string, "depart":string})

def cust_turnover_sorting_detail_output_list_webbl(idflag:string, b_list_data:[B_list]):
    doneflag = False
    counter:int = 0
    queasy = None

    b_list = bqueasy = pqueasy = tqueasy = None

    Bqueasy = create_buffer("Bqueasy",Queasy)
    Pqueasy = create_buffer("Pqueasy",Queasy)
    Tqueasy = create_buffer("Tqueasy",Queasy)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal doneflag, counter, queasy
        nonlocal idflag
        nonlocal bqueasy, pqueasy, tqueasy


        nonlocal b_list, bqueasy, pqueasy, tqueasy

        return {"doneflag": doneflag, "b-list": b_list_data}

    for queasy in db_session.query(Queasy).filter(
             (Queasy.key == 280) & (Queasy.char1 == ("Guest Turnover Detail").lower()) & (Queasy.char3 == idflag)).order_by(Queasy.number1).yield_per(100):
        counter = counter + 1

        if counter > 1000:
            break
        b_list = B_list()
        b_list_data.append(b_list)

        b_list.gastnr = to_int(entry(0, queasy.char2, "|"))
        b_list.cust_name = entry(1, queasy.char2, "|")
        b_list.gesamtumsatz =  to_decimal(to_decimal(entry(2 , queasy.char2 , "|")) )
        b_list.logiernachte =  to_decimal(to_decimal(entry(3 , queasy.char2 , "|")) )
        b_list.argtumsatz =  to_decimal(to_decimal(entry(4 , queasy.char2 , "|")) )
        b_list.f_b_umsatz =  to_decimal(to_decimal(entry(5 , queasy.char2 , "|")) )
        b_list.sonst_umsatz =  to_decimal(to_decimal(entry(6 , queasy.char2 , "|")) )
        b_list.wohnort = entry(7, queasy.char2, "|")
        b_list.plz = entry(8, queasy.char2, "|")
        b_list.land = entry(9, queasy.char2, "|")
        b_list.sales_id = entry(10, queasy.char2, "|")
        b_list.ba_umsatz =  to_decimal(to_decimal(entry(11 , queasy.char2 , "|")) )
        b_list.ly_rev =  to_decimal(to_decimal(entry(12 , queasy.char2 , "|")) )
        b_list.region = entry(13, queasy.char2, "|")
        b_list.region1 = entry(14, queasy.char2, "|")
        b_list.stayno = to_int(entry(15, queasy.char2, "|"))
        b_list.resnr = entry(16, queasy.char2, "|")
        b_list.counter = to_int(entry(17, queasy.char2, "|"))
        b_list.counterall = to_int(entry(18, queasy.char2, "|"))
        b_list.resno = to_int(entry(19, queasy.char2, "|"))
        b_list.reslinnr = to_int(entry(20, queasy.char2, "|"))
        b_list.curr_pos = to_int(entry(21, queasy.char2, "|"))
        b_list.count_room = entry(22, queasy.char2, "|")
        b_list.rm_sharer = entry(23, queasy.char2, "|")
        b_list.arrival = entry(24, queasy.char2, "|")
        b_list.depart = entry(25, queasy.char2, "|")

        bqueasy = db_session.query(Bqueasy).filter(
                 (Bqueasy._recid == queasy._recid)).first()
        db_session.delete(bqueasy)
        pass

    pqueasy = db_session.query(Pqueasy).filter(
             (Pqueasy.key == 280) & (Pqueasy.char1 == ("Guest Turnover Detail").lower()) & (Pqueasy.char3 == idflag)).first()

    if pqueasy:
        doneflag = False


    else:

        tqueasy = db_session.query(Tqueasy).filter(
                 (Tqueasy.key == 285) & (Tqueasy.char1 == ("Guest Turnover Detail").lower()) & (Tqueasy.number1 == 1) & (Tqueasy.char2 == idflag)).first()

        if tqueasy:
            doneflag = False


        else:
            doneflag = True

    tqueasy = db_session.query(Tqueasy).filter(
             (Tqueasy.key == 285) & (Tqueasy.char1 == ("Guest Turnover Detail").lower()) & (Tqueasy.number1 == 0) & (Tqueasy.char2 == idflag)).first()

    if tqueasy:
        pass
        db_session.delete(tqueasy)
        pass

    return generate_output()