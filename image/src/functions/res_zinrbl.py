from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line, Zimmer, Outorder, Paramtext, Guest

def res_zinrbl(case_type:int, resno:int, reslinno:int, zikatno:int, ankunft1:date, abreise1:date):
    room_list_list = []
    htl_feature_list = []
    vhp_limited:bool = False
    res_rowid:int = 0
    ci_date:date = None
    res_line = zimmer = outorder = paramtext = guest = None

    om_list = htl_feature = room_list = resline = res_line1 = None

    om_list_list, Om_list = create_model("Om_list", {"zinr":str, "ind":int})
    htl_feature_list, Htl_feature = create_model("Htl_feature", {"s":str, "flag":int}, {"flag": 1})
    room_list_list, Room_list = create_model("Room_list", {"i":int, "flag":bool, "sleeping":bool, "feature":str, "himmelsr":str, "build":str, "zikennz":str, "build_flag":str, "zistat":str, "infochar":str, "zinr":str, "bezeich":str, "etage":int, "outlook":str, "setup":str, "name":str, "comment":str, "verbindung1":str, "verbindung2":str, "infonum":int, "prioritaet":int, "recid1":int, "recid2":int, "infostr":str}, {"flag": True, "sleeping": True})

    Resline = Res_line
    Res_line1 = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list
        return {"room-list": room_list_list, "htl-feature": htl_feature_list}

    def create_list():

        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list


        room_list_list.clear()

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.zikatnr == zikatno) &  (Zimmer.zinr != "")).all():

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (not Outorder.gespstart > abreise1) &  (not Outorder.gespende < ankunft1) &  (Outorder.betriebsnr <= 2)).first()

            if not outorder:

                if zimmer.zistatus == 6 and ankunft1 <= ci_date:
                    1
                else:
                    room_list = Room_list()
                    room_list_list.append(room_list)

                    room_list.zinr = zimmer.zinr
                    room_list.prioritaet = zimmer.prioritaet
                    room_list.sleeping = zimmer.sleeping

        for resline in db_session.query(Resline).filter(
                (Resline.zikatnr == zikatno) &  (Resline.zinr != "") &  (Resline.resstatus != 12) &  (Resline.active_flag <= 1) &  (Resline.l_zuordnung[2] == 0)).all():

            if to_int(resline._recid) == res_rowid:
                1

            elif resline.resstatus == 6 and resline.abreise <= ankunft1:
                pass

            elif (resline.abreise <= ankunft1) or (resline.ankunft >= abreise1):
                pass
            else:

                room_list = query(room_list_list, filters=(lambda room_list :room_list.zinr == resline.zinr), first=True)

                if room_list:
                    room_list_list.remove(room_list)
        complete_list()

    def create_all_list():

        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list


        room_list_list.clear()

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.zinr != "")).all():

            outorder = db_session.query(Outorder).filter(
                    (Outorder.zinr == zimmer.zinr) &  (not Outorder.gespstart > abreise1) &  (not Outorder.gespende < ankunft1) &  (Outorder.betriebsnr <= 2)).first()

            if not outorder:
                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.zinr = zimmer.zinr
                room_list.prioritaet = zimmer.prioritaet
                room_list.sleeping = zimmer.sleeping

        for resline in db_session.query(Resline).filter(
                (Resline.zinr != "") &  (Resline.resstatus != 12) &  (Resline.active_flag <= 1) &  (Resline.l_zuordnung[2] == 0)).all():

            if to_int(resline._recid) == res_rowid:
                1

            elif resline.resstatus == 6 and resline.abreise <= ankunft1:
                pass

            elif (resline.abreise <= ankunft1) or (resline.ankunft >= abreise1):
                pass
            else:

                room_list = query(room_list_list, filters=(lambda room_list :room_list.zinr == resline.zinr), first=True)

                if room_list:
                    room_list_list.remove(room_list)
        complete_list()

    def complete_list():

        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list

        stat_list:[str] = ["", "", "", "", "", "", "", "", "", "", ""]
        stat_list[0] = "VC"
        stat_list[1] = "CU"
        stat_list[2] = "VD"
        stat_list[3] = "ED"
        stat_list[4] = "OD"
        stat_list[5] = "OC"

        for zimmer in db_session.query(Zimmer).all():
            om_list = Om_list()
            om_list_list.append(om_list)

            om_list.zinr = zimmer.zinr
            om_list.ind = zimmer.zistatus + 1

        for outorder in db_session.query(Outorder).filter(
                (Outorder.betriebsnr >= 2) &  (Outorder.gespstart <= ci_date) &  (Outorder.gespende >= ci_date)).all():

            om_list = query(om_list_list, filters=(lambda om_list :om_list.zinr == outorder.zinr), first=True)

            if om_list:
                om_list.ind = 8

        for room_list in query(room_list_list):

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == room_list.zinr)).first()
            room_list.zikennz = zimmer.zikennz

            if zimmer.himmelsr != "":
                fill_feature()
            room_list.bezeich = zimmer.bezeich
            room_list.verbindung1 = zimmer.verbindung[0]
            room_list.verbindung2 = zimmer.verbindung[1]
            room_list.etage = zimmer.etage

            if zimmer.typ != 0:

                paramtext = db_session.query(Paramtext).filter(
                        (Paramtext.txtnr == 230) &  (Paramtext.sprachcode == zimmer.typ)).first()

                if paramtext:
                    room_list.outlook = paramtext.ptexte

            if zimmer.setup != 0:

                paramtext = db_session.query(Paramtext).filter(
                        (Paramtext.txtnr == (zimmer.setup + 9200))).first()

                if paramtext:
                    room_list.setup = trim(paramtext.ptexte)

            resline = db_session.query(Resline).filter(
                    (Resline.zinr == room_list.zinr) &  (Resline.active_flag < 2) &  (Resline.abreise == ankunft1) &  (Resline.resstatus <= 6)).first()

            if resline:
                room_list.infonum = room_list.infonum - 2
                room_list.recid1 = to_int(resline._recid)

            resline = db_session.query(Resline).filter(
                    (Resline.zinr == room_list.zinr) &  (Resline.active_flag == 0) &  (Resline.ankunft == abreise)).first()

            if resline:
                room_list.infonum = room_list.infonum - 1
                room_list.recid2 = to_int(resline._recid)

            if room_list.infonum == 0:
                room_list.infochar = "<>"

            elif room_list.infonum == 1:
                room_list.infochar = "< "

            elif room_list.infonum == 2:
                room_list.infochar = " >"

            om_list = query(om_list_list, filters=(lambda om_list :om_list.zinr == room_list.zinr), first=True)

            if room_list.prioritaet < 99999:
                room_list.zistat = stat_list[om_list.ind - 1]

    def fill_feature():

        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list

        i:int = 0
        j:int = 0
        k:int = 0
        n:int = 0
        ch:str = ""
        n = 0
        j = 1
        room_list.himmelsr = ""
        for i in range(1,len(zimmer.himmelsr)  + 1) :

            if substring(zimmer.himmelsr, i - 1, 1) == ";" or substring(zimmer.himmelsr, i - 1, 1) == ",":
                ch = ""
                for k in range(j,(j + n - 1)  + 1) :

                    if substring(zimmer.himmelsr, k - 1, 1) != chr (10):
                        ch = ch + substring(zimmer.himmelsr, k - 1, 1)
                ch = trim(ch)

                if (len(ch) != 0) and (substring(ch, 0, 1) != "$"):
                    room_list.i = room_list.i + 1
                    room_list.feature[room_list.i - 1] = ch

                    htl_feature = query(htl_feature_list, filters=(lambda htl_feature :htl_feature.s.lower()  == (ch).lower()), first=True)

                    if not htl_feature:
                        htl_feature = Htl_feature()
                        htl_feature_list.append(htl_feature)

                        htl_feature.s = ch
                        room_list.himmelsr = room_list.himmelsr + ch + ";"


                j = i + 1
                n = 0
            else:
                n = n + 1

        if n != 0:
            ch = ""
            for k in range(j,(j + n - 1)  + 1) :

                if substring(zimmer.himmelsr, k - 1, 1) != chr (10):
                    ch = ch + substring(zimmer.himmelsr, k - 1, 1)
            ch = trim(ch)

            if (len(ch) != 0) and (substring(ch, 0, 1) != "$"):
                room_list.i = room_list.i + 1
                room_list.feature[room_list.i - 1] = ch

                htl_feature = query(htl_feature_list, filters=(lambda htl_feature :htl_feature.s.lower()  == (ch).lower()), first=True)

                if not htl_feature:
                    htl_feature = Htl_feature()
                    htl_feature_list.append(htl_feature)

                    htl_feature.s = ch
                    room_list.himmelsr = room_list.himmelsr + ch + ";"


        room_list.himmelsr = zimmer.himmelsr

    def show_info():

        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list


        room_list.infostr = ""

        if room_list and room_list.infochar != "":

            if substring(room_list.infochar, 0, 1) == "<":

                res_line1 = db_session.query(Res_line1).filter(
                        (Res_line1._recid == room_list.recid1)).first()

                if res_line1:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line1.gastnrpay)).first()
                    room_list.infostr = ""
                    room_list.infostr = room_list.infostr + "<  resno:  " + to_string(res_line1.resnr) + chr (10)
                    room_list.infostr = room_list.infostr + "    " + guest.name + ", " + guest.vorname1 + guest.anredefirma + chr (10)
                    room_list.infostr = room_list.infostr + "Arrival : " + to_string(res_line1.ankunft) + chr (10)
                    room_list.infostr = room_list.infostr + "Depart : " + to_string(res_line1.abreise)
                    room_list.infostr = room_list.infostr + chr (10) + chr (10)

            if substring(room_list.infochar, 1, 1) == ">":

                res_line1 = db_session.query(Res_line1).filter(
                        (Res_line1._recid == room_list.recid2)).first()

                if res_line1:

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line1.gastnrpay)).first()
                    room_list.infostr = room_list.infostr + ">  resno:  " + to_string(res_line1.resnr) + chr (10)
                    room_list.infostr = room_list.infostr + "    " + guest.name + ", " + guest.vorname1 + guest.anredefirma + chr (10)
                    room_list.infostr = room_list.infostr + "Arrival : " + to_string(res_line1.ankunft) + chr (10)
                    room_list.infostr = room_list.infostr + "Depart : " + to_string(res_line1.abreise) + chr (10)


    ci_date = get_output(htpdate(87))

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()
    res_rowid = to_int(res_line._recid)

    if case_type == 1:
        create_list()

    elif case_type == 2:
        create_all_list()

    for room_list in query(room_list_list):
        show_info()

    return generate_output()