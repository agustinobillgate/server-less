from functions.additional_functions import *
import decimal
from datetime import date
from models import Nation, Natstat1

def nation_productbl(pvilanguage:int, mm:int, yy:int, sorttype:int):
    room_list_list = []
    datum:date = None
    from_date:date = None
    to_date:date = None
    i:int = 0
    do_it:bool = False
    lfr_date:date = None
    lto_date:date = None
    lvcarea:str = "nation_product"
    nation = natstat1 = None

    room_list = r_list = natbuff = None

    room_list_list, Room_list = create_model("Room_list", {"flag":int, "num":int, "natnr":int, "nr":int, "bezeich":str, "room":[int, 12], "ytd":int, "lytd":int})

    R_list = Room_list
    r_list_list = room_list_list

    Natbuff = Nation

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_list, datum, from_date, to_date, i, do_it, lfr_date, lto_date, lvcarea, nation, natstat1
        nonlocal r_list, natbuff


        nonlocal room_list, r_list, natbuff
        nonlocal room_list_list
        return {"room-list": room_list_list}


    room_list_list.clear()
    from_date = date_mdy(1, 1, yy)
    to_date = (date_mdy(mm , 1, yy) + 32)
    to_date = date_mdy(get_month(to_date) , 1, get_year(to_date)) - 1
    lfr_date = date_mdy(1, 1, yy - 1)
    lto_date = (date_mdy(mm , 1, yy - 1) + 32)
    lto_date = date_mdy(get_month(lto_date) , 1, get_year(lto_date)) - 1

    for natstat1 in db_session.query(Natstat1).filter(
                (Natstat1.datum >= from_date) &  (Natstat1.datum <= to_date)).all():
        i = get_month(natstat.datum)

        nation = db_session.query(Nation).filter(
                    (Nation.natcode == 0) &  (Nationnr == natstat1.nationnr)).first()

        natbuff = db_session.query(Natbuff).filter(
                    (Natbuff.natcode > 0) &  (Natbuff.nationnr == natstat1.nationnr)).first()

        if nation or (not nation and not natbuff):

            room_list = query(room_list_list, filters=(lambda room_list :room_list.natnr == natstat1.nationnr), first=True)

            if not room_list:
                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.natnr = natstat1.nationnr

                if nation:
                    room_list.bezeich = nation.bezeich
                else:
                    room_list.bezeich = "UNKNOWN"

            if sorttype == 0:
                room_list.room[i - 1] = room_list.room[i - 1] + + natstat1.persanz
                room_list.ytd = room_list.ytd + natstat1.persanz


            else:
                room_list.room[i - 1] = room_list.room[i - 1] + + natstat1.zimmeranz
                room_list.ytd = room_list.ytd + natstat1.zimmeranz

    for natstat1 in db_session.query(Natstat1).filter(
                (Natstat1.datum >= lfr_date) &  (Natstat1.datum <= lto_date)).all():
        i = get_month(natstat1.datum)

        nation = db_session.query(Nation).filter(
                    (Nation.natcode == 0) &  (Nationnr == natstat1.nationnr)).first()

        natbuff = db_session.query(Natbuff).filter(
                    (Natbuff.natcode > 0) &  (Natbuff.nationnr == natstat1.nationnr)).first()

        if nation or (not nation and not natbuff):

            room_list = query(room_list_list, filters=(lambda room_list :room_list.natnr == natstat1.nationnr), first=True)

            if not room_list:
                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.natnr = natstat1.nationnr

                nation = db_session.query(Nation).filter(
                            (Nationnr == natstat1.nationnr)).first()

                if nation:
                    room_list.bezeich = nation.bezeich
                else:
                    room_list.bezeich = "UNKNOWN"

            if sorttype == 0:
                room_list.lytd = room_list.lytd + natstat1.persanz


            else:
                room_list.lytd = room_list.lytd + natstat1.zimmeranz


    i = 0

    for room_list in query(room_list_list, filters=(lambda room_list :room_list.ytd != 0 or room_list.lytd != 0)):
        i = i + 1
        room_list.nr = i
        room_list.num = i

    for room_list in query(room_list_list, filters=(lambda room_list :(room_list.nr == 0))):
        room_list_list.remove(room_list)
    room_list = Room_list()
    room_list_list.append(room_list)

    room_list.num = 9999
    room_list.flag = 1
    room_list.bezeich = translateExtended ("TOTAL", lvcarea, "")

    for r_list in query(r_list_list, filters=(lambda r_list :r_list.num < 9999)):
        for i in range(1,12 + 1) :
            room_list.room[i - 1] = room_list.room[i - 1] + r_list.room[i - 1]
        room_list.ytd = room_list.ytd + r_list.ytd
        room_list.lytd = room_list.lytd + r_list.lytd

    return generate_output()