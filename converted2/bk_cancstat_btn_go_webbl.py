#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Guest, Bediener, Bk_raum, Ba_typ, Bk_stat

def bk_cancstat_btn_go_webbl(sorttype:int, fdate:date, tdate:date):

    prepare_cache ([Guest, Bk_raum, Ba_typ, Bk_stat])

    output_list_data = []
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
    guest = bediener = bk_raum = ba_typ = bk_stat = None

    f_list = output_list = gast = usr = room = event = None

    f_list_data, F_list = create_model("F_list", {"bname":string, "room":string, "id":string, "event":string, "cdate":date, "cancel":date, "pax":int, "rmrev":Decimal, "fbrev":Decimal, "otrev":Decimal, "totrev":Decimal})
    output_list_data, Output_list = create_model("Output_list", {"flag":string, "bezeich":string, "room":string, "id":string, "ba_event":string, "datum":date, "cancel":date, "pax":int, "rmrev":Decimal, "fbrev":Decimal, "othrev":Decimal, "totrev":Decimal})

    Gast = create_buffer("Gast",Guest)
    Usr = create_buffer("Usr",Bediener)
    Room = create_buffer("Room",Bk_raum)
    Event = create_buffer("Event",Ba_typ)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_stat
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event


        nonlocal f_list, output_list, gast, usr, room, event
        nonlocal f_list_data, output_list_data

        return {"output-list": output_list_data}

    def create_browse():

        nonlocal output_list_data, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_stat
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event


        nonlocal f_list, output_list, gast, usr, room, event
        nonlocal f_list_data, output_list_data

        groupby:string = ""
        line1:int = 0
        output_list_data.clear()
        create_list()
        totrmrev =  to_decimal("0")
        totfbrev =  to_decimal("0")
        totother =  to_decimal("0")
        totpax = 0
        totrev =  to_decimal("0")

        if sorttype == 0:

            for f_list in query(f_list_data, sort_by=[("id",False)]):
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

            for f_list in query(f_list_data, sort_by=[("room",False)]):
                line1 = line1 + 1

                if line1 == 1:
                    groupby = f_list.room
                    create_group("ROOM", groupby)

                if f_list.room.lower()  != (groupby).lower() :
                    create_subtotal()
                    create_group("ROOM", f_list.room)
                create_data()
                groupby = f_list.room
        else:

            for f_list in query(f_list_data, sort_by=[("event",False)]):
                line1 = line1 + 1

                if line1 == 1:
                    groupby = f_list.event
                    create_group("EVENT", groupby)

                if f_list.event.lower()  != (groupby).lower() :
                    create_subtotal()
                    create_group("EVENT", f_list.event)
                create_data()
                groupby = f_list.event

        f_list = query(f_list_data, first=True)

        if f_list:
            create_subtotal()
            output_list = Output_list()
            output_list_data.append(output_list)

            output_list.flag = "TOTAL"
            output_list.bezeich = "T O T A L"
            output_list.pax = totpax
            output_list.rmrev =  to_decimal(totrmrev)
            output_list.fbrev =  to_decimal(totfbrev)
            output_list.othrev =  to_decimal(totother)
            output_list.totrev =  to_decimal(totrev)


    def create_data():

        nonlocal output_list_data, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_stat
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event


        nonlocal f_list, output_list, gast, usr, room, event
        nonlocal f_list_data, output_list_data


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = f_list.bname
        output_list.room = f_list.room
        output_list.id = f_list.ID
        output_list.ba_event = f_list.EVENT
        output_list.datum = f_list.cDATE
        output_list.cancel = f_list.cancel
        output_list.pax = f_list.pax
        output_list.rmrev =  to_decimal(f_list.rmrev)
        output_list.fbrev =  to_decimal(f_list.fbrev)
        output_list.othrev =  to_decimal(f_list.otrev)
        output_list.totrev =  to_decimal(f_list.totrev)


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


    def create_list():

        nonlocal output_list_data, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_stat
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event


        nonlocal f_list, output_list, gast, usr, room, event
        nonlocal f_list_data, output_list_data

        salesid:string = ""
        roomdesc:string = ""
        bname:string = ""
        other_rev:Decimal = to_decimal("0.0")
        eventdesc:string = ""
        f_list_data.clear()

        for bk_stat in db_session.query(Bk_stat).filter(
                 (Bk_stat.datum >= fdate) & (Bk_stat.datum <= tdate) & (Bk_stat.isstatus == 9)).order_by(Bk_stat._recid).all():

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
            f_list = F_list()
            f_list_data.append(f_list)

            f_list.bname = bname
            f_list.room = roomdesc
            f_list.id = bk_stat.salesid
            f_list.event = eventdesc
            f_list.cdate = bk_stat.datum
            f_list.cancel = bk_stat.cancel_date
            f_list.pax = bk_stat.pax
            f_list.rmrev =  to_decimal(bk_stat.rm_rev)
            f_list.fbrev =  to_decimal(bk_stat.fb_rev)
            f_list.otrev =  to_decimal(bk_stat.other_rev)
            f_list.totrev =  to_decimal(bk_stat.rm_rev) + to_decimal(bk_stat.fb_rev) +\
                    bk_stat.other_rev


    def create_group(bezeich:string, bezeich1:string):

        nonlocal output_list_data, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_stat
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event


        nonlocal f_list, output_list, gast, usr, room, event
        nonlocal f_list_data, output_list_data


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = "GROUP"
        output_list.bezeich = bezeich + " : " + bezeich1


    def create_subtotal():

        nonlocal output_list_data, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, guest, bediener, bk_raum, ba_typ, bk_stat
        nonlocal sorttype, fdate, tdate
        nonlocal gast, usr, room, event


        nonlocal f_list, output_list, gast, usr, room, event
        nonlocal f_list_data, output_list_data


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = "LINE"


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = "SUB"
        output_list.bezeich = "Subtotal"
        output_list.pax = subpax
        output_list.rmrev =  to_decimal(subrmrev)
        output_list.fbrev =  to_decimal(subfbrev)
        output_list.othrev =  to_decimal(subother)
        output_list.totrev =  to_decimal(subrev)


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = "SPACE"
        subrmrev =  to_decimal("0")
        subfbrev =  to_decimal("0")
        subother =  to_decimal("0")
        subrev =  to_decimal("0")
        subpax = 0


    create_browse()

    return generate_output()