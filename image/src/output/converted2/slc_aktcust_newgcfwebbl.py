#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.new_gcfnrbl import new_gcfnrbl
from models import Guest

def slc_aktcust_newgcfwebbl(gname:string, user_init:string, sorttype:int):
    gastnr = 0
    t_guest_list = []
    curr_gastnr:int = 0
    del_gastnr:int = 0
    dd:int = 0
    mm:int = 0
    yy:int = 0
    len_:int = 0
    fullfname:string = None
    province:string = ""
    city:string = ""
    succes_flag:bool = False
    guest = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal gastnr, t_guest_list, curr_gastnr, del_gastnr, dd, mm, yy, len_, fullfname, province, city, succes_flag, guest
        nonlocal gname, user_init, sorttype


        nonlocal t_guest
        nonlocal t_guest_list

        return {"gastnr": gastnr, "t-guest": t_guest_list}


    curr_gastnr = get_output(new_gcfnrbl())
    t_guest = T_guest()
    t_guest_list.append(t_guest)

    t_guest.gastnr = curr_gastnr
    t_guest.name = gname
    t_guest.char1 = user_init
    t_guest.karteityp = sorttype
    t_guest.phonetik3 = user_init


    gastnr = t_guest.gastnr

    return generate_output()