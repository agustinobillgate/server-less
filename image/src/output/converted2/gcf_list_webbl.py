from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.htpint import htpint
from models import Guest, Mc_guest, Segment, Guestseg, Cl_member, Guest_pr, Ratecode, Htparam

def gcf_list_webbl(case_type:int, sorttype:int, lname:str, fname:str, num1:int):
    first_gastnr = None
    curr_lname = ""
    curr_fname = ""
    total_record = to_decimal("0.0")
    t_guest_list = []
    counter:int = 0
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    guest = mc_guest = segment = guestseg = cl_member = guest_pr = ratecode = htparam = None

    t_guest = None

    t_guest_list, T_guest = create_model("T_guest", {"akt_gastnr":int, "karteityp":int, "master_gastnr":int, "pr_flag":int, "mc_flag":bool, "gname":str, "adresse":str, "steuernr":str, "firma":str, "namekontakt":str, "phonetik3":str, "rabatt":decimal, "endperiode":date, "firmen_nr":int, "land":str, "wohnort":str, "telefon":str, "plz":str, "geschlecht":str, "ausweis_nr1":str, "gastnr":int, "zahlungsart":int, "kreditlimit":decimal, "bezeich":str, "alertbox":bool, "warningbox":bool, "zimmeranz":int, "bemerk":str, "geburt_ort1":str, "nation1":str, "nation2":str, "fax":str, "geburtdatum1":date, "email_adr":str, "mobil_telefon":str, "beruf":str, "main_segment":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list
        return {"first_gastnr": first_gastnr, "curr_lname": curr_lname, "curr_fname": curr_fname, "total_record": total_record, "t-guest": t_guest_list}

    def case2a():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list


        pass

        if num1 == 0:

            guest = db_session.query(Guest).filter(
                     (func.lower(Guest.name) == (lname).lower()) & (Guest.karteityp == sorttype) & (Guest.gastnr > 0)).first()

        if guest:

            if fname != " ":

                for guest in db_session.query(Guest).filter(
                         ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (func.lower(Guest.name) == (lname).lower()) & ((Guest.vorname1 + Guest.anredefirma) >= (fname).lower()))).order_by(Guest.name).all():
                    t_guest = T_guest()
                    t_guest_list.append(t_guest)

                    buffer_copy(guest, t_guest)
                    t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                            " " + guest.anrede1
                    t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                    t_guest.firma = guest.name + ", " + guest.anredefirma
                    curr_lname = chr(255)
                    curr_fname = chr(255)


                    check_prcode()
            else:

                for guest in db_session.query(Guest).filter(
                         ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (func.lower(Guest.name) == (lname).lower()))).order_by(Guest.name).all():
                    t_guest = T_guest()
                    t_guest_list.append(t_guest)

                    buffer_copy(guest, t_guest)
                    t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                            " " + guest.anrede1
                    t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                    t_guest.firma = guest.name + ", " + guest.anredefirma
                    curr_lname = chr(255)
                    curr_fname = chr(255)


                    check_prcode()
        else:

            if lname == chr(255):
                curr_lname = lname

                return

            for guest in db_session.query(Guest).filter(
                     ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (func.lower(Guest.name) > (lname).lower()) & ((Guest.vorname1 + Guest.anredefirma) >= (fname).lower()))).order_by(Guest.name).all():
                counter = counter + 1

                if counter == 1:
                    first_gastnr = guest.gastnr

                if (counter >= 30) and (curr_lname != guest.name):
                    break
                t_guest = T_guest()
                t_guest_list.append(t_guest)

                buffer_copy(guest, t_guest)
                t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                        " " + guest.anrede1
                t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                t_guest.firma = guest.name + ", " + guest.anredefirma
                curr_lname = guest.name
                curr_fname = guest.vorname1 + guest.anredefirma


                check_prcode()


    def case2b():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        if substring(lname, len(lname) - 1, 1) != ("*").lower() :
            lname = lname + "*"

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0)) & ((Guest.karteityp == sorttype)) & (func.lower((Guest.name + Guest.vorname1)).op("~")(((lname.lower().replace("*",".*")))))).order_by(Guest.name).all():
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = chr(255)
            curr_fname = chr(255)


            check_prcode()


    def case2c():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (func.lower((Guest.vorname1 + Guest.anredefirma)).op("~")(("*" + fname + "*".lower().replace("*",".*")))))).order_by(Guest.name).all():
            counter = counter + 1

            if counter == 1:
                first_gastnr = guest.gastnr

            if (counter >= 30) and (curr_lname != guest.name):
                break
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = guest.name
            curr_fname = guest.vorname1 + guest.anredefirma


            check_prcode()


    def case3a():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (substring(Guest.name, 0, len((lname).lower() )) == (lname).lower()) & ((Guest.vorname1 + Guest.anredefirma) >= ""))).order_by(Guest.name).all():
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = chr(255)
            curr_fname = chr(255)


            check_prcode()


    def case3b():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        if substring(lname, len(lname) - 1, 1) != ("*").lower() :
            lname = lname + "*"

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (func.lower((Guest.name + Guest.vorname1)).op("~")(((lname).lower().replace("*",".*")))) & ((Guest.vorname1 + Guest.anredefirma) >= (fname).lower()))).order_by(Guest.name).all():
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = chr(255)
            curr_fname = chr(255)


            check_prcode()


    def case4():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        cardnum:str = ""
        from_pos:int = 0
        to_pos:int = 0
        cardnum = lname

        mc_guest = db_session.query(Mc_guest).filter(
                 (Mc_guest.cardnum == cardnum)).first()

        if not mc_guest:
            from_pos = get_output(htpint(337))
            to_pos = get_output(htpint(338))

            if from_pos > 0 and to_pos > 0:
                cardnum = substring(cardnum, from_pos - 1, (to_pos - from_pos + 1))
                curr_fname = cardnum

                mc_guest = db_session.query(Mc_guest).filter(
                         (Mc_guest.cardnum == cardnum)).first()

        if mc_guest:

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == mc_guest.gastnr)).first()
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = chr(255)


            check_prcode()


    def case5():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        cardnum:str = ""
        from_pos:int = 0
        to_pos:int = 0

        if lname == "":

            return

        for guest in db_session.query(Guest).filter(
                 (Guest.karteityp == 0) & (Guest.gastnr > 0) & (func.lower(Guest.ausweis_nr1).op("~")(("*" + lname + "*".lower().replace("*",".*"))))).order_by(Guest.name).all():
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = chr(255)
            curr_fname = chr(255)


            check_prcode()


    def case6():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        from_gastnr:int = 0
        from_gastnr = to_int(lname)

        for guest in db_session.query(Guest).filter(
                 (Guest.karteityp == sorttype) & (Guest.gastnr >= from_gastnr)).order_by(Guest.gastnr).all():
            counter = counter + 1

            if counter == 1:
                first_gastnr = guest.gastnr

            if counter >= 30:
                break
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = to_string(guest.gastnr + 1)
            curr_fname = guest.vorname1 + guest.anredefirma


            check_prcode()


    def case7():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        found:bool = False
        curr_gastnr:int = 0

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == num1)).first()

        if not guest:

            return
        lname = guest.name
        curr_gastnr = guest.gastnr

        for guest in db_session.query(Guest).filter(
                 ((Guest.karteityp == sorttype) & (Guest.name >= trim(lname)) & ((Guest.vorname1 + Guest.anredefirma) >= ""))).order_by(Guest.name).all():

            if guest.gastnr == curr_gastnr:
                found = True

            if found:
                counter = counter + 1

                if counter == 1:
                    first_gastnr = guest.gastnr

                if counter >= 30:
                    break
                t_guest = T_guest()
                t_guest_list.append(t_guest)

                buffer_copy(guest, t_guest)
                t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                        " " + guest.anrede1
                t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                t_guest.firma = guest.name + ", " + guest.anredefirma
                curr_lname = guest.name
                curr_fname = guest.vorname1 + guest.anredefirma


                check_prcode()


    def case8():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        for guest in db_session.query(Guest).filter(
                 (func.lower(to_string(Guest.gastnr)).op("~")(("*" + lname + "*".lower().replace("*",".*"))))).order_by(Guest._recid).all():
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = chr(255)
            curr_fname = chr(255)


            check_prcode()


    def case9():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        cl_member = db_session.query(Cl_member).filter(
                 (func.lower(Cl_member.codenum) == (lname).lower())).first()

        if cl_member:

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == cl_member.gastnr)).first()

            if guest:
                t_guest = T_guest()
                t_guest_list.append(t_guest)

                buffer_copy(guest, t_guest)
                t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                        " " + guest.anrede1
                t_guest.adresse = guest.adresse1 + " " + guest.adresse2
                t_guest.firma = guest.name + ", " + guest.anredefirma
                curr_lname = chr(255)
                curr_fname = chr(255)


                check_prcode()


    def check_prcode():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == guest.gastnr)).order_by(Guest_pr._recid).all():

            ratecode = db_session.query(Ratecode).filter(
                     (Ratecode.code == guest_pr.code) & (Ratecode.endperiode > get_current_date())).first()

            if ratecode:
                t_guest.pr_flag = 2

                return
            else:

                ratecode = db_session.query(Ratecode).filter(
                         (Ratecode.code == guest_pr.code)).first()

                if ratecode:
                    t_guest.pr_flag = 1


    def get_vipnr():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_list, counter, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1


        nonlocal t_guest
        nonlocal t_guest_list

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 700)).first()

        if htparam.finteger != 0:
            vipnr1 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 701)).first()

        if htparam.finteger != 0:
            vipnr2 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 702)).first()

        if htparam.finteger != 0:
            vipnr3 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 703)).first()

        if htparam.finteger != 0:
            vipnr4 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 704)).first()

        if htparam.finteger != 0:
            vipnr5 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 705)).first()

        if htparam.finteger != 0:
            vipnr6 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 706)).first()

        if htparam.finteger != 0:
            vipnr7 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 707)).first()

        if htparam.finteger != 0:
            vipnr8 = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 708)).first()

        if htparam.finteger != 0:
            vipnr9 = htparam.finteger

    total_record =  to_decimal("0")

    for guest in db_session.query(Guest).filter(
             (Guest.karteityp == sorttype)).order_by(Guest._recid).all():
        total_record =  to_decimal(total_record) + to_decimal("1")

    if case_type == 1:

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (func.lower(Guest.name) > (lname).lower()) & ((Guest.vorname1 + Guest.anredefirma) >= (fname).lower()))).order_by(Guest.name).all():
            counter = counter + 1

            if counter == 1:
                first_gastnr = guest.gastnr

            if (counter >= 30) and (curr_lname != guest.name):
                break
            t_guest = T_guest()
            t_guest_list.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            t_guest.bemerk = guest.bemerk
            t_guest.zimmeranz = guest.zimmeranz
            curr_lname = guest.name
            curr_fname = guest.vorname1 + guest.anredefirma


            check_prcode()
    elif case_type == 2:

        if substring(lname, 0, 1) != ("*").lower()  and lname != " ":
            case2a()

        elif len(lname) >= 2 and substring(lname, 0, 1) == ("*").lower() :
            case2b()

        elif lname == " " and fname != " ":
            case2c()
    elif case_type == 3:

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            case3a()

        elif len(lname) >= 2 and substring(lname, 0, 1) == ("*").lower() :
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

    for t_guest in query(t_guest_list):

        mc_guest = db_session.query(Mc_guest).filter(
                 (Mc_guest.gastnr == t_guest.gastnr) & (Mc_guest.activeflag)).first()
        t_guest.mc_flag = None ! == mc_guest

        guestseg_obj_list = []
        for guestseg, segment in db_session.query(Guestseg, Segment).join(Segment,(Segment.segmentcode == Guestseg.segmentcode)).filter(
                 (Guestseg.gastnr == t_guest.gastnr)).order_by(Guestseg._recid).all():
            if guestseg._recid in guestseg_obj_list:
                continue
            else:
                guestseg_obj_list.append(guestseg._recid)


            t_guest.bezeich = entry(0, segment.bezeich, "$$0")
            break

        guestseg_obj_list = []
        for guestseg, segment in db_session.query(Guestseg, Segment).join(Segment,(Segment.segmentcode == Guestseg.segmentcode) & (Segment.betriebsnr == 4)).filter(
                 (Guestseg.gastnr == t_guest.gastnr)).order_by(Guestseg._recid).all():
            if guestseg._recid in guestseg_obj_list:
                continue
            else:
                guestseg_obj_list.append(guestseg._recid)


            t_guest.warningbox = True
            t_guest.bezeich = entry(0, segment.bezeich, "$$0")
            break

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == t_guest.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

        if guestseg:

            segment = db_session.query(Segment).filter(
                     (Segment.segmentcode == guestseg.segmentcode)).first()
            t_guest.alertbox = True
            t_guest.bezeich = entry(0, segment.bezeich, "$$0")

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == t_guest.gastnr) & (Guestseg.reihenfolge == 1)).first()

        if guestseg:

            segment = db_session.query(Segment).filter(
                     (Segment.segmentcode == guestseg.segmentcode)).first()

            if segment:
                t_guest.main_segment = to_string(segment.segmentcode) + " - " + entry(0, segment.bezeich, "$$0")

    return generate_output()