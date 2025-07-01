#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_moveproperty, Eg_location

def eg_rephistorymove_create_browsebl(pvilanguage:int, prop_nr:int, fdate:date, tdate:date):

    prepare_cache ([Eg_moveproperty, Eg_location])

    smove_list = []
    lvcarea:string = "eg-RepHistoryMove"
    eg_moveproperty = eg_location = None

    smove = movement = location = None

    smove_list, Smove = create_model("Smove", {"datum":date, "flocation_str":string, "froom":string, "tlocation_str":string, "troom":string})

    Movement = create_buffer("Movement",Eg_moveproperty)
    Location = create_buffer("Location",Eg_location)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal smove_list, lvcarea, eg_moveproperty, eg_location
        nonlocal pvilanguage, prop_nr, fdate, tdate
        nonlocal movement, location


        nonlocal smove, movement, location
        nonlocal smove_list

        return {"sMove": smove_list}

    def create_browse():

        nonlocal smove_list, lvcarea, eg_moveproperty, eg_location
        nonlocal pvilanguage, prop_nr, fdate, tdate
        nonlocal movement, location


        nonlocal smove, movement, location
        nonlocal smove_list


        smove_list.clear()

        for movement in db_session.query(Movement).filter(
                 (Movement.property_nr == prop_nr) & (Movement.datum >= fdate) & (Movement.datum <= tdate)).order_by(Movement._recid).all():
            add_line()


    def add_line():

        nonlocal smove_list, lvcarea, eg_moveproperty, eg_location
        nonlocal pvilanguage, prop_nr, fdate, tdate
        nonlocal movement, location


        nonlocal smove, movement, location
        nonlocal smove_list

        unknown:string = ""
        unknown = translateExtended ("unknown", lvcarea, "")
        smove = Smove()
        smove_list.append(smove)

        smove.datum = movement.datum
        smove.froom = movement.fr_room
        smove.troom = movement.to_room

        location = get_cache (Eg_location, {"nr": [(eq, movement.fr_location)]})

        if location:
            smove.flocation_str = location.bezeich
        else:
            smove.flocation_str = unknown

        location = get_cache (Eg_location, {"nr": [(eq, movement.to_location)]})

        if location:
            smove.tlocation_str = location.bezeich
        else:
            smove.tlocation_str = unknown

    create_browse()

    return generate_output()