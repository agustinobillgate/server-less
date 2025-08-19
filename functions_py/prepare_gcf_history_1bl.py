#using conversion tools version: 1.0.0.118

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Htparam

def prepare_gcf_history_1bl(gastnr:int):

    prepare_cache ([Guest, Htparam])

    fdate = None
    t_tittle = ""
    ip_port = ""
    guest_phone = ""
    guest_name = ""
    guest_email = ""
    guest = htparam = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal fdate, t_tittle, ip_port, guest_phone, guest_name, guest_email, guest, htparam
        nonlocal gastnr

        return {"fdate": fdate, "t_tittle": t_tittle, "ip_port": ip_port, "guest_phone": guest_phone, "guest_name": guest_name, "guest_email": guest_email}


    guest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})

    if guest:
        t_tittle = t_tittle + " - " + (guest.name + ", " + guest.vorname1 + guest.anredefirma)
        guest_email = guest.email_adr
        guest_name = guest.name

        if guest.mobil_telefon == "" or guest.mobil_telefon == None:
            guest_phone = guest.telefon


        else:
            guest_phone = guest.mobil_telefon

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        fdate = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1343)]})

    if htparam:

        if htparam.fchar != "" and htparam.fchar != None:

            if num_entries(htparam.fchar, ":") > 1:
                ip_port = htparam.fchar

    return generate_output()