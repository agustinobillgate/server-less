#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Zimmer, Zimkateg, Zinrstat

def day_ruse_create_browsebl(from_room:string, curr_date:date):

    prepare_cache ([Zimmer, Zimkateg, Zinrstat])

    room_list_list = []
    zimmer = zimkateg = zinrstat = None

    room_list = None

    room_list_list, Room_list = create_model("Room_list", {"recid1":[int,18], "etage":int, "zinr":string, "c_char":string, "i_char":string, "zikatnr":int, "rmcat":string, "gstatus":[int,18], "room":[string,18]})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_list, zimmer, zimkateg, zinrstat
        nonlocal from_room, curr_date


        nonlocal room_list
        nonlocal room_list_list

        return {"curr_date": curr_date, "room-list": room_list_list}

    def create_browse():

        nonlocal room_list_list, zimmer, zimkateg, zinrstat
        nonlocal from_room, curr_date


        nonlocal room_list
        nonlocal room_list_list

        datum1:date = None
        datum2:date = None
        to_date:date = None
        i:int = 0
        j:int = 0
        counter_date:int = 0

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.zinr >= (from_room).lower())).order_by(Zimmer._recid).all():

            zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
            room_list = Room_list()
            room_list_list.append(room_list)

            room_list.etage = zimmer.etage
            room_list.zinr = zimmer.zinr
            room_list.c_char = " " + zimmer.zikennz + " "
            room_list.rmcat = zimkateg.kurzbez

            if not zimmer.sleeping:
                room_list.i_char = " i "
        to_date = curr_date + timedelta(days=17)

        for zinrstat in db_session.query(Zinrstat).filter(
                 ((Zinrstat.datum >= curr_date) & (Zinrstat.datum <= to_date)) & (Zinrstat.zinr >= (from_room).lower()) & (Zinrstat.zimmeranz > 0)).order_by(Zinrstat._recid).all():

            room_list = query(room_list_list, filters=(lambda room_list: room_list.zinr == zinrstat.zinr), first=True)

            if room_list:
                datum1 = curr_date
                datum2 = to_date

                if get_month(zinrstat.datum) == get_month(datum1):
                    j = get_day(zinrstat.datum) - get_day(datum1)
                    counter_date = j
                else:
                    j = counter_date + get_day(zinrstat.datum) - get_day(datum1)
                i = j + 1
                room_list.room[i - 1] = to_string(zinrstat.zimmeranz, ">9") + "/" + to_string(zinrstat.personen, "99")
                room_list.gstatus[i - 1] = 9


    if curr_date == None:
        curr_date = get_output(htpdate(87))
    create_browse()

    return generate_output()