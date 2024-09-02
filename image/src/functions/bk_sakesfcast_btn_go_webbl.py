from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Bk_raum, Guest, Bediener, Ba_typ, Bk_func, Bk_veran, Bk_rart, B_history

def bk_sakesfcast_btn_go_webbl(checklist:bool, sorttype:int, fdate:date, tdate:date, disp_flag:int):
    output_list_list = []
    cob:str = ""
    str1:str = ""
    totrmrev:decimal = 0
    totfbrev:decimal = 0
    totother:decimal = 0
    totrev:decimal = 0
    totpax:int = 0
    subrmrev:decimal = 0
    subfbrev:decimal = 0
    subother:decimal = 0
    subrev:decimal = 0
    subpax:int = 0
    bk_raum = guest = bediener = ba_typ = bk_func = bk_veran = bk_rart = b_history = None

    f_list = output_list = room = gast = usr = event = None

    f_list_list, F_list = create_model("F_list", {"rstat":str, "bname":str, "room":str, "id":str, "event":str, "cdate":date, "pax":int, "rmrev":decimal, "fbrev":decimal, "otrev":decimal, "totrev":decimal, "cp":str, "resnr":int, "date_book":date, "in_sales":str, "sales":str, "ev_time":str})
    output_list_list, Output_list = create_model("Output_list", {"flag":str, "bezeich":str, "rstat":str, "room":str, "id":str, "ba_event":str, "datum":date, "pax":int, "rmrev":decimal, "fbrev":decimal, "othrev":decimal, "totrev":decimal, "cp":str, "resnr":int, "date_book":date, "in_sales":str, "ev_time":str})

    Room = Bk_raum
    Gast = Guest
    Usr = Bediener
    Event = Ba_typ

    db_session = local_storage.db_session

    def generate_output():
        nonlocal output_list_list, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, bk_rart, b_history
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_list, output_list_list
        return {"output-list": output_list_list}

    def create_browse():

        nonlocal output_list_list, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, bk_rart, b_history
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_list, output_list_list

        groupby:str = ""
        line1:int = 0
        output_list_list.clear()
        create_list()
        totrmrev = 0
        totfbrev = 0
        totpax = 0
        totrev = 0
        totother = 0

        if not checklist:

            if sorttype == 0:

                if disp_flag == 1:

                    for f_list in query(f_list_list):
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

                    for f_list in query(f_list_list):
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

                for f_list in query(f_list_list):
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

                for f_list in query(f_list_list):
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
                output_list.rmrev = totrmrev
                output_list.fbrev = totfbrev
                output_list.othrev = totother
                output_list.totrev = totrev


        else:

            if sorttype == 0:

                if disp_flag == 1:

                    for f_list in query(f_list_list):
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

                    for f_list in query(f_list_list):
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

                for f_list in query(f_list_list):
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

                for f_list in query(f_list_list):
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
                output_list.rmrev = totrmrev
                output_list.fbrev = totfbrev
                output_list.othrev = totother
                output_list.totrev = totrev

    def create_group(bezeich:str, bezeich1:str):

        nonlocal output_list_list, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, bk_rart, b_history
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_list, output_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "GROUP"

        if bezeich.lower()  == "SALES ID" or bezeich.lower()  == "SALES INCHARGE":
            output_list.bezeich = bezeich1
        else:
            output_list.bezeich = bezeich + " : " + bezeich1

    def create_data():

        nonlocal output_list_list, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, bk_rart, b_history
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_list, output_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.bezeich = f_list.bname
        output_list.room = f_list.room
        output_list.id = f_list.ID
        output_list.ba_event = f_list.EVENT
        output_list.datum = f_list.cDATE
        output_list.pax = f_list.pax
        output_list.rmrev = f_list.rmrev
        output_list.fbrev = f_list.fbrev
        output_list.othrev = f_list.otrev
        output_list.totrev = f_list.totrev
        output_list.resnr = f_list.resnr
        output_list.cp = f_list.cp
        output_list.rstat = f_list.rstat
        output_list.date_book = f_list.date_book
        output_list.in_sales = f_list.in_sales
        output_list.ev_time = f_list.ev_time


        subpax = subpax + f_list.pax
        subrmrev = subrmrev + f_list.rmrev
        subfbrev = subfbrev + f_list.fbrev
        subother = subother + f_list.otrev
        subrev = subrev + f_list.totrev
        totpax = totpax + f_list.pax
        totrmrev = totrmrev + f_list.rmrev
        totfbrev = totfbrev + f_list.fbrev
        totother = totother + f_list.otrev
        totrev = totrev + f_list.totrev

    def create_list():

        nonlocal output_list_list, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, bk_rart, b_history
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_list, output_list_list

        salesid:str = ""
        salesid2:str = ""
        roomdesc:str = ""
        bname:str = ""
        other_rev:decimal = 0
        in_sales:str = ""
        in_sales1:str = ""
        in_sales2:str = ""
        datum:date = None
        f_list_list.clear()

        if not checklist:
            for datum in range(fdate,tdate + 1) :

                bk_func = db_session.query(Bk_func).filter(
                        (Bk_func.datum == datum)).first()

                if bk_func:

                    bk_func_obj_list = []
                    for bk_func, bk_veran in db_session.query(Bk_func, Bk_veran).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                            (Bk_func.datum == datum) &  (Bk_func.resstatus == 1)).all():
                        if bk_func._recid in bk_func_obj_list:
                            continue
                        else:
                            bk_func_obj_list.append(bk_func._recid)

                        room = db_session.query(Room).filter(
                                (Room.raum == bk_func.raeume[0])).first()

                        if room:
                            roomdesc = room.bezeich
                        else:
                            roomdesc = "Not defined"

                        gast = db_session.query(Gast).filter(
                                (Gast.gastnr == bk_veran.gastnr)).first()

                        if gast:
                            bname = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:
                            bname = "Not defined"

                        usr = db_session.query(Usr).filter(
                                (Usr.nr == bk_veran.bediener_nr)).first()

                        if usr:
                            salesid = usr.userinit
                            salesid2 = salesid + " - " + usr.username
                        else:
                            salesid = "**"
                            salesid2 = ""

                        for bk_rart in db_session.query(Bk_rart).filter(
                                (Bk_rart.veran_nr == bk_func.veran_nr) &  (Bk_rart.veran_seite == bk_func.veran_seite)).all():
                            other_rev = other_rev + (bk_rart.preis * anzahl)
                        in_sales1 = trim(bk_veran.payment_userinit[8])
                        in_sales2 = substring(in_sales1, 0, len(in_sales1) - 1)

                        usr = db_session.query(Usr).filter(
                                (func.lower(Usr.userinit) == (in_sales2).lower())).first()

                        if usr:
                            in_sales = to_string(usr.userinit + " - " + usr.username)
                        else:
                            in_sales = "**"
                        f_list = F_list()
                        f_list_list.append(f_list)

                        f_list.bname = bname
                        f_list.room = roomdesc
                        f_list.ID = salesid
                        f_list.event = bk_func.zweck[0]
                        f_list.cdate = bk_func.datum
                        f_list.pax = bk_func.rpersonen[0]
                        f_list.rmrev = bk_func.rpreis[0]
                        f_list.fbrev = bk_func.rpreis[6] * bk_func.rpersonen[0]
                        f_list.otrev = other_rev
                        f_list.totrev = bk_func.rpreis[0] + other_rev +\
                                (bk_func.rpreis[6] * bk_func.rpersonen[0])
                        f_list.resnr = bk_func.veran_nr
                        f_list.cp = bk_func.kontaktperson[0]
                        f_list.rstat = "F"
                        f_list.date_book = bk_func.auf__datum
                        f_list.in_sales = in_sales
                        f_list.sales = salesid2
                        f_list.ev_time = bk_func.uhrzeit


                else:

                    b_history_obj_list = []
                    for b_history, bk_veran in db_session.query(B_history, Bk_veran).join(Bk_veran,(Bk_veran.veran_nr == B_history.veran_nr)).filter(
                            (B_history.datum == datum) &  (B_history.resstatus == 1)).all():
                        if b_history._recid in b_history_obj_list:
                            continue
                        else:
                            b_history_obj_list.append(b_history._recid)

                        room = db_session.query(Room).filter(
                                (Room.raum == b_history.raeume[0])).first()

                        if room:
                            roomdesc = room.bezeich
                        else:
                            roomdesc = "Not defined"

                        gast = db_session.query(Gast).filter(
                                (Gast.gastnr == bk_veran.gastnr)).first()

                        if gast:
                            bname = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:
                            bname = "Not defined"

                        usr = db_session.query(Usr).filter(
                                (Usr.nr == bk_veran.bediener_nr)).first()

                        if usr:
                            salesid = usr.userinit
                            salesid2 = salesid + " - " + usr.username
                        else:
                            salesid = "**"
                            salesid2 = ""

                        for bk_rart in db_session.query(Bk_rart).filter(
                                (Bk_rart.veran_nr == b_history.veran_nr) &  (Bk_rart.veran_seite == b_history.veran_seite)).all():
                            other_rev = other_rev + (bk_rart.preis * anzahl)
                        in_sales1 = trim(bk_veran.payment_userinit[8])
                        in_sales2 = substring(in_sales1, 0, len(in_sales1) - 1)

                        usr = db_session.query(Usr).filter(
                                (func.lower(Usr.userinit) == (in_sales2).lower())).first()

                        if usr:
                            in_sales = to_string(usr.userinit + " - " + usr.username)
                        else:
                            in_sales = "**"
                        f_list = F_list()
                        f_list_list.append(f_list)

                        f_list.bname = bname
                        f_list.room = roomdesc
                        f_list.ID = salesid
                        f_list.event = b_history.zweck[0]
                        f_list.cdate = b_history.datum
                        f_list.pax = b_history.rpersonen[0]
                        f_list.rmrev = b_history.rpreis[0]
                        f_list.fbrev = b_history.rpreis[6] * b_history.rpersonen[0]
                        f_list.otrev = other_rev
                        f_list.totrev = b_history.rpreis[0] + other_rev +\
                                (b_history.rpreis[6] * b_history.rpersonen[0])
                        f_list.resnr = b_history.veran_nr
                        f_list.cp = b_history.kontaktperson[0]
                        f_list.rstat = "F"
                        f_list.date_book = b_history.auf__datum
                        f_list.in_sales = in_sales
                        f_list.sales = salesid2
                        f_list.ev_time = b_history.uhrzeit


        else:
            for datum in range(fdate,tdate + 1) :

                bk_func = db_session.query(Bk_func).filter(
                        (Bk_func.datum == datum)).first()

                if bk_func:

                    bk_func_obj_list = []
                    for bk_func, bk_veran in db_session.query(Bk_func, Bk_veran).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr)).filter(
                            (Bk_func.datum == datum) &  (Bk_func.resstatus != 9)).all():
                        if bk_func._recid in bk_func_obj_list:
                            continue
                        else:
                            bk_func_obj_list.append(bk_func._recid)

                        room = db_session.query(Room).filter(
                                (Room.raum == bk_func.raeume[0])).first()

                        if room:
                            roomdesc = room.bezeich
                        else:
                            roomdesc = "Not defined"

                        gast = db_session.query(Gast).filter(
                                (Gast.gastnr == bk_veran.gastnr)).first()

                        if gast:
                            bname = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:
                            bname = "Not defined"

                        usr = db_session.query(Usr).filter(
                                (Usr.nr == bk_veran.bediener_nr)).first()

                        if usr:
                            salesid = usr.userinit
                            salesid2 = salesid + " - " + usr.username
                        else:
                            salesid = "**"
                            salesid2 = ""

                        for bk_rart in db_session.query(Bk_rart).filter(
                                (Bk_rart.veran_nr == bk_func.veran_nr) &  (Bk_rart.veran_seite == bk_func.veran_seite)).all():
                            other_rev = other_rev + (bk_rart.preis * anzahl)
                        in_sales1 = trim(bk_veran.payment_userinit[8])
                        in_sales2 = substring(in_sales1, 0, len(in_sales1) - 1)

                        usr = db_session.query(Usr).filter(
                                (func.lower(Usr.userinit) == (in_sales2).lower())).first()

                        if usr:
                            in_sales = to_string(usr.userinit + " - " + usr.username)
                        else:
                            in_sales = "**"

                        if bk_func.resstatus == 1:
                            cob = "F"

                        elif bk_func.resstatus == 2:
                            cob = "T"


                        else:
                            cob = "W"


                        f_list = F_list()
                        f_list_list.append(f_list)

                        f_list.rstat = cob
                        f_list.bname = bname
                        f_list.room = roomdesc
                        f_list.ID = salesid
                        f_list.event = bk_func.zweck[0]
                        f_list.cdate = bk_func.datum
                        f_list.pax = bk_func.rpersonen[0]
                        f_list.rmrev = bk_func.rpreis[0]
                        f_list.fbrev = bk_func.rpreis[6] * bk_func.rpersonen[0]
                        f_list.otrev = other_rev
                        f_list.totrev = bk_func.rpreis[0] + other_rev +\
                                (bk_func.rpreis[6] * bk_func.rpersonen[0])
                        f_list.resnr = bk_func.veran_nr
                        f_list.cp = bk_func.kontaktperson[0]
                        f_list.date_book = bk_func.auf__datum
                        f_list.in_sales = in_sales
                        f_list.sales = salesid2
                        f_list.ev_time = bk_func.uhrzeit


                else:

                    b_history_obj_list = []
                    for b_history, bk_veran in db_session.query(B_history, Bk_veran).join(Bk_veran,(Bk_veran.veran_nr == B_history.veran_nr)).filter(
                            (B_history.datum == datum) &  (bk_func.resstatus != 9)).all():
                        if b_history._recid in b_history_obj_list:
                            continue
                        else:
                            b_history_obj_list.append(b_history._recid)

                        room = db_session.query(Room).filter(
                                (Room.raum == b_history.raeume[0])).first()

                        if room:
                            roomdesc = room.bezeich
                        else:
                            roomdesc = "Not defined"

                        gast = db_session.query(Gast).filter(
                                (Gast.gastnr == bk_veran.gastnr)).first()

                        if gast:
                            bname = gast.name + ", " + gast.vorname1 + " " + gast.anrede1 + gast.anredefirma
                        else:
                            bname = "Not defined"

                        usr = db_session.query(Usr).filter(
                                (Usr.nr == bk_veran.bediener_nr)).first()

                        if usr:
                            salesid = usr.userinit
                            salesid2 = salesid + " - " + usr.username
                        else:
                            salesid = "**"
                            salesid2 = ""

                        for bk_rart in db_session.query(Bk_rart).filter(
                                (Bk_rart.veran_nr == b_history.veran_nr) &  (Bk_rart.veran_seite == b_history.veran_seite)).all():
                            other_rev = other_rev + (bk_rart.preis * anzahl)
                        in_sales1 = trim(bk_veran.payment_userinit[8])
                        in_sales2 = substring(in_sales1, 0, len(in_sales1) - 1)

                        usr = db_session.query(Usr).filter(
                                (func.lower(Usr.userinit) == (in_sales2).lower())).first()

                        if usr:
                            in_sales = to_string(usr.userinit + " - " + usr.username)
                        else:
                            in_sales = "**"

                        if b_history.resstatus == 1:
                            cob = "F"

                        elif b_history.resstatus == 2:
                            cob = "T"


                        else:
                            cob = "W"


                        f_list = F_list()
                        f_list_list.append(f_list)

                        f_list.rstat = cob
                        f_list.bname = bname
                        f_list.room = roomdesc
                        f_list.ID = salesid
                        f_list.event = b_history.zweck[0]
                        f_list.cdate = b_history.datum
                        f_list.pax = b_history.rpersonen[0]
                        f_list.rmrev = b_history.rpreis[0]
                        f_list.fbrev = b_history.rpreis[6] * b_history.rpersonen[0]
                        f_list.otrev = other_rev
                        f_list.totrev = b_history.rpreis[0] + other_rev +\
                                (b_history.rpreis[6] * b_history.rpersonen[0])
                        f_list.resnr = b_history.veran_nr
                        f_list.cp = b_history.kontaktperson[0]
                        f_list.date_book = b_history.auf__datum
                        f_list.in_sales = in_sales
                        f_list.sales = salesid2
                        f_list.ev_time = b_history.uhrzeit

    def create_subtotal():

        nonlocal output_list_list, cob, str1, totrmrev, totfbrev, totother, totrev, totpax, subrmrev, subfbrev, subother, subrev, subpax, bk_raum, guest, bediener, ba_typ, bk_func, bk_veran, bk_rart, b_history
        nonlocal room, gast, usr, event


        nonlocal f_list, output_list, room, gast, usr, event
        nonlocal f_list_list, output_list_list


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "LINE"


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "SUB"
        output_list.bezeich = "Subtotal"
        output_list.pax = subpax
        output_list.rmrev = subrmrev
        output_list.fbrev = subfbrev
        output_list.othrev = subother
        output_list.totrev = subrev


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.flag = "SPACE"
        subpax = 0
        subrmrev = 0
        subfbrev = 0
        subother = 0
        subrev = 0

    create_browse()

    return generate_output()