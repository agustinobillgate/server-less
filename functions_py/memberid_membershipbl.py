#using conversion tools version: 1.0.0.117
#----------------------------------------
# Rd, 26/11/2025, Update with_for_update
#----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.if_siteminder_read_mappingbl import if_siteminder_read_mappingbl
from models import Guest, Mc_guest, Mc_types, Bediener, Res_history, Nation

member_list_data, Member_list = create_model("Member_list", {"member_code":string, "member_type":string, "titled":string, "fullname":string, "firstname":string, "lastname":string, "email":string, "mobilenumber":string, "birthdate":date, "gender":string, "country":string, "city":string, "address":string, "stamps":int, "reg_date":date, "is_active":bool})

def memberid_membershipbl(case_type:int, gastnr:int, member_list_data:[Member_list], user_init:string):

    prepare_cache ([Guest, Mc_guest, Mc_types, Bediener, Res_history, Nation])

    updated = False
    nr:int = 0
    t_guest_nat:string = ""
    guest = mc_guest = mc_types = bediener = res_history = nation = None

    member_list = bguest = None

    Bguest = create_buffer("Bguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal updated, nr, t_guest_nat, guest, mc_guest, mc_types, bediener, res_history, nation
        nonlocal case_type, gastnr, user_init
        nonlocal bguest


        nonlocal member_list, bguest

        return {"updated": updated}

    member_list = query(member_list_data, first=True)

    if case_type == 1:

        # mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, gastnr)]})
        mc_guest = db_session.query(Mc_guest).filter(Mc_guest.gastnr == gastnr).with_for_update().first()

        if not mc_guest:
            mc_guest = Mc_guest()
            db_session.add(mc_guest)

            mc_guest.gastnr = gastnr
            mc_guest.cardnum = member_list.member_code
            mc_guest.number1 = member_list.stamps
            mc_guest.activeflag = member_list.is_active

            mc_types = get_cache (Mc_types, {"bezeich": [(eq, member_list.member_type)]})

            if mc_types:
                mc_guest.nr = mc_types.nr

            elif not mc_types:

                mc_types = db_session.query(Mc_types).order_by(Mc_types._recid.desc()).first()

                if mc_types:
                    nr = mc_types.nr + 1
                mc_types = Mc_types()
                db_session.add(mc_types)

                mc_types.bezeich = member_list.member_type
                mc_types.nr = nr
                mc_guest.nr = nr

            # bguest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
            bguest = db_session.query(Guest).filter(Guest.gastnr == gastnr).with_for_update().first()

            if bguest:

                if member_list.birthdate != None:
                    bguest.geburtdatum1 = member_list.birthdate

                if member_list.email != "":
                    bguest.email_adr = member_list.email

                if member_list.mobilenumber != "":
                    bguest.mobil_telefon = member_list.mobilenumber
            pass
            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Membership"


                res_history.aenderung = "Create/Tag MemberID " + member_list.member_code + " to PMS, Date:" + to_string(get_current_date(), "99/99/99") + "."

        elif mc_guest:
            pass
            mc_guest.cardnum = member_list.member_code
            mc_guest.number1 = member_list.stamps
            mc_guest.activeflag = member_list.is_active

            # mc_types = get_cache (Mc_types, {"bezeich": [(eq, member_list.member_type)]})
            mc_types = db_session.query(Mc_types).filter(Mc_types.bezeich == member_list.member_type).with_for_update().first()

            if mc_types:
                mc_guest.nr = mc_types.nr

            if not mc_types:

                mc_types = db_session.query(Mc_types).order_by(Mc_types._recid.desc()).first()
                nr = mc_types.nr + 1
                mc_types = Mc_types()
                db_session.add(mc_types)

                mc_types.bezeich = member_list.member_type
                mc_types.nr = nr
                mc_guest.nr = nr


            pass
            pass

            # bguest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
            bguest = db_session.query(Guest).filter(Guest.gastnr == gastnr).with_for_update().first()

            if bguest:

                if member_list.birthdate != None:
                    bguest.geburtdatum1 = member_list.birthdate

                if member_list.email != "":
                    bguest.email_adr = member_list.email

                if member_list.mobilenumber != "":
                    bguest.mobil_telefon = member_list.mobilenumber
            pass
            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Membership"


                res_history.aenderung = "updated MemberID " + member_list.member_code + " to PMS, Date:" + to_string(get_current_date(), "99/99/99") + "."
    elif case_type == 2:

        # mc_guest = get_cache (Mc_guest, {"cardnum": [(eq, member_list.member_code)]})
        mc_guest = db_session.query(Mc_guest).filter(Mc_guest.cardnum == member_list.member_code).with_for_update().first()

        if mc_guest:
            gastnr = mc_guest.gastnr
            pass
            mc_guest.cardnum = member_list.member_code
            mc_guest.number1 = member_list.stamps
            mc_guest.activeflag = member_list.is_active

            # mc_types = get_cache (Mc_types, {"bezeich": [(eq, member_list.member_type)]})
            mc_types = db_session.query(Mc_types).filter(Mc_types.bezeich == member_list.member_type).with_for_update().first()

            if mc_types:
                mc_guest.nr = mc_types.nr

            if not mc_types:

                mc_types = db_session.query(Mc_types).order_by(Mc_types._recid.desc()).first()
                nr = mc_types.nr + 1
                mc_types = Mc_types()
                db_session.add(mc_types)

                mc_types.bezeich = member_list.member_type
                mc_types.nr = nr
                mc_guest.nr = nr


            pass
            pass

            # bguest = get_cache (Guest, {"gastnr": [(eq, gastnr)]})
            bguest = db_session.query(Guest).filter(Guest.gastnr == gastnr).with_for_update().first()

            if bguest:

                if member_list.birthdate != None:
                    bguest.geburtdatum1 = member_list.birthdate

                if member_list.email != "":
                    bguest.email_adr = member_list.email

                if member_list.mobilenumber != "":
                    bguest.mobil_telefon = member_list.mobilenumber
            pass
            pass

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Membership"


                res_history.aenderung = "updated MemberID " + member_list.member_code + " to PMS FROM Outlet Sync,Date:" + to_string(get_current_date(), "99/99/99") + "."

        elif not mc_guest:

            guest = db_session.query(Guest).filter(
                     (matches(Guest.name,member_list.lastname)) & (Guest.email_adr == member_list.email)).first()

            if not guest:

                guest = db_session.query(Guest).filter(
                         (matches(Guest.name,member_list.lastname)) & (Guest.mobil_telefon == member_list.mobilenumber)).first()

            if not guest:

                guest = get_cache (Guest, {"name": [(eq, member_list.fullname)],"email_adr": [(eq, member_list.email)]})

            if not guest:

                guest = get_cache (Guest, {"name": [(eq, member_list.fullname)],"mobil_telefon": [(eq, member_list.mobilenumber)]})

            if not guest:

                guest = get_cache (Guest, {"email_adr": [(eq, member_list.email)]})

            if not guest:

                guest = get_cache (Guest, {"mobil_telefon": [(eq, member_list.mobilenumber)]})

            if not guest:

                guest = get_cache (Guest, {"name": [(eq, member_list.fullname)]})

            if not guest:

                nation = get_cache (Nation, {"bezeich": [(eq, member_list.country)]})

                if nation:
                    t_guest_nat = nation.kurzbez
                else:
                    t_guest_nat = get_output(if_siteminder_read_mappingbl(2, member_list.country))

                    if t_guest_nat != "":

                        nation = get_cache (Nation, {"kurzbez": [(eq, t_guest_nat)]})

                        if nation:
                            t_guest_nat = nation.kurzbez
                    else:

                        nation = db_session.query(Nation).filter(
                                 (matches(Nation.bezeich,"*Unknown*"))).first()

                        if nation:
                            t_guest_nat = nation.kurzbez

                # guest = db_session.query(Guest).order_by(Guest._recid.desc()).first()
                guest = db_session.query(Guest).order_by(Guest.gastnr.desc()).first()

                if guest:
                    gastnr = guest.gastnr + 1
                guest = Guest()
                db_session.add(guest)

                guest.gastnr = gastnr
                guest.anrede1 = member_list.titled
                guest.name = member_list.firstname
                guest.vorname1 = member_list.lastname
                guest.adresse1 = member_list.address
                guest.wohnort = member_list.city
                guest.land = t_guest_nat
                guest.email_adr = member_list.email
                guest.mobil_telefon = member_list.mobilenumber
                guest.nation1 = t_guest_nat
                guest.geburtdatum1 = member_list.birthdate

                if guest.name == "":
                    guest.name = member_list.fullname


            else:
                gastnr = guest.gastnr

                # bguest = get_cache (Guest, {"_recid": [(eq, guest._recid)]})
                bguest = db_session.query(Guest).filter(Guest._recid == guest._recid).with_for_update().first()

                if bguest:
                    bguest.anrede1 = member_list.titled
                    bguest.email_adr = member_list.email
                    bguest.geburtdatum1 = member_list.birthdate
                    bguest.mobil_telefon = member_list.mobilenumber


                pass
                pass
            mc_guest = Mc_guest()
            db_session.add(mc_guest)

            mc_guest.gastnr = gastnr
            mc_guest.cardnum = member_list.member_code
            mc_guest.number1 = member_list.stamps
            mc_guest.activeflag = member_list.is_active

            # mc_types = get_cache (Mc_types, {"bezeich": [(eq, member_list.member_type)]})
            mc_types = db_session.query(Mc_types).filter(Mc_types.bezeich == member_list.member_type).with_for_update().first()

            if mc_types:
                mc_guest.nr = mc_types.nr

            elif not mc_types:

                mc_types = db_session.query(Mc_types).order_by(Mc_types._recid.desc()).first()

                if mc_types:
                    nr = mc_types.nr + 1
                mc_types = Mc_types()
                db_session.add(mc_types)

                mc_types.bezeich = member_list.member_type
                mc_types.nr = nr
                mc_guest.nr = nr

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Membership"


                res_history.aenderung = "Create/Tag MemberID " + member_list.member_code + " to PMS FROM Outlet Sync,Date:" + to_string(get_current_date(), "99/99/99") + "."
    updated = True

    return generate_output()