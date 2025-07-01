#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_moveproperty, Queasy, Eg_location, Eg_property

def eg_rephistorymove_btn_gobl(pvilanguage:int, main_nr:int, fdate:date, tdate:date):

    prepare_cache ([Eg_moveproperty, Eg_location, Eg_property])

    smove_list = []
    nr:int = 0
    nm:string = ""
    lvcarea:string = "eg-rephistorymoveAll"
    eg_moveproperty = queasy = eg_location = eg_property = None

    smove = movement = maintask = location = None

    smove_list, Smove = create_model("Smove", {"object_nr":int, "object_nm":string, "datum":date, "flocation_str":string, "froom":string, "tlocation_str":string, "troom":string})

    Movement = create_buffer("Movement",Eg_moveproperty)
    Maintask = create_buffer("Maintask",Queasy)
    Location = create_buffer("Location",Eg_location)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal smove_list, nr, nm, lvcarea, eg_moveproperty, queasy, eg_location, eg_property
        nonlocal pvilanguage, main_nr, fdate, tdate
        nonlocal movement, maintask, location


        nonlocal smove, movement, maintask, location
        nonlocal smove_list

        return {"sMove": smove_list}

    def create_browse():

        nonlocal smove_list, nr, nm, lvcarea, eg_moveproperty, queasy, eg_location, eg_property
        nonlocal pvilanguage, main_nr, fdate, tdate
        nonlocal movement, maintask, location


        nonlocal smove, movement, maintask, location
        nonlocal smove_list


        smove_list.clear()

        for eg_property in db_session.query(Eg_property).filter(
                 (Eg_property.maintask == main_nr)).order_by(Eg_property.nr).all():
            nr = eg_property.nr
            nm = eg_property.bezeich

            for movement in db_session.query(Movement).filter(
                     (Movement.property_nr == eg_property.nr) & (Movement.datum >= fdate) & (Movement.datum <= tdate)).order_by(Movement._recid).all():
                add_line()
            nr = 0
            nm = ""


    def add_line():

        nonlocal smove_list, nr, nm, lvcarea, eg_moveproperty, queasy, eg_location, eg_property
        nonlocal pvilanguage, main_nr, fdate, tdate
        nonlocal movement, maintask, location


        nonlocal smove, movement, maintask, location
        nonlocal smove_list

        unknown:string = ""
        unknown = translateExtended ("unknown", lvcarea, "")
        smove = Smove()
        smove_list.append(smove)

        smove.object_nr = nr
        smove.object_nm = nm
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