#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd, 21/8/2025
# gitlab: 
# rmBuff, range (int())
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_raum, Guest, Bediener, Ba_typ, Bk_func, Bk_veran, Artikel, Bk_rart, B_history

def bk_sakesfcast_btn_go_webbl(checklist:bool, sorttype:int, fdate:date, tdate:date, disp_flag:int):

    prepare_cache ([Bk_raum, Guest, Bediener, Bk_func, Bk_veran, Artikel, Bk_rart, B_history])

    output_list_data = []
    cob:string = ""
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
    bk_raum = guest = bediener = ba_typ = bk_func = bk_veran = artikel = bk_rart = b_history = None

    f_list = output_list = room = gast = usr = event = None

    f_list_data, F_list = create_model("F_list", {"rstat":string, "bname":string, "room":string, "id":string, "event":string, "cdate":date, "pax":int, "rmrev":Decimal, "fbrev":Decimal, "otrev":Decimal, "totrev":Decimal, "cp":string, "resnr":int, "date_book":date, "in_sales":string, "sales":string, "ev_time":string})
    output_list_data, Output_list = create_model("Output_list", {"flag":string, "bezeich":string, "rstat":string, "room":string, "id":string, "ba_event":string, "datum":date, "pax":int, "rmrev":Decimal, "fbrev":Decimal, "othrev":Decimal, "totrev":Decimal, "cp":string, "resnr":int, "date_book":date, "in_sales":string, "ev_time":string})

    Room = create_buffer("Room",Bk_raum)
    Gast = create_buffer("Gast",Guest)
    Usr = create_buffer("Usr",Bediener)
    Event = create_buffer("Event",Ba_typ)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_data, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, artikel, bk_rart, b_history
        nonlocal checklist, sorttype, fdate, tdate, disp_flag
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_data, output_list_data

        return {"output-list": output_list_data}

    def create_browse():

        nonlocal output_list_data, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, artikel, bk_rart, b_history
        nonlocal checklist, sorttype, fdate, tdate, disp_flag
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_data, output_list_data

        groupby:string = ""
        line1:int = 0
        output_list_data.clear()
        create_list()
        totrmrev =  to_decimal("0")
        totfbrev =  to_decimal("0")
        totpax = 0
        totrev =  to_decimal("0")
        totother =  to_decimal("0")

        if not checklist:

            if sorttype == 0:

                if disp_flag == 1:

                    for f_list in query(f_list_data, sort_by=[("sales",False),("cdate",False),("room",False)]):
                        line1 = line1 + 1

                        if line1 == 1:
                            groupby = f_list.sales
                            create_group("SALES ID", groupby)

                        if f_list.sales.lower()  != (groupby).lower() :
                            create_subtotal()
                            create_group("SALES ID", f_list.sales)
                        create_data()
                        groupby = f_list.sales

                elif disp_flag == 2:

                    for f_list in query(f_list_data, sort_by=[("in_sales",False),("cdate",False),("room",False)]):
                        line1 = line1 + 1

                        if line1 == 1:
                            groupby = f_list.in_sales
                            create_group("SALES INCHARGE", groupby)

                        if f_list.in_sales.lower()  != (groupby).lower() :
                            create_subtotal()
                            create_group("SALES INCHARGE", f_list.in_sales)
                        create_data()
                        groupby = f_list.in_sales

            elif sorttype == 1:

                for f_list in query(f_list_data, sort_by=[("room",False),("cdate",False)]):
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

                for f_list in query(f_list_data, sort_by=[("event",False),("cdate",False),("room",False)]):
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


        else:

            if sorttype == 0:

                if disp_flag == 1:

                    for f_list in query(f_list_data, sort_by=[("sales",False),("cdate",False),("room",False)]):
                        line1 = line1 + 1

                        if line1 == 1:
                            groupby = f_list.sales
                            create_group("SALES ID", groupby)

                        if f_list.sales.lower()  != (groupby).lower() :
                            create_subtotal()
                            create_group("SALES ID", f_list.sales)
                        create_data()
                        groupby = f_list.sales

                elif disp_flag == 2:

                    for f_list in query(f_list_data, sort_by=[("in_sales",False),("cdate",False),("room",False)]):
                        line1 = line1 + 1

                        if line1 == 1:
                            groupby = f_list.in_sales
                            create_group("SALES INCHARGE", groupby)

                        if f_list.in_sales.lower()  != (groupby).lower() :
                            create_subtotal()
                            create_group("SALES INCHARGE", f_list.in_sales)
                        create_data()
                        groupby = f_list.in_sales

            elif sorttype == 1:

                for f_list in query(f_list_data, sort_by=[("room",False),("cdate",False)]):
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

                for f_list in query(f_list_data, sort_by=[("event",False),("cdate",False),("room",False)]):
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


    def create_group(bezeich:string, bezeich1:string):

        nonlocal output_list_data, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, artikel, bk_rart, b_history
        nonlocal checklist, sorttype, fdate, tdate, disp_flag
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_data, output_list_data


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.flag = "GROUP"

        if bezeich.lower()  == ("SALES ID").lower()  or bezeich.lower()  == ("SALES INCHARGE").lower() :
            output_list.bezeich = bezeich1
        else:
            output_list.bezeich = bezeich + " : " + bezeich1


    def create_data():

        nonlocal output_list_data, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, artikel, bk_rart, b_history
        nonlocal checklist, sorttype, fdate, tdate, disp_flag
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_data, output_list_data


        output_list = Output_list()
        output_list_data.append(output_list)

        output_list.bezeich = f_list.bname
        output_list.room = f_list.room
        # Rd 21/8/2025
        # output_list.id = f_list.ID
        # output_list.ba_event = f_list.EVENT
        # output_list.datum = f_list.cDATE
        output_list.id = f_list.id
        output_list.ba_event = f_list.event
        output_list.datum = f_list.cdate

        output_list.pax = f_list.pax
        output_list.rmrev =  to_decimal(f_list.rmrev)
        output_list.fbrev =  to_decimal(f_list.fbrev)
        output_list.othrev =  to_decimal(f_list.otrev)
        output_list.totrev =  to_decimal(f_list.totrev)
        output_list.resnr = f_list.resnr
        output_list.cp = f_list.cp
        output_list.rstat = f_list.rstat
        output_list.date_book = f_list.date_book
        output_list.in_sales = f_list.in_sales
        output_list.ev_time = f_list.ev_time


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

        nonlocal output_list_data, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, artikel, bk_rart, b_history
        nonlocal checklist, sorttype, fdate, tdate, disp_flag
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_data, output_list_data

        salesid:string = ""
        salesid2:string = ""
        roomdesc:string = ""
        bname:string = ""
        other_rev:Decimal = to_decimal("0.0")
        fb_rev:Decimal = to_decimal("0.0")
        in_sales:string = ""
        in_sales1:string = ""
        in_sales2:string = ""
        datum:date = None
        found_chr2:bool = False
        count_i:int = 0
        bq_resnr:int = 0
        bq_reslinnr:int = 0
        f_list_data.clear()

        if not checklist:
            for datum in date_range(fdate,tdate) :

                bk_func = get_cache (Bk_func, {"datum": [(eq, datum)]})

                if bk_func:

                    bk_func_obj_list = {}
                    bk_func = Bk_func()
                    bk_veran = Bk_veran()
                    for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.zweck, bk_func.datum, bk_func.rpersonen, bk_func.rpreis, bk_func.kontaktperson, bk_func.auf__datum, bk_func.uhrzeit, bk_func.resstatus, bk_func._recid, bk_veran.gastnr, bk_veran.payment_userinit, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.zweck, Bk_func.datum, Bk_func.rpersonen, Bk_func.rpreis, Bk_func.kontaktperson, Bk_func.auf__datum, Bk_func.uhrzeit, Bk_func.resstatus, Bk_func._recid, Bk_veran.gastnr, Bk_veran.payment_userinit, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                             (Bk_func.datum == datum) & (Bk_func.resstatus == 1)).order_by(Bk_func.datum).all():
                        if bk_func_obj_list.get(bk_func._recid):
                            continue
                        else:
                            bk_func_obj_list[bk_func._recid] = True


                        fb_rev =  to_decimal("0")
                        other_rev =  to_decimal("0")

                        room = get_cache (Bk_raum, {"raum": [(eq, bk_func.raeume[0])]})

                        if room:
                            roomdesc = room.bezeich
                        else:
                            roomdesc = "Not defined"

                        gast = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                        if gast:
                            bname = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:
                            bname = "Not defined"

                        bk_rart_obj_list = {}
                        bk_rart = Bk_rart()
                        artikel = Artikel()
                        for bk_rart.preis, bk_rart.anzahl, bk_rart._recid, artikel.umsatzart, artikel._recid in db_session.query(Bk_rart.preis, Bk_rart.anzahl, Bk_rart._recid, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == Bk_rart.veran_artnr) & (Artikel.departement == Bk_rart.departement)).filter(
                                 (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                            if bk_rart_obj_list.get(bk_rart._recid):
                                continue
                            else:
                                bk_rart_obj_list[bk_rart._recid] = True

                            if (artikel.umsatzart == 5 or artikel.umsatzart == 3 or artikel.umsatzart == 6):
                                fb_rev =  to_decimal(fb_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))

                            elif artikel.umsatzart == 4:
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))
                        in_sales1 = trim(bk_veran.payment_userinit[8])
                        for count_i in range(1,length(in_sales1)  + 1) :

                            if substring(in_sales1, count_i - 1, 1) == chr_unicode(2):
                                found_chr2 = True
                                break

                        if found_chr2:

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(0, in_sales1, chr_unicode(2)))]})

                            if usr:
                                in_sales = to_string(usr.userinit + " - " + usr.username)
                            else:
                                in_sales = "**"

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(1, in_sales1, chr_unicode(2)))]})

                            if usr:
                                salesid2 = to_string(usr.userinit + " - " + usr.username)
                            else:
                                salesid2 = "**"
                        else:

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(0, in_sales1, chr_unicode(2)))]})

                            if usr:
                                in_sales = to_string(usr.userinit + " - " + usr.username)
                            else:
                                in_sales = "**"
                        found_chr2 = False
                        f_list = F_list()
                        f_list_data.append(f_list)

                        f_list.bname = bname
                        f_list.room = roomdesc
                        f_list.id = salesid
                        f_list.event = bk_func.zweck[0]
                        f_list.cdate = bk_func.datum
                        f_list.pax = bk_func.rpersonen[0]
                        f_list.rmrev =  to_decimal(bk_func.rpreis[0])
                        f_list.fbrev = ( to_decimal(bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev)
                        f_list.otrev =  to_decimal(other_rev)
                        f_list.totrev =  to_decimal(bk_func.rpreis[0] + other_rev + fb_rev +\
                                (bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0]) )
                        f_list.resnr = bk_func.veran_nr
                        f_list.cp = bk_func.kontaktperson[0]
                        f_list.rstat = "F"
                        f_list.date_book = bk_func.auf__datum
                        f_list.in_sales = in_sales
                        f_list.sales = salesid2
                        f_list.ev_time = bk_func.uhrzeit


                else:

                    b_history_obj_list = {}
                    b_history = B_history()
                    bk_veran = Bk_veran()
                    for b_history.raeume, b_history.veran_nr, b_history.veran_seite, b_history.zweck, b_history.datum, b_history.rpersonen, b_history.rpreis, b_history.kontaktperson, b_history.auf__datum, b_history.uhrzeit, b_history.resstatus, b_history._recid, bk_veran.gastnr, bk_veran.payment_userinit, bk_veran._recid in db_session.query(B_history.raeume, B_history.veran_nr, B_history.veran_seite, B_history.zweck, B_history.datum, B_history.rpersonen, B_history.rpreis, B_history.kontaktperson, B_history.auf__datum, B_history.uhrzeit, B_history.resstatus, B_history._recid, Bk_veran.gastnr, Bk_veran.payment_userinit, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == B_history.veran_nr)).filter(
                             (B_history.datum == datum) & (B_history.resstatus == 1)).order_by(B_history.datum).all():
                        if b_history_obj_list.get(b_history._recid):
                            continue
                        else:
                            b_history_obj_list[b_history._recid] = True


                        fb_rev =  to_decimal("0")
                        other_rev =  to_decimal("0")

                        room = get_cache (Bk_raum, {"raum": [(eq, b_history.raeume[0])]})

                        if room:
                            roomdesc = room.bezeich
                        else:
                            roomdesc = "Not defined"

                        gast = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                        if gast:
                            bname = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:
                            bname = "Not defined"

                        bk_rart_obj_list = {}
                        bk_rart = Bk_rart()
                        artikel = Artikel()
                        for bk_rart.preis, bk_rart.anzahl, bk_rart._recid, artikel.umsatzart, artikel._recid in db_session.query(Bk_rart.preis, Bk_rart.anzahl, Bk_rart._recid, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == Bk_rart.veran_artnr) & (Artikel.departement == Bk_rart.departement)).filter(
                                 (Bk_rart.veran_nr == b_history.veran_nr) & (Bk_rart.veran_seite == b_history.veran_seite)).order_by(Bk_rart._recid).all():
                            if bk_rart_obj_list.get(bk_rart._recid):
                                continue
                            else:
                                bk_rart_obj_list[bk_rart._recid] = True

                            if (artikel.umsatzart == 5 or artikel.umsatzart == 3 or artikel.umsatzart == 6):
                                fb_rev =  to_decimal(fb_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))

                            elif artikel.umsatzart == 4:
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))
                        in_sales1 = trim(bk_veran.payment_userinit[8])
                        for count_i in range(1,length(in_sales1)  + 1) :

                            if substring(in_sales1, count_i - 1, 1) == chr_unicode(2):
                                found_chr2 = True
                                break

                        if found_chr2:

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(0, in_sales1, chr_unicode(2)))]})

                            if usr:
                                in_sales = to_string(usr.userinit + " - " + usr.username)
                            else:
                                in_sales = "**"

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(1, in_sales1, chr_unicode(2)))]})

                            if usr:
                                salesid2 = to_string(usr.userinit + " - " + usr.username)
                            else:
                                salesid2 = "**"
                        else:

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(0, in_sales1, chr_unicode(2)))]})

                            if usr:
                                in_sales = to_string(usr.userinit + " - " + usr.username)
                            else:
                                in_sales = "**"
                        found_chr2 = False
                        f_list = F_list()
                        f_list_data.append(f_list)

                        f_list.bname = bname
                        f_list.room = roomdesc
                        f_list.id = salesid
                        f_list.event = b_history.zweck[0]
                        f_list.cdate = b_history.datum
                        f_list.pax = b_history.rpersonen[0]
                        f_list.rmrev =  to_decimal(b_history.rpreis[0])
                        f_list.fbrev = ( to_decimal(b_history.rpreis[6]) * to_decimal(b_history.rpersonen[0])) + to_decimal(fb_rev)
                        f_list.otrev =  to_decimal(other_rev)
                        f_list.totrev =  to_decimal(b_history.rpreis[0] + other_rev + fb_rev +\
                                (b_history.rpreis[6]) * to_decimal(b_history.rpersonen[0]) )
                        f_list.resnr = b_history.veran_nr
                        f_list.cp = b_history.kontaktperson[0]
                        f_list.rstat = "F"
                        f_list.date_book = b_history.auf__datum
                        f_list.in_sales = in_sales
                        f_list.sales = salesid2
                        f_list.ev_time = b_history.uhrzeit


        else:
            for datum in date_range(fdate,tdate) :

                bk_func = get_cache (Bk_func, {"datum": [(eq, datum)]})

                if bk_func:

                    bk_func_obj_list = {}
                    bk_func = Bk_func()
                    bk_veran = Bk_veran()
                    for bk_func.raeume, bk_func.veran_nr, bk_func.veran_seite, bk_func.zweck, bk_func.datum, bk_func.rpersonen, bk_func.rpreis, bk_func.kontaktperson, bk_func.auf__datum, bk_func.uhrzeit, bk_func.resstatus, bk_func._recid, bk_veran.gastnr, bk_veran.payment_userinit, bk_veran._recid in db_session.query(Bk_func.raeume, Bk_func.veran_nr, Bk_func.veran_seite, Bk_func.zweck, Bk_func.datum, Bk_func.rpersonen, Bk_func.rpreis, Bk_func.kontaktperson, Bk_func.auf__datum, Bk_func.uhrzeit, Bk_func.resstatus, Bk_func._recid, Bk_veran.gastnr, Bk_veran.payment_userinit, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                             (Bk_func.datum == datum) & (Bk_func.resstatus != 9)).order_by(Bk_func.datum).all():
                        if bk_func_obj_list.get(bk_func._recid):
                            continue
                        else:
                            bk_func_obj_list[bk_func._recid] = True


                        fb_rev =  to_decimal("0")
                        other_rev =  to_decimal("0")

                        room = get_cache (Bk_raum, {"raum": [(eq, bk_func.raeume[0])]})

                        if room:
                            roomdesc = room.bezeich
                        else:
                            roomdesc = "Not defined"

                        gast = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                        if gast:
                            bname = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:
                            bname = "Not defined"

                        bk_rart_obj_list = {}
                        bk_rart = Bk_rart()
                        artikel = Artikel()
                        for bk_rart.preis, bk_rart.anzahl, bk_rart._recid, artikel.umsatzart, artikel._recid in db_session.query(Bk_rart.preis, Bk_rart.anzahl, Bk_rart._recid, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == Bk_rart.veran_artnr) & (Artikel.departement == Bk_rart.departement)).filter(
                                 (Bk_rart.veran_nr == bk_func.veran_nr) & (Bk_rart.veran_seite == bk_func.veran_seite)).order_by(Bk_rart._recid).all():
                            if bk_rart_obj_list.get(bk_rart._recid):
                                continue
                            else:
                                bk_rart_obj_list[bk_rart._recid] = True

                            if (artikel.umsatzart == 5 or artikel.umsatzart == 3 or artikel.umsatzart == 6):
                                fb_rev =  to_decimal(fb_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))

                            elif artikel.umsatzart == 4:
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))
                        in_sales1 = trim(bk_veran.payment_userinit[8])
                        for count_i in range(1,length(in_sales1)  + 1) :

                            if substring(in_sales1, count_i - 1, 1) == chr_unicode(2):
                                found_chr2 = True
                                break

                        if found_chr2:

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(0, in_sales1, chr_unicode(2)))]})

                            if usr:
                                in_sales = to_string(usr.userinit + " - " + usr.username)
                            else:
                                in_sales = "**"

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(1, in_sales1, chr_unicode(2)))]})

                            if usr:
                                salesid2 = to_string(usr.userinit + " - " + usr.username)
                            else:
                                salesid2 = "**"
                        else:

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(0, in_sales1, chr_unicode(2)))]})

                            if usr:
                                in_sales = to_string(usr.userinit + " - " + usr.username)
                            else:
                                in_sales = "**"
                        found_chr2 = False

                        if bk_func.resstatus == 1:
                            cob = "F"

                        elif bk_func.resstatus == 2:
                            cob = "T"


                        else:
                            cob = "W"


                        f_list = F_list()
                        f_list_data.append(f_list)

                        f_list.rstat = cob
                        f_list.bname = bname
                        f_list.room = roomdesc
                        f_list.id = salesid
                        f_list.event = bk_func.zweck[0]
                        f_list.cdate = bk_func.datum
                        f_list.pax = bk_func.rpersonen[0]
                        f_list.rmrev =  to_decimal(bk_func.rpreis[0])
                        f_list.fbrev = ( to_decimal(bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0])) + to_decimal(fb_rev)
                        f_list.otrev =  to_decimal(other_rev)
                        f_list.totrev =  to_decimal(bk_func.rpreis[0] + other_rev + fb_rev +\
                                (bk_func.rpreis[6]) * to_decimal(bk_func.rpersonen[0]) )
                        f_list.resnr = bk_func.veran_nr
                        f_list.cp = bk_func.kontaktperson[0]
                        f_list.date_book = bk_func.auf__datum
                        f_list.in_sales = in_sales
                        f_list.sales = salesid2
                        f_list.ev_time = bk_func.uhrzeit


                else:

                    b_history_obj_list = {}
                    b_history = B_history()
                    bk_veran = Bk_veran()
                    for b_history.raeume, b_history.veran_nr, b_history.veran_seite, b_history.zweck, b_history.datum, b_history.rpersonen, b_history.rpreis, b_history.kontaktperson, b_history.auf__datum, b_history.uhrzeit, b_history.resstatus, b_history._recid, bk_veran.gastnr, bk_veran.payment_userinit, bk_veran._recid in db_session.query(B_history.raeume, B_history.veran_nr, B_history.veran_seite, B_history.zweck, B_history.datum, B_history.rpersonen, B_history.rpreis, B_history.kontaktperson, B_history.auf__datum, B_history.uhrzeit, B_history.resstatus, B_history._recid, Bk_veran.gastnr, Bk_veran.payment_userinit, Bk_veran._recid).join(Bk_veran,(Bk_veran.veran_nr == B_history.veran_nr)).filter(
                             (B_history.datum == datum) & (B_history.resstatus != 9)).order_by(B_history.datum).all():
                        if b_history_obj_list.get(b_history._recid):
                            continue
                        else:
                            b_history_obj_list[b_history._recid] = True


                        fb_rev =  to_decimal("0")
                        other_rev =  to_decimal("0")

                        room = get_cache (Bk_raum, {"raum": [(eq, b_history.raeume[0])]})

                        if room:
                            roomdesc = room.bezeich
                        else:
                            roomdesc = "Not defined"

                        gast = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

                        if gast:
                            bname = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:
                            bname = "Not defined"

                        bk_rart_obj_list = {}
                        bk_rart = Bk_rart()
                        artikel = Artikel()
                        for bk_rart.preis, bk_rart.anzahl, bk_rart._recid, artikel.umsatzart, artikel._recid in db_session.query(Bk_rart.preis, Bk_rart.anzahl, Bk_rart._recid, Artikel.umsatzart, Artikel._recid).join(Artikel,(Artikel.artnr == Bk_rart.veran_artnr) & (Artikel.departement == Bk_rart.departement)).filter(
                                 (Bk_rart.veran_nr == b_history.veran_nr) & (Bk_rart.veran_seite == b_history.veran_seite)).order_by(Bk_rart._recid).all():
                            if bk_rart_obj_list.get(bk_rart._recid):
                                continue
                            else:
                                bk_rart_obj_list[bk_rart._recid] = True

                            if (artikel.umsatzart == 5 or artikel.umsatzart == 3 or artikel.umsatzart == 6):
                                fb_rev =  to_decimal(fb_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))

                            elif artikel.umsatzart == 4:
                                other_rev =  to_decimal(other_rev) + to_decimal((bk_rart.preis) * to_decimal(bk_rart.anzahl))
                        in_sales1 = trim(bk_veran.payment_userinit[8])
                        for count_i in range(1,length(in_sales1)  + 1) :

                            if substring(in_sales1, count_i - 1, 1) == chr_unicode(2):
                                found_chr2 = True
                                break

                        if found_chr2:

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(0, in_sales1, chr_unicode(2)))]})

                            if usr:
                                in_sales = to_string(usr.userinit + " - " + usr.username)
                            else:
                                in_sales = "**"

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(1, in_sales1, chr_unicode(2)))]})

                            if usr:
                                salesid2 = to_string(usr.userinit + " - " + usr.username)
                            else:
                                salesid2 = "**"
                        else:

                            usr = get_cache (Bediener, {"userinit": [(eq, entry(0, in_sales1, chr_unicode(2)))]})

                            if usr:
                                in_sales = to_string(usr.userinit + " - " + usr.username)
                            else:
                                in_sales = "**"
                        found_chr2 = False

                        if b_history.resstatus == 1:
                            cob = "F"

                        elif b_history.resstatus == 2:
                            cob = "T"


                        else:
                            cob = "W"


                        f_list = F_list()
                        f_list_data.append(f_list)

                        f_list.rstat = cob
                        f_list.bname = bname
                        f_list.room = roomdesc
                        f_list.id = salesid
                        f_list.event = b_history.zweck[0]
                        f_list.cdate = b_history.datum
                        f_list.pax = b_history.rpersonen[0]
                        f_list.rmrev =  to_decimal(b_history.rpreis[0])
                        f_list.fbrev = ( to_decimal(b_history.rpreis[6]) * to_decimal(b_history.rpersonen[0])) + to_decimal(fb_rev)
                        f_list.otrev =  to_decimal(other_rev)
                        f_list.totrev =  to_decimal(b_history.rpreis[0] + other_rev + fb_rev +\
                                (b_history.rpreis[6]) * to_decimal(b_history.rpersonen[0]) )
                        f_list.resnr = b_history.veran_nr
                        f_list.cp = b_history.kontaktperson[0]
                        f_list.date_book = b_history.auf__datum
                        f_list.in_sales = in_sales
                        f_list.sales = salesid2
                        f_list.ev_time = b_history.uhrzeit


    def create_subtotal():

        nonlocal output_list_data, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, artikel, bk_rart, b_history
        nonlocal checklist, sorttype, fdate, tdate, disp_flag
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
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
        subpax = 0
        subrmrev =  to_decimal("0")
        subfbrev =  to_decimal("0")
        subother =  to_decimal("0")
        subrev =  to_decimal("0")


    create_browse()

    return generate_output()