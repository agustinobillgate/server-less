#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.read_guestbl import read_guestbl
from models import Guest

def prepare_clear_aktline_webbl(akt_line_gastnr:int, akt_line_bemerk:string):
    lname = ""
    comment = ""
    zeit = ""
    guest = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lname, comment, zeit, guest
        nonlocal akt_line_gastnr, akt_line_bemerk


        nonlocal t_guest
        nonlocal t_guest_list

        return {"akt_line_gastnr": akt_line_gastnr, "lname": lname, "comment": comment, "zeit": zeit}


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