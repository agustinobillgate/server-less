from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Htparam, Sourccod, Genlayout, Nation

def prepare_mk_gcf1bl(lastname:str, firstname:str):
    err_nr = 0
    curr_gastnr = 0
    lname = ""
    f_logical = False
    avail_genlayout = False
    t_nation1_list = []
    t_sourccod1_list = []
    t_guest_list = []
    guest = htparam = sourccod = genlayout = nation = None

    t_nation1 = t_guest = t_sourccod1 = None

    t_nation1_list, T_nation1 = create_model("T_nation1", {"kurzbez":str})
    t_guest_list, T_guest = create_model_like(Guest)
    t_sourccod1_list, T_sourccod1 = create_model("T_sourccod1", {"source_code":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_nr, curr_gastnr, lname, f_logical, avail_genlayout, t_nation1_list, t_sourccod1_list, t_guest_list, guest, htparam, sourccod, genlayout, nation


        nonlocal t_nation1, t_guest, t_sourccod1
        nonlocal t_nation1_list, t_guest_list, t_sourccod1_list
        return {"err_nr": err_nr, "curr_gastnr": curr_gastnr, "lname": lname, "f_logical": f_logical, "avail_genlayout": avail_genlayout, "t-nation1": t_nation1_list, "t-sourccod1": t_sourccod1_list, "t-guest": t_guest_list}


    curr_gastnr = 0

    guest = db_session.query(Guest).filter(
            (Guest.gastnr < 0)).first()

    if guest:
        curr_gastnr = - guest.gastnr
        db_session.delete(guest)

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == curr_gastnr)).first()

        if guest:
            curr_gastnr = 0

    if curr_gastnr == 0:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr != None)).first()

        if guest:
            curr_gastnr = guest.gastnr + 1
        else:
            curr_gastnr = 1

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 999)).first()

    if htparam.flogical  and curr_gastnr > 300:
        err_nr = 1

        return generate_output()
    guest = Guest()
    db_session.add(guest)

    guest.karteityp = 1
    guest.gastnr = curr_gastnr


    lname = lastname
    guest.anredefirma = firstname
    lname = substring(lname, 0, 1).upper() + substring(lname, 1, len(lname))

    guest = db_session.query(Guest).first()
    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 223)).first()
    f_logical = htparam.flogical

    for sourccod in db_session.query(Sourccod).filter(
            (Sourccod.betriebsnr == 0) &  (Sourccod.source_code != guest.segment3)).all():
        t_sourccod1 = T_sourccod1()
        t_sourccod1_list.append(t_sourccod1)

        t_sourccod1.source_code = sourccod.source_code
        t_sourccod1.bezeich = sourccod.bezeich

    genlayout = db_session.query(Genlayout).filter(
            (func.lower(Genlayout.key) == "Guest Card")).first()

    if genlayout:
        avail_genlayout = True

    for nation in db_session.query(Nation).all():
        t_nation1 = T_nation1()
        t_nation1_list.append(t_nation1)

        t_nation1.kurzbez = nation.kurzbez

    return generate_output()