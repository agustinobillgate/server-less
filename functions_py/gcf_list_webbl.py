# using conversion tools version: 1.0.0.119
# ------------------------------------------
# Rd, 31/10/2025
# Ticket:6CE187

# yusufwijasena, 14/11/2025
# fix issue cannot search company profile with guest number
# use f"string" to gname, adresse, firma, & curr_fname
# fix guest.anredefirma or "" to show company with no title

# Rd, 21/11/2025
# Update Indent ELSE di IF num1 = 0, kurang ke kiri
# ------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Guest, Akt_kont, Mc_guest, Segment, Guestseg, Cl_member, Guest_pr, Ratecode, Htparam


def gcf_list_webbl(case_type: int, sorttype: int, lname: string, fname: string, num1: int):

    prepare_cache([Akt_kont, Segment, Guestseg, Cl_member, Guest_pr, Htparam])

    first_gastnr = None
    curr_lname = ""
    curr_fname = ""
    total_record = to_decimal("0.0")
    t_guest_data = []
    counter: int = 0
    vipnr1: int = 999999999
    vipnr2: int = 999999999
    vipnr3: int = 999999999
    vipnr4: int = 999999999
    vipnr5: int = 999999999
    vipnr6: int = 999999999
    vipnr7: int = 999999999
    vipnr8: int = 999999999
    vipnr9: int = 999999999
    vipnr10: int = 999999999
    priority_flag: int = 0
    guest_number: int = 0
    guest_idcard: string = ""
    guest = akt_kont = mc_guest = segment = guestseg = cl_member = guest_pr = ratecode = htparam = None

    t_guest = None

    t_guest_data, T_guest = create_model(
        "T_guest",
        {
            "akt_gastnr": int,
            "karteityp": int,
            "master_gastnr": int,
            "pr_flag": int,
            "mc_flag": bool,
            "gname": string,
            "adresse": string,
            "steuernr": string,
            "firma": string,
            "namekontakt": string,
            "phonetik3": string,
            "rabatt": Decimal,
            "endperiode": date,
            "firmen_nr": int,
            "land": string,
            "wohnort": string,
            "telefon": string,
            "plz": string,
            "geschlecht": string,
            "ausweis_nr1": string,
            "gastnr": int,
            "zahlungsart": int,
            "kreditlimit": Decimal,
            "bezeich": string,
            "alertbox": bool,
            "warningbox": bool,
            "zimmeranz": int,
            "bemerk": string,
            "geburt_ort1": string,
            "nation1": string,
            "nation2": string,
            "fax": string,
            "geburtdatum1": date,
            "email_adr": string,
            "mobil_telefon": string,
            "beruf": string,
            "main_segment": string,
            "membership_card": string
        })

    db_session = local_storage.db_session

    lname = lname.strip()
    fname = fname.strip()

    def generate_output():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        return {
            "first_gastnr": first_gastnr,
            "curr_lname": curr_lname,
            "curr_fname": curr_fname,
            "total_record": total_record,
            "t-guest": t_guest_data
        }

    def case2a():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        count_i: int = 0
        guest_name: string = ""

        if lname == (""):
            curr_lname = lname

            return

        for guest in db_session.query(Guest).filter(
                (Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (matches((Guest.name + Guest.vorname1), ("*" + fname + "*")))).order_by(Guest.name).all():
            count_i = count_i + 1
            guest_name = guest.name + guest.vorname1

        if num1 == 0:
            for guest in db_session.query(Guest).filter(
                    (Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (matches((Guest.name + Guest.vorname1), ("*" + fname + "*")))).order_by(Guest.name).all():
                counter = counter + 1
                t_guest = T_guest()
                t_guest_data.append(t_guest)

                buffer_copy(guest, t_guest)
                t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
                t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                t_guest.firma = guest.name + ", " + guest.anredefirma
                curr_lname = guest.name
                curr_fname = guest.vorname1

                if (guest.name + guest.vorname1) == (guest_name):
                    curr_fname = ""

                if counter == 1:
                    first_gastnr = guest.gastnr

                if counter >= 30:
                    break
                check_prcode()
            
        else:
            for guest in db_session.query(Guest).filter(
                    (Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (matches((Guest.name + Guest.vorname1), ("*" + fname + "*")))).order_by(Guest.name).all():

                if (guest.name + guest.vorname1) > (lname):
                    counter = counter + 1
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                    buffer_copy(guest, t_guest)
                    t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                        " " + guest.anrede1
                    t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                    t_guest.firma = guest.name + ", " + guest.anredefirma
                    curr_lname = guest.name
                    curr_fname = guest.vorname1

                    if (guest.name + guest.vorname1) == (guest_name):
                        curr_fname = ""

                    if counter == 1:
                        first_gastnr = guest.gastnr

                    if (counter >= 30) and (guest.name != (lname)):
                        break
                    check_prcode()

    def case2b():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        if substring(lname, length(lname) - 1, 1) != ("*"):
            lname = lname + "*"

        for guest in db_session.query(Guest).filter(
                ((Guest.gastnr > 0)) & ((Guest.karteityp == sorttype)) & (matches((Guest.name + Guest.vorname1), (lname)))).order_by(Guest.name).all():
            t_guest = T_guest()
            t_guest_data.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = chr_unicode(255)
            curr_fname = chr_unicode(255)

            check_prcode()

    def case2c():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        for guest in db_session.query(Guest).filter(
                ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (matches((Guest.vorname1 + Guest.anredefirma), "*" + fname + "*")))).order_by(Guest.name).yield_per(100):
            counter = counter + 1

            if counter == 1:
                first_gastnr = guest.gastnr

            if (counter >= 30) and (curr_lname != guest.name):
                break
            t_guest = T_guest()
            t_guest_data.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = guest.name
            curr_fname = guest.vorname1 + guest.anredefirma

            check_prcode()

    def case3a():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        for guest in db_session.query(Guest).filter(
                ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (substring(Guest.name, 0, length((lname))) == (lname)) & ((Guest.vorname1 + Guest.anredefirma) >= ""))).order_by(Guest.name).all():
            t_guest = T_guest()
            t_guest_data.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = chr_unicode(255)
            curr_fname = chr_unicode(255)

            check_prcode()

    def case3b():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        if substring(lname, length(lname) - 1, 1) != ("*"):
            lname = lname + "*"

        for guest in db_session.query(Guest).filter(
                ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (matches((Guest.name + Guest.vorname1), (lname))) & ((Guest.vorname1 + Guest.anredefirma) >= (fname)))).order_by(Guest.name).all():
            t_guest = T_guest()
            t_guest_data.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = chr_unicode(255)
            curr_fname = chr_unicode(255)

            check_prcode()

    def case4():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        cardnum: string = ""
        from_pos: int = 0
        to_pos: int = 0
        count_i: int = 0
        last_cardnum: string = ""
        cardnum = lname

        mc_guest_obj_list = {}
        for mc_guest, guest in db_session.query(Mc_guest, Guest).join(Guest, (Guest.gastnr == Mc_guest.gastnr)).filter(
                (matches(Mc_guest.cardnum, ("*" + fname + "*")))).order_by(Mc_guest.cardnum).all():
            if mc_guest_obj_list.get(mc_guest._recid):
                continue
            else:
                mc_guest_obj_list[mc_guest._recid] = True

            count_i = count_i + 1
            last_cardnum = mc_guest.cardnum

        if num1 == 0:
            mc_guest_obj_list = {}
            for mc_guest, guest in db_session.query(Mc_guest, Guest).join(Guest, (Guest.gastnr == Mc_guest.gastnr)).filter(
                    (matches(Mc_guest.cardnum, ("*" + fname + "*")))).order_by(Mc_guest.cardnum).all():
                if mc_guest_obj_list.get(mc_guest._recid):
                    continue
                else:
                    mc_guest_obj_list[mc_guest._recid] = True

                counter = counter + 1
                t_guest = T_guest()
                t_guest_data.append(t_guest)

                buffer_copy(guest, t_guest)
                t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
                t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                t_guest.firma = guest.name + ", " + guest.anredefirma
                curr_lname = mc_guest.cardnum
                t_guest.membership_card = mc_guest.cardnum

                if mc_guest.cardnum == mc_guest.cardnum:
                    curr_fname = ""

                if counter == 1:
                    curr_fname = mc_guest.cardnum

                if (counter >= 30) and (mc_guest.cardnum != cardnum):
                    break
                check_prcode()
            
        else:
            for mc_guest in db_session.query(Mc_guest).filter(
                    (matches(Mc_guest.cardnum, ("*" + fname + "*")))).order_by(Mc_guest.cardnum).all():

                if mc_guest.cardnum > cardnum:

                    guest = get_cache(
                        Guest, {"gastnr": [(eq, mc_guest.gastnr)]})

                    if guest:
                        counter = counter + 1
                        t_guest = T_guest()
                        t_guest_data.append(t_guest)

                        buffer_copy(guest, t_guest)
                        t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                            " " + guest.anrede1
                        t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                        t_guest.firma = guest.name + ", " + guest.anredefirma
                        curr_lname = mc_guest.cardnum
                        t_guest.membership_card = mc_guest.cardnum

                        if mc_guest.cardnum == mc_guest.cardnum:
                            curr_fname = ""

                        if counter == 1:
                            curr_fname = mc_guest.cardnum

                        if (counter >= 30) and (mc_guest.cardnum != cardnum):
                            break
                        check_prcode()

    def case5():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        cardnum: string = ""
        from_pos: int = 0
        to_pos: int = 0
        count_i: int = 0
        last_idcard: string = ""

        if lname == "":
            return

        for guest in db_session.query(Guest).filter(
                (matches(Guest.ausweis_nr1, ("*" + fname + "*"))) & (Guest.karteityp == sorttype)).order_by(Guest.ausweis_nr1).all():
            count_i = count_i + 1
            last_idcard = guest.ausweis_nr1
        guest_idcard = lname

        if num1 == 0:
            for guest in db_session.query(Guest).filter(
                    (matches(Guest.ausweis_nr1, ("*" + fname + "*"))) & (Guest.karteityp == sorttype)).order_by(Guest.ausweis_nr1).all():
                counter = counter + 1
                t_guest = T_guest()
                t_guest_data.append(t_guest)

                buffer_copy(guest, t_guest)
                t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
                t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                t_guest.firma = guest.name + ", " + guest.anredefirma
                curr_lname = guest.ausweis_nr1

                if guest.ausweis_nr1 == (last_idcard):
                    curr_fname = ""

                if counter == 1:
                    curr_fname = guest.ausweis_nr1

                if (counter >= 30) and (guest.ausweis_nr1 != (guest_idcard)):
                    break
                check_prcode()
            
        else:
            for guest in db_session.query(Guest).filter(
                    (matches(Guest.ausweis_nr1, ("*" + fname + "*"))) & (Guest.karteityp == sorttype)).order_by(Guest.ausweis_nr1).all():

                if guest.ausweis_nr1 > (guest_idcard):
                    counter = counter + 1
                    t_guest = T_guest()
                    t_guest_data.append(t_guest)

                    buffer_copy(guest, t_guest)
                    t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                        " " + guest.anrede1
                    t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                    t_guest.firma = guest.name + ", " + guest.anredefirma
                    curr_lname = guest.ausweis_nr1

                    if guest.ausweis_nr1 == (last_idcard):
                        curr_fname = ""

                    if counter == 1:
                        curr_fname = guest.ausweis_nr1

                    if (counter >= 30) and (guest.ausweis_nr1 != (guest_idcard)):
                        break
                check_prcode()

    def case6():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        from_gastnr: int = 0
        from_gastnr = to_int(lname)

        for guest in db_session.query(Guest).filter(
                (Guest.karteityp == sorttype) & (Guest.gastnr >= from_gastnr)).order_by(Guest.gastnr).yield_per(100):
            counter = counter + 1

            if counter == 1:
                first_gastnr = guest.gastnr

            if counter >= 30:
                break
            t_guest = T_guest()
            t_guest_data.append(t_guest)

            buffer_copy(guest, t_guest)
            # yusufwijasena: fix cannot search company profile with guest number
            # t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1
            # t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            # t_guest.firma = guest.name + ", " + guest.anredefirma
            t_guest.gname = f"{guest.name}, {guest.vorname1}{guest.anredefirma or ""} {guest.anrede1}"
            t_guest.adresse = f"{guest.adresse1} {guest.adresse2}"
            t_guest.firma = f"{guest.name}, {guest.anredefirma}"
            curr_lname = to_string(guest.gastnr + 1)
            curr_fname = f"{guest.vorname1}{guest.anredefirma or ""}"

            check_prcode()

    def case7():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        found: bool = False
        curr_gastnr: int = 0

        guest = get_cache(Guest, {"gastnr": [(eq, num1)]})

        if not guest:
            return
        lname = guest.name
        curr_gastnr = guest.gastnr

        for guest in db_session.query(Guest).filter(
                ((Guest.karteityp == sorttype) & (Guest.name >= trim(lname)) & ((Guest.vorname1 + Guest.anredefirma) >= ""))).order_by(Guest.name).yield_per(100):

            if guest.gastnr == curr_gastnr:
                found = True

            if found:
                counter = counter + 1

                if counter == 1:
                    first_gastnr = guest.gastnr

                if counter >= 30:
                    break
                t_guest = T_guest()
                t_guest_data.append(t_guest)

                buffer_copy(guest, t_guest)
                t_guest.gname = guest.name + ", " + guest.vorname1 + \
                    guest.anredefirma + " " + guest.anrede1
                t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                t_guest.firma = guest.name + ", " + guest.anredefirma
                curr_lname = guest.name
                curr_fname = guest.vorname1 + guest.anredefirma

                check_prcode()

    def case8():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        count_i: int = 0
        last_gastnr: int = 0

        for guest in db_session.query(Guest).filter(
                (matches(to_string(Guest.gastnr), ("*" + fname + "*"))) & (Guest.karteityp == sorttype)).order_by(Guest.gastnr).all():
            count_i = count_i + 1
            last_gastnr = guest.gastnr

        if num1 == 0:
            guest_number = to_int(lname)

            for guest in db_session.query(Guest).filter(
                    (matches(to_string(Guest.gastnr), ("*" + fname + "*"))) & (Guest.karteityp == sorttype)).order_by(Guest.gastnr).all():
                counter = counter + 1
                t_guest = T_guest()
                t_guest_data.append(t_guest)

                buffer_copy(guest, t_guest)
                t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
                t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                t_guest.firma = guest.name + ", " + guest.anredefirma
                curr_lname = to_string(guest.gastnr)

                if guest.gastnr == last_gastnr:
                    curr_fname = ""

                if counter == 1:
                    first_gastnr = guest.gastnr

                if (counter >= 30) and (guest.gastnr != guest_number):
                    break
                check_prcode()
        else:
            guest_number = to_int(lname)

            for guest in db_session.query(Guest).filter(
                    (matches(to_string(Guest.gastnr), ("*" + fname + "*"))) & (Guest.karteityp == sorttype) & (Guest.gastnr > guest_number)).order_by(Guest.gastnr).all():
                counter = counter + 1
                t_guest = T_guest()
                t_guest_data.append(t_guest)

                buffer_copy(guest, t_guest)
                t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
                t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                t_guest.firma = guest.name + ", " + guest.anredefirma
                curr_lname = to_string(guest.gastnr)

                if guest.gastnr == last_gastnr:
                    curr_fname = ""

                if counter == 1:
                    first_gastnr = guest.gastnr

                if (counter >= 30) and (guest.gastnr != guest_number):
                    break
                check_prcode()

    def case9():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        cl_member = get_cache(Cl_member, {"codenum": [(eq, lname)]})

        if cl_member:
            guest = get_cache(Guest, {"gastnr": [(eq, cl_member.gastnr)]})

            if guest:
                t_guest = T_guest()
                t_guest_data.append(t_guest)

                buffer_copy(guest, t_guest)
                t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
                t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                t_guest.firma = guest.name + ", " + guest.anredefirma
                curr_lname = chr_unicode(255)
                curr_fname = chr_unicode(255)

                check_prcode()

    def check_prcode():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        for guest_pr in db_session.query(Guest_pr).filter(
                (Guest_pr.gastnr == guest.gastnr)).order_by(Guest_pr._recid).all():

            ratecode = get_cache(Ratecode, {"code": [(eq, guest_pr.code)], "endperiode": [
                                 (gt, get_current_date())]})

            if ratecode:
                t_guest.pr_flag = 2

                return
            else:
                ratecode = get_cache(Ratecode, {"code": [(eq, guest_pr.code)]})

                if ratecode:
                    t_guest.pr_flag = 1

    def get_vipnr():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, priority_flag, guest_number, guest_idcard, guest, akt_kont, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1
        nonlocal t_guest
        nonlocal t_guest_data

        htparam = get_cache(Htparam, {"paramnr": [(eq, 700)]})

        if htparam.finteger != 0:
            vipnr1 = htparam.finteger

        htparam = get_cache(Htparam, {"paramnr": [(eq, 701)]})

        if htparam.finteger != 0:
            vipnr2 = htparam.finteger

        htparam = get_cache(Htparam, {"paramnr": [(eq, 702)]})

        if htparam.finteger != 0:
            vipnr3 = htparam.finteger

        htparam = get_cache(Htparam, {"paramnr": [(eq, 703)]})

        if htparam.finteger != 0:
            vipnr4 = htparam.finteger

        htparam = get_cache(Htparam, {"paramnr": [(eq, 704)]})

        if htparam.finteger != 0:
            vipnr5 = htparam.finteger

        htparam = get_cache(Htparam, {"paramnr": [(eq, 705)]})

        if htparam.finteger != 0:
            vipnr6 = htparam.finteger

        htparam = get_cache(Htparam, {"paramnr": [(eq, 706)]})

        if htparam.finteger != 0:
            vipnr7 = htparam.finteger

        htparam = get_cache(Htparam, {"paramnr": [(eq, 707)]})

        if htparam.finteger != 0:
            vipnr8 = htparam.finteger

        htparam = get_cache(Htparam, {"paramnr": [(eq, 708)]})

        if htparam.finteger != 0:
            vipnr9 = htparam.finteger

        htparam = get_cache(Htparam, {"paramnr": [(eq, 712)]})

        if htparam.finteger != 0:
            vipnr10 = htparam.finteger

    total_record = to_decimal("0")

    if case_type == 1:
        for guest in db_session.query(Guest).filter(
                ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (Guest.name > (lname)) & ((Guest.vorname1 + Guest.anredefirma) >= (fname)))).order_by(Guest.name).yield_per(100):

            akt_kont = db_session.query(Akt_kont).first()
            counter = counter + 1

            if counter == 1:
                first_gastnr = guest.gastnr

            if (counter >= 30) and (curr_lname != guest.name):
                break
            t_guest = T_guest()
            t_guest_data.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            t_guest.bemerk = guest.bemerkung
            t_guest.zimmeranz = guest.zimmeranz
            curr_lname = guest.name
            curr_fname = guest.vorname1 + guest.anredefirma
            t_guest.namekontakt = guest.namekontakt

            akt_kont = get_cache(
                Akt_kont, {"gastnr": [(eq, guest.gastnr)], "hauptkontakt": [(eq, True)]})

            if akt_kont:
                t_guest.namekontakt = akt_kont.name + ", " + \
                    akt_kont.vorname + " " + akt_kont.anrede
            check_prcode()
    elif case_type == 2:

        if substring(lname, 0, 1) != ("*") and lname != "":
            case2a()

        elif length(lname) >= 2 and substring(lname, 0, 1) == ("*"):
            case2b()

        elif lname == "" and fname != "":
            case2c()
    elif case_type == 3:

        if lname != "" and substring(lname, 0, 1) != ("*"):
            case3a()

        elif length(lname) >= 2 and substring(lname, 0, 1) == ("*"):
            case3b()
    elif case_type == 4:
        case4()
    elif case_type == 5:
        case5()
    elif case_type == 6:
        case6()
    elif case_type == 7:
        case7()
    elif case_type == 8:
        case8()
    elif case_type == 9:
        case9()
    get_vipnr()

    for t_guest in query(t_guest_data):
        mc_guest = get_cache(
            Mc_guest, {"gastnr": [(eq, t_guest.gastnr)], "activeflag": [(eq, True)]})
        t_guest.mc_flag = None != mc_guest

        priority_flag = 0

        guestseg_obj_list = {}
        guestseg = Guestseg()
        segment = Segment()
        for guestseg.segmentcode, guestseg.reihenfolge, guestseg._recid, segment.bezeich, segment.segmentcode, segment.betriebsnr, segment._recid in db_session.query(Guestseg.segmentcode, Guestseg.reihenfolge, Guestseg._recid, Segment.bezeich, Segment.segmentcode, Segment.betriebsnr, Segment._recid).join(Segment, (Segment.segmentcode == Guestseg.segmentcode)).filter(
                (Guestseg.gastnr == t_guest.gastnr)).order_by(Guestseg._recid).yield_per(100):
            if guestseg_obj_list.get(guestseg._recid):
                continue
            else:
                guestseg_obj_list[guestseg._recid] = True

            if priority_flag < 3 and (guestseg.segmentcode == vipnr1 or guestseg.segmentcode == vipnr2 or guestseg.segmentcode == vipnr3 or guestseg.segmentcode == vipnr4 or guestseg.segmentcode == vipnr5 or guestseg.segmentcode == vipnr6 or guestseg.segmentcode == vipnr7 or guestseg.segmentcode == vipnr8 or guestseg.segmentcode == vipnr9):
                priority_flag = 3
                t_guest.alertbox = True
                t_guest.bezeich = entry(0, segment.bezeich, "$$0")

            elif priority_flag < 2 and segment.betriebsnr == 4:
                priority_flag = 2
                t_guest.alertbox = True
                t_guest.bezeich = entry(0, segment.bezeich, "$$0")

            elif priority_flag < 1:
                priority_flag = 1
                t_guest.bezeich = entry(0, segment.bezeich, "$$0")

            if guestseg.reihenfolge == 1:
                t_guest.main_segment = to_string(
                    segment.segmentcode) + " - " + entry(0, segment.bezeich, "$$0")

                if priority_flag == 3:
                    break

    return generate_output()
