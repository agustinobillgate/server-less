from functions.additional_functions import *
import decimal
from functions.read_guestbl import read_guestbl
from models import Guest

def prepare_clear_aktline_webbl(akt_line_gastnr:int, akt_line_bemerk:str):
    lname = ""
    comment = ""
    zeit = ""
    guest = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lname, comment, zeit, guest


        nonlocal t_guest
        nonlocal t_guest_list
        return {"lname": lname, "comment": comment, "zeit": zeit}


    t_guest_list = get_output(read_guestbl(1, akt_line_gastnr, "", ""))

    t_guest = query(t_guest_list, first=True)

    if t_guest:
        lname = t_guest.name + ", " + t_guest.anredefirma
        akt_line_gastnr = t_guest.gastnr
    else:
        lname = ""
    comment = akt_line_bemerk
    zeit = to_string(get_current_time_in_seconds(), "HH:MM")

    return generate_output()