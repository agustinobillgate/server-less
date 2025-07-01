#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Htparam, Sourccod, Genlayout, Nation

def prepare_mk_gcf1_1bl(lastname:string, firstname:string):

    prepare_cache ([Htparam, Sourccod, Nation])

    err_nr = 0
    curr_gastnr = 0
    lname = ""
    f_logical = False
    avail_genlayout = False
    refno_label = ""
    t_nation1_list = []
    t_sourccod1_list = []
    t_guest_list = []
    guest = htparam = sourccod = genlayout = nation = None

    t_nation1 = t_guest = t_sourccod1 = None

    t_nation1_list, T_nation1 = create_model("T_nation1", {"kurzbez":string})
    t_guest_list, T_guest = create_model_like(Guest)
    t_sourccod1_list, T_sourccod1 = create_model("T_sourccod1", {"source_code":int, "bezeich":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_nr, curr_gastnr, lname, f_logical, avail_genlayout, refno_label, t_nation1_list, t_sourccod1_list, t_guest_list, guest, htparam, sourccod, genlayout, nation
        nonlocal lastname, firstname


        nonlocal t_nation1, t_guest, t_sourccod1
        nonlocal t_nation1_list, t_guest_list, t_sourccod1_list

        return {"err_nr": err_nr, "curr_gastnr": curr_gastnr, "lname": lname, "f_logical": f_logical, "avail_genlayout": avail_genlayout, "refno_label": refno_label, "t-nation1": t_nation1_list, "t-sourccod1": t_sourccod1_list, "t-guest": t_guest_list}


    curr_gastnr = 0

    guest = db_session.query(Guest).filter(
             (Guest.gastnr < 0)).first()

    if guest:
        curr_gastnr = - guest.gastnr
        db_session.delete(guest)

        guest = get_cache (Guest, {"gastnr": [(eq, curr_gastnr)]})

        if guest:
            curr_gastnr = 0

    if curr_gastnr == 0:

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr != None)).order_by(Guest._recid.desc()).first()

        if guest:
            curr_gastnr = guest.gastnr + 1
        else:
            curr_gastnr = 1

    htparam = get_cache (Htparam, {"paramnr": [(eq, 999)]})

    if htparam.flogical  and curr_gastnr > 300:
        err_nr = 1

        return generate_output()
    guest = Guest()
    db_session.add(guest)

    guest.karteityp = 1
    guest.gastnr = curr_gastnr


    lname = lastname
    guest.anredefirma = firstname
    lname = substring(lname, 0, 1).upper() + substring(lname, 1, length(lname))
    pass
    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 223)]})
    f_logical = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1356)]})

    if htparam:
        refno_label = htparam.fchar

    for sourccod in db_session.query(Sourccod).filter(
             (Sourccod.betriebsnr == 0) & (Sourccod.source_code != guest.segment3)).order_by(Sourccod.source_code).all():
        t_sourccod1 = T_sourccod1()
        t_sourccod1_list.append(t_sourccod1)

        t_sourccod1.source_code = sourccod.source_code
        t_sourccod1.bezeich = sourccod.bezeich

    genlayout = get_cache (Genlayout, {"key": [(eq, "guest card")]})

    if genlayout:
        avail_genlayout = True

    for nation in db_session.query(Nation).order_by(Nation._recid).all():
        t_nation1 = T_nation1()
        t_nation1_list.append(t_nation1)

        t_nation1.kurzbez = nation.kurzbez

    return generate_output()