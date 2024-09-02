from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Eg_property, Eg_location, Queasy

def prepare_eg_merge_item_webbl(item_nr:int):
    merge_list_list = []
    object_no:int = 0
    loc_no:int = 0
    room_no:str = ""
    eg_property = eg_location = queasy = None

    merge_list = None

    merge_list_list, Merge_list = create_model_like(Eg_property, {"object_nm":str, "loc_nm":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal merge_list_list, object_no, loc_no, room_no, eg_property, eg_location, queasy


        nonlocal merge_list
        nonlocal merge_list_list
        return {"merge-list": merge_list_list}

    eg_property = db_session.query(Eg_property).filter(
            (Eg_property.nr == item_nr)).first()

    if eg_property:
        object_no = eg_property.maintask
        loc_no = eg_property.location
        room_no = eg_property.zinr

    for eg_property in db_session.query(Eg_property).filter(
            (Eg_property.nr != item_nr) &  (Eg_property.maintask == object_no) &  (Eg_property.location == loc_no) &  (func.lower(Eg_property.zinr) == (room_no).lower())).all():
        merge_list = Merge_list()
        merge_list_list.append(merge_list)

        buffer_copy(eg_property, merge_list)

        eg_location = db_session.query(Eg_location).filter(
                (Eg_location.nr == eg_property.location)).first()

        if eg_location:
            merge_list.loc_nm = eg_location.bezeich

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 133) &  (Queasy.number1 == eg_property.maintask)).first()

        if queasy:
            merge_list.object_nm = queasy.char1

    return generate_output()