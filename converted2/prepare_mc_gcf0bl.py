#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Mc_guest, Mc_types, Htparam, Guest, Mc_fee

def prepare_mc_gcf0bl(pvilanguage:int, gastno:int):

    prepare_cache ([Htparam, Guest, Mc_fee])

    ci_date = None
    card_exist = False
    f_tittle = ""
    bezeich = ""
    last_paydate = None
    gname = ""
    g_list_data = []
    t_mc_guest_data = []
    t_mc_types_data = []
    lvcarea:string = "mc-gcf"
    mc_guest = mc_types = htparam = guest = mc_fee = None

    g_list = t_mc_guest = t_mc_types = None

    g_list_data, G_list = create_model_like(Mc_guest)
    t_mc_guest_data, T_mc_guest = create_model_like(Mc_guest)
    t_mc_types_data, T_mc_types = create_model_like(Mc_types)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, card_exist, f_tittle, bezeich, last_paydate, gname, g_list_data, t_mc_guest_data, t_mc_types_data, lvcarea, mc_guest, mc_types, htparam, guest, mc_fee
        nonlocal pvilanguage, gastno


        nonlocal g_list, t_mc_guest, t_mc_types
        nonlocal g_list_data, t_mc_guest_data, t_mc_types_data

        return {"ci_date": ci_date, "card_exist": card_exist, "f_tittle": f_tittle, "bezeich": bezeich, "last_paydate": last_paydate, "gname": gname, "g-list": g_list_data, "t-mc-guest": t_mc_guest_data, "t-mc-types": t_mc_types_data}

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})
    gname = guest.name + ", " + guest.vorname1 +\
            " " + guest.anrede1

    mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gastno)]})
    card_exist = None != mc_guest

    if mc_guest:
        t_mc_guest = T_mc_guest()
        t_mc_guest_data.append(t_mc_guest)

        buffer_copy(mc_guest, t_mc_guest)
    f_tittle = translateExtended ("Card's Member", lvcarea, "") + " - " + guest.name + " " + guest.vorname1 + ", " + guest.anrede1

    if card_exist:

        mc_types = get_cache (Mc_types, {"nr": [(eq, mc_guest.nr)]})

        if mc_types:
            t_mc_types = T_mc_types()
            t_mc_types_data.append(t_mc_types)

            buffer_copy(mc_types, t_mc_types)
            bezeich = mc_types.bezeich
        g_list = G_list()
        g_list_data.append(g_list)

        buffer_copy(mc_guest, g_list)

    if card_exist:

        mc_fee = get_cache (Mc_fee, {"gastnr": [(eq, gastno)],"bis_datum": [(eq, mc_guest.tdate)]})

        if mc_fee:
            last_paydate = mc_fee.bez_datum

    return generate_output()