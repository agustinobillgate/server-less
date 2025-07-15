#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_moveproperty, Eg_property, Eg_request, Eg_maintain

def eg_propertylist_btn_okbl(case_type:int, nonr:int, location2:int, zinr:string):

    prepare_cache ([Eg_moveproperty, Eg_property, Eg_request, Eg_maintain])

    msg = False
    eg_moveproperty = eg_property = eg_request = eg_maintain = None

    queri2 = None

    Queri2 = create_buffer("Queri2",Eg_moveproperty)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg, eg_moveproperty, eg_property, eg_request, eg_maintain
        nonlocal case_type, nonr, location2, zinr
        nonlocal queri2


        nonlocal queri2

        return {"msg": msg}


    if case_type == 1:

        eg_property = get_cache (Eg_property, {"nr": [(eq, nonr)]})

        if eg_property:

            if eg_property.location != location2:
                queri2 = Eg_moveproperty()
                db_session.add(queri2)

                queri2.datum = get_current_date()
                queri2.property_nr = eg_property.nr
                queri2.fr_location = eg_property.location
                queri2.to_location = location2
                queri2.fr_room = eg_property.zinr
                queri2.to_room = zinr


            else:
                queri2 = Eg_moveproperty()
                db_session.add(queri2)

                queri2.datum = get_current_date()
                queri2.property_nr = eg_property.nr
                queri2.fr_location = eg_property.location
                queri2.to_location = location2
                queri2.fr_room = eg_property.zinr
                queri2.to_room = zinr


            eg_property.location = location2
            eg_property.zinr = zinr

            for eg_request in db_session.query(Eg_request).filter(
                     (Eg_request.propertynr == eg_property.nr) & (Eg_request.reqstatus < 3)).order_by(Eg_request._recid).all():
                eg_request.reserve_int = location2
                eg_request.zinr = zinr

            for eg_maintain in db_session.query(Eg_maintain).filter(
                     (Eg_maintain.propertynr == eg_property.nr) & (Eg_maintain.type == 1)).order_by(Eg_maintain._recid).all():
                eg_maintain.location = location2
                eg_maintain.zinr = zinr


            msg = True

    elif case_type == 2:

        eg_property = get_cache (Eg_property, {"nr": [(eq, nonr)]})

        if eg_property:

            if eg_property.location != location2:
                queri2 = Eg_moveproperty()
                db_session.add(queri2)

                queri2.datum = get_current_date()
                queri2.property_nr = eg_property.nr
                queri2.fr_location = eg_property.location
                queri2.to_location = location2
                queri2.fr_room = eg_property.zinr
                queri2.to_room = zinr


            else:
                queri2 = Eg_moveproperty()
                db_session.add(queri2)

                queri2.datum = get_current_date()
                queri2.property_nr = eg_property.nr
                queri2.fr_location = eg_property.location
                queri2.to_location = location2
                queri2.fr_room = eg_property.zinr
                queri2.to_room = zinr


            eg_property.location = location2
            eg_property.zinr = zinr

            for eg_request in db_session.query(Eg_request).filter(
                     (Eg_request.propertynr == eg_property.nr) & (Eg_request.reqstatus < 3)).order_by(Eg_request._recid).all():
                eg_request.reserve_int = location2
                eg_request.zinr = zinr

            for eg_maintain in db_session.query(Eg_maintain).filter(
                     (Eg_maintain.propertynr == eg_property.nr) & (Eg_maintain.type == 1)).order_by(Eg_maintain._recid).all():
                eg_maintain.location = location2
                eg_maintain.zinr = zinr


            msg = True

    return generate_output()