#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal

def prepare_new_drrbl():
    menu_drr_data = []

    menu_drr = None

    menu_drr_data, Menu_drr = create_model("Menu_drr", {"nr":int, "descr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal menu_drr_data


        nonlocal menu_drr
        nonlocal menu_drr_data

        return {"menu-drr": menu_drr_data}

    menu_drr = query(menu_drr_data, first=True)

    if not menu_drr:
        menu_drr = Menu_drr()
        menu_drr_data.append(menu_drr)

        menu_drr.nr = 1
        menu_drr.descr = "STATISTIC"


        menu_drr = Menu_drr()
        menu_drr_data.append(menu_drr)

        menu_drr.nr = 2
        menu_drr.descr = "REVENUE BY SEGMENT"


        menu_drr = Menu_drr()
        menu_drr_data.append(menu_drr)

        menu_drr.nr = 3
        menu_drr.descr = "REVENUE"


        menu_drr = Menu_drr()
        menu_drr_data.append(menu_drr)

        menu_drr.nr = 4
        menu_drr.descr = "PAYABLE"


        menu_drr = Menu_drr()
        menu_drr_data.append(menu_drr)

        menu_drr.nr = 5
        menu_drr.descr = "PAYMENT"


        menu_drr = Menu_drr()
        menu_drr_data.append(menu_drr)

        menu_drr.nr = 6
        menu_drr.descr = "GUEST LEDGER"


        menu_drr = Menu_drr()
        menu_drr_data.append(menu_drr)

        menu_drr.nr = 7
        menu_drr.descr = "FB SALES BY SHIFT"

    return generate_output()