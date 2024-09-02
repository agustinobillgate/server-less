from functions.additional_functions import *
import decimal
from datetime import date
from models import Mc_guest, Mc_types, Htparam, Guest, Mc_fee

def prepare_mc_gcf0bl(pvilanguage:int, gastno:int):
    ci_date = None
    card_exist = False
    f_tittle = ""
    bezeich = ""
    last_paydate = None
    gname = ""
    g_list_list = []
    t_mc_guest_list = []
    t_mc_types_list = []
    lvcarea:str = "mc_gcf"
    mc_guest = mc_types = htparam = guest = mc_fee = None

    g_list = t_mc_guest = t_mc_types = None

    g_list_list, G_list = create_model_like(Mc_guest)
    t_mc_guest_list, T_mc_guest = create_model_like(Mc_guest)
    t_mc_types_list, T_mc_types = create_model_like(Mc_types)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, card_exist, f_tittle, bezeich, last_paydate, gname, g_list_list, t_mc_guest_list, t_mc_types_list, lvcarea, mc_guest, mc_types, htparam, guest, mc_fee
        nonlocal g_list, t_mc_guest, t_mc_types
        nonlocal g_list_list, t_mc_guest_list, t_mc_types_list
        return {"ci_date": ci_date, "card_exist": card_exist, "f_tittle": f_tittle, "bezeich": bezeich, "last_paydate": last_paydate, "gname": gname, "g-list": g_list_list, "t-mc-guest": t_mc_guest_list, "t-mc-types": t_mc_types_list}

    htparam = db_session.query(Htparam).filter((Htparam.paramnr == 87)).first()
    if htparam:
        ci_date = htparam.fdate
        local_storage.debugging = local_storage.debugging + "-fdate:" + str(ci_date)

    guest = db_session.query(Guest).filter((Guest.gastnr == gastno)).first()
    if guest:
        gname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
        local_storage.debugging = local_storage.debugging + "-Name:" + gname

    mc_guest = db_session.query(Mc_guest).filter((Mc_guest.gastnr == gastno)).first()
    if mc_guest:
         card_exist = True
         
    local_storage.debugging = local_storage.debugging + "-Card:" + str(card_exist)
    if mc_guest:
        local_storage.debugging = local_storage.debugging + "-mc_guest:ada" 
        card_exist = True
        t_mc_guest = T_mc_guest()
        t_mc_guest_list.append(t_mc_guest)
        buffer_copy(mc_guest, t_mc_guest)

# #     f_tittle = translateExtended ("Card's Member", lvcarea, "") + " - " + guest.name + " " + guest.vorname1 + ", " + guest.anrede1

        f_tittle = "Card's Member" + " - " + guest.name + " " + guest.vorname1 + ", " + guest.anrede1

        local_storage.debugging = local_storage.debugging + "-Card:" + str(card_exist)
    
    if card_exist:
        mc_types = db_session.query(Mc_types).filter((Mc_types.nr == mc_guest.nr)).first()

        if mc_types:
            t_mc_types = T_mc_types()
            t_mc_types_list.append(t_mc_types)

            buffer_copy(mc_types, t_mc_types)
            bezeich = mc_types.bezeich
        g_list = G_list()
        g_list_list.append(g_list)

        buffer_copy(mc_guest, g_list)

    if card_exist:
        mc_fee = db_session.query(Mc_fee).filter(
                (Mc_fee.gastnr == gastno) &  (Mc_fee.bis_datum == mc_guest.tdate)).first()

        if mc_fee:
            last_paydate = mc_fee.bez_datum

    return generate_output()