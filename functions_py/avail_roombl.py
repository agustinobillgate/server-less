#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 22/7/2025
# zistatus kosong
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zimmer, Outorder, Res_line, Zimkateg, Paramtext, Zimplan, Guest

def avail_roombl(mi_clean:bool, mi_clean1:bool, mi_dirty:bool, mi_depart:bool, mi_occ:bool, mi_ooo:bool, mi_off:bool, ankunft:date, abreise:date):

    prepare_cache ([Zimmer, Outorder, Res_line, Zimkateg, Paramtext, Zimplan, Guest])

    room_list_data = []
    do_it:bool = False
    zikatnr:int = 0
    zimmer = outorder = res_line = zimkateg = paramtext = zimplan = guest = None

    room_list = None

    room_list_data, Room_list = create_model("Room_list", {"flag":int, "build":string, "build_flag":string, "zistatus":int, "infochar":string, "inactive":string, "zinr":string, "bezeich":string, "zikatnr":int, "rmcat":string, "etage":int, "outlook":string, "setup":string, "verbindung":[string,2], "infonum":int, "recid1":int, "recid2":int, "infostr":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_data, do_it, zikatnr, zimmer, outorder, res_line, zimkateg, paramtext, zimplan, guest
        nonlocal mi_clean, mi_clean1, mi_dirty, mi_depart, mi_occ, mi_ooo, mi_off, ankunft, abreise


        nonlocal room_list
        nonlocal room_list_data

        return {"room-list": room_list_data}


    room_list_data.clear()

    for zimmer in db_session.query(Zimmer).order_by(Zimmer.zinr).all():
        do_it = False

        if zikatnr == 0 or zimmer.zikatnr == zikatnr:
            do_it = True

        if do_it:

            if zimmer.zistatus == 0 and mi_clean == False:
                do_it = False

            if zimmer.zistatus == 1 and mi_clean1 == False:
                do_it = False

            if zimmer.zistatus == 2 and mi_dirty == False:
                do_it = False

            if zimmer.zistatus == 3 and mi_depart == False:
                do_it = False

            if zimmer.zistatus == 4 or zimmer.zistatus == 5 or zimmer.zistatus == 8 and mi_occ == False:
                do_it = False

            if zimmer.zistatus == 6 and mi_ooo == False:
                do_it = False

            if zimmer.zistatus == 7 and mi_off == False:
                do_it = False

        if do_it:

            outorder = db_session.query(Outorder).filter(
                     (Outorder.zinr == zimmer.zinr) & (((Outorder.gespstart < ankunft) & (Outorder.gespende > ankunft)) | ((Outorder.gespstart < abreise) & (Outorder.gespende > abreise)) | ((Outorder.gespstart >= ankunft) & (Outorder.gespstart <= abreise)) | ((Outorder.gespende >= ankunft) & (Outorder.gespende <= abreise)))).first()

            if not outorder:

                # res_line = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(ne, 12)],"zinr": [(eq, zimmer.zinr)],"ankunft": [(ge, abreise)],"abreise": [(le, ankunft)]})
                res_line = db_session.query(Res_line).filter(
                         (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.zinr == zimmer.zinr) & (Res_line.ankunft < abreise) & (Res_line.abreise > ankunft)).first()
                if not res_line:
                    room_list = Room_list()
                    room_list_data.append(room_list)

                    # Rd 22/7/2025, default infonum = 3
                    room_list.infonum = 3

                    room_list.zinr = zimmer.zinr

                    if not zimmer.sleeping:
                        room_list.inactive = "I"
                else:
                    room_list = Room_list()
                    room_list_data.append(room_list)
                    # Rd 22/7/2025, default infonum = 3
                    room_list.infonum = 3

                    room_list.zinr = zimmer.zinr

                    if zimmer.zistatus == 8:
                        room_list.flag = 4
                    else:

                        if res_line.active_flag == 0:
                            room_list.flag = 4
                        else:
                            room_list.flag = zimmer.zistatus

                    if not zimmer.sleeping:
                        room_list.inactive = "I"
            else:
                room_list = Room_list()
                room_list_data.append(room_list)
                # Rd 22/7/2025, default infonum = 3
                room_list.infonum = 3

                room_list.zinr = zimmer.zinr

                if outorder.betriebsnr >= 2:
                    room_list.flag = 7
                else:
                    room_list.flag = 6

                if not zimmer.sleeping:
                    room_list.inactive = "I"

    for room_list in query(room_list_data):

        # zimmer = get_cache (Zimmer, {"zinr": [(eq, room_list.zinr)]})
        zimmer = db_session.query(Zimmer).filter(
                 (Zimmer.zinr == room_list.zinr)).first()

        # zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, zimmer.zikatnr)]})
        zimkateg = db_session.query(Zimkateg).filter(
                 (Zimkateg.zikatnr == zimmer.zikatnr)).first()

        if zimmer.build != "":
            room_list.build = zimmer.build
            room_list.build_flag = "*"
        room_list.bezeich = zimmer.kbezeich
        room_list.verbindung[0] = zimmer.verbindung[0]
        room_list.verbindung[1] = zimmer.verbindung[1]
        room_list.etage = zimmer.etage
        room_list.rmcat = zimkateg.kurzbez
        room_list.zikatnr = zimkateg.zikatnr

        if zimmer.typ != 0:

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, 230)],"sprachcode": [(eq, zimmer.typ)]})

            if paramtext:
                room_list.outlook = paramtext.ptexte

        if zimmer.setup != 0:

            paramtext = get_cache (Paramtext, {"txtnr": [(eq, (zimmer.setup + 9200))]})

            if paramtext:
                room_list.setup = paramtext.ptexte

        # zimplan = get_cache (Zimplan, {"zinr": [(eq, room_list.zinr)],"datum": [(eq, ankunft - timedelta(days=1))]})
        zimplan = db_session.query(Zimplan).filter(
                 (Zimplan.zinr == room_list.zinr) & (Zimplan.datum == (ankunft - timedelta(days=1)))).first()

        if zimplan:
            room_list.infonum = room_list.infonum - 2
            room_list.recid1 = zimplan.res_recid

        # zimplan = get_cache (Zimplan, {"zinr": [(eq, room_list.zinr)],"datum": [(eq, abreise)]})
        zimplan = db_session.query(Zimplan).filter(
                 (Zimplan.zinr == room_list.zinr) & (Zimplan.datum == abreise)).first()

        if zimplan:
            room_list.infonum = room_list.infonum - 1
            room_list.recid2 = zimplan.res_recid

        if room_list.infonum == 0:
            room_list.infochar = "<>"

        elif room_list.infonum == 1:
            room_list.infochar = "< "

        elif room_list.infonum == 2:
            room_list.infochar = " >"

        if zimmer.zistatus == 8:
            room_list.zistat = 5
        else:
            room_list.zistatus = zimmer.zistatus + 1

        if room_list.flag == 7:
            room_list.zistatus = 8

    for room_list in query(room_list_data):

        if substring(room_list.infochar, 0, 1) == "<":

            # res_line = get_cache (Res_line, {"_recid": [(eq, room_list.recid1)]})
            res_line = db_session.query(Res_line).filter(
                     (Res_line._recid == room_list.recid1)).first() 

            if res_line:

                # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnrpay)).first()
                
                room_list.infostr = room_list.infostr +\
                        "< ResNo: " +\
                        to_string(res_line.resnr) + chr_unicode(10)
                room_list.infostr = room_list.infostr + " " + guest.name + ", " +\
                        guest.vorname1 + guest.anredefirma + chr_unicode(10)
                room_list.infostr = room_list.infostr + "Arrival : " + to_string(res_line.ankunft) +\
                        chr_unicode(10)
                room_list.infostr = room_list.infostr + "Depart : " + to_string(res_line.abreise) +\
                        chr_unicode(10) + chr_unicode(10)

        if substring(room_list.infochar, 1, 1) == ">":

            # res_line = get_cache (Res_line, {"_recid": [(eq, room_list.recid2)]})
            res_line = db_session.query(Res_line).filter(
                     (Res_line._recid == room_list.recid2)).first()

            if res_line:

                # guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrpay)]})
                guest = db_session.query(Guest).filter(
                         (Guest.gastnr == res_line.gastnrpay)).first()
                room_list.infostr = room_list.infostr +\
                        "> ResNo: " +\
                        to_string(res_line.resnr) + chr_unicode(10)
                room_list.infostr = room_list.infostr + " " + guest.name + ", " +\
                        guest.vorname1 + guest.anredefirma + chr_unicode(10)
                room_list.infostr = room_list.infostr + "Arrival : " + to_string(res_line.ankunft) + chr_unicode(10)
                room_list.infostr = room_list.infostr + "Depart : " + to_string(res_line.abreise)

        if room_list.zistatus == 7:

            # outorder = get_cache (Outorder, {"zinr": [(eq, room_list.zinr)]})
            outorder = db_session.query(Outorder).filter(
                     (Outorder.zinr == room_list.zinr)).first()

            if outorder:

                if room_list.infostr != "":
                    room_list.infostr = room_list.infostr + chr_unicode(10)
                room_list.infostr = room_list.infostr + outorder.gespgrund

        if room_list.zistatus == 8:

            # outorder = get_cache (Outorder, {"zinr": [(eq, room_list.zinr)]})
            outorder = db_session.query(Outorder).filter(
                     (Outorder.zinr == room_list.zinr)).first()

            if outorder:

                if room_list.infostr != "":
                    room_list.infostr = room_list.infostr + chr_unicode(10)
                room_list.infostr = room_list.infostr + outorder.gespgrund

    return generate_output()