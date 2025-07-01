#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Bediener, Bk_raum, Ba_typ, Bk_veran, Bk_stat, Bk_func, Akt_kont

def bk_salestat_btn_go_webbl(sorttype:int, fdate:date, tdate:date):

    prepare_cache ([Guest, Bk_raum, Ba_typ, Bk_veran, Bk_stat, Bk_func, Akt_kont])

    output_list_list = []
    str1:string = ""
    totrmrev:Decimal = to_decimal("0.0")
    totfbrev:Decimal = to_decimal("0.0")
    totother:Decimal = to_decimal("0.0")
    totrev:Decimal = to_decimal("0.0")
    totpax:int = 0
    subrmrev:Decimal = to_decimal("0.0")
    subfbrev:Decimal = to_decimal("0.0")
    subother:Decimal = to_decimal("0.0")
    subrev:Decimal = to_decimal("0.0")
    subpax:int = 0
    guest = bediener = bk_raum = ba_typ = bk_veran = bk_stat = bk_func = akt_kont = None

    output_list = f_list = gast = usr = room = event = id = None

    output_list_list, Output_list = create_model("Output_list", {"flag":string, "bezeich":string, "room":string, "id":string, "ba_event":string, "datum":date, "pax":int, "rmrev":Decimal, "fbrev":Decimal, "othrev":Decimal, "totrev":Decimal, "ev_time":string, "main_contact":string})
    f_list_list, F_list = create_model("F_list", {"bname":string, "room":string, "id":string, "event":string, "cdate":date, "pax":int, "rmrev":Decimal, "fbrev":Decimal, "otrev":Decimal, "totrev":Decimal, "payment_id":string, "ev_time":string, "main_contact":string})

    Gast = create_buffer("Gast",Guest)
    Usr = create_buffer("Usr",Bediener)
    Room = create_buffer("Room",Bk_raum)
    Event = create_buffer("Event",Ba_typ)
    Id = create_buffer("Id",Bk_veran)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_veran, bk_stat, bk_func, akt_kont
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event, id


        nonlocal output_list, f_list, gast, usr, room, event, id
        nonlocal output_list_list, f_list_list

        return {"output-list": output_list_list}

    def create_browse():

        nonlocal output_list_list, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_veran, bk_stat, bk_func, akt_kont
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event, id


        nonlocal output_list, f_list, gast, usr, room, event, id
        nonlocal output_list_list, f_list_list

        groupby:string = ""
        line1:int = 0
        output_list_list.clear()
        create_list()
        totrmrev =  to_decimal("0")
        totfbrev =  to_decimal("0")
        totother =  to_decimal("0")
        totpax = 0
        totrev =  to_decimal("0")

        if sorttype == 0:

            for f_list in query(f_list_list, sort_by=[("id",False)]):
                line1 = line1 + 1

                if line1 == 1:
                    groupby = f_list.ID
                    create_group("SALES ID", groupby)

                if f_list.ID.lower()  != (groupby).lower() :
                    create_subtotal()
                    create_group("SALES ID", f_list.id)
                create_data()
                groupby = f_list.ID

        elif sorttype == 1:

            for f_list in query(f_list_list, sort_by=[("room",False)]):
                line1 = line1 + 1

                if line1 == 1:
                    groupby = f_list.room
                    create_group("ROOM", groupby)

                if f_list.room.lower()  != (groupby).lower() :
                    create_subtotal()
                    create_group("ROOM", f_list.room)
                create_data()
                groupby = f_list.room

        elif sorttype == 2:

            for f_list in query(f_list_list, sort_by=[("payment_id",False)]):
                line1 = line1 + 1

                if line1 == 1:
                    groupby = f_list.payment_id
                    create_group("INCHARGE", groupby)

                if f_list.room.lower()  != (groupby).lower() :
                    create_subtotal()
                    create_group("INCHARGE", f_list.payment_id)
                create_data()
                groupby = f_list.payment_id
        else:

            for f_list in query(f_list_list, sort_by=[("event",False)]):
                line1 = line1 + 1

                if line1 == 1:
                    groupby = f_list.event
                    create_group("EVENT", groupby)

                if f_list.event.lower()  != (groupby).lower() :
                    create_subtotal()
                    create_group("EVENT", f_list.event)
                create_data()
                groupby = f_list.event

        f_list = query(f_list_list, first=True)

        if f_list:
            create_subtotal()
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.flag = "TOTAL"
            output_list.bezeich = "T O T A L"
            output_list.pax = totpax
            output_list.rmrev =  to_decimal(totrmrev)
            output_list.fbrev =  to_decimal(totfbrev)
            output_list.othrev =  to_decimal(totother)
            output_list.totrev =  to_decimal(totrev)


    def create_list():

        nonlocal output_list_list, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_veran, bk_stat, bk_func, akt_kont
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event, id


        nonlocal output_list, f_list, gast, usr, room, event, id
        nonlocal output_list_list, f_list_list

        salesid:string = ""
        roomdesc:string = ""
        bname:string = ""
        other_rev:Decimal = to_decimal("0.0")
        eventdesc:string = ""
        id_name:string = ""
        id_sales:string = ""
        id_conv:string = ""
        ev_zeit:string = ""
        bguest = None
        Bguest =  create_buffer("Bguest",Guest)
        f_list_list.clear()

        for bk_stat in db_session.query(Bk_stat).filter(
                 (Bk_stat.datum >= fdate) & (Bk_stat.datum <= tdate) & (Bk_stat.isstatus == 0)).order_by(Bk_stat._recid).all():

            bk_veran = get_cache (Bk_veran, {"gastnr": [(eq, bk_stat.gastnr)]})

            room = get_cache (Bk_raum, {"raum": [(eq, bk_stat.room)]})

            if room:
                roomdesc = room.bezeich
            else:
                roomdesc = "Not defined"

            gast = get_cache (Guest, {"gastnr": [(eq, bk_stat.gastnr)]})

            if gast:
                bname = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
            else:
                bname = "Not defined"

            event = get_cache (Ba_typ, {"typ_id": [(eq, bk_stat.event_nr)]})

            if event:
                eventdesc = event.bezeichnung

            id = get_cache (Bk_veran, {"veran_nr": [(eq, bk_stat.resnr)]})

            if id:

                if num_entries(id.payment_userinit[8], chr_unicode(2)) >= 2:
                    id_sales = entry(0, id.payment_userinit[8], chr_unicode(2))
                    id_conv = entry(1, id.payment_userinit[8], chr_unicode(2))


                else:

                    bguest = get_cache (Guest, {"gastnr": [(eq, id.gastnr)]})

                    if bguest:
                        id_sales = guest.phonetik3
                        id_conv = guest.phonetik2

            bk_func = get_cache (Bk_func, {"veran_nr": [(eq, bk_stat.resnr)],"veran_seite": [(eq, bk_stat.reslinnr)],"raeume[0]": [(eq, bk_stat.room)]})

            if bk_func:
                ev_zeit = bk_func.uhrzeit
            f_list = F_list()
            f_list_list.append(f_list)

            f_list.bname = bname
            f_list.room = roomdesc
            f_list.id = id_sales
            f_list.event = eventdesc
            f_list.cdate = bk_stat.datum
            f_list.pax = bk_stat.pax
            f_list.rmrev =  to_decimal(bk_stat.rm_rev)
            f_list.fbrev =  to_decimal(bk_stat.fb_rev)
            f_list.otrev =  to_decimal(bk_stat.other_rev)
            f_list.totrev =  to_decimal(bk_stat.rm_rev) + to_decimal(bk_stat.fb_rev) + to_decimal(bk_stat.other_rev)
            f_list.payment_id = id_conv
            f_list.ev_time = ev_zeit

            akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, bk_stat.gastnr)]})

            if akt_kont:
                f_list.main_contact = akt_kont.name


    def create_group(bezeich:string, bezeich1:string):

        nonlocal output_list_list, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_veran, bk_stat, bk_func, akt_kont
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event, id


        nonlocal output_list, f_list, gast, usr, room, event, id
        nonlocal output_list_list, f_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "GROUP"
        output_list.bezeich = bezeich + " : " + bezeich1


    def create_data():

        nonlocal output_list_list, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_veran, bk_stat, bk_func, akt_kont
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event, id


        nonlocal output_list, f_list, gast, usr, room, event, id
        nonlocal output_list_list, f_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.bezeich = f_list.bname
        output_list.room = f_list.room
        output_list.id = f_list.ID
        output_list.ba_event = f_list.EVENT
        output_list.datum = f_list.cDATE
        output_list.pax = f_list.pax
        output_list.rmrev =  to_decimal(f_list.rmrev)
        output_list.fbrev =  to_decimal(f_list.fbrev)
        output_list.othrev =  to_decimal(f_list.otrev)
        output_list.totrev =  to_decimal(f_list.totrev)
        output_list.ev_time = f_list.ev_time
        output_list.main_contact = f_list.main_contact


        subpax = subpax + f_list.pax
        subrmrev =  to_decimal(subrmrev) + to_decimal(f_list.rmrev)
        subfbrev =  to_decimal(subfbrev) + to_decimal(f_list.fbrev)
        subother =  to_decimal(subother) + to_decimal(f_list.otrev)
        subrev =  to_decimal(subrev) + to_decimal(f_list.totrev)
        totpax = totpax + f_list.pax
        totrmrev =  to_decimal(totrmrev) + to_decimal(f_list.rmrev)
        totfbrev =  to_decimal(totfbrev) + to_decimal(f_list.fbrev)
        totother =  to_decimal(totother) + to_decimal(f_list.otrev)
        totrev =  to_decimal(totrev) + to_decimal(f_list.totrev)


    def create_subtotal():

        nonlocal output_list_list, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_veran, bk_stat, bk_func, akt_kont
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event, id


        nonlocal output_list, f_list, gast, usr, room, event, id
        nonlocal output_list_list, f_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "LINE"


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "SUB"
        output_list.bezeich = "Subtotal"
        output_list.pax = subpax
        output_list.rmrev =  to_decimal(subrmrev)
        output_list.fbrev =  to_decimal(subfbrev)
        output_list.othrev =  to_decimal(subother)
        output_list.totrev =  to_decimal(subrev)

        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "SPACE"
        subpax = 0
        subrmrev =  to_decimal("0")
        subfbrev =  to_decimal("0")
        subother =  to_decimal("0")
        subrev =  to_decimal("0")


    create_browse()

    return generate_output()