#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.htpint import htpint
from models import Guest, Mc_guest, Segment, Guestseg, Cl_member, Guest_pr, Ratecode, Htparam

t_g_data, T_g = create_model("T_g", {"akt_gastnr":int, "karteityp":int, "master_gastnr":int, "pr_flag":int, "mc_flag":bool, "gname":string, "adresse":string, "steuernr":string, "firma":string, "namekontakt":string, "phonetik3":string, "rabatt":Decimal, "endperiode":date, "firmen_nr":int, "land":string, "wohnort":string, "telefon":string, "plz":string, "geschlecht":string, "ausweis_nr1":string, "gastnr":int, "zahlungsart":int, "kreditlimit":Decimal, "bezeich":string, "alertbox":bool, "warningbox":bool, "ctr":int})

def gcf_list1_webbl(case_type:int, sorttype:int, lname:string, fname:string, num1:int, cntr:int, t_g_data:[T_g]):

    prepare_cache ([Segment, Guestseg, Cl_member, Guest_pr, Htparam])

    first_gastnr = None
    curr_lname = ""
    curr_fname = ""
    total_record = to_decimal("0.0")
    t_guest_data = []
    counter:int = 0
    ct:int = 0
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

    t_guest = t_g = None

    t_guest_data, T_guest = create_model("T_guest", {"akt_gastnr":int, "karteityp":int, "master_gastnr":int, "pr_flag":int, "mc_flag":bool, "gname":string, "adresse":string, "steuernr":string, "firma":string, "namekontakt":string, "phonetik3":string, "rabatt":Decimal, "endperiode":date, "firmen_nr":int, "land":string, "wohnort":string, "telefon":string, "plz":string, "geschlecht":string, "ausweis_nr1":string, "gastnr":int, "zahlungsart":int, "kreditlimit":Decimal, "bezeich":string, "alertbox":bool, "warningbox":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        return {"first_gastnr": first_gastnr, "curr_lname": curr_lname, "curr_fname": curr_fname, "total_record": total_record, "cntr": cntr, "t-guest": t_guest_data, "t-g": t_g_data}

    def case2a():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data


        pass

        if num1 == 0:

            guest = get_cache (Guest, {"name": [(eq, lname)],"karteityp": [(eq, sorttype)],"gastnr": [(gt, 0)]})

        if guest:

            for guest in db_session.query(Guest).filter(
                     ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (matches(Guest.name,("*" + lname + "*"))) & (matches((Guest.vorname1 + Guest.anredefirma),("*" + fname + "*"))))).order_by(Guest.name).all():
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
        else:

            if lname == chr_unicode(255):
                curr_lname = lname

                return

            for guest in db_session.query(Guest).filter(
                     ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (matches(Guest.name,("*" + lname + "*"))) & (matches((Guest.vorname1 + Guest.anredefirma),("*" + fname + "*"))))).order_by(Guest.name).all():
                counter = counter + 1

                if counter == 1:
                    first_gastnr = guest.gastnr

                if (counter >= 17) and (curr_lname != guest.name):
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


    def case2b():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        if substring(lname, length(lname) - 1, 1) != ("*").lower() :
            lname = lname + "*"

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0)) & ((Guest.karteityp == sorttype)) & (matches((Guest.name + Guest.vorname1),("*" + lname + "*")))).order_by(Guest.name).all():
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


    def case3a():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (matches(substring(Guest.name, 0, length(lname)),("*" + lname + "*"))) & (matches((Guest.vorname1 + Guest.anredefirma),("*" + fname + "*"))))).order_by(Guest.name).all():
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

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        if substring(lname, length(lname) - 1, 1) != ("*").lower() :
            lname = lname + "*"

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (matches((Guest.name + Guest.vorname1),("*" + lname + "*"))) & (matches((Guest.vorname1 + Guest.anredefirma),("*" + lname + "*"))))).order_by(Guest.name).all():
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

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        cardnum:string = ""
        from_pos:int = 0
        to_pos:int = 0
        cardnum = lname

        mc_guest = get_cache (Mc_guest, {"cardnum": [(eq, cardnum)]})

        if not mc_guest:
            from_pos = get_output(htpint(337))
            to_pos = get_output(htpint(338))

            if from_pos > 0 and to_pos > 0:
                cardnum = substring(cardnum, from_pos - 1, (to_pos - from_pos + 1))
                curr_fname = cardnum

                mc_guest = get_cache (Mc_guest, {"cardnum": [(eq, cardnum)]})

        if mc_guest:

            guest = get_cache (Guest, {"gastnr": [(eq, mc_guest.gastnr)]})
            t_guest = T_guest()
            t_guest_data.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = chr_unicode(255)


            check_prcode()


    def case5():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        cardnum:string = ""
        from_pos:int = 0
        to_pos:int = 0

        if lname == "":

            return

        for guest in db_session.query(Guest).filter(
                 (Guest.karteityp == 0) & (Guest.gastnr > 0) & (Guest.ausweis_nr1 == (lname).lower())).order_by(Guest.name).all():
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


    def case6():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        from_gastnr:int = 0
        from_gastnr = to_int(lname)

        for guest in db_session.query(Guest).filter(
                 (Guest.karteityp == sorttype) & (Guest.gastnr >= from_gastnr)).order_by(Guest.gastnr).all():
            counter = counter + 1

            if counter == 1:
                first_gastnr = guest.gastnr

            if counter >= 17:
                break
            t_guest = T_guest()
            t_guest_data.append(t_guest)

            buffer_copy(guest, t_guest)
            t_guest.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_guest.adresse = guest.adresse1 + " " + guest.adresse2
            t_guest.firma = guest.name + ", " + guest.anredefirma
            curr_lname = to_string(guest.gastnr + 1)
            curr_fname = guest.vorname1 + guest.anredefirma


            check_prcode()


    def case7():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        found:bool = False
        curr_gastnr:int = 0

        guest = get_cache (Guest, {"gastnr": [(eq, num1)]})

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

                if counter >= 17:
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


    def case8():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        guest = get_cache (Guest, {"gastnr": [(eq, to_int(lname))]})

        if not AVAILAB guest:

            return
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


    def case9():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        cl_member = get_cache (Cl_member, {"codenum": [(eq, lname)]})

        if cl_member:

            guest = get_cache (Guest, {"gastnr": [(eq, cl_member.gastnr)]})

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

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        for guest_pr in db_session.query(Guest_pr).filter(
                 (Guest_pr.gastnr == guest.gastnr)).order_by(Guest_pr._recid).all():

            ratecode = get_cache (Ratecode, {"code": [(eq, guest_pr.code)],"endperiode": [(gt, get_current_date())]})

            if ratecode:
                t_guest.pr_flag = 2

                return
            else:

                ratecode = get_cache (Ratecode, {"code": [(eq, guest_pr.code)]})

                if ratecode:
                    t_guest.pr_flag = 1


    def get_vipnr():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data

        htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})

        if htparam.finteger != 0:
            vipnr1 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})

        if htparam.finteger != 0:
            vipnr2 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})

        if htparam.finteger != 0:
            vipnr3 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})

        if htparam.finteger != 0:
            vipnr4 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})

        if htparam.finteger != 0:
            vipnr5 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})

        if htparam.finteger != 0:
            vipnr6 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})

        if htparam.finteger != 0:
            vipnr7 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})

        if htparam.finteger != 0:
            vipnr8 = htparam.finteger

        htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})

        if htparam.finteger != 0:
            vipnr9 = htparam.finteger


    def case10():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data


        cntr = 0

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (matches(Guest.name,("*" + lname + "*"))) & (matches((Guest.vorname1 + Guest.anredefirma),("*" + fname + "*"))))).order_by((Guest.vorname1 + Guest.anredefirma)).all():
            counter = counter + 1

            if counter == 1:
                first_gastnr = guest.gastnr

            if (counter >= 17) and (curr_lname != guest.name):
                break

            if (counter >= 17) and (curr_fname != (guest.vorname1 + guest.anredefirma)):
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
            cntr = counter


            check_prcode()

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0) & (Guest.karteityp == 0) & (matches(Guest.name,("*" + lname + "*"))) & (matches((Guest.vorname1 + Guest.anredefirma),("*" + fname + "*"))))).order_by((Guest.vorname1 + Guest.anredefirma)).all():
            ct = ct + 1

            if counter == 1:
                first_gastnr = guest.gastnr
            t_g = T_g()
            t_g_data.append(t_g)

            buffer_copy(guest, t_g)
            t_g.ctr = ct
            t_g.gname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                    " " + guest.anrede1
            t_g.adresse = guest.adresse1 + " " + guest.adresse2
            t_g.firma = guest.name + ", " + guest.anredefirma


            check_prcode()


    def case11():

        nonlocal first_gastnr, curr_lname, curr_fname, total_record, t_guest_data, counter, ct, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, guest, mc_guest, segment, guestseg, cl_member, guest_pr, ratecode, htparam
        nonlocal case_type, sorttype, lname, fname, num1, cntr


        nonlocal t_guest, t_g
        nonlocal t_guest_data


        t_guest_data.clear()

        for t_g in query(t_g_data, filters=(lambda t_g:(t_g.gastnr > 0 and t_g.karteityp == 0 and t_g.ctr > cntr)), sort_by=[("(",False))]:
            cntr = cntr + 1
            t_guest = T_guest()
            t_guest_data.append(t_guest)

            buffer_copy(t_g, t_guest)
            check_prcode()


    total_record =  to_decimal("0")

    for guest in db_session.query(Guest).filter(
             (Guest.karteityp == sorttype)).order_by(Guest._recid).all():
        total_record =  to_decimal(total_record) + to_decimal("1")

    if case_type == 1:

        for guest in db_session.query(Guest).filter(
                 ((Guest.gastnr > 0) & (Guest.karteityp == sorttype) & (Guest.name > trim(lname)))).order_by(Guest.name).all():
            counter = counter + 1

            if counter == 1:
                first_gastnr = guest.gastnr

            if (counter >= 17) and (curr_lname != guest.name):
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
    elif case_type == 2:

        if substring(lname, 0, 1) != ("*").lower() :
            case2a()

        elif length(lname) >= 2 and substring(lname, 0, 1) == ("*").lower() :
            case2b()
    elif case_type == 3:

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            case3a()

        elif length(lname) >= 2 and substring(lname, 0, 1) == ("*").lower() :
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
    elif case_type == 10:
        case10()
    elif case_type == 11:
        case11()
    get_vipnr()

    for t_guest in query(t_guest_data):

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, t_guest.gastnr)],"activeflag": [(eq, True)]})
        t_guest.mc_flag = None != mc_guest

        guestseg_obj_list = {}
        guestseg = Guestseg()
        segment = Segment()
        for guestseg.segmentcode, guestseg._recid, segment.bezeich, segment._recid in db_session.query(Guestseg.segmentcode, Guestseg._recid, Segment.bezeich, Segment._recid).join(Segment,(Segment.segmentcode == Guestseg.segmentcode) & (Segment.betriebsnr == 4)).filter(
                 (Guestseg.gastnr == t_guest.gastnr)).order_by(Guestseg._recid).all():
            if guestseg_obj_list.get(guestseg._recid):
                continue
            else:
                guestseg_obj_list[guestseg._recid] = True


            t_guest.warningbox = True
            t_guest.bezeich = entry(0, segment.bezeich, "$$0")
            break

        guestseg = db_session.query(Guestseg).filter(
                 (Guestseg.gastnr == t_guest.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

        if guestseg:

            segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})
            t_guest.alertbox = True
            t_guest.bezeich = entry(0, segment.bezeich, "$$0")

    return generate_output()