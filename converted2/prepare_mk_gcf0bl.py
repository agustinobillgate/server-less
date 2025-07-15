#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Htparam, Nation, Genlayout, Queasy

def prepare_mk_gcf0bl(lastname:string, firstname:string):

    prepare_cache ([Htparam, Nation])

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
    t_nation1_data = []
    t_nation2_data = []
    t_nation3_data = []
    t_guest_data = []
    guest = htparam = nation = genlayout = queasy = None

    t_guest = t_nation1 = t_nation2 = t_nation3 = None

    t_guest_data, T_guest = create_model_like(Guest)
    t_nation1_data, T_nation1 = create_model("T_nation1", {"kurzbez":string})
    t_nation2_data, T_nation2 = create_model_like(T_nation1)
    t_nation3_data, T_nation3 = create_model_like(T_nation1)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal read_birthdate, err_nr, def_natcode, curr_gastnr, nation1, land, lname, fname, f_logical, f_logical1, htparam_feldtyp, htparam_flogical, avail_genlayout, avail_queasy, l_param472, t_nation1_data, t_nation2_data, t_nation3_data, t_guest_data, guest, htparam, nation, genlayout, queasy
        nonlocal lastname, firstname


        nonlocal t_guest, t_nation1, t_nation2, t_nation3
        nonlocal t_guest_data, t_nation1_data, t_nation2_data, t_nation3_data

        return {"read_birthdate": read_birthdate, "err_nr": err_nr, "def_natcode": def_natcode, "curr_gastnr": curr_gastnr, "nation1": nation1, "land": land, "lname": lname, "fname": fname, "f_logical": f_logical, "f_logical1": f_logical1, "htparam_feldtyp": htparam_feldtyp, "htparam_flogical": htparam_flogical, "avail_genlayout": avail_genlayout, "avail_queasy": avail_queasy, "l_param472": l_param472, "t-nation1": t_nation1_data, "t-nation2": t_nation2_data, "t-nation3": t_nation3_data, "t-guest": t_guest_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 937)]})
    read_birthdate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})

    nation = get_cache (Nation, {"kurzbez": [(eq, htparam.fchar)]})

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
        err_nr = 2

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 472)]})

    if htparam.paramgruppe == 99 and htparam.feldtyp == 4:
        l_param472 = htparam.flogical


    guest = Guest()
    db_session.add(guest)

    guest.karteityp = 0
    guest.name = ""
    guest.vornamekind[0] = ""
    guest.gastnr = curr_gastnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})
    nation1 = htparam.fchar
    land = htparam.fchar
    lname = lastname
    fname = firstname
    lname = substring(lname, 0, 1).upper() +\
            substring(lname, 1, length(lname))
    fname = substring(fname, 0, 1).upper() +\
            substring(fname, 1, length(fname))


    pass
    t_guest = T_guest()
    t_guest_data.append(t_guest)

    buffer_copy(guest, t_guest)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 223)]})

    if htparam:
        f_logical = True

    htparam = get_cache (Htparam, {"paramnr": [(eq, 939)]})

    if htparam:
        f_logical1 = True

    for nation in db_session.query(Nation).filter(
             (Nation.natcode == 0)).order_by(Nation._recid).all():
        t_nation1 = T_nation1()
        t_nation1_data.append(t_nation1)

        t_nation1.kurzbez = nation.kurzbez

    for nation in db_session.query(Nation).filter(
             (Nation.natcode > 0)).order_by(Nation._recid).all():
        t_nation2 = T_nation2()
        t_nation2_data.append(t_nation2)

        t_nation2.kurzbez = nation.kurzbez

    for nation in db_session.query(Nation).order_by(Nation._recid).all():
        t_nation3 = T_nation3()
        t_nation3_data.append(t_nation3)

        t_nation3.kurzbez = nation.kurzbez

    htparam = get_cache (Htparam, {"paramnr": [(eq, 961)]})
    htparam_feldtyp = htparam.feldtyp
    htparam_flogical = htparam.flogical

    genlayout = get_cache (Genlayout, {"key": [(eq, "guest card")]})

    if genlayout:
        avail_genlayout = True

    queasy = get_cache (Queasy, {"key": [(eq, 27)]})

    if queasy:
        avail_queasy = True

    return generate_output()