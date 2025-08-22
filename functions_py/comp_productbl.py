#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 19/8/2025
# date, timedelta
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guestat1, Guest

def comp_productbl(pvilanguage:int, curr_date:string):

    prepare_cache ([Guestat1, Guest])

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
    guestat1 = guest = None

    compproduct_list = c_list = r_list = None

    compproduct_list_data, Compproduct_list = create_model("Compproduct_list", {"num":int, "nr":int, "bezeich":string, "room":[int,12], "ytd":int, "lytd":int})
    c_list_data, C_list = create_model_like(Compproduct_list, {"gastnr":int})

    R_list = Compproduct_list
    r_list_data = compproduct_list_data

    db_session = local_storage.db_session

    def generate_output():
        nonlocal compproduct_list_data, mm, yy, i, from_date, to_date, datum, jml, lvcarea, curr_guest, curr_name, do_it, created, counter, troom, tytd, tlytd, guestat1, guest
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
        # Rd 19/8/2025
        # to_date = date_mdy(1, 1, yy + timedelta(days=1)) - timedelta(days=1)
        to_date = date_mdy(1, 1, yy + 1) - timedelta(days=1)
    else:
        to_date = date_mdy(mm + 1, 1, yy) - timedelta(days=1)

    for guestat1 in db_session.query(Guestat1).filter(
             (Guestat1.datum >= from_date) & (Guestat1.datum <= to_date)).order_by(Guestat1.gastnr).all():
        do_it = False

        if curr_guest != guestat1.gastnr:

            guest = get_cache (Guest, {"karteityp": [(eq, 1)],"gastnr": [(eq, guestat1.gastnr)]})

            if guest:
                curr_guest = guest.gastnr
                curr_name = guest.name


            else:
                curr_guest = 0

        if curr_guest != 0:
            do_it = True

        if do_it:

            c_list = query(c_list_data, filters=(lambda c_list: c_list.gastnr == curr_guest), first=True)

            if not c_list:
                c_list = C_list()
                c_list_data.append(c_list)

                c_list.gastnr = curr_guest
                c_list.bezeich = curr_name


            i = get_month(guestat1.datum)
            c_list.room[i - 1] = c_list.room[i - 1] + guestat1.zimmeranz
            c_list.ytd = c_list.ytd + guestat1.zimmeranz
    from_date = date_mdy(1, 1, jml)

    if mm == 12:
        # Rd 19/8/2025
        # to_date = date_mdy(1, 1, jml + timedelta(days=1)) - timedelta(days=1)
        to_date = date_mdy(1, 1, jml + 1) - timedelta(days=1)
    else:
        to_date = date_mdy(mm + 1, 1, jml) - timedelta(days=1)
    curr_guest = 0
    curr_name = ""

    for guestat1 in db_session.query(Guestat1).filter(
             (Guestat1.datum >= from_date) & (Guestat1.datum <= to_date)).order_by(Guestat1.gastnr).all():
        created = True

        c_list = query(c_list_data, filters=(lambda c_list: c_list.gastnr == guestat1.gastnr), first=True)

        if not c_list:

            guest = get_cache (Guest, {"karteityp": [(eq, 1)],"gastnr": [(eq, guestat1.gastnr)]})

            if guest:
                c_list = C_list()
                c_list_data.append(c_list)

                c_list.gastnr = guest.gastnr
                c_list.bezeich = guest.name


            else:
                created = False

        if created:

            c_list = query(c_list_data, filters=(lambda c_list: c_list.gastnr == curr_guest), first=True)

            if c_list:
                c_list.lytd = c_list.lytd + guestat1.zimmeranz
    counter = 0

    for c_list in query(c_list_data, sort_by=[("ytd",True),("bezeich",False)]):

        if c_list.ytd == 0 and c_list.lytd == 0:
            c_list_data.remove(c_list)
        else:
            counter = counter + 1
            compproduct_list = Compproduct_list()
            compproduct_list_data.append(compproduct_list)

            compproduct_list.nr = counter
            compproduct_list.num = counter
            compproduct_list.bezeich = c_list.bezeich
            compproduct_list.ytd = c_list.ytd
            compproduct_list.lytd = c_list.lytd
            tytd = tytd + c_list.ytd
            tlytd = tlytd + c_list.lytd


            for i in range(1,12 + 1) :
                compproduct_list.room[i - 1] = c_list.room[i - 1]
                troom[i - 1] = troom[i - 1] + c_list.room[i - 1]


    compproduct_list = Compproduct_list()
    compproduct_list_data.append(compproduct_list)

    compproduct_list.num = 9999
    compproduct_list.bezeich = translateExtended ("T O T A L", lvcarea, "")
    compproduct_list.ytd = tytd
    compproduct_list.ytd = tlytd


    for i in range(1,12 + 1) :
        compproduct_list.room[i - 1] = troom[i - 1]

    return generate_output()