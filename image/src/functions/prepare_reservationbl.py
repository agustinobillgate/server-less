from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.htpchar import htpchar
from functions.htpdate import htpdate
from models import Guest

def prepare_reservationbl(gastno:int):
    i_param297 = 0
    i_cardtype = 0
    ext_char = ""
    ci_date = None
    t_guest_list = []
    guest = None

    t_guest = None

    t_guest_list, T_guest = create_model_like(Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i_param297, i_cardtype, ext_char, ci_date, t_guest_list, guest


        nonlocal t_guest
        nonlocal t_guest_list
        return {"i_param297": i_param297, "i_cardtype": i_cardtype, "ext_char": ext_char, "ci_date": ci_date, "t-guest": t_guest_list}


    i_param297 = get_output(htpint(297))
    ext_char = get_output(htpchar(148))
    ci_date = get_output(htpdate(87))

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastno)).first()
    i_cardtype = guest.karteityp


    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)

    return generate_output()