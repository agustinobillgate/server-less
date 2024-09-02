from functions.additional_functions import *
import decimal
from datetime import date
from models import Eg_property, Eg_moveproperty

def eg_property_btn_exit2bl(property:[Property], nr:int, curr_date:date):
    eg_property = eg_moveproperty = None

    property = queri = queri2 = None

    property_list, Property = create_model_like(Eg_property)

    Queri = Eg_property
    Queri2 = Eg_moveproperty

    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_property, eg_moveproperty
        nonlocal queri, queri2


        nonlocal property, queri, queri2
        nonlocal property_list
        return {}

    property = query(property_list, first=True)

    eg_property = db_session.query(Eg_property).filter(
            (Eg_property.nr == nr)).first()

    eg_property = db_session.query(Eg_property).first()

    if eg_property:

        if eg_property.location != property.location:
            queri2 = Queri2()
            db_session.add(queri2)

            queri2.datum = curr_date
            queri2.property_nr = property.nr
            queri2.fr_location = eg_property.location
            queri2.to_location = property.location
            queri2.fr_room = eg_property.zinr
            queri2.to_room = property.zinr


        else:

            if eg_property.zinr != "":

                if eg_property.zinr != property.zinr:
                    queri2 = Queri2()
                    db_session.add(queri2)

                    queri2.datum = curr_date
                    queri2.property_nr = property.nr
                    queri2.fr_location = eg_property.location
                    queri2.to_location = property.location
                    queri2.fr_room = eg_property.zinr
                    queri2.to_room = property.zinr


            else:

                if eg_property.zinr != property.zinr:
                    queri2 = Queri2()
                    db_session.add(queri2)

                    queri2.datum = curr_date
                    queri2.property_nr = property.nr
                    queri2.fr_location = eg_property.location
                    queri2.to_location = property.location
                    queri2.fr_room = eg_property.zinr
                    queri2.to_room = property.zinr


    buffer_copy(property, eg_property)

    eg_property = db_session.query(Eg_property).first()

    return generate_output()