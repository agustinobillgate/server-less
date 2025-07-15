#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_location, Zimmer

def prepare_sel_copypropbl():

    prepare_cache ([Eg_location, Zimmer])

    location_data = []
    room_data = []
    eg_location = zimmer = None

    location = room = None

    location_data, Location = create_model("Location", {"loc_nr":int, "loc_nm":string, "loc_selected":bool})
    room_data, Room = create_model("Room", {"room_nm":string, "room_selected":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal location_data, room_data, eg_location, zimmer


        nonlocal location, room
        nonlocal location_data, room_data

        return {"location": location_data, "room": room_data}

    def loc():

        nonlocal location_data, room_data, eg_location, zimmer


        nonlocal location, room
        nonlocal location_data, room_data

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Eg_location)
        location_data.clear()

        for eg_location in db_session.query(Eg_location).filter(
                 (Eg_location.guestflag == False)).order_by(Eg_location._recid).all():
            location = Location()
            location_data.append(location)

            location.loc_nr = eg_location.nr
            location.loc_nm = eg_location.bezeich
            location.loc_selected = False


    def room():

        nonlocal location_data, room_data, eg_location, zimmer


        nonlocal location, room
        nonlocal location_data, room_data

        i:int = 0
        qbuff = None
        Qbuff =  create_buffer("Qbuff",Zimmer)
        room_data.clear()

        for zimmer in db_session.query(Zimmer).order_by(Zimmer.zinr).all():
            room = Room()
            room_data.append(room)

            room.room_nm = zimmer.zinr
            room.room_selected = False


    loc()
    room()

    return generate_output()