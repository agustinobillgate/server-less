from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Htparam, Nation, Genlayout, Queasy

def prepare_mk_gcf0bl(lastname:str, firstname:str):
    read_birthdate = False
    err_nr = 0
    def_natcode = ""
    curr_gastnr = 0
    nation1 = ""
    land = ""
    lname = ""
    fname = ""
    f_logical = False
    f_logical1 = False
    htparam_feldtyp = 0
    htparam_flogical = False
    avail_genlayout = False
    avail_queasy = False
    l_param472 = False
    t_nation1_list = []
    t_nation2_list = []
    t_nation3_list = []
    t_guest_list = []
    guest = htparam = nation = genlayout = queasy = None

    t_guest = t_nation1 = t_nation2 = t_nation3 = None

    t_guest_list, T_guest = create_model_like(Guest)
    t_nation1_list, T_nation1 = create_model("T_nation1", {"kurzbez":str})
    t_nation2_list, T_nation2 = create_model_like(T_nation1)
    t_nation3_list, T_nation3 = create_model_like(T_nation1)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal read_birthdate, err_nr, def_natcode, curr_gastnr, nation1, land, lname, fname, f_logical, f_logical1, htparam_feldtyp, htparam_flogical, avail_genlayout, avail_queasy, l_param472, t_nation1_list, t_nation2_list, t_nation3_list, t_guest_list, guest, htparam, nation, genlayout, queasy


        nonlocal t_guest, t_nation1, t_nation2, t_nation3
        nonlocal t_guest_list, t_nation1_list, t_nation2_list, t_nation3_list
        return {"read_birthdate": read_birthdate, "err_nr": err_nr, "def_natcode": def_natcode, "curr_gastnr": curr_gastnr, "nation1": nation1, "land": land, "lname": lname, "fname": fname, "f_logical": f_logical, "f_logical1": f_logical1, "htparam_feldtyp": htparam_feldtyp, "htparam_flogical": htparam_flogical, "avail_genlayout": avail_genlayout, "avail_queasy": avail_queasy, "l_param472": l_param472, "t-nation1": t_nation1_list, "t-nation2": t_nation2_list, "t-nation3": t_nation3_list, "t-guest": t_guest_list}


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 937)).first()
    read_birthdate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 153)).first()

    nation = db_session.query(Nation).filter(
            (Nation.kurzbez == htparam.fchar)).first()

    if not nation:
        err_nr = 1

        return generate_output()
    def_natcode = nation.kurzbez
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
        err_nr = 2

        return generate_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 472)).first()

    if htparam.paramgruppe == 99 and htparam.feldtyp == 4:
        l_param472 = htparam.flogical


    guest = Guest()
    db_session.add(guest)

    guest.karteityp = 0
    guest.name = ""
    guest.vornamekind[0] = ""
    guest.gastnr = curr_gastnr

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 153)).first()
    nation1 = htparam.fchar
    land = htparam.fchar
    lname = lastname
    fname = firstname
    lname = substring(lname, 0, 1).upper() +\
            substring(lname, 1, len(lname))
    fname = substring(fname, 0, 1).upper() +\
            substring(fname, 1, len(fname))

    guest = db_session.query(Guest).first()
    t_guest = T_guest()
    t_guest_list.append(t_guest)

    buffer_copy(guest, t_guest)

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 223)).first()

    if htparam:
        f_logical = True

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 939)).first()

    if htparam:
        f_logical1 = True

    for nation in db_session.query(Nation).filter(
            (Nation.natcode == 0)).all():
        t_nation1 = T_nation1()
        t_nation1_list.append(t_nation1)

        t_nation1.kurzbez = nation.kurzbez

    for nation in db_session.query(Nation).filter(
            (Nation.natcode > 0)).all():
        t_nation2 = T_nation2()
        t_nation2_list.append(t_nation2)

        t_nation2.kurzbez = nation.kurzbez

    for nation in db_session.query(Nation).all():
        t_nation3 = T_nation3()
        t_nation3_list.append(t_nation3)

        t_nation3.kurzbez = nation.kurzbez

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 961)).first()
    htparam_feldtyp = htparam.feldtyp
    htparam_flogical = htparam.flogical

    genlayout = db_session.query(Genlayout).filter(
            (func.lower(Genlayout.key) == "Guest Card")).first()

    if genlayout:
        avail_genlayout = True

    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 27)).first()

    if queasy:
        avail_queasy = True

    return generate_output()