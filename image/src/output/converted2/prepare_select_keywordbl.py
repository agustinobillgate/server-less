#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal

def prepare_select_keywordbl():
    str_list_list = []

    str_list = None

    str_list_list, Str_list = create_model("Str_list", {"nr":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal str_list_list


        nonlocal str_list
        nonlocal str_list_list

        return {"str-list": str_list_list}

    str_list = query(str_list_list, first=True)

    if not str_list:
        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 1
        str_list.bezeich = "Total Room"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 2
        str_list.bezeich = "Rooms Available"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 3
        str_list.bezeich = "Rooms Occupied"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 4
        str_list.bezeich = "House Uses"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 5
        str_list.bezeich = "Complimentary Room"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 6
        str_list.bezeich = "Paying Room"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 7
        str_list.bezeich = "OOO Room"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 8
        str_list.bezeich = "Complimentary Paying Guest"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 9
        str_list.bezeich = "Room Sold"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 10
        str_list.bezeich = "Vacant Rooms"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 11
        str_list.bezeich = "% Occupancy"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 12
        str_list.bezeich = "% Occupancy with Comp and HU"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 13
        str_list.bezeich = "Person In House"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 14
        str_list.bezeich = "Out of Order Rooms"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 15
        str_list.bezeich = "Average Room Rate Rp"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 16
        str_list.bezeich = "Average Room Rate Foreign"


        str_list = Str_list()
        str_list_list.append(str_list)

        str_list.nr = 17
        str_list.bezeich = "RevPar"

    return generate_output()