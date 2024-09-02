from functions.additional_functions import *
import decimal
from models import Eg_location, Zimmer

def prepare_sel_copypropbl():
    location_list = []
    room_list = []
    eg_location = zimmer = None

    location = room = qbuff = None

    location_list, Location = create_model("Location", {"loc_nr":int, "loc_nm":str, "loc_selected":bool})
    room_list, Room = create_model("Room", {"room_nm":str, "room_selected":bool})

    Qbuff = Zimmer

    db_session = local_storage.db_session

    def generate_output():
        nonlocal location_list, room_list, eg_location, zimmer
        nonlocal qbuff


        nonlocal location, room, qbuff
        nonlocal location_list, room_list
        return {"location": location_list, "room": room_list}

    def loc():

        nonlocal location_list, room_list, eg_location, zimmer
        nonlocal qbuff


        nonlocal location, room, qbuff
        nonlocal location_list, room_list

        i:int = 0
        Qbuff = Eg_location
        location_list.clear()

        for eg_location in db_session.query(Eg_location).filter(
                (Eg_location.guestflag == False)).all():
            location = Location()
            location_list.append(location)

            location.loc_nr = eg_location.nr
            location.loc_nm = eg_location.bezeich
            location.loc_SELECTED = False

    def room():

        nonlocal location_list, room_list, eg_location, zimmer
        nonlocal qbuff


        nonlocal location, room, qbuff
        nonlocal location_list, room_list

        i:int = 0
        Qbuff = Zimmer
        room_list.clear()

        for zimmer in db_session.query(Zimmer).all():
            room = Room()
            room_list.append(room)

            room.room_nm = zimmer.zinr
            room.room_SELECTED = False

    loc()
    oom()

    return generate_output()