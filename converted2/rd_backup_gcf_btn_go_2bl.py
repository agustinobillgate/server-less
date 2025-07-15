from functions.additional_functions import *
import decimal
from sqlalchemy import func
from functions.update_gcfname import update_gcfname
from functions.intevent_1 import intevent_1
from models import Guest, Htparam, Bediener, Nation, Guestseg, Akt_cust, Res_history, Res_line, Queasy

t_guest_list, T_guest = create_model_like(Guest)

def gcf_btn_go_2bl(icase:int, pvilanguage:int, user_init:str, refno4:str, t_guest_list:[T_guest]):
    msg_str = ""
    error_number = 0
    gastno:int = 0
    def_natcode:str = ""
    name_changed:bool = False
    zugriff:bool = False
    priscilla_active:bool = True
    lvcarea:str = "chg-gcf0"
    i:int = 0
    str:str = ""
    str1:str = ""
    sum_i:int = 0
    guest = htparam = bediener = nation = guestseg = akt_cust = res_history = res_line = queasy = None

    t_guest = tlist = None

    tlist_list, Tlist = create_model("Tlist", {"tfield":str, "tcount":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, error_number, gastno, def_natcode, name_changed, zugriff, priscilla_active, lvcarea, i, str, str1, sum_i, guest, htparam, bediener, nation, guestseg, akt_cust, res_history, res_line, queasy
        nonlocal icase, pvilanguage, user_init, refno4


        nonlocal t_guest, tlist
        nonlocal t_guest_list, tlist_list
        return {"msg_str": msg_str, "error_number": error_number}

    def update_record():

        nonlocal msg_str, error_number, gastno, def_natcode, name_changed, zugriff, priscilla_active, lvcarea, i, str, str1, sum_i, guest, htparam, bediener, nation, guestseg, akt_cust, res_history, res_line, queasy
        nonlocal icase, pvilanguage, user_init, refno4


        nonlocal t_guest, tlist
        nonlocal t_guest_list, tlist_list

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastno)).first()

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

        if priscilla_active:

            if (t_guest.name != guest.name) or (t_guest.vorname1 != guest.vorname1) or (t_guest.anrede1 != guest.anrede1) or (t_guest.email_adr != guest.email_adr):

                # for res_line in db_session.query(Res_line).filter(
                #          (Res_line.gastnrmember == guest.gastnr) & 
                #          (Res_line.active_flag <= 1) & 
                #          (Res_line.resstatus != 12) & (Res_line.l_zuordnung[inc_value(2)] != 1))]).order_by(Res_line._recid).all():
                #     get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))
                for res_line in db_session.query(Res_line).filter(
                         (Res_line.gastnrmember == guest.gastnr) & 
                         (Res_line.active_flag <= 1) & 
                         (Res_line.resstatus != 12) & (Res_line.l_zuordnung[2] != 1)).order_by(Res_line._recid).all():
                    get_output(intevent_1(9, res_line.zinr, "Priscilla", res_line.resnr, res_line.reslinnr))

        if refno4 != "":

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 231) & (Queasy.number1 == gastno)).first()

            if queasy:
                queasy.char1 = refno4


            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 231
                queasy.number1 = gastno
                queasy.char1 = refno4


        buffer_copy(t_guest, guest)


    def new_record():

        nonlocal msg_str, error_number, gastno, def_natcode, name_changed, zugriff, priscilla_active, lvcarea, i, str, str1, sum_i, guest, htparam, bediener, nation, guestseg, akt_cust, res_history, res_line, queasy
        nonlocal icase, pvilanguage, user_init, refno4


        nonlocal t_guest, tlist
        nonlocal t_guest_list, tlist_list

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == gastno)).first()
        buffer_copy(t_guest, guest)

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 1023)).first()

        if htparam and htparam.flogical :

            if guest.karteityp > 0:
                get_output(intevent_1(36, "", "newgcf", guest.gastnr, guest.karteityp))

        if refno4 != "":

            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 231) & (Queasy.number1 == gastno)).first()

            if queasy:
                queasy.char1 = refno4


            else:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 231
                queasy.number1 = gastno
                queasy.char1 = refno4

    if refno4 == None:
        refno4 = ""

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 50) & (Htparam.paramgruppe == 6)).first()

    if htparam and htparam.fchar != "":
        for i in range(1,num_entries(htparam.fchar, ";")  + 1) :

            if entry(i - 1, htparam.fchar, ";") != "":
                sum_i = sum_i + 1
                tlist = Tlist()
                tlist_list.append(tlist)

                tlist.tfield = entry(i - 1, htparam.fchar, ";")
                tlist.tcount = sum_i

    bediener = db_session.query(Bediener).filter(
             (func.lower(Bediener.userinit) == (user_init).lower())).first()

    t_guest = query(t_guest_list, first=True)
    gastno = t_guest.gastnr

    tlist = query(tlist_list, first=True)

    if tlist and t_guest.karteityp == 0:

        for tlist in query(tlist_list):

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
                str = substring(str, 0, len(str) - 2) + " & "+ str1

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

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 153)).first()

    nation = db_session.query(Nation).filter(
             (Nation.kurzbez == htparam.fchar)).first()
    def_natcode = nation.kurzbez

    if icase == 1:

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == gastno)).first()

        if not guestseg or guestseg.segment == 0:

            if guestseg and guestseg.segment == 0:
                db_session.delete(guestseg)

            if t_guest.karteityp > 0:
                msg_str = translateExtended ("Guest segment not yet defined.", lvcarea, "")
                error_number = 1

                return generate_output()

    if t_guest.name == "":
        msg_str = translateExtended ("Name not defined yet.", lvcarea, "")
        error_number = 2

        return generate_output()

    if t_guest.karteityp == 0:

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 961)).first()

        if htparam.feldtyp == 4 and htparam.flogical:

            if trim(t_guest.anrede1) == "":
                msg_str = translateExtended ("Guest Title not yet defined.", lvcarea, "")
                error_number = 3

                return generate_output()

        nation = db_session.query(Nation).filter(
                 (Nation.kurzbez == t_guest.nation1)).first()

        if not nation:
            msg_str = translateExtended ("Nationality not yet defined.", lvcarea, "")
            error_number = 4

            return generate_output()

        if t_guest.land.lower()  != (def_natcode).lower()  and t_guest.nation2 != "":
            msg_str = translateExtended ("Local Region for local country only.", lvcarea, "")
            error_number = 5

            return generate_output()

    nation = db_session.query(Nation).filter(
             (Nation.kurzbez == t_guest.land)).first()

    if not nation:
        msg_str = translateExtended ("Country not yet defined.", lvcarea, "")
        error_number = 6

        return generate_output()

    if t_guest.phonetik3 != "":

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 1002)).first()

        if htparam.flogical:

            akt_cust = db_session.query(Akt_cust).filter(
                     (Akt_cust.gastnr == t_guest.gastnr)).first()

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
                    akt_cust.c_init = user_init
                    akt_cust.userinit = t_guest.phonetik3


    else:

        akt_cust = db_session.query(Akt_cust).filter(
                 (Akt_cust.gastnr == t_guest.gastnr) & (Akt_cust.userinit == t_guest.phonetik3)).first()

        if akt_cust:
            db_session.delete(akt_cust)
            pass

    return generate_output()