from functions.additional_functions import *
import decimal
from models import Eg_location, Queasy, Eg_property

def eg_propertylist_btn_go_webbl(location:int, rmno:str, main_nr:int, sguestflag:bool):
    q1_list_list = []
    eg_location = queasy = eg_property = None

    q1_list = None

    q1_list_list, Q1_list = create_model("Q1_list", {"nr":int, "bezeich":str, "maintask":int, "char3":str, "char2":str, "zinr":str, "datum":date, "brand":str, "capacity":str, "dimension":str, "type":str, "price":decimal, "spec":str, "location":int, "activeflag":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal q1_list_list, eg_location, queasy, eg_property


        nonlocal q1_list
        nonlocal q1_list_list
        return {"q1-list": q1_list_list}

    def create_it():

        nonlocal q1_list_list, eg_location, queasy, eg_property


        nonlocal q1_list
        nonlocal q1_list_list


        q1_list = Q1_list()
        q1_list_list.append(q1_list)

        q1_list.nr = eg_property.nr
        q1_list.bezeich = eg_property.bezeich
        q1_list.maintask = queasy.number1
        q1_list.char3 = queasy.char1
        q1_list.char2 = eg_Location.bezeich
        q1_list.zinr = eg_property.zinr
        q1_list.datum = eg_property.datum
        q1_list.brand = eg_property.brand
        q1_list.capacity = eg_property.capacity
        q1_list.dimension = eg_property.dimension
        q1_list.TYPE = eg_property.TYPE
        q1_list.price = eg_property.price
        q1_list.Spec = eg_property.Spec
        q1_list.location = eg_property.location
        q1_list.activeflag = eg_property.activeflag

    if sguestflag :

        eg_location = db_session.query(Eg_location).filter(
                (Eg_location.guestflag)).first()

        if eg_location:
            location = eg_location.nr

        if trim (rmno) != "" and main_nr == 0:

            eg_property_obj_list = []
            for eg_property, eg_Location, queasy in db_session.query(Eg_property, Eg_Location, Queasy).join(Eg_Location,(Eg_Location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) &  (Queasy.number1 == Eg_property.maintask)).filter(
                    (Eg_property.zinr == rmno)).all():
                if eg_property._recid in eg_property_obj_list:
                    continue
                else:
                    eg_property_obj_list.append(eg_property._recid)


                create_it()


        elif trim (rmno) != "" and main_nr != 0:

            eg_property_obj_list = []
            for eg_property, eg_Location, queasy in db_session.query(Eg_property, Eg_Location, Queasy).join(Eg_Location,(Eg_Location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) &  (Queasy.number1 == Eg_property.maintask)).filter(
                    (Eg_property.zinr == rmno) &  (Eg_property.maintask == main_nr)).all():
                if eg_property._recid in eg_property_obj_list:
                    continue
                else:
                    eg_property_obj_list.append(eg_property._recid)


                create_it()


        elif trim (rmno) == "" and main_nr == 0:

            eg_property_obj_list = []
            for eg_property, eg_Location, queasy in db_session.query(Eg_property, Eg_Location, Queasy).join(Eg_Location,(Eg_Location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) &  (Queasy.number1 == Eg_property.maintask)).filter(
                    (Eg_property.location == location)).all():
                if eg_property._recid in eg_property_obj_list:
                    continue
                else:
                    eg_property_obj_list.append(eg_property._recid)


                create_it()


        elif trim (rmno) == "" and main_nr != 0:

            eg_property_obj_list = []
            for eg_property, eg_Location, queasy in db_session.query(Eg_property, Eg_Location, Queasy).join(Eg_Location,(Eg_Location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) &  (Queasy.number1 == Eg_property.maintask)).filter(
                    (Eg_property.location == location) &  (Eg_property.maintask == main_nr)).all():
                if eg_property._recid in eg_property_obj_list:
                    continue
                else:
                    eg_property_obj_list.append(eg_property._recid)


                create_it()

    else:

        if location == 0:

            if main_nr == 0:

                eg_property_obj_list = []
                for eg_property, eg_Location, queasy in db_session.query(Eg_property, Eg_Location, Queasy).join(Eg_Location,(Eg_Location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) &  (Queasy.number1 == Eg_property.maintask)).all():
                    if eg_property._recid in eg_property_obj_list:
                        continue
                    else:
                        eg_property_obj_list.append(eg_property._recid)


                    create_it()


            elif main_nr != 0:

                eg_property_obj_list = []
                for eg_property, eg_Location, queasy in db_session.query(Eg_property, Eg_Location, Queasy).join(Eg_Location,(Eg_Location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) &  (Queasy.number1 == Eg_property.maintask)).filter(
                        (Eg_property.maintask == main_nr)).all():
                    if eg_property._recid in eg_property_obj_list:
                        continue
                    else:
                        eg_property_obj_list.append(eg_property._recid)


                    create_it()

        else:

            if main_nr == 0:

                eg_property_obj_list = []
                for eg_property, eg_Location, queasy in db_session.query(Eg_property, Eg_Location, Queasy).join(Eg_Location,(Eg_Location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) &  (Queasy.number1 == Eg_property.maintask)).filter(
                        (Eg_property.location == location)).all():
                    if eg_property._recid in eg_property_obj_list:
                        continue
                    else:
                        eg_property_obj_list.append(eg_property._recid)


                    create_it()


            elif main_nr != 0:

                eg_property_obj_list = []
                for eg_property, eg_Location, queasy in db_session.query(Eg_property, Eg_Location, Queasy).join(Eg_Location,(Eg_Location.nr == Eg_property.location)).join(Queasy,(Queasy.key == 133) &  (Queasy.number1 == Eg_property.maintask)).filter(
                        (Eg_property.location == location) &  (Eg_property.maintask == main_nr)).all():
                    if eg_property._recid in eg_property_obj_list:
                        continue
                    else:
                        eg_property_obj_list.append(eg_property._recid)


                    create_it()


    return generate_output()