#using conversion tools version: 1.0.0.117

# ==========================================
# Rulita, 26-11-2025
# - Added with_for_update all query 
# ==========================================

from functions.additional_functions import *
from decimal import Decimal
from functions.update_gcfname import update_gcfname
from functions.intevent_1 import intevent_1
from models import Guest, Htparam, Bediener, Nation, Guestseg, Akt_cust, Res_history, Res_line

t_guest_data, T_guest = create_model_like(Guest)

def gcf_btn_gobl(icase:int, pvilanguage:int, user_init:string, t_guest_data:[T_guest]):

    prepare_cache ([Guest, Htparam, Bediener, Nation, Res_history])

    msg_str = ""
    error_number = 0
    gastno:int = 0
    def_natcode:string = ""
    name_changed:bool = False
    zugriff:bool = False
    priscilla_active:bool = True
    lvcarea:string = "chg-gcf0"
    i:int = 0
    str:string = ""
    str1:string = ""
    sum_i:int = 0
    guest = htparam = bediener = nation = guestseg = akt_cust = res_history = res_line = None

    t_guest = tlist = None

    tlist_data, Tlist = create_model("Tlist", {"tfield":string, "tcount":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_number, gastno, def_natcode, name_changed, zugriff, priscilla_active, lvcarea, i, str, str1, sum_i, guest, htparam, bediener, nation, guestseg, akt_cust, res_history, res_line
        nonlocal icase, pvilanguage, user_init


        nonlocal t_guest, tlist
        nonlocal tlist_data

        return {"msg_str": msg_str, "error_number": error_number}

    def update_record():

        nonlocal msg_str, error_number, gastno, def_natcode, name_changed, zugriff, priscilla_active, lvcarea, i, str, str1, sum_i, guest, htparam, bediener, nation, guestseg, akt_cust, res_history, res_line
        nonlocal icase, pvilanguage, user_init


        nonlocal t_guest, tlist
        nonlocal tlist_data

        # guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})
        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastno)).with_for_update().first()

        if (t_guest.name != guest.name) or (t_guest.vorname1 != guest.vorname1) or (t_guest.anrede1 != guest.anrede1) or (t_guest.vornamekind[0] != guest.vornamekind[0]) or (t_guest.kreditlimit != guest.kreditlimit):
            name_changed = True
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "GuestFile"

            if (t_guest.name != guest.name) or (t_guest.vorname1 != t_guest.vorname1) or (t_guest.anrede1 != guest.anrede1):
                res_history.aenderung = "GuestCard: gastno " + to_string(guest.gastnr) + " " + guest.name + "," + guest.vorname1 + " changed to " + t_guest.name + "," + t_guest.vorname1

            if t_guest.vornamekind[0] != guest.vornamekind[0]:

                if res_history.aenderung != "":
                    res_history.aenderung = res_history.aenderung + "; "
                res_history.aenderung = res_history.aenderung + "Changed Picture file from " + guest.vornamekind[0]

            if t_guest.kreditlimit != guest.kreditlimit:

                if res_history.aenderung != "":
                    res_history.aenderung = res_history.aenderung + "; "
                res_history.aenderung = res_history.aenderung + "Credit Limit changed from" + " " + to_string(guest.kreditlimit) + " TO " + to_string(t_guest.kreditlimit)
            pass
            pass

        if priscilla_active:

            if (t_guest.name != guest.name) or (t_guest.vorname1 != guest.vorname1) or (t_guest.anrede1 != guest.anrede1) or (t_guest.email_adr != guest.email_adr):

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.gastnrmember == guest.gastnr) & (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] != 1)).order_by(Res_line._recid).all():
                    get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))
        pass
        buffer_copy(t_guest, guest)
        pass
        db_session.refresh(guest,with_for_update=True)


    def new_record():

        nonlocal msg_str, error_number, gastno, def_natcode, name_changed, zugriff, priscilla_active, lvcarea, i, str, str1, sum_i, guest, htparam, bediener, nation, guestseg, akt_cust, res_history, res_line
        nonlocal icase, pvilanguage, user_init


        nonlocal t_guest, tlist
        nonlocal tlist_data

        # guest = get_cache (Guest, {"gastnr": [(eq, gastno)]})
        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastno)).with_for_update().first()
        buffer_copy(t_guest, guest)

        if guest.karteityp > 0:
            get_output(intevent_1(36, "", "newgcf", guest.gastnr, guest.karteityp))
        pass
        db_session.refresh(guest,with_for_update=True)


    htparam = get_cache (Htparam, {"paramnr": [(eq, 50)],"paramgruppe": [(eq, 6)]})

    if htparam and htparam.fchar != "":
        for i in range(1,num_entries(htparam.fchar, ";")  + 1) :

            if entry(i - 1, htparam.fchar, ";") != "":
                sum_i = sum_i + 1
                tlist = Tlist()
                tlist_data.append(tlist)

                tlist.tfield = entry(i - 1, htparam.fchar, ";")
                tlist.tcount = sum_i

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    t_guest = query(t_guest_data, first=True)
    gastno = t_guest.gastnr

    tlist = query(tlist_data, first=True)

    if tlist and t_guest.karteityp == 0:

        for tlist in query(tlist_data):

            if (tlist.tfield.lower()  == ("ttl").lower()  and t_guest.anrede1 == "") or (tlist.tfield.lower()  == ("dob").lower()  and t_guest.geburtdatum1 == None) or (tlist.tfield.lower()  == ("sex").lower()  and t_guest.geschlecht == "") or (tlist.tfield.lower()  == ("adr").lower()  and t_guest.adresse1 == "" and t_guest.adresse2 == "" and t_guest.adresse3 == ""):
                error_number = 7

            if tlist.tfield.lower()  == ("ttl").lower() :
                str1 = "Title"

            elif tlist.tfield.lower()  == ("dob").lower() :
                str1 = "Birthdate"

            elif tlist.tfield.lower()  == ("sex").lower() :
                str1 = "Sex"

            elif tlist.tfield.lower()  == ("adr").lower() :
                str1 = "Address"

            if tlist.tcount != sum_i:
                str = str + str1 + ", "
            else:
                str = substring(str, 0, length(str) - 2) + " & "+ str1

    if error_number == 7:
        msg_str = translateExtended ("Please fill all the mandatory fields in parameter number 50 (" + str + ")." , lvcarea, "")

        return generate_output()

    if icase == 2:
        update_record()

        if name_changed:
            get_output(update_gcfname(gastno))

        return generate_output()

    elif icase == 3:
        new_record()

        return generate_output()

    htparam = get_cache (Htparam, {"paramnr": [(eq, 153)]})

    nation = get_cache (Nation, {"kurzbez": [(eq, htparam.fchar)]})
    def_natcode = nation.kurzbez

    if icase == 1:

        # guestseg = get_cache (Guestseg, {"gastnr": [(eq, gastno)]})
        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == gastno)).with_for_update().first()

        if not guestseg or guestseg.segment == 0:

            if guestseg and guestseg.segment == 0:
                pass
                db_session.delete(guestseg)
                db_session.refresh(guestseg,with_for_update=True)

            if t_guest.karteityp > 0:
                msg_str = translateExtended ("Guest segment not yet defined.", lvcarea, "")
                error_number = 1

                return generate_output()

    if t_guest.name == "":
        msg_str = translateExtended ("Name not defined yet.", lvcarea, "")
        error_number = 2

        return generate_output()

    if t_guest.karteityp == 0:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 961)]})

        if htparam.feldtyp == 4 and htparam.flogical:

            if trim(t_guest.anrede1) == "":
                msg_str = translateExtended ("Guest Title not yet defined.", lvcarea, "")
                error_number = 3

                return generate_output()

        nation = get_cache (Nation, {"kurzbez": [(eq, t_guest.nation1)]})

        if not nation:
            msg_str = translateExtended ("Nationality not yet defined.", lvcarea, "")
            error_number = 4

            return generate_output()

        if t_guest.land.lower()  != (def_natcode).lower()  and t_guest.nation2 != "":
            msg_str = translateExtended ("Local Region for local country only.", lvcarea, "")
            error_number = 5

            return generate_output()

    nation = get_cache (Nation, {"kurzbez": [(eq, t_guest.land)]})

    if not nation:
        msg_str = translateExtended ("Country not yet defined.", lvcarea, "")
        error_number = 6

        return generate_output()

    if t_guest.phonetik3 != "":

        htparam = get_cache (Htparam, {"paramnr": [(eq, 1002)]})

        if htparam.flogical:

            # akt_cust = get_cache (Akt_cust, {"gastnr": [(eq, t_guest.gastnr)]})
            akt_cust = db_session.query(Akt_cust).filter(
                     (Akt_cust.gastnr == t_guest.gastnr)).with_for_update().first()

            if not akt_cust:
                akt_cust = Akt_cust()
                db_session.add(akt_cust)

                akt_cust.gastnr = t_guest.gastnr
                akt_cust.c_init = user_init
                akt_cust.userinit = t_guest.phonetik3


            else:

                if akt_cust.userinit == t_guest.phonetik3:
                    pass
                else:
                    pass
                    akt_cust.c_init = user_init
                    akt_cust.userinit = t_guest.phonetik3


                    pass
                db_session.refresh(akt_cust,with_for_update=True)
    else:

        # akt_cust = get_cache (Akt_cust, {"gastnr": [(eq, t_guest.gastnr)],"userinit": [(eq, t_guest.phonetik3)]})
        akt_cust = db_session.query(Akt_cust).filter(
                 (Akt_cust.gastnr == t_guest.gastnr) & (Akt_cust.userinit == t_guest.phonetik3)).with_for_update().first()

        if akt_cust:
            db_session.delete(akt_cust)
            pass
            db_session.refresh(akt_cust,with_for_update=True)

    return generate_output()
