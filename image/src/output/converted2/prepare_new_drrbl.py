from functions.additional_functions import *
import decimal

def prepare_new_drrbl():
    menu_drr_list = []

    menu_drr = None

    menu_drr_list, Menu_drr = create_model("Menu_drr", {"nr":int, "descr":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal menu_drr_list


        nonlocal menu_drr
        nonlocal menu_drr_list

        return {"menu-drr": menu_drr_list}

    menu_drr = query(menu_drr_list, first=True)

    if not menu_drr:
        menu_drr = Menu_drr()
        menu_drr_list.append(menu_drr)

        menu_drr.nr = 1
        menu_drr.descr = "STATISTIC"


        menu_drr = Menu_drr()
        menu_drr_list.append(menu_drr)

        menu_drr.nr = 2
        menu_drr.descr = "REVENUE BY SEGMENT"


        menu_drr = Menu_drr()
        menu_drr_list.append(menu_drr)

        menu_drr.nr = 3
        menu_drr.descr = "REVENUE"


        menu_drr = Menu_drr()
        menu_drr_list.append(menu_drr)

        menu_drr.nr = 4
        menu_drr.descr = "PAYABLE"


        menu_drr = Menu_drr()
        menu_drr_list.append(menu_drr)

        menu_drr.nr = 5
        menu_drr.descr = "PAYMENT"


        menu_drr = Menu_drr()
        menu_drr_list.append(menu_drr)

        menu_drr.nr = 6
        menu_drr.descr = "GUEST LEDGER"


        menu_drr = Menu_drr()
        menu_drr_list.append(menu_drr)

        menu_drr.nr = 7
        menu_drr.descr = "FB SALES BY SHIFT"

    return generate_output()