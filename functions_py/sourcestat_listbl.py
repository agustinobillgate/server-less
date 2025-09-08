#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 8/9/2025
# jml data tidak sama
# from functions import log_program_rd

#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Sourccod, Sources

def sourcestat_listbl(from_month:string, ci_date:date, sorttype:int, hide_zero:bool):

    prepare_cache ([Sourccod, Sources])

    room_list_data = []
    mm:int = 0
    yy:int = 0
    datum:date = None
    i:int = 0
    j:int = 0
    from_date:date = None
    to_date:date = None
    sourccod = sources = None

    room_list = None

    room_list_data, Room_list = create_model("Room_list", {"flag":int, "bezeich":string, "summe":int, "room":[int,31]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_data, mm, yy, datum, i, j, from_date, to_date, sourccod, sources
        nonlocal from_month, ci_date, sorttype, hide_zero


        nonlocal room_list
        nonlocal room_list_data

        return {"room-list": room_list_data}


    room_list_data.clear()
    mm = to_int(substring(from_month, 0, 2))
    yy = to_int(substring(from_month, 2, 4))

    if mm != 12:
        from_date = date_mdy(mm, 1, yy)
        mm = mm + 1
        to_date = date_mdy(mm, 1, yy) - timedelta(days=1)


    else:
        from_date = date_mdy(mm, 1, yy)

        # Rd, 19/8/2025
        # to_date = date_mdy(1, 1, yy + timedelta(days=1)) - timedelta(days=1)
        to_date = date_mdy(1, 1, yy + 1) - timedelta(days=1)

    if to_date > ci_date:
        to_date = ci_date

    for sourccod in db_session.query(Sourccod).order_by(Sourccod.bezeich).all():
        room_list = Room_list()
        room_list_data.append(room_list)

        room_list.bezeich = sourccod.bezeich
        for datum in date_range(from_date,to_date) :
            i = get_day(datum)

            for sources in db_session.query(Sources).filter(
                     (Sources.source_code == sourccod.source_code) & (Sources.datum == datum)).order_by(Sources._recid).all():

                if sorttype == 1:
                    room_list.room[i - 1] = sources.zimmeranz
                    room_list.summe = room_list.summe + sources.zimmeranz
                else:
                    room_list.room[i - 1] = sources.persanz
                    room_list.summe = room_list.summe + sources.persanz

    if hide_zero :

        for room_list in query(room_list_data, filters=(lambda room_list: room_list.summe == 0)):
            room_list_data.remove(room_list)

    return generate_output()