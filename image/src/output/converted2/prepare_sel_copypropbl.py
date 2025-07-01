#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_location, Zimmer

def prepare_sel_copypropbl():

    prepare_cache ([Eg_location, Zimmer])

    location_list = []
    room_list = []
    eg_location = zimmer = None

    location = room = None

    location_list, Location = create_model("Location", {"loc_nr":int, "loc_nm":string, "loc_selected":bool})
    room_list, Room = create_model("Room", {"room_nm":string, "room_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal location_list, room_list, eg_location, zimmer


        nonlocal location, room
        nonlocal location_list, room_list

        return {"location": location_list, "room": room_list}

    def loc():

        nonlocal location_list, room_list, eg_location, zimmer


        nonlocal location, room
        nonlocal location_list, room_list

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_location)
        location_list.clear()

        for eg_location in db_session.query(Eg_location).filter(
                 (Eg_location.guestflag == False)).order_by(Eg_location._recid).all():
            location = Location()
            location_list.append(location)

            location.loc_nr = eg_location.nr
            location.loc_nm = eg_location.bezeich
            location.loc_selected = False


    def room():

        nonlocal location_list, room_list, eg_location, zimmer


        nonlocal location, room
        nonlocal location_list, room_list

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Zimmer)
        room_list.clear()

        for zimmer in db_session.query(Zimmer).order_by(Zimmer.zinr).all():
            room = Room()
            room_list.append(room)

            room.room_nm = zimmer.zinr
            room.room_selected = False


    loc()
    room()

    return generate_output()