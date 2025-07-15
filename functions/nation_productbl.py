#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Nation, Natstat1

def nation_productbl(pvilanguage:int, mm:int, yy:int, sorttype:int):

    prepare_cache ([Natstat1])

    room_list_data = []
    datum:date = None
    from_date:date = None
    to_date:date = None
    i:int = 0
    do_it:bool = False
    lfr_date:date = None
    lto_date:date = None
    lvcarea:string = "nation-product"
    nation = natstat1 = None

    room_list = tt_nation = tt_natbuff = r_list = natbuff = None

    room_list_data, Room_list = create_model("Room_list", {"flag":int, "num":int, "natnr":int, "nr":int, "bezeich":string, "room":[int,12], "ytd":int, "lytd":int})
    tt_nation_data, Tt_nation = create_model_like(Nation)
    tt_natbuff_data, Tt_natbuff = create_model_like(Nation)

    R_list = Room_list
    r_list_data = room_list_data

    Natbuff = create_buffer("Natbuff",Nation)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_data, datum, from_date, to_date, i, do_it, lfr_date, lto_date, lvcarea, nation, natstat1
        nonlocal pvilanguage, mm, yy, sorttype
        nonlocal r_list, natbuff


        nonlocal room_list, tt_nation, tt_natbuff, r_list, natbuff
        nonlocal room_list_data, tt_nation_data, tt_natbuff_data

        return {"room-list": room_list_data}


    room_list_data.clear()
    from_date = date_mdy(1, 1, yy)
    to_date = (date_mdy(mm , 1, yy) + timedelta(days=32))
    to_date = date_mdy(get_month(to_date) , 1, get_year(to_date)) - timedelta(days=1)
    lfr_date = date_mdy(1, 1, yy - 1)
    lto_date = (date_mdy(mm , 1, yy - 1) + timedelta(days=32))
    lto_date = date_mdy(get_month(lto_date) , 1, get_year(lto_date)) - timedelta(days=1)

    for nation in db_session.query(Nation).filter(
             (Nation.natcode == 0)).order_by(Nation._recid).all():
        tt_nation = Tt_nation()
        tt_nation_data.append(tt_nation)

        buffer_copy(nation, tt_nation)

    for natbuff in db_session.query(Natbuff).filter(
             (Natbuff.natcode > 0)).order_by(Natbuff._recid).all():
        tt_natbuff = Tt_natbuff()
        tt_natbuff_data.append(tt_natbuff)

        buffer_copy(nation, tt_natbuff)

    for natstat1 in db_session.query(Natstat1).filter(
                 (Natstat1.datum >= from_date) & (Natstat1.datum <= to_date)).order_by(Natstat1.nationnr, Natstat1.datum).all():
        i = get_month(natstat1.datum)

        tt_nation = query(tt_nation_data, filters=(lambda tt_nation: tt_nation.nationnr == natstat1.nationnr), first=True)

        tt_natbuff = query(tt_natbuff_data, filters=(lambda tt_natbuff: tt_natbuff.nationnr > natstat1.nationnr), first=True)

        if tt_nation or (not tt_nation and not tt_natbuff):

            room_list = query(room_list_data, filters=(lambda room_list: room_list.natnr == natstat1.nationnr), first=True)

            if not room_list:
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.natnr = natstat1.nationnr

                if tt_nation:
                    room_list.bezeich = tt_nation.bezeich
                else:
                    room_list.bezeich = "UNKNOWN"

            if sorttype == 0:
                room_list.room[i - 1] = room_list.room[i - 1] + + natstat1.persanz
                room_list.ytd = room_list.ytd + natstat1.persanz


            else:
                room_list.room[i - 1] = room_list.room[i - 1] + + natstat1.zimmeranz
                room_list.ytd = room_list.ytd + natstat1.zimmeranz

    for natstat1 in db_session.query(Natstat1).filter(
                 (Natstat1.datum >= lfr_date) & (Natstat1.datum <= lto_date)).order_by(Natstat1.nationnr, Natstat1.datum).all():
        i = get_month(natstat1.datum)

        tt_nation = query(tt_nation_data, filters=(lambda tt_nation: tt_nation.nationnr == natstat1.nationnr), first=True)

        tt_natbuff = query(tt_natbuff_data, filters=(lambda tt_natbuff: tt_natbuff.nationnr > natstat1.nationnr), first=True)

        if tt_nation or (not tt_nation and not tt_natbuff):

            room_list = query(room_list_data, filters=(lambda room_list: room_list.natnr == natstat1.nationnr), first=True)

            if not room_list:
                room_list = Room_list()
                room_list_data.append(room_list)

                room_list.natnr = natstat1.nationnr

                if tt_nation:
                    room_list.bezeich = tt_nation.bezeich
                else:
                    room_list.bezeich = "UNKNOWN"

            if sorttype == 0:
                room_list.lytd = room_list.lytd + natstat1.persanz


            else:
                room_list.lytd = room_list.lytd + natstat1.zimmeranz


    i = 0

    for room_list in query(room_list_data, filters=(lambda room_list: room_list.ytd != 0 or room_list.lytd != 0), sort_by=[("ytd",True),("bezeich",False)]):
        i = i + 1
        room_list.nr = i
        room_list.num = i

    for room_list in query(room_list_data, filters=(lambda room_list:(room_list.nr == 0))):
        room_list_data.remove(room_list)
    room_list = Room_list()
    room_list_data.append(room_list)

    room_list.num = 9999
    room_list.flag = 1
    room_list.bezeich = translateExtended ("TOTAL", lvcarea, "")

    for r_list in query(r_list_data, filters=(lambda r_list: r_list.num < 9999)):
        for i in range(1,12 + 1) :
            room_list.room[i - 1] = room_list.room[i - 1] + r_list.room[i - 1]
        room_list.ytd = room_list.ytd + r_list.ytd
        room_list.lytd = room_list.lytd + r_list.lytd

    return generate_output()