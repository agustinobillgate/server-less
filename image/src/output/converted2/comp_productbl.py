#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guestat1, Guest

def comp_productbl(pvilanguage:int, curr_date:string):

    prepare_cache ([Guestat1, Guest])

    compproduct_list_list = []
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
    guestat1 = guest = None

    compproduct_list = c_list = r_list = gstat = None

    compproduct_list_list, Compproduct_list = create_model("Compproduct_list", {"num":int, "nr":int, "bezeich":string, "room":[int,12], "ytd":int, "lytd":int})
    c_list_list, C_list = create_model("C_list", {"num":int, "nr":int, "bezeich":string, "room":[int,12], "ytd":int, "lytd":int, "gastnr":int})

    R_list = Compproduct_list
    r_list_list = compproduct_list_list

    Gstat = create_buffer("Gstat",Guestat1)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal compproduct_list_list, mm, yy, i, from_date, to_date, datum, jml, lvcarea, curr_guest, curr_name, do_it, created, counter, troom, tytd, tlytd, lfdate, ltdate, guestat1, guest
        nonlocal pvilanguage, curr_date
        nonlocal r_list, gstat


        nonlocal compproduct_list, c_list, r_list, gstat
        nonlocal compproduct_list_list, c_list_list

        return {"compproduct-list": compproduct_list_list}

    mm = to_int(substring(curr_date, 0, 2))
    yy = to_int(substring(curr_date, 2, 4))
    jml = yy - 1
    r_list_list.clear()
    from_date = date_mdy(1, 1, yy)

    if mm == 12:
        to_date = date_mdy(1, 1, yy + timedelta(days=1)) - timedelta(days=1)
    else:
        to_date = date_mdy(mm + 1, 1, yy) - timedelta(days=1)
    lfdate = date_mdy(1, 1, jml)

    if mm == 12:
        ltdate = date_mdy(1, 1, jml + timedelta(days=1)) - timedelta(days=1)
    else:
        ltdate = date_mdy(mm + 1, 1, jml) - timedelta(days=1)

    for guestat1 in db_session.query(Guestat1).filter(
             (Guestat1.datum >= from_date) & (Guestat1.datum <= to_date)).order_by(Guestat1.gastnr, Guestat1.datum).all():
        i = get_month(guestat1.datum)

        if curr_guest == 0 or curr_guest != guestat1.gastnr:

            guest = get_cache (Guest, {"karteityp": [(eq, 1)],"gastnr": [(eq, guestat1.gastnr)]})

            if guest:
                c_list = C_list()
                c_list_list.append(c_list)

                c_list.gastnr = guest.gastnr
                c_list.bezeich = guest.name
                c_list.room[i - 1] = guestat1.zimmeranz


                c_list.ytd = c_list.ytd + guestat1.zimmeranz
        else:

            c_list = query(c_list_list, filters=(lambda c_list: c_list.gastnr == guestat1.gastnr), first=True)

            if c_list:
                c_list.room[i - 1] = c_list.room[i - 1] + guestat1.zimmeranz
                c_list.ytd = c_list.ytd + guestat1.zimmeranz


        curr_guest = guestat1.gastnr
    curr_guest = 0

    for guestat1 in db_session.query(Guestat1).filter(
             (Guestat1.datum >= lfdate) & (Guestat1.datum <= ltdate)).order_by(Guestat1.gastnr).all():

        if curr_guest == 0 or curr_guest != guestat1.gastnr:

            guest = get_cache (Guest, {"karteityp": [(eq, 1)],"gastnr": [(eq, guestat1.gastnr)]})

            if guest:

                c_list = query(c_list_list, filters=(lambda c_list: c_list.gastnr == guest.gastnr), first=True)

                if not c_list:
                    c_list = C_list()
                    c_list_list.append(c_list)

                    c_list.gastnr = guest.gastnr
                    c_list.bezeich = guest.name
                    c_list.lytd = c_list.lytd + guestat1.zimmeranz


                else:
                    c_list.lytd = c_list.lytd + guestat1.zimmeranz
        else:

            c_list = query(c_list_list, filters=(lambda c_list: c_list.gastnr == guestat1.gastnr), first=True)

            if c_list:
                c_list.lytd = c_list.lytd + guestat1.zimmeranz
    counter = 0

    for c_list in query(c_list_list, sort_by=[("ytd",True),("bezeich",False)]):
        counter = counter + 1
        compproduct_list = Compproduct_list()
        compproduct_list_list.append(compproduct_list)

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
    compproduct_list_list.append(compproduct_list)

    compproduct_list.num = 9999
    compproduct_list.bezeich = translateExtended ("T O T A L", lvcarea, "")
    compproduct_list.ytd = tytd
    compproduct_list.lytd = tlytd


    for i in range(1,12 + 1) :
        compproduct_list.room[i - 1] = troom[i - 1]

    return generate_output()