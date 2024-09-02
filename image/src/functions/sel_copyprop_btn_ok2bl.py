from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_property, Queasy

def sel_copyprop_btn_ok2bl(tempcopy:[Tempcopy], property_nr:int):
    flag = 0
    blcopy:str = ""
    nr:int = 0
    asset:str = ""
    bezeich:str = ""
    location:int = 0
    zinr:str = ""
    brand:str = ""
    capacity:str = ""
    dimension:str = ""
    type:str = ""
    maintask:int = 0
    str_maintask:str = ""
    datum:date = None
    price:decimal = 0
    spec:str = ""
    meterrec:bool = False
    edbezeich:str = ""
    i:int = 0
    j:str = ""
    tmp_nr:int = 0
    eg_property = queasy = None

    tempcopy = propbuff = None

    tempcopy_list, Tempcopy = create_model("Tempcopy", {"loc_nr":int, "loc_nm":str, "zinr":str, "qty":int, "temp_selected":bool})

    Propbuff = Eg_property

    db_session = local_storage.db_session

    def generate_output():
        nonlocal flag, blcopy, nr, asset, bezeich, location, zinr, brand, capacity, dimension, type, maintask, str_maintask, datum, price, spec, meterrec, edbezeich, i, j, tmp_nr, eg_property, queasy
        nonlocal propbuff


        nonlocal tempcopy, propbuff
        nonlocal tempcopy_list
        return {"flag": flag}

    def init_nr():

        nonlocal flag, blcopy, nr, asset, bezeich, location, zinr, brand, capacity, dimension, type, maintask, str_maintask, datum, price, spec, meterrec, edbezeich, i, j, tmp_nr, eg_property, queasy
        nonlocal propbuff


        nonlocal tempcopy, propbuff
        nonlocal tempcopy_list

        def_nr = 0
        temp_nr:int = 0

        def generate_inner_output():
            return def_nr

        for eg_property in db_session.query(Eg_property).all():

            if temp_nr == 0:
                temp_nr = eg_property.nr
            else:

                if temp_nr < eg_property.nr:
                    temp_nr = eg_property.nr
                else:
                    temp_nr = temp_nr
        def_nr = temp_nr + 1


        return generate_inner_output()

    eg_property = db_session.query(Eg_property).filter(
            (Eg_property.nr == property_nr)).first()

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
        price = eg_property.price
        spec = eg_property.spec
        meterrec = eg_property.meterrec


        i = num_entries(bezeich, "(")
        edbezeich = trim (entry(0 , bezeich , "("))

        queasy = db_session.query(Queasy).filter(
                (Queasy.KEY == 133) &  (Queasy.number1 == maintask)).first()

        if queasy:
            str_maintask = queasy.CHAR1
    else:
        blcopy = "0"

    if blcopy.lower()  == "1":

        for tempcopy in query(tempcopy_list, filters=(lambda tempcopy :tempcopy.temp_selected)):
            tmp_nr = init_nr()
            nr = tmp_nr

            if tempcopy.zinr == "":

                propbuff = db_session.query(Propbuff).filter(
                        (Propbuff.bezeich == edbezeich) &  (Propbuff.maintask == maintask) &  (Propbuff.location == tempcopy.loc_nr)).first()

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
                    eg_property.price = price
                    eg_property.spec = spec
                    eg_property.activeflag = True
                    eg_property.meterrec = meterrec


            else:

                propbuff = db_session.query(Propbuff).filter(
                        (Propbuff.bezeich == edbezeich) &  (Propbuff.maintask == maintask) &  (Propbuff.location == tempcopy.loc_nr) &  (Propbuff.zinr == tempcopy.zinr)).first()

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
                    eg_property.price = price
                    eg_property.spec = spec
                    eg_property.activeflag = True
                    eg_property.meterrec = meterrec


        tempcopy_list.clear()
        flag = 1

    return generate_output()