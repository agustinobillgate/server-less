#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest

def arl_list_btn_gcfbl(t_gastnrmember:int, ext_char:string):

    prepare_cache ([Guest])

    progname = ""
    t_gastnr = 0
    guest = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal progname, t_gastnr, guest
        nonlocal t_gastnrmember, ext_char

        return {"progname": progname, "t_gastnr": t_gastnr}


    guest = get_cache (Guest, {"gastnr": [(eq, t_gastnrmember)]})
    progname = "chg-gcf" + ext_char + to_string(guest.karteityp) + "UI.p"
    t_gastnr = guest.gastnr

    return generate_output()