from functions.additional_functions import *
import decimal
from models import Eg_property, Eg_maintain, Eg_location

def prepare_sel_copymaintenancebl(maintain_nr:int):
    property_list = []
    eg_property = eg_maintain = eg_location = None

    property = qbuff1 = None

    property_list, Property = create_model("Property", {"prop_nr":int, "prop_nm":str, "prop_loc":int, "prop_loc_nm":str, "prop_zinr":str, "prop_selected":bool, "str":str})

    Qbuff1 = Eg_property

    db_session = local_storage.db_session

    def generate_output():
        nonlocal property_list, eg_property, eg_maintain, eg_location
        nonlocal qbuff1


        nonlocal property, qbuff1
        nonlocal property_list
        return {"property": property_list}

    def prop():

        nonlocal property_list, eg_property, eg_maintain, eg_location
        nonlocal qbuff1


        nonlocal property, qbuff1
        nonlocal property_list

        i:int = 0
        a:int = 0
        loc_nm:str = ""
        Qbuff1 = Eg_property
        property_list.clear()

        eg_maintain = db_session.query(Eg_maintain).filter(
                (Eg_maintain.maintainnr == maintain_nr)).first()

        if eg_maintain:
            i = eg_maintain.propertynr

            eg_property = db_session.query(Eg_property).filter(
                    (Eg_property.nr == eg_maintain.propertynr)).first()

            if eg_property:
                a = eg_property.maintask

            for eg_property in db_session.query(Eg_property).filter(
                    (Eg_property.maintask == a) &  (Eg_property.nr != i)).all():

                eg_location = db_session.query(Eg_location).filter(
                        (Eg_location.nr == eg_property.location)).first()

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
                property.prop_SELECTED = False


    prop()

    return generate_output()