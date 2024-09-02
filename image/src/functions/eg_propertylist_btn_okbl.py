from functions.additional_functions import *
import decimal
from models import Eg_moveproperty, Eg_property, Eg_request, Eg_maintain

def eg_propertylist_btn_okbl(case_type:int, nonr:int, location2:int, zinr:str):
    msg = False
    eg_moveproperty = eg_property = eg_request = eg_maintain = None

    queri2 = None

    Queri2 = Eg_moveproperty

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg, eg_moveproperty, eg_property, eg_request, eg_maintain
        nonlocal queri2


        nonlocal queri2
        return {"msg": msg}


    if case_type == 1:

        eg_property = db_session.query(Eg_property).filter(
                (Eg_property.nr == nonr)).first()

        if eg_property:

            if eg_property.location != location:
                queri2 = Queri2()
                db_session.add(queri2)

                queri2.datum = get_current_date()
                queri2.property_nr = eg_property.nr
                queri2.fr_location = eg_property.location
                queri2.to_location = location2
                queri2.fr_room = eg_property.zinr
                queri2.to_room = zinr


            else:
                queri2 = Queri2()
                db_session.add(queri2)

                queri2.datum = get_current_date()
                queri2.property_nr = eg_property.nr
                queri2.fr_location = eg_property.location
                queri2.to_location = location2
                queri2.fr_room = eg_property.zinr
                queri2.to_room = zinr


            eg_property.location = location2
            eg_property.zinr = zinr

            for eg_request in db_session.query(Eg_request).all():
                eg_request.reserve_int = location2 eg_request.zinr == zinr

            for eg_maintain in db_session.query(Eg_maintain).all():
                eg_maintain.location = location2 eg_maintain.zinr == zinr


            msg = True

    elif case_type == 2:

        eg_property = db_session.query(Eg_property).filter(
                (Eg_property.nr == nonr)).first()

        if eg_property:

            if eg_property.location != location2:
                queri2 = Queri2()
                db_session.add(queri2)

                queri2.datum = get_current_date()
                queri2.property_nr = eg_property.nr
                queri2.fr_location = eg_property.location
                queri2.to_location = location2
                queri2.fr_room = eg_property.zinr
                queri2.to_room = zinr


            else:
                queri2 = Queri2()
                db_session.add(queri2)

                queri2.datum = get_current_date()
                queri2.property_nr = eg_property.nr
                queri2.fr_location = eg_property.location
                queri2.to_location = location2
                queri2.fr_room = eg_property.zinr
                queri2.to_room = zinr


            eg_property.location = location2
            eg_property.zinr = zinr

            for eg_request in db_session.query(Eg_request).all():
                eg_request.reserve_int = location2 eg_request.zinr == zinr

            for eg_maintain in db_session.query(Eg_maintain).all():
                eg_maintain.location = location2 eg_maintain.zinr == zinr


            msg = True

    return generate_output()