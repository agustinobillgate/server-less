from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_moveproperty, Queasy, Eg_location, Eg_property

def eg_rephistorymove_btn_gobl(pvilanguage:int, main_nr:int, fdate:date, tdate:date):
    smove_list = []
    nr:int = 0
    nm:str = ""
    lvcarea:str = "eg_rephistorymoveAll"
    eg_moveproperty = queasy = eg_location = eg_property = None

    smove = movement = maintask = location = None

    smove_list, Smove = create_model("Smove", {"object_nr":int, "object_nm":str, "datum":date, "flocation_str":str, "froom":str, "tlocation_str":str, "troom":str})

    Movement = Eg_moveproperty
    Maintask = Queasy
    Location = Eg_location

    db_session = local_storage.db_session

    def generate_output():
        nonlocal smove_list, nr, nm, lvcarea, eg_moveproperty, queasy, eg_location, eg_property
        nonlocal movement, maintask, location


        nonlocal smove, movement, maintask, location
        nonlocal smove_list
        return {"sMove": smove_list}

    def create_browse():

        nonlocal smove_list, nr, nm, lvcarea, eg_moveproperty, queasy, eg_location, eg_property
        nonlocal movement, maintask, location


        nonlocal smove, movement, maintask, location
        nonlocal smove_list


        sMove_list.clear()

        for eg_property in db_session.query(Eg_property).filter(
                (Eg_property.maintask == main_nr)).all():
            nr = eg_property.nr
            nm = eg_property.bezeich

            for movement in db_session.query(Movement).filter(
                    (Movement.property_nr == eg_property.nr) &  (Movement.datum >= fdate) &  (Movement.datum <= tdate)).all():
                add_line()
            nr = 0
            nm = ""

    def add_line():

        nonlocal smove_list, nr, nm, lvcarea, eg_moveproperty, queasy, eg_location, eg_property
        nonlocal movement, maintask, location


        nonlocal smove, movement, maintask, location
        nonlocal smove_list

        unknown:str = ""
        unknown = translateExtended ("unknown", lvcarea, "")
        smove = Smove()
        smove_list.append(smove)

        smove.object_nr = nr
        smove.Object_nm = nm
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