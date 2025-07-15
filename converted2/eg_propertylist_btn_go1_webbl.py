#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_location, Queasy, Eg_property

input_param_data, Input_param = create_model("Input_param", {"rmno":string, "main_nr":int, "sguestflag":bool, "last_nr":int, "item_nr":int}, {"rmno": "0"})

def eg_propertylist_btn_go1_webbl(location:int, input_param_data:[Input_param]):

    prepare_cache ([Eg_location, Queasy, Eg_property])

    q1_list_data = []
    output_list_data = []
    counter:int = 0
    eg_location = queasy = eg_property = None

    q1_list = output_list = input_param = None

    q1_list_data, Q1_list = create_model("Q1_list", {"nr":int, "bezeich":string, "maintask":int, "char3":string, "char2":string, "zinr":string, "datum":date, "brand":string, "capacity":string, "dimension":string, "type":string, "price":Decimal, "spec":string, "location":int, "activeflag":bool})
    output_list_data, Output_list = create_model("Output_list", {"last_nr":int, "all_data":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_data, output_list_data, counter, eg_location, queasy, eg_property
        nonlocal location


        nonlocal q1_list, output_list, input_param
        nonlocal q1_list_data, output_list_data

        return {"location": location, "q1-list": q1_list_data, "output-list": output_list_data}

    def create_it():

        nonlocal q1_list_data, output_list_data, counter, eg_location, queasy, eg_property
        nonlocal location


        nonlocal q1_list, output_list, input_param
        nonlocal q1_list_data, output_list_data


        q1_list = Q1_list()
        q1_list_data.append(q1_list)

        q1_list.nr = eg_property.nr
        q1_list.bezeich = eg_property.bezeich
        q1_list.maintask = queasy.number1
        q1_list.char3 = queasy.char1
        q1_list.char2 = eg_location.bezeich
        q1_list.zinr = eg_property.zinr
        q1_list.datum = eg_property.datum
        q1_list.brand = eg_property.brand
        q1_list.capacity = eg_property.capacity
        q1_list.dimension = eg_property.dimension
        q1_list.type = eg_property.type
        q1_list.price =  to_decimal(eg_property.price)
        q1_list.spec = eg_property.spec
        q1_list.location = eg_property.location
        q1_list.activeflag = eg_property.activeflag


    input_param = query(input_param_data, first=True)
    output_list = Output_list()
    output_list_data.append(output_list)

    counter = 0

    if input_param.sguestflag :

        eg_location = get_cache (Eg_location, {"guestflag": [(eq, True)]})

        if eg_location:
            location = eg_location.nr

        if trim (input_param.rmno) != "" and input_param.main_nr == 0:

            if input_param.item_nr == 0:

                eg_property_obj_list = {}
                eg_property = Eg_property()
                eg_location = Eg_location()
                queasy = Queasy()
                for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                         (Eg_property.zinr == input_param.rmno) & (Eg_property.nr > input_param.last_nr)).order_by(Eg_property._recid).yield_per(100):
                    if eg_property_obj_list.get(eg_property._recid):
                        continue
                    else:
                        eg_property_obj_list[eg_property._recid] = True


                    counter = counter + 1
                    create_it()

                    if counter == 300:
                        output_list.last_nr = eg_property.nr
                        break
            else:

                eg_property_obj_list = {}
                eg_property = Eg_property()
                eg_location = Eg_location()
                queasy = Queasy()
                for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                         (Eg_property.zinr == input_param.rmno) & (Eg_property.nr == input_param.item_nr)).order_by(Eg_property._recid).yield_per(100):
                    if eg_property_obj_list.get(eg_property._recid):
                        continue
                    else:
                        eg_property_obj_list[eg_property._recid] = True


                    counter = counter + 1
                    create_it()

                    if counter == 300:
                        output_list.last_nr = eg_property.nr
                        break

        elif trim (input_param.rmno) != "" and input_param.main_nr != 0:

            if input_param.item_nr == 0:

                eg_property_obj_list = {}
                eg_property = Eg_property()
                eg_location = Eg_location()
                queasy = Queasy()
                for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                         (Eg_property.zinr == input_param.rmno) & (Eg_property.maintask == input_param.main_nr) & (Eg_property.nr > input_param.last_nr)).order_by(Eg_property._recid).yield_per(100):
                    if eg_property_obj_list.get(eg_property._recid):
                        continue
                    else:
                        eg_property_obj_list[eg_property._recid] = True


                    counter = counter + 1
                    create_it()

                    if counter == 300:
                        output_list.last_nr = eg_property.nr
                        break
            else:

                eg_property_obj_list = {}
                eg_property = Eg_property()
                eg_location = Eg_location()
                queasy = Queasy()
                for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                         (Eg_property.zinr == input_param.rmno) & (Eg_property.maintask == input_param.main_nr) & (Eg_property.nr == input_param.item_nr)).order_by(Eg_property._recid).yield_per(100):
                    if eg_property_obj_list.get(eg_property._recid):
                        continue
                    else:
                        eg_property_obj_list[eg_property._recid] = True


                    counter = counter + 1
                    create_it()

                    if counter == 300:
                        output_list.last_nr = eg_property.nr
                        break

        elif trim (input_param.rmno) == "" and input_param.main_nr == 0:

            if input_param.item_nr == 0:

                eg_property_obj_list = {}
                eg_property = Eg_property()
                eg_location = Eg_location()
                queasy = Queasy()
                for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                         (Eg_property.location == location) & (Eg_property.nr > input_param.last_nr)).order_by(Eg_property._recid).yield_per(100):
                    if eg_property_obj_list.get(eg_property._recid):
                        continue
                    else:
                        eg_property_obj_list[eg_property._recid] = True


                    counter = counter + 1
                    create_it()

                    if counter == 300:
                        output_list.last_nr = eg_property.nr
                        break
            else:

                eg_property_obj_list = {}
                eg_property = Eg_property()
                eg_location = Eg_location()
                queasy = Queasy()
                for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                         (Eg_property.location == location) & (Eg_property.nr == input_param.item_nr)).order_by(Eg_property._recid).yield_per(100):
                    if eg_property_obj_list.get(eg_property._recid):
                        continue
                    else:
                        eg_property_obj_list[eg_property._recid] = True


                    counter = counter + 1
                    create_it()

                    if counter == 300:
                        output_list.last_nr = eg_property.nr
                        break

        elif trim (input_param.rmno) == "" and input_param.main_nr != 0:

            if input_param.item_nr == 0:

                eg_property_obj_list = {}
                eg_property = Eg_property()
                eg_location = Eg_location()
                queasy = Queasy()
                for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                         (Eg_property.location == location) & (Eg_property.maintask == input_param.main_nr) & (Eg_property.nr > input_param.last_nr)).order_by(Eg_property._recid).yield_per(100):
                    if eg_property_obj_list.get(eg_property._recid):
                        continue
                    else:
                        eg_property_obj_list[eg_property._recid] = True


                    counter = counter + 1
                    create_it()

                    if counter == 300:
                        output_list.last_nr = eg_property.nr
                        break
            else:

                eg_property_obj_list = {}
                eg_property = Eg_property()
                eg_location = Eg_location()
                queasy = Queasy()
                for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                         (Eg_property.location == location) & (Eg_property.maintask == input_param.main_nr) & (Eg_property.nr == input_param.item_nr)).order_by(Eg_property._recid).yield_per(100):
                    if eg_property_obj_list.get(eg_property._recid):
                        continue
                    else:
                        eg_property_obj_list[eg_property._recid] = True


                    counter = counter + 1
                    create_it()

                    if counter == 300:
                        output_list.last_nr = eg_property.nr
                        break
    else:

        if location == 0:

            if input_param.main_nr == 0:

                if input_param.item_nr == 0:

                    eg_property_obj_list = {}
                    eg_property = Eg_property()
                    eg_location = Eg_location()
                    queasy = Queasy()
                    for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location) & (Eg_property.nr > input_param.last_nr)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).order_by(Eg_property._recid).yield_per(100):
                        if eg_property_obj_list.get(eg_property._recid):
                            continue
                        else:
                            eg_property_obj_list[eg_property._recid] = True


                        counter = counter + 1
                        create_it()

                        if counter == 300:
                            output_list.last_nr = eg_property.nr
                            break
                else:

                    eg_property_obj_list = {}
                    eg_property = Eg_property()
                    eg_location = Eg_location()
                    queasy = Queasy()
                    for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location) & (Eg_property.nr == input_param.item_nr)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).order_by(Eg_property._recid).yield_per(100):
                        if eg_property_obj_list.get(eg_property._recid):
                            continue
                        else:
                            eg_property_obj_list[eg_property._recid] = True


                        counter = counter + 1
                        create_it()

                        if counter == 300:
                            output_list.last_nr = eg_property.nr
                            break

            elif input_param.main_nr != 0:

                if input_param.item_nr == 0:

                    eg_property_obj_list = {}
                    eg_property = Eg_property()
                    eg_location = Eg_location()
                    queasy = Queasy()
                    for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                             (Eg_property.maintask == input_param.main_nr) & (Eg_property.nr > input_param.last_nr)).order_by(Eg_property._recid).yield_per(100):
                        if eg_property_obj_list.get(eg_property._recid):
                            continue
                        else:
                            eg_property_obj_list[eg_property._recid] = True


                        counter = counter + 1
                        create_it()

                        if counter == 300:
                            output_list.last_nr = eg_property.nr
                            break
                else:

                    eg_property_obj_list = {}
                    eg_property = Eg_property()
                    eg_location = Eg_location()
                    queasy = Queasy()
                    for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                             (Eg_property.maintask == input_param.main_nr) & (Eg_property.nr == input_param.item_nr)).order_by(Eg_property._recid).yield_per(100):
                        if eg_property_obj_list.get(eg_property._recid):
                            continue
                        else:
                            eg_property_obj_list[eg_property._recid] = True


                        counter = counter + 1
                        create_it()

                        if counter == 300:
                            output_list.last_nr = eg_property.nr
                            break
        else:

            if input_param.main_nr == 0:

                if input_param.item_nr == 0:

                    eg_property_obj_list = {}
                    eg_property = Eg_property()
                    eg_location = Eg_location()
                    queasy = Queasy()
                    for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                             (Eg_property.location == location) & (Eg_property.nr > input_param.last_nr)).order_by(Eg_property._recid).yield_per(100):
                        if eg_property_obj_list.get(eg_property._recid):
                            continue
                        else:
                            eg_property_obj_list[eg_property._recid] = True


                        counter = counter + 1
                        create_it()

                        if counter == 300:
                            output_list.last_nr = eg_property.nr
                            break
                else:

                    eg_property_obj_list = {}
                    eg_property = Eg_property()
                    eg_location = Eg_location()
                    queasy = Queasy()
                    for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                             (Eg_property.location == location) & (Eg_property.nr == input_param.item_nr)).order_by(Eg_property._recid).yield_per(100):
                        if eg_property_obj_list.get(eg_property._recid):
                            continue
                        else:
                            eg_property_obj_list[eg_property._recid] = True


                        counter = counter + 1
                        create_it()

                        if counter == 300:
                            output_list.last_nr = eg_property.nr
                            break

            elif input_param.main_nr != 0:

                if input_param.item_nr == 0:

                    eg_property_obj_list = {}
                    eg_property = Eg_property()
                    eg_location = Eg_location()
                    queasy = Queasy()
                    for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                             (Eg_property.location == location) & (Eg_property.maintask == input_param.main_nr) & (Eg_property.nr > input_param.last_nr)).order_by(Eg_property._recid).yield_per(100):
                        if eg_property_obj_list.get(eg_property._recid):
                            continue
                        else:
                            eg_property_obj_list[eg_property._recid] = True


                        counter = counter + 1
                        create_it()

                        if counter == 300:
                            output_list.last_nr = eg_property.nr
                            break
                else:

                    eg_property_obj_list = {}
                    eg_property = Eg_property()
                    eg_location = Eg_location()
                    queasy = Queasy()
                    for eg_property.nr, eg_property.bezeich, eg_property.zinr, eg_property.datum, eg_property.brand, eg_property.capacity, eg_property.dimension, eg_property.type, eg_property.price, eg_property.spec, eg_property.location, eg_property.activeflag, eg_property._recid, eg_location.bezeich, eg_location.nr, eg_location._recid, queasy.number1, queasy.char1, queasy._recid in db_session.query(Eg_property.nr, Eg_property.bezeich, Eg_property.zinr, Eg_property.datum, Eg_property.brand, Eg_property.capacity, Eg_property.dimension, Eg_property.type, Eg_property.price, Eg_property.spec, Eg_property.location, Eg_property.activeflag, Eg_property._recid, Eg_location.bezeich, Eg_location.nr, Eg_location._recid, Queasy.number1, Queasy.char1, Queasy._recid).join(Eg_location,(Eg_location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) & (Queasy.number1 == Eg_property.maintask)).filter(
                             (Eg_property.location == location) & (Eg_property.maintask == input_param.main_nr) & (Eg_property.nr == input_param.item_nr)).order_by(Eg_property._recid).yield_per(100):
                        if eg_property_obj_list.get(eg_property._recid):
                            continue
                        else:
                            eg_property_obj_list[eg_property._recid] = True


                        counter = counter + 1
                        create_it()

                        if counter == 300:
                            output_list.last_nr = eg_property.nr
                            break

    if counter < 300:
        output_list.all_data = True

    return generate_output()