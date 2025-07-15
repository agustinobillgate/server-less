from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Htparam, Sourccod, Nation, Genlayout

def prepare_mk_gcf2_1bl(lastname:str, firstname:str):
    err_nr = 0
    curr_gastnr = 0
    lname = ""
    f_logical = False
    avail_genlayout = False
    refno_label = ""
    t_guest_list = []
    t_sourccod1_list = []
    t_nation1_list = []
    guest = htparam = sourccod = nation = genlayout = None

    t_nation1 = t_guest = t_sourccod1 = None

    t_nation1_list, T_nation1 = create_model("T_nation1", {"kurzbez":str})
    t_guest_list, T_guest = create_model_like(Guest)
    t_sourccod1_list, T_sourccod1 = create_model("T_sourccod1", {"source_code":int, "bezeich":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal err_nr, curr_gastnr, lname, f_logical, avail_genlayout, refno_label, t_guest_list, t_sourccod1_list, t_nation1_list, guest, htparam, sourccod, nation, genlayout
        nonlocal lastname, firstname


        nonlocal t_nation1, t_guest, t_sourccod1
        nonlocal t_nation1_list, t_guest_list, t_sourccod1_list
        return {"err_nr": err_nr, "curr_gastnr": curr_gastnr, "lname": lname, "f_logical": f_logical, "avail_genlayout": avail_genlayout, "refno_label": refno_label, "t-guest": t_guest_list, "t-sourccod1": t_sourccod1_list, "t-nation1": t_nation1_list}


    curr_gastnr = 0

    guest = db_session.query(Guest).filter(
            (Guest.gastnr < 0)).first()

    if guest:
        curr_gastnr = - guest.gastnr
        db_session.delete(guest)
        pass

        guest = db_session.query(Guest).filter(
                (Guest.gastnr == curr_gastnr)).first()

        if guest:
            curr_gastnr = 0

    if curr_gastnr == 0:

        guest = db_session.query(Guest).filter(
                (Guest.gastnr != None)).order_by(Guest._recid.desc()).first()

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

    guest.karteityp = 2
    guest.gastnr = curr_gastnr
    lname = lastname
    guest.anredefirma = firstname


    lname = substring(lname, 0, 1).upper() + substring(lname, 1, len(lname))
    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 223)).first()

    if not htparam.flogical:
        f_logical = False

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 1356)).first()

    if htparam:
        refno_label = htparam.fchar

    for sourccod in db_session.query(Sourccod).filter(
            (Sourccod.betriebsnr == 0) &  (Sourccod.source_code != guest.segment3)).order_by(Sourccod.source_code).all():
        t_sourccod1 = T_sourccod1()
        t_sourccod1_list.append(t_sourccod1)

        t_sourccod1.source_code = sourccod.source_code
        t_sourccod1.bezeich = sourccod.bezeich

    for nation in db_session.query(Nation).order_by(Nation._recid).all():
        t_nation1 = T_nation1()
        t_nation1_list.append(t_nation1)

        t_nation1.kurzbez = nation.kurzbez

    genlayout = db_session.query(Genlayout).filter(
            (func.lower(Genlayout.key) == ("Guest Card").lower())).first()

    if genlayout:
        avail_genlayout = True

    return generate_output()