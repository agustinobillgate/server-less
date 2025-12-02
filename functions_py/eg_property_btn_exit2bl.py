#using conversion tools version: 1.0.0.117

# ==================================
# Rulita, 27-11-2025
# - Added with_for_update all query 
# ==================================

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Eg_property, Eg_moveproperty

property_data, Property = create_model_like(Eg_property)

def eg_property_btn_exit2bl(property_data:[Property], nr:int, curr_date:date):

    prepare_cache ([Eg_property, Eg_moveproperty])

    eg_property = eg_moveproperty = None

    property = queri = queri2 = None

    Queri = create_buffer("Queri",Eg_property)
    Queri2 = create_buffer("Queri2",Eg_moveproperty)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal eg_property, eg_moveproperty
        nonlocal nr, curr_date
        nonlocal queri, queri2


        nonlocal property, queri, queri2

        return {}

    property = query(property_data, first=True)

    # eg_property = get_cache (Eg_property, {"nr": [(eq, nr)]})
    eg_property = db_session.query(Eg_property).filter(
             (Eg_property.nr == nr)).with_for_update().first()
    pass

    if eg_property:

        if eg_property.location != property.location:
            queri2 = Eg_moveproperty()
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
                    queri2 = Eg_moveproperty()
                    db_session.add(queri2)

                    queri2.datum = curr_date
                    queri2.property_nr = property.nr
                    queri2.fr_location = eg_property.location
                    queri2.to_location = property.location
                    queri2.fr_room = eg_property.zinr
                    queri2.to_room = property.zinr


            else:

                if eg_property.zinr != property.zinr:
                    queri2 = Eg_moveproperty()
                    db_session.add(queri2)

                    queri2.datum = curr_date
                    queri2.property_nr = property.nr
                    queri2.fr_location = eg_property.location
                    queri2.to_location = property.location
                    queri2.fr_room = eg_property.zinr
                    queri2.to_room = property.zinr


    buffer_copy(property, eg_property)
    db_session.refresh(eg_property,with_for_update=True)

    return generate_output()
