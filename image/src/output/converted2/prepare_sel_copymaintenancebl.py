#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property, Eg_maintain, Eg_location

def prepare_sel_copymaintenancebl(maintain_nr:int):

    prepare_cache ([Eg_property, Eg_maintain, Eg_location])

    property_list = []
    eg_property = eg_maintain = eg_location = None

    property = None

    property_list, Property = create_model("Property", {"prop_nr":int, "prop_nm":string, "prop_loc":int, "prop_loc_nm":string, "prop_zinr":string, "prop_selected":bool, "str":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal property_list, eg_property, eg_maintain, eg_location
        nonlocal maintain_nr


        nonlocal property
        nonlocal property_list

        return {"property": property_list}

    def prop():

        nonlocal property_list, eg_property, eg_maintain, eg_location
        nonlocal maintain_nr


        nonlocal property
        nonlocal property_list

        i:int = 0
        a:int = 0
        loc_nm:string = ""
        qbuff1 = None
        Qbuff1 =  create_buffer("Qbuff1",Eg_property)
        property_list.clear()

        eg_maintain = get_cache (Eg_maintain, {"maintainnr": [(eq, maintain_nr)]})

        if eg_maintain:
            i = eg_maintain.propertynr

            eg_property = get_cache (Eg_property, {"nr": [(eq, eg_maintain.propertynr)]})

            if eg_property:
                a = eg_property.maintask

            for eg_property in db_session.query(Eg_property).filter(
                     (Eg_property.maintask == a) & (Eg_property.nr != i)).order_by(Eg_property.location, Eg_property.zinr).all():

                eg_location = get_cache (Eg_location, {"nr": [(eq, eg_property.location)]})

                if eg_location:
                    loc_nm = eg_location.bezeich
                else:
                    loc_nm = ""
                property = Property()
                property_list.append(property)

                property.prop_nr = eg_property.nr
                property.prop_nm = eg_property.bezeich
                property.prop_loc = eg_property.location
                property.prop_loc_nm = loc_nm
                property.prop_zinr = eg_property.zinr
                property.prop_selected = False

    prop()

    return generate_output()