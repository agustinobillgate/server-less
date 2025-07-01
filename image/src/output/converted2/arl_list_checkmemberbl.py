#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Mc_guest, Guest, Htparam

def arl_list_checkmemberbl(gast_no:int):

    prepare_cache ([Guest, Htparam])

    email = ""
    member_exist = False
    loyalty_name = ""
    mc_guest = guest = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal email, member_exist, loyalty_name, mc_guest, guest, htparam
        nonlocal gast_no

        return {"email": email, "member_exist": member_exist, "loyalty_name": loyalty_name}


    mc_guest = db_session.query(Mc_guest).filter(
             (Mc_guest.gastnr == gast_no) & (Mc_guest.activeflag)).first()

    if mc_guest:
        member_exist = True

    guest = get_cache (Guest, {"gastnr": [(eq, gast_no)]})

    if guest:
        email = guest.email_adr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 787)]})

    if htparam:
        loyalty_name = entry(0, htparam.fchar, "-")

    return generate_output()