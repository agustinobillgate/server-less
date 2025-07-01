#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_property, Queasy

tempcopy_list, Tempcopy = create_model("Tempcopy", {"loc_nr":int, "loc_nm":string, "zinr":string, "qty":int, "temp_selected":bool})

def sel_copyprop_btn_ok2bl(tempcopy_list:[Tempcopy], property_nr:int):

    prepare_cache ([Eg_property, Queasy])

    flag = 0
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
    tmp_nr:int = 0
    eg_property = queasy = None

    tempcopy = propbuff = None

    Propbuff = create_buffer("Propbuff",Eg_property)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, blcopy, nr, asset, bezeich, location, zinr, brand, capacity, dimension, type, maintask, str_maintask, datum, price, spec, meterrec, edbezeich, i, j, tmp_nr, eg_property, queasy
        nonlocal property_nr
        nonlocal propbuff


        nonlocal tempcopy, propbuff

        return {"flag": flag}

    def init_nr():

        nonlocal flag, blcopy, nr, asset, bezeich, location, zinr, brand, capacity, dimension, type, maintask, str_maintask, datum, price, spec, meterrec, edbezeich, i, j, tmp_nr, eg_property, queasy
        nonlocal property_nr
        nonlocal propbuff


        nonlocal tempcopy, propbuff

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

        for tempcopy in query(tempcopy_list, filters=(lambda tempcopy: tempcopy.temp_selected)):
            tmp_nr = init_nr()
            nr = tmp_nr

            if tempcopy.zinr == "":

                propbuff = get_cache (Eg_property, {"bezeich": [(eq, edbezeich)],"maintask": [(eq, maintask)],"location": [(eq, tempcopy.loc_nr)]})

                if not propbuff:
                    eg_property = Eg_property()
                    db_session.add(eg_property)

                    eg_property.nr = nr
                    eg_property.asset = asset
                    eg_property.bezeich = edbezeich
                    eg_property.location = tempcopy.loc_nr
                    eg_property.zinr = ""
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


            else:

                propbuff = get_cache (Eg_property, {"bezeich": [(eq, edbezeich)],"maintask": [(eq, maintask)],"location": [(eq, tempcopy.loc_nr)],"zinr": [(eq, tempcopy.zinr)]})

                if not propbuff:
                    eg_property = Eg_property()
                    db_session.add(eg_property)

                    eg_property.nr = nr
                    eg_property.asset = asset
                    eg_property.bezeich = edbezeich
                    eg_property.location = tempcopy.loc_nr
                    eg_property.zinr = tempcopy.zinr
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


        tempcopy_list.clear()
        flag = 1

    return generate_output()