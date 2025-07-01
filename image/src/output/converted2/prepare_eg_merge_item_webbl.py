#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Eg_property, Eg_location, Queasy

def prepare_eg_merge_item_webbl(item_nr:int):

    prepare_cache ([Eg_location, Queasy])

    merge_list_list = []
    object_no:int = 0
    loc_no:int = 0
    room_no:string = ""
    eg_property = eg_location = queasy = None

    merge_list = None

    merge_list_list, Merge_list = create_model_like(Eg_property, {"object_nm":string, "loc_nm":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal merge_list_list, object_no, loc_no, room_no, eg_property, eg_location, queasy
        nonlocal item_nr


        nonlocal merge_list
        nonlocal merge_list_list

        return {"merge-list": merge_list_list}

    eg_property = get_cache (Eg_property, {"nr": [(eq, item_nr)]})

    if eg_property:
        object_no = eg_property.maintask
        loc_no = eg_property.location
        room_no = eg_property.zinr

    for eg_property in db_session.query(Eg_property).filter(
             (Eg_property.nr != item_nr) & (Eg_property.maintask == object_no) & (Eg_property.location == loc_no) & (Eg_property.zinr == (room_no).lower())).order_by(Eg_property._recid).all():
        merge_list = Merge_list()
        merge_list_list.append(merge_list)

        buffer_copy(eg_property, merge_list)

        eg_location = get_cache (Eg_location, {"nr": [(eq, eg_property.location)]})

        if eg_location:
            merge_list.loc_nm = eg_location.bezeich

        queasy = get_cache (Queasy, {"key": [(eq, 133)],"number1": [(eq, eg_property.maintask)]})

        if queasy:
            merge_list.object_nm = queasy.char1

    return generate_output()