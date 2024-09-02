from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_moveproperty, Eg_location

def eg_rephistorymove_create_browsebl(pvilanguage:int, prop_nr:int, fdate:date, tdate:date):
    smove_list = []
    lvcarea:str = "eg_RepHistoryMove"
    eg_moveproperty = eg_location = None

    smove = movement = location = None

    smove_list, Smove = create_model("Smove", {"datum":date, "flocation_str":str, "froom":str, "tlocation_str":str, "troom":str})

    Movement = Eg_moveproperty
    Location = Eg_location

    db_session = local_storage.db_session

    def generate_output():
        nonlocal smove_list, lvcarea, eg_moveproperty, eg_location
        nonlocal movement, location


        nonlocal smove, movement, location
        nonlocal smove_list
        return {"sMove": smove_list}

    def create_browse():

        nonlocal smove_list, lvcarea, eg_moveproperty, eg_location
        nonlocal movement, location


        nonlocal smove, movement, location
        nonlocal smove_list


        sMove_list.clear()

        for movement in db_session.query(Movement).filter(
                (Movement.property_nr == prop_nr) &  (Movement.datum >= fdate) &  (Movement.datum <= tdate)).all():
            add_line()

    def add_line():

        nonlocal smove_list, lvcarea, eg_moveproperty, eg_location
        nonlocal movement, location


        nonlocal smove, movement, location
        nonlocal smove_list

        unknown:str = ""
        unknown = translateExtended ("unknown", lvcarea, "")
        smove = Smove()
        smove_list.append(smove)

        smove.datum = movement.datum
        smove.fRoom = movement.fr_room
        smove.tRoom = movement.to_room

        location = db_session.query(Location).filter(
                (Location.nr == movement.fr_location)).first()

        if location:
            smove.flocation_str = location.bezeich
        else:
            smove.flocation_str = unknown

        location = db_session.query(Location).filter(
                (Location.nr == movement.to_location)).first()

        if location:
            smove.tlocation_str = location.bezeich
        else:
            smove.tlocation_str = unknown


    create_browse()

    return generate_output()