#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from sqlalchemy import func
from models import Guest

def gcf_check_same_guestbl(casetype:int, gastno:int, email_adr:string, mobil_phone:string):

    prepare_cache ([Guest])

    same_guest = False
    tlist_list = []
    gphone:string = ""
    guest = None

    tlist = bguest = None

    tlist_list, Tlist = create_model("Tlist", {"gastno":int})

    Bguest = create_buffer("Bguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal same_guest, tlist_list, gphone, guest
        nonlocal casetype, gastno, email_adr, mobil_phone
        nonlocal bguest


        nonlocal tlist, bguest
        nonlocal tlist_list

        return {"same_guest": same_guest, "tlist": tlist_list}


    tlist_list.clear()

    if casetype == 1:

        guest = get_cache (Guest, {"gastnr": [(eq, gastno)],"karteityp": [(eq, 0)]})

        if guest:

            if matches(guest.mobil_telefon,r"62*"):
                gphone = replace_str(substring(guest.mobil_telefon, 0, 2) , "62", "0") + substring(guest.mobil_telefon, 2)

            elif matches(guest.mobil_telefon,r"+62*"):
                gphone = replace_str(substring(guest.mobil_telefon, 0, 3) , "+62", "0") + substring(guest.mobil_telefon, 3)

            elif matches(guest.mobil_telefon,r"*-*"):
                gphone = replace_str(guest.mobil_telefon, "-", "")

            if matches(guest.mobil_telefon,r"62*"):
                gphone = replace_str(substring(guest.mobil_telefon, 0, 3) , "62 ", "0") + trim(substring(guest.mobil_telefon, 3))

            if substring(guest.mobil_telefon, 1, 1) == chr_unicode(32):
                gphone = replace_str(guest.mobil_telefon, " ", "")

            if guest.email_adr != " ":

                for bguest in db_session.query(Bguest).filter(
                         (Bguest.gastnr != guest.gastnr) & (Bguest.email_adr == guest.email_adr)).order_by(Bguest._recid).all():

                    tlist = query(tlist_list, filters=(lambda tlist: tlist.gastno == bguest.gastnr), first=True)

                    if not tlist:
                        tlist = Tlist()
                        tlist_list.append(tlist)

                        tlist.gastno = bguest.gastnr

            elif gphone != "":

                bguest = db_session.query(Bguest).filter(
                         (Bguest.gastnr != guest.gastnr) & (matches(Bguest.mobil_telefon,("*" + gphone)))).first()

                if bguest:

                    for bguest in db_session.query(Bguest).filter(
                             (Bguest.gastnr != guest.gastnr) & (matches(Bguest.mobil_telefon,("*" + gphone)))).order_by(Bguest._recid).all():

                        tlist = query(tlist_list, filters=(lambda tlist: tlist.gastno == bguest.gastnr), first=True)

                        if not tlist:
                            tlist = Tlist()
                            tlist_list.append(tlist)

                            tlist.gastno = bguest.gastnr


                else:

                    for bguest in db_session.query(Bguest).filter(
                             (Bguest.gastnr != guest.gastnr) & (Bguest.mobil_telefon == guest.mobil_telefon)).order_by(Bguest._recid).all():

                        tlist = query(tlist_list, filters=(lambda tlist: tlist.gastno == bguest.gastnr), first=True)

                        if not tlist:
                            tlist = Tlist()
                            tlist_list.append(tlist)

                            tlist.gastno = bguest.gastnr

    elif casetype == 2:

        if email_adr != "":

            for bguest in db_session.query(Bguest).filter(
                     (Bguest.gastnr != gastno) & (Bguest.email_adr == (email_adr).lower())).order_by(Bguest._recid).all():

                tlist = query(tlist_list, filters=(lambda tlist: tlist.gastno == bguest.gastnr), first=True)

                if not tlist:
                    tlist = Tlist()
                    tlist_list.append(tlist)

                    tlist.gastno = bguest.gastnr

        elif mobil_phone != "":

            if matches(mobil_phone,r"62*"):
                gphone = replace_str(substring(mobil_phone, 0, 2) , "62", "0") + substring(mobil_phone, 2)

            elif matches(mobil_phone,r"+62*"):
                gphone = replace_str(substring(mobil_phone, 0, 3) , "+62", "0") + substring(mobil_phone, 3)

            elif matches(mobil_phone,r"*-*"):
                gphone = replace_str(mobil_phone, "-", "")

            if matches(mobil_phone,r"62*"):
                gphone = replace_str(substring(mobil_phone, 0, 3) , "62 ", "0") + trim(substring(mobil_phone, 3))

            if substring(mobil_phone, 1, 1) == chr_unicode(32):
                gphone = replace_str(mobil_phone, " ", "")

            for bguest in db_session.query(Bguest).filter(
                     (Bguest.gastnr != gastno) & (matches(Bguest.mobil_telefon,("*" + gphone)))).order_by(Bguest._recid).all():

                tlist = query(tlist_list, filters=(lambda tlist: tlist.gastno == bguest.gastnr), first=True)

                if not tlist:
                    tlist = Tlist()
                    tlist_list.append(tlist)

                    tlist.gastno = bguest.gastnr

    tlist = query(tlist_list, first=True)

    if tlist:
        same_guest = True

    return generate_output()