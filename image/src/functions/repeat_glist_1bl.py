from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.get_room_breakdown import get_room_breakdown
from models import Guest, Zimmer, Genstat, Waehrung, Res_line, Nation, Guestseg, Segment, Paramtext

def repeat_glist_1bl(pvilanguage:int, from_date:date, to_date:date, ci_date:date, create_inhouse:bool):
    g_list_list = []
    repeat_list_list = []
    cur_date_list = []
    tot_payrm:int = 0
    tot_rm:int = 0
    tot_a:int = 0
    tot_c:int = 0
    tot_co:int = 0
    tot_avail:int = 0
    inactive:int = 0
    curr_date:date = None
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    integerflag:int = 0
    lvcarea:str = "pickup_list"
    guest = zimmer = genstat = waehrung = res_line = nation = guestseg = segment = paramtext = None

    setup_list = g_list = repeat_list = cur_date = gfirma = gbuff = None

    setup_list_list, Setup_list = create_model("Setup_list", {"nr":int, "char":str})
    g_list_list, G_list = create_model("G_list", {"resnr":int, "gastnr":int, "name":str, "ankunft":date, "abreise":date, "zinr":str, "reslinnr":int, "zipreis":decimal, "currency":str, "argt":str, "erwachs":int, "kind1":int, "gratis":int, "arrflag":bool, "resname":str, "lodging":decimal})
    repeat_list_list, Repeat_list = create_model("Repeat_list", {"flag":int, "gastnr":int, "name":str, "nation":str, "birthdate":date, "email":str, "telefon":str, "vip":str, "city":str, "stay":int, "rmnite":int, "ankunft":date, "arrflag":bool, "zinr":str, "remark":str, "resname":str, "lodging":decimal, "pax":int, "mobil_telefon":str})
    cur_date_list, Cur_date = create_model("Cur_date", {"curr_date":date})

    Gfirma = Guest
    Gbuff = G_list
    gbuff_list = g_list_list


    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_list_list, repeat_list_list, cur_date_list, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, integerflag, lvcarea, guest, zimmer, genstat, waehrung, res_line, nation, guestseg, segment, paramtext
        nonlocal gfirma, gbuff


        nonlocal setup_list, g_list, repeat_list, cur_date, gfirma, gbuff
        nonlocal setup_list_list, g_list_list, repeat_list_list, cur_date_list
        return {"g-list": g_list_list, "repeat-list": repeat_list_list, "cur-date": cur_date_list}

    def create_inhouse():

        nonlocal g_list_list, repeat_list_list, cur_date_list, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, integerflag, lvcarea, guest, zimmer, genstat, waehrung, res_line, nation, guestseg, segment, paramtext
        nonlocal gfirma, gbuff


        nonlocal setup_list, g_list, repeat_list, cur_date, gfirma, gbuff
        nonlocal setup_list_list, g_list_list, repeat_list_list, cur_date_list

        i:int = 0
        vip_flag:str = ""
        nr:int = 0
        curr_gastnr:int = 0
        curr_resnr:int = 0
        datum:date = None
        datum1:date = None
        datum2:date = None
        curr_i:int = 0
        net_lodg:decimal = 0
        fnet_lodg:decimal = 0
        tot_breakfast:decimal = 0
        tot_lunch:decimal = 0
        tot_dinner:decimal = 0
        tot_other:decimal = 0
        tot_rmrev:decimal = 0
        tot_vat:decimal = 0
        tot_service:decimal = 0
        tot_lodging:decimal = 0
        Gfirma = Guest
        Gbuff = G_list
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0
        curr_date = None


        repeat_list_list.clear()
        g_list_list.clear()
        tot_avail = 0

        for zimmer in db_session.query(Zimmer).filter(
                (Zimmer.sleeping)).all():
            tot_avail = tot_avail + 1
        cur_date_list.clear()

        if to_date < ci_date:

            for genstat in db_session.query(Genstat).filter(
                    (Genstat.datum >= from_date) &  (Genstat.datum <= to_date) &  (Genstat.gastnrmember > 0) &  (Genstat.zinr != "") &  (Genstat.resstatus != 13) &  (Genstat.res_logic[1])).all():

                if curr_date != genstat.datum:
                    cur_date = Cur_date()
                    cur_date_list.append(cur_date)

                    cur_date.curr_date = genstat.datum

                g_list = query(g_list_list, filters=(lambda g_list :g_list.resnr == genstat.resnr and g_list.reslinnr == genstat.res_int[0] and g_list.gastnr == genstat.gastnrmember), first=True)

                if not g_list:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == genstat.wahrungsnr)).first()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == genstat.gastnrmember)).first()

                    gfirma = db_session.query(Gfirma).filter(
                            (Gfirma.gastnr == genstat.gastnr)).first()
                    g_list = G_list()
                    g_list_list.append(g_list)

                    g_list.resnr = genstat.resnr
                    g_list.gastnr = genstat.gastnrmember
                    g_list.name = gfirma.name + ", " + gfirma.anredefirma
                    g_list.reslinnr = genstat.res_int[0]
                    g_list.ankunft = genstat.res_date[0]
                    g_list.abreise = genstat.res_date[1]
                    g_list.zinr = genstat.zinr
                    g_list.zipreis = genstat.zipreis
                    g_list.argt = genstat.argt
                    g_list.lodging = g_list.lodging + genstat.logis
                    g_list.erwachs = g_list.erwachs + genstat.erwachs
                    g_list.kind1 = g_list.kind1 + genstat.kind1 + genstat.kind2
                    g_list.gratis = g_list.gratis + genstat.gratis

                    if waehrung:
                        g_list.currency = waehrung.wabkurz

        elif to_date >= ci_date:
            curr_date = None

            for res_line in db_session.query(Res_line).filter(
                    (Res_line.active_flag <= 2) &  (Res_line.resstatus != 9) &  (Res_line.resstatus != 10) &  (Res_line.resstatus != 12) &  (Res_line.resstatus != 99) &  (Res_line.ankunft >= from_date) &  (Res_line.ankunft <= to_date)).all():

                if curr_date != res_line.ankunft:
                    cur_date = Cur_date()
                    cur_date_list.append(cur_date)

                    cur_date.curr_date = res_line.ankunft

                g_list = query(g_list_list, filters=(lambda g_list :g_list.resnr == res_line.resnr and g_list.reslinnr == res_line.reslinnr and g_list.gastnr == res_line.gastnrmember), first=True)

                if not g_list:

                    waehrung = db_session.query(Waehrung).filter(
                            (Waehrungsnr == res_line.betriebsnr)).first()

                    guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember)).first()

                    gfirma = db_session.query(Gfirma).filter(
                            (Gfirma.gastnr == res_line.gastnr)).first()
                    g_list = G_list()
                    g_list_list.append(g_list)

                    g_list.resnr = res_line.resnr
                    g_list.gastnr = res_line.gastnrmember
                    g_list.name = gfirma.name + ", " + gfirma.anredefirma
                    g_list.reslinnr = res_line.reslinnr
                    g_list.ankunft = res_line.ankunft
                    g_list.abreise = res_line.abreise
                    g_list.zinr = res_line.zinr
                    g_list.zipreis = res_line.zipreis
                    g_list.argt = res_line.arrangement
                    g_list.arrFlag = (res_line.active_flag == 0)
                    g_list.resname = res_line.resname
                    g_list.erwachs = res_line.erwachs
                    g_list.kind1 = res_line.kind1 + res_line.kind2
                    g_list.gratis = res_line.gratis


                    datum1 = res_line.ankunft

                    if res_line.ankunft == res_line.abreise:
                        datum2 = res_line.abreise


                    else:
                        datum2 = res_line.abreise - 1


                    curr_i = 0


                    for datum in range(datum1,datum2 + 1) :
                        net_lodg = 0
                        tot_breakfast = 0
                        tot_lunch = 0
                        tot_dinner = 0
                        tot_other = 0
                        curr_i = curr_i + 1


                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, datum))
                        g_list.lodging = g_list.lodging + net_lodg

                    if waehrung:
                        g_list.currency = waehrung.wabkurz
        curr_gastnr = 0
        curr_resnr = 0

        for g_list in query(g_list_list):

            if curr_gastnr != g_list.gastnr:
                repeat_list = Repeat_list()
                repeat_list_list.append(repeat_list)

                curr_gastnr = g_list.gastnr
                curr_resnr = g_list.resnr
                repeat_list.gastnr = g_list.gastnr
                repeat_list.zinr = g_list.zinr
                repeat_list.ankunft = g_list.ankunft
                repeat_list.pax = g_list.erwachs + g_list.kind1 + g_list.gratis

                if not g_list.arrFlag:
                    repeat_list.stay = 1
                else:
                    repeat_list.arrFlag = True
            else:

                if g_list.resnr != curr_resnr:
                    curr_resnr = g_list.resnr

                    if not g_list.arrFlag:
                        repeat_list.stay = repeat_list.stay + 1
                    else:
                        repeat_list.arrFlag = True

            if not g_list.arrFlag:
                repeat_list.rmnite = repeat_list.rmnite + g_list.abreise - g_list.ankunft


            repeat_list.lodging = g_list.lodging

        for repeat_list in query(repeat_list_list):

            if repeat_list.stay < 2 and not repeat_list.arrFLag:
                repeat_list_list.remove(repeat_list)
            else:

                genstat = db_session.query(Genstat).filter(
                        (Genstat.gastnr == repeat_list.gastnr)).first()

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == repeat_list.gastnr)).first()

                nation = db_session.query(Nation).filter(
                        (Nation.kurzbez == guest.nation1)).first()
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                        (Guestseg.gastnr == guest.gastnr) &  ((Guestseg.segmentcode == vipnr1) |  (Guestseg.segmentcode == vipnr2) |  (Guestseg.segmentcode == vipnr3) |  (Guestseg.segmentcode == vipnr4) |  (Guestseg.segmentcode == vipnr5) |  (Guestseg.segmentcode == vipnr6) |  (Guestseg.segmentcode == vipnr7) |  (Guestseg.segmentcode == vipnr8) |  (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = db_session.query(Segment).filter(
                            (Segment.segmentcode == guestseg.segmentcode)).first()

                    if segment:
                        vip_flag = segment.bezeich


                repeat_list.vip = vip_flag
                repeat_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
                repeat_list.birthdate = guest.geburtdatum1
                repeat_list.email = guest.email_adr
                repeat_list.telefon = guest.telefon
                repeat_list.city = guest.wohnort
                repeat_list.remark = guest.bemerk
                repeat_list.mobil_telefon = guest.mobil_telefon

                if nation:
                    repeat_list.nation = nation.bezeich

                res_line = db_session.query(Res_line).filter(
                        (Res_line.active_flag == 1) &  (Res_line.gastnrmember == repeat_list.gastnr)).first()

                if res_line:
                    repeat_list.flag = 2
                    repeat_list.zinr = res_line.zinr
                    repeat_list.ankunft = res_line.ankunft
                    repeat_list.resname = res_line.resname


                else:

                    for res_line in db_session.query(Res_line).filter(
                            (Res_line.active_flag == 0) &  (Res_line.gastnrmember == repeat_list.gastnr)).all():
                        repeat_list.flag = 1
                        repeat_list.ankunft = res_line.ankunft
                        repeat_list.resname = res_line.resname


                        break

    def bed_setup():

        nonlocal g_list_list, repeat_list_list, cur_date_list, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, integerflag, lvcarea, guest, zimmer, genstat, waehrung, res_line, nation, guestseg, segment, paramtext
        nonlocal gfirma, gbuff


        nonlocal setup_list, g_list, repeat_list, cur_date, gfirma, gbuff
        nonlocal setup_list_list, g_list_list, repeat_list_list, cur_date_list


        setup_list_list.clear()
        setup_list = Setup_list()
        setup_list_list.append(setup_list)

        setup_list.nr = 1
        setup_list.char = " "

        for paramtext in db_session.query(Paramtext).filter(
                (Paramtext.txtnr >= 9201) &  (Paramtext.txtnr <= 9299)).all():
            setup_list = Setup_list()
            setup_list_list.append(setup_list)

            setup_list.nr = paramtext.txtnr - 9199
            setup_list.char = substring(paramtext.notes, 0, 1)

    integerflag = get_output(htpint(700))

    if integerflag > 0:
        vipnr1 = integerflag
    integerflag = get_output(htpint(701))

    if integerflag > 0:
        vipnr2 = integerflag
    integerflag = get_output(htpint(702))

    if integerflag > 0:
        vipnr3 = integerflag
    integerflag = get_output(htpint(703))

    if integerflag > 0:
        vipnr4 = integerflag
    integerflag = get_output(htpint(704))

    if integerflag > 0:
        vipnr5 = integerflag
    integerflag = get_output(htpint(705))

    if integerflag > 0:
        vipnr6 = integerflag
    integerflag = get_output(htpint(706))

    if integerflag > 0:
        vipnr7 = integerflag
    integerflag = get_output(htpint(707))

    if integerflag > 0:
        vipnr8 = integerflag
    integerflag = get_output(htpint(708))

    if integerflag > 0:
        vipnr9 = integerflag
    bed_setup()
    create_inhouse()

    return generate_output()