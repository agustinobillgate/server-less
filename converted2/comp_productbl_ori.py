#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Guestat1

def comp_productbl_ori(pvilanguage:int, curr_date:string):

    prepare_cache ([Guest, Guestat1])

    compproduct_list_data = []
    mm:int = 0
    yy:int = 0
    i:int = 0
    from_date:date = None
    to_date:date = None
    datum:date = None
    jml:int = 0
    lvcarea:string = "comp-product"
    curr_guest:int = 0
    curr_name:string = ""
    do_it:bool = False
    created:bool = False
    counter:int = 0
    troom:List[int] = create_empty_list(12,0)
    tytd:int = 0
    tlytd:int = 0
    lfdate:date = None
    ltdate:date = None
    guest = guestat1 = None

    compproduct_list = c_list = r_list = None

    compproduct_list_data, Compproduct_list = create_model("Compproduct_list", {"num":int, "nr":int, "bezeich":string, "room":[int,12], "ytd":int, "lytd":int})
    c_list_data, C_list = create_model_like(Compproduct_list, {"gastnr":int})

    R_list = Compproduct_list
    r_list_data = compproduct_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal compproduct_list_data, mm, yy, i, from_date, to_date, datum, jml, lvcarea, curr_guest, curr_name, do_it, created, counter, troom, tytd, tlytd, lfdate, ltdate, guest, guestat1
        nonlocal pvilanguage, curr_date
        nonlocal r_list


        nonlocal compproduct_list, c_list, r_list
        nonlocal compproduct_list_data, c_list_data

        return {"compproduct-list": compproduct_list_data}

    mm = to_int(substring(curr_date, 0, 2))
    yy = to_int(substring(curr_date, 2, 4))
    jml = yy - 1
    r_list_data.clear()
    from_date = date_mdy(1, 1, yy)

    if mm == 12:
        # Rd, 19/8/2025
        # to_date = date_mdy(1, 1, yy + timedelta(days=1)) - timedelta(days=1)
        to_date = date_mdy(1, 1, yy + 1) - timedelta(days=1)
    else:
        to_date = date_mdy(mm + 1, 1, yy) - timedelta(days=1)
    lfdate = date_mdy(1, 1, jml)

    if mm == 12:
        ltdate = date_mdy(1, 1, yy) - timedelta(days=1)
    else:
        ltdate = date_mdy(mm + 1, 1, jml) - timedelta(days=1)

    for guest in db_session.query(Guest).filter(
             (Guest.karteityp == 1)).order_by(Guest._recid).all():
        compproduct_list = Compproduct_list()
        compproduct_list_data.append(compproduct_list)

        compproduct_list.bezeich = guest.name
        for i in range(1,mm + 1) :
            from_date = date_mdy(i, 1, yy)

            if i == 12:
                to_date = date_mdy(1, 1, yy + timedelta(days=1)) - timedelta(days=1)
            else:
                to_date = date_mdy(i + 1, 1, yy) - timedelta(days=1)

            for guestat1 in db_session.query(Guestat1).filter(
                     (Guestat1.gastnr == guest.gastnr) & (Guestat1.datum >= from_date) & (Guestat1.datum <= to_date)).order_by(Guestat1._recid).all():
                compproduct_list.room[i - 1] = compproduct_list.room[i - 1] + guestat1.zimmeranz
                compproduct_list.ytd = compproduct_list.ytd + guestat1.zimmeranz
        for i in range(1,mm + 1) :
            from_date = date_mdy(i, 1, jml)

            if i == 12:
                to_date = date_mdy(1, 1, jml + timedelta(days=1)) - timedelta(days=1)
            else:
                to_date = date_mdy(i + 1, 1, jml) - timedelta(days=1)

            for guestat1 in db_session.query(Guestat1).filter(
                     (Guestat1.gastnr == guest.gastnr) & (Guestat1.datum >= from_date) & (Guestat1.datum <= to_date)).order_by(Guestat1._recid).all():
                compproduct_list.lytd = compproduct_list.lytd + guestat1.zimmeranz
    i = 0

    for compproduct_list in query(compproduct_list_data, filters=(lambda compproduct_list: compproduct_list.ytd != 0 or compproduct_list.lytd != 0), sort_by=[("ytd",True),("bezeich",False)]):
        i = i + 1
        compproduct_list.nr = i
        compproduct_list.num = i

    for compproduct_list in query(compproduct_list_data, filters=(lambda compproduct_list:(compproduct_list.nr == 0))):
        compproduct_list_data.remove(compproduct_list)

    for r_list in query(r_list_data, filters=(lambda r_list: r_list.num < 9999)):
        for i in range(1,12 + 1) :
            compproduct_list.room[i - 1] = compproduct_list.room[i - 1] + r_list.room[i - 1]
        compproduct_list.ytd = compproduct_list.ytd + r_list.ytd
        compproduct_list.lytd = compproduct_list.lytd + r_list.lytd

    return generate_output()