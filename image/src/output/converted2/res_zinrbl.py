#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpdate import htpdate
from models import Res_line, Zimmer, Outorder, Paramtext, Guest

def res_zinrbl(case_type:int, resno:int, reslinno:int, zikatno:int, ankunft1:date, abreise1:date):

    prepare_cache ([Res_line, Zimmer, Outorder, Paramtext, Guest])

    room_list_list = []
    htl_feature_list = []
    vhp_limited:bool = False
    res_rowid:int = 0
    ci_date:date = None
    res_line = zimmer = outorder = paramtext = guest = None

    om_list = htl_feature = room_list = resline = res_line1 = None

    om_list_list, Om_list = create_model("Om_list", {"zinr":string, "ind":int})
    htl_feature_list, Htl_feature = create_model("Htl_feature", {"s":string, "flag":int}, {"flag": 1})
    room_list_list, Room_list = create_model("Room_list", {"i":int, "flag":bool, "sleeping":bool, "feature":[string,99], "himmelsr":string, "build":string, "zikennz":string, "build_flag":string, "zistat":string, "infochar":string, "zinr":string, "bezeich":string, "etage":int, "outlook":string, "setup":string, "name":string, "comment":string, "verbindung1":string, "verbindung2":string, "infonum":int, "prioritaet":int, "recid1":int, "recid2":int, "infostr":string}, {"flag": True, "sleeping": True})

    Resline = create_buffer("Resline",Res_line)
    Res_line1 = create_buffer("Res_line1",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal case_type, resno, reslinno, zikatno, ankunft1, abreise1
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list

        return {"room-list": room_list_list, "htl-feature": htl_feature_list}

    def create_list():

        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal case_type, resno, reslinno, zikatno, ankunft1, abreise1
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list


        room_list_list.clear()

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.zikatnr == zikatno) & (Zimmer.zinr != "")).order_by(Zimmer.zinr).all():

            outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(gt, abreise1)],"gespende": [(lt, ankunft1)],"betriebsnr": [(le, 2)]})

            if not outorder:

                if zimmer.zistatus == 6 and ankunft1 <= ci_date:
                    pass
                else:
                    room_list = Room_list()
                    room_list_list.append(room_list)

                    room_list.zinr = zimmer.zinr
                    room_list.prioritaet = zimmer.prioritaet
                    room_list.sleeping = zimmer.sleeping

        for resline in db_session.query(Resline).filter(
                 (Resline.zikatnr == zikatno) & (Resline.zinr != "") & (Resline.resstatus != 12) & (Resline.active_flag <= 1) & (Resline.l_zuordnung[inc_value(2)] == 0)).order_by(Resline._recid).all():

            if to_int(resline._recid) == res_rowid:
                pass

            elif resline.resstatus == 6 and resline.abreise <= ankunft1:
                pass

            elif (resline.abreise <= ankunft1) or (resline.ankunft >= abreise1):
                pass
            else:

                room_list = query(room_list_list, filters=(lambda room_list: room_list.zinr == resline.zinr), first=True)

                if room_list:
                    room_list_list.remove(room_list)
        complete_list()


    def create_all_list():

        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal case_type, resno, reslinno, zikatno, ankunft1, abreise1
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list


        room_list_list.clear()

        for zimmer in db_session.query(Zimmer).filter(
                 (Zimmer.zinr != "")).order_by(Zimmer.zinr).all():

            outorder = get_cache (Outorder, {"zinr": [(eq, zimmer.zinr)],"gespstart": [(gt, abreise1)],"gespende": [(lt, ankunft1)],"betriebsnr": [(le, 2)]})

            if not outorder:
                room_list = Room_list()
                room_list_list.append(room_list)

                room_list.zinr = zimmer.zinr
                room_list.prioritaet = zimmer.prioritaet
                room_list.sleeping = zimmer.sleeping

        for resline in db_session.query(Resline).filter(
                 (Resline.zinr != "") & (Resline.resstatus != 12) & (Resline.active_flag <= 1) & (Resline.l_zuordnung[inc_value(2)] == 0)).order_by(Resline._recid).all():

            if to_int(resline._recid) == res_rowid:
                pass

            elif resline.resstatus == 6 and resline.abreise <= ankunft1:
                pass

            elif (resline.abreise <= ankunft1) or (resline.ankunft >= abreise1):
                pass
            else:

                room_list = query(room_list_list, filters=(lambda room_list: room_list.zinr == resline.zinr), first=True)

                if room_list:
                    room_list_list.remove(room_list)
        complete_list()


    def complete_list():

        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal case_type, resno, reslinno, zikatno, ankunft1, abreise1
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list

        stat_list:List[string] = create_empty_list(10,"")
        stat_list[0] = "VC"
        stat_list[1] = "CU"
        stat_list[2] = "VD"
        stat_list[3] = "ED"
        stat_list[4] = "OD"
        stat_list[5] = "OC"

        for zimmer in db_session.query(Zimmer).order_by(Zimmer._recid).all():
            om_list = Om_list()
            om_list_list.append(om_list)

            om_list.zinr = zimmer.zinr
            om_list.ind = zimmer.zistatus + 1

        for outorder in db_session.query(Outorder).filter(
                 (Outorder.betriebsnr >= 2) & (Outorder.gespstart <= ci_date) & (Outorder.gespende >= ci_date)).order_by(Outorder._recid).all():

            om_list = query(om_list_list, filters=(lambda om_list: om_list.zinr == outorder.zinr), first=True)

            if om_list:
                om_list.ind = 8

        for room_list in query(room_list_list):

            zimmer = get_cache (Zimmer, {"zinr": [(eq, room_list.zinr)]})
            room_list.zikennz = zimmer.zikennz

            if zimmer.himmelsr != "":
                fill_feature()
            room_list.bezeich = zimmer.bezeich
            room_list.verbindung1 = zimmer.verbindung[0]
            room_list.verbindung2 = zimmer.verbindung[1]
            room_list.etage = zimmer.etage

            if zimmer.typ != 0:

                paramtext = get_cache (Paramtext, {"txtnr": [(eq, 230)],"sprachcode": [(eq, zimmer.typ)]})

                if paramtext:
                    room_list.outlook = paramtext.ptexte

            if zimmer.setup != 0:

                paramtext = get_cache (Paramtext, {"txtnr": [(eq, (zimmer.setup + 9200))]})

                if paramtext:
                    room_list.setup = trim(paramtext.ptexte)

            resline = get_cache (Res_line, {"zinr": [(eq, room_list.zinr)],"active_flag": [(lt, 2)],"abreise": [(eq, ankunft1)],"resstatus": [(le, 6)]})

            if resline:
                room_list.infonum = room_list.infonum - 2
                room_list.recid1 = to_int(resline._recid)

            resline = get_cache (Res_line, {"zinr": [(eq, room_list.zinr)],"active_flag": [(eq, 0)],"ankunft": [(eq, abreise)]})

            if resline:
                room_list.infonum = room_list.infonum - 1
                room_list.recid2 = to_int(resline._recid)

            if room_list.infonum == 0:
                room_list.infochar = "<>"

            elif room_list.infonum == 1:
                room_list.infochar = "< "

            elif room_list.infonum == 2:
                room_list.infochar = " >"

            om_list = query(om_list_list, filters=(lambda om_list: om_list.zinr == room_list.zinr), first=True)

            if room_list.prioritaet < 99999:
                room_list.zistat = stat_list[om_list.ind - 1]


    def fill_feature():

        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal case_type, resno, reslinno, zikatno, ankunft1, abreise1
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list

        i:int = 0
        j:int = 0
        k:int = 0
        n:int = 0
        ch:string = ""
        n = 0
        j = 1
        room_list.himmelsr = ""
        for i in range(1,length(zimmer.himmelsr)  + 1) :

            if substring(zimmer.himmelsr, i - 1, 1) == (";").lower()  or substring(zimmer.himmelsr, i - 1, 1) == (",").lower() :
                ch = ""
                for k in range(j,(j + n - 1)  + 1) :

                    if substring(zimmer.himmelsr, k - 1, 1) != chr_unicode(10):
                        ch = ch + substring(zimmer.himmelsr, k - 1, 1)
                ch = trim(ch)

                if (length(ch) != 0) and (substring(ch, 0, 1) != ("$").lower()):
                    room_list.i = room_list.i + 1
                    room_list.feature[room_list.i - 1] = ch

                    htl_feature = query(htl_feature_list, filters=(lambda htl_feature: htl_feature.s.lower()  == (ch).lower()), first=True)

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

                if substring(zimmer.himmelsr, k - 1, 1) != chr_unicode(10):
                    ch = ch + substring(zimmer.himmelsr, k - 1, 1)
            ch = trim(ch)

            if (length(ch) != 0) and (substring(ch, 0, 1) != ("$").lower()):
                room_list.i = room_list.i + 1
                room_list.feature[room_list.i - 1] = ch

                htl_feature = query(htl_feature_list, filters=(lambda htl_feature: htl_feature.s.lower()  == (ch).lower()), first=True)

                if not htl_feature:
                    htl_feature = Htl_feature()
                    htl_feature_list.append(htl_feature)

                    htl_feature.s = ch
                    room_list.himmelsr = room_list.himmelsr + ch + ";"


        room_list.himmelsr = zimmer.himmelsr


    def show_info():

        nonlocal room_list_list, htl_feature_list, vhp_limited, res_rowid, ci_date, res_line, zimmer, outorder, paramtext, guest
        nonlocal case_type, resno, reslinno, zikatno, ankunft1, abreise1
        nonlocal resline, res_line1


        nonlocal om_list, htl_feature, room_list, resline, res_line1
        nonlocal om_list_list, htl_feature_list, room_list_list


        room_list.infostr = ""

        if room_list and room_list.infochar != "":

            if substring(room_list.infochar, 0, 1) == "<":

                res_line1 = get_cache (Res_line, {"_recid": [(eq, room_list.recid1)]})

                if res_line1:

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line1.gastnrpay)]})
                    room_list.infostr = ""
                    room_list.infostr = room_list.infostr + "< resno: " + to_string(res_line1.resnr) + chr_unicode(10)
                    room_list.infostr = room_list.infostr + " " + guest.name + ", " + guest.vorname1 + guest.anredefirma + chr_unicode(10)
                    room_list.infostr = room_list.infostr + "Arrival : " + to_string(res_line1.ankunft) + chr_unicode(10)
                    room_list.infostr = room_list.infostr + "Depart : " + to_string(res_line1.abreise)
                    room_list.infostr = room_list.infostr + chr_unicode(10) + chr_unicode(10)

            if substring(room_list.infochar, 1, 1) == ">":

                res_line1 = get_cache (Res_line, {"_recid": [(eq, room_list.recid2)]})

                if res_line1:

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line1.gastnrpay)]})
                    room_list.infostr = room_list.infostr + "> resno: " + to_string(res_line1.resnr) + chr_unicode(10)
                    room_list.infostr = room_list.infostr + " " + guest.name + ", " + guest.vorname1 + guest.anredefirma + chr_unicode(10)
                    room_list.infostr = room_list.infostr + "Arrival : " + to_string(res_line1.ankunft) + chr_unicode(10)
                    room_list.infostr = room_list.infostr + "Depart : " + to_string(res_line1.abreise) + chr_unicode(10)

    ci_date = get_output(htpdate(87))

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})
    res_rowid = to_int(res_line._recid)

    if case_type == 1:
        create_list()

    elif case_type == 2:
        create_all_list()

    for room_list in query(room_list_list):
        show_info()

    return generate_output()