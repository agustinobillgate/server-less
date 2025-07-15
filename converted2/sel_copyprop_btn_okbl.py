#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_property, Queasy, Eg_location

location_data, location = create_model("location", {"loc_nr":int, "loc_nm":string, "loc_selected":bool})
room_data, Room = create_model("Room", {"room_nm":string, "room_selected":bool})

def sel_copyprop_btn_okbl(location_data:[location], room_data:[Room], property_nr:int, sguestflag:bool):

    prepare_cache ([Eg_property, Queasy, Eg_location])

    tempcopy_data = []
    blcopy:string = ""
    nr:int = 0
    asset:string = ""
    bezeich:string = ""
    location:int = 0
    zinr:string = ""
    brand:string = ""
    capacity:string = ""
    dimension:string = ""
    type:string = ""
    maintask:int = 0
    str_maintask:string = ""
    datum:date = None
    price:Decimal = to_decimal("0.0")
    spec:string = ""
    meterrec:bool = False
    edbezeich:string = ""
    i:int = 0
    j:string = ""
    c:int = 0
    stlocation:string = ""
    tmp_nr:int = 0
    eg_property = queasy = eg_location = None

    room = tempcopy = location = propbuff = None

    tempcopy_data, Tempcopy = create_model("Tempcopy", {"loc_nr":int, "loc_nm":string, "zinr":string, "qty":int, "temp_selected":bool})

    Propbuff = create_buffer("Propbuff",Eg_property)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tempcopy_data, blcopy, nr, asset, bezeich, location, zinr, brand, capacity, dimension, type, maintask, str_maintask, datum, price, spec, meterrec, edbezeich, i, j, c, stlocation, tmp_nr, eg_property, queasy, eg_location
        nonlocal property_nr, sguestflag
        nonlocal propbuff


        nonlocal room, tempcopy, location, propbuff
        nonlocal tempcopy_data

        return {"tempcopy": tempcopy_data}

    def init_nr():

        nonlocal tempcopy_data, blcopy, nr, asset, bezeich, location, zinr, brand, capacity, dimension, type, maintask, str_maintask, datum, price, spec, meterrec, edbezeich, i, j, c, stlocation, tmp_nr, eg_property, queasy, eg_location
        nonlocal property_nr, sguestflag
        nonlocal propbuff


        nonlocal room, tempcopy, location, propbuff
        nonlocal tempcopy_data

        def_nr = 0
        temp_nr:int = 0

        def generate_inner_output():
            return (def_nr)


        for eg_property in db_session.query(Eg_property).order_by(Eg_property.nr).all():

            if temp_nr == 0:
                temp_nr = eg_property.nr
            else:

                if temp_nr < eg_property.nr:
                    temp_nr = eg_property.nr
                else:
                    temp_nr = temp_nr
        def_nr = temp_nr + 1

        return generate_inner_output()


    eg_property = get_cache (Eg_property, {"nr": [(eq, property_nr)]})

    if eg_property:
        blcopy = "1"
        asset = eg_property.asset
        bezeich = eg_property.bezeich
        location = eg_property.location
        zinr = eg_property.zinr
        brand = eg_property.brand
        capacity = eg_property.capacity
        dimension = eg_property.dimension
        type = eg_property.type
        maintask = eg_property.maintask
        datum = get_current_date()
        price =  to_decimal(eg_property.price)
        spec = eg_property.spec
        meterrec = eg_property.meterrec


        i = num_entries(bezeich, "(")
        edbezeich = trim (entry(0 , bezeich , "("))

        queasy = db_session.query(Queasy).filter(
                 (Queasy.key == 133) & (Queasy.number1 == maintask)).first()

        if queasy:
            str_maintask = queasy.char1
    else:
        blcopy = "0"

    if blcopy.lower()  == ("1").lower() :

        for location in query(location_data, filters=(lambda location: location.loc_selected)):

            eg_property = get_cache (Eg_property, {"location": [(eq, location.loc_nr)],"maintask": [(eq, maintask)]})

            if eg_property:
                c = 0

                for eg_property in db_session.query(Eg_property).filter(
                         (Eg_property.location == location.loc_nr) & (Eg_property.maintask == maintask)).order_by(Eg_property._recid).all():
                    c = c + 1
                tempcopy = Tempcopy()
                tempcopy_data.append(tempcopy)

                tempcopy.loc_nr = location.loc_nr
                tempcopy.loc_nm = location.loc_nm
                tempcopy.zinr = ""
                tempcopy.qty = c


            else:
                tmp_nr = init_nr()
                nr = tmp_nr

                propbuff = get_cache (Eg_property, {"bezeich": [(eq, edbezeich)],"maintask": [(eq, maintask)],"location": [(eq, location.loc_nr)]})

                if not propbuff:
                    eg_property = Eg_property()
                    db_session.add(eg_property)

                    eg_property.nr = nr
                    eg_property.asset = asset
                    eg_property.bezeich = edbezeich
                    eg_property.location = location.loc_nr
                    eg_property.brand = brand
                    eg_property.capacity = capacity
                    eg_property.dimension = dimension
                    eg_property.type = type
                    eg_property.maintask = maintask
                    eg_property.datum = datum
                    eg_property.price =  to_decimal(price)
                    eg_property.spec = spec
                    eg_property.activeflag = True
                    eg_property.meterrec = meterrec

    if sguestflag :

        eg_location = get_cache (Eg_location, {"guestflag": [(eq, True)]})

        if eg_location:
            location = eg_location.nr
            stlocation = eg_location.bezeich
        else:
            location = 0
            stlocation = ""

        for room in query(room_data, filters=(lambda room: room.room_selected)):

            eg_property = get_cache (Eg_property, {"zinr": [(eq, room.room_nm)],"maintask": [(eq, maintask)]})

            if eg_property:
                c = 0

                for eg_property in db_session.query(Eg_property).filter(
                         (Eg_property.zinr == room.room_nm) & (Eg_property.maintask == maintask)).order_by(Eg_property._recid).all():
                    c = c + 1
                tempcopy = Tempcopy()
                tempcopy_data.append(tempcopy)

                tempcopy.loc_nr = location
                tempcopy.loc_nm = stlocation
                tempcopy.zinr = room.room_nm
                tempcopy.qty = c


            else:
                tmp_nr = init_nr()
                nr = tmp_nr

                propbuff = get_cache (Eg_property, {"bezeich": [(eq, edbezeich)],"maintask": [(eq, maintask)],"location": [(eq, location)],"zinr": [(eq, room.room_nm)]})

                if not propbuff:
                    eg_property = Eg_property()
                    db_session.add(eg_property)

                    eg_property.nr = nr
                    eg_property.asset = asset
                    eg_property.bezeich = edbezeich
                    eg_property.location = location
                    eg_property.zinr = room.room_nm
                    eg_property.brand = brand
                    eg_property.capacity = capacity
                    eg_property.dimension = dimension
                    eg_property.type = type
                    eg_property.maintask = maintask
                    eg_property.datum = datum
                    eg_property.price =  to_decimal(price)
                    eg_property.spec = spec
                    eg_property.activeflag = True
                    eg_property.meterrec = meterrec

    return generate_output()