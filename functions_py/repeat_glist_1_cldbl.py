#using conversion tools version: 1.0.0.117
# pyright: reportAttributeAccessIssue=false

"""_yusufwijasena_

    TICKET ID:
    ISSUE:  - fix definition variabel
            - activate model Genstat, Res_line, & Guest
            - fix python indentation
            - add type ignore to avoid warning
            - update import from function_py 
"""

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions_py.htpint import htpint
from functions_py.get_room_breakdown import get_room_breakdown
from models import Guest, Zimmer, Genstat, Waehrung, Sourccod, Res_line, Reservation, Guestseg, Segment, Nation, Paramtext

def repeat_glist_1_cldbl(pvilanguage:int, from_date:date, to_date:date, ci_date:date, inhouse:bool): # create_inhouse:bool to inhouse:bool

    prepare_cache ([Guest, Genstat, Waehrung, Res_line, Reservation, Guestseg, Segment, Nation, Paramtext])

    g_list_data = []
    repeat_list_data = []
    cur_date_data = []
    tot_payrm:int = 0
    tot_rm:int = 0
    tot_a:int = 0
    tot_c:int = 0
    tot_co:int = 0
    tot_avail:int = 0
    inactive:int = 0
    curr_date:date 
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
    lvcarea:string = "pickup-list"
    zimmer =  waehrung = sourccod =  reservation = guestseg = segment = nation = paramtext = None
    
    genstat = Genstat()
    res_line = Res_line()
    guest = Guest()

    setup_list = g_list = repeat_list = cur_date = gbuff = None

    setup_list_data, Setup_list = create_model(
        "Setup_list", {
            "nr":int, 
            "char":string
            }
        )
    g_list_data, G_list = create_model(
        "G_list", {
            "resnr":int, 
            "gastnr":int, 
            "name":string, 
            "ankunft":date, 
            "abreise":date, 
            "zinr":string, 
            "reslinnr":int, 
            "zipreis":Decimal, 
            "currency":string, 
            "argt":string, 
            "erwachs":int, 
            "kind1":int, 
            "gratis":int, 
            "arrflag":bool, 
            "resname":string, 
            "lodging":Decimal, 
            "source_bez":string
            }
        )
    repeat_list_data, Repeat_list = create_model(
        "Repeat_list", {
            "flag":int, 
            "gastnr":int, 
            "name":string, 
            "nation":string, 
            "birthdate":date, 
            "email":string, 
            "telefon":string, 
            "vip":string, 
            "city":string, 
            "stay":int, 
            "rmnite":int, 
            "ankunft":date, 
            "arrflag":bool, 
            "zinr":string, 
            "remark":string, 
            "resname":string, 
            "lodging":Decimal, 
            "pax":int, 
            "mobil_telefon":string, 
            "source_bez":string
            }
        )
    cur_date_data, Cur_date = create_model(
        "Cur_date", {
            "curr_date":date
            }
        )

    db_session = local_storage.db_session

    def generate_output():
        nonlocal g_list_data, repeat_list_data, cur_date_data, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, integerflag, lvcarea, guest, zimmer, genstat, waehrung, sourccod, res_line, reservation, guestseg, segment, nation, paramtext
        nonlocal pvilanguage, from_date, to_date, ci_date, inhouse
        nonlocal setup_list, g_list, repeat_list, cur_date, gbuff
        nonlocal setup_list_data, g_list_data, repeat_list_data, cur_date_data

        return {
            "g-list": g_list_data, 
            "repeat-list": repeat_list_data, 
            "cur-date": cur_date_data
        }

    def create_inhouse():
        nonlocal g_list_data, repeat_list_data, cur_date_data, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, integerflag, lvcarea, guest, zimmer, genstat, waehrung, sourccod, res_line, reservation, guestseg, segment, nation, paramtext
        nonlocal pvilanguage, from_date, to_date, ci_date, inhouse
        nonlocal setup_list, g_list, repeat_list, cur_date, gbuff
        nonlocal setup_list_data, g_list_data, repeat_list_data, cur_date_data

        i:int = 0
        vip_flag:string = ""
        nr:int = 0
        curr_gastnr:int = 0
        curr_resnr:int = 0
        datum:date 
        datum1:date 
        datum2:date 
        curr_i:int = 0
        net_lodg = to_decimal("0.0")
        fnet_lodg = to_decimal("0.0")
        tot_breakfast = to_decimal("0.0")
        tot_lunch = to_decimal("0.0")
        tot_dinner = to_decimal("0.0")
        tot_other = to_decimal("0.0")
        tot_rmrev = to_decimal("0.0")
        tot_vat = to_decimal("0.0")
        tot_service = to_decimal("0.0")
        tot_lodging = to_decimal("0.0")
        zeit:int = 0
        gfirma = None
        Gfirma =  create_buffer("Gfirma",Guest)
        Gbuff = G_list
        gbuff_data = g_list_data
        tot_payrm = 0
        tot_rm = 0
        tot_a = 0
        tot_c = 0
        tot_co = 0
        inactive = 0


        repeat_list_data.clear()
        g_list_data.clear()
        tot_avail = 0

        for zimmer in db_session.query(Zimmer).filter(
        (Zimmer.sleeping)).order_by(Zimmer._recid).all():
            tot_avail = tot_avail + 1
        cur_date_data.clear()

        if to_date < ci_date:
            for genstat in db_session.query(Genstat).filter(
            (Genstat.datum >= from_date) & (Genstat.datum <= to_date) & (Genstat.gastnrmember > 0) & (Genstat.zinr != "") & (Genstat.resstatus != 13) & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.datum).all():

                if curr_date != genstat.datum:
                    cur_date = Cur_date()
                    cur_date_data.append(cur_date)

                    cur_date.curr_date = genstat.datum 
                    
                g_list = query(g_list_data, filters=(lambda g_list: g_list.resnr == genstat.resnr and g_list.reslinnr == genstat.res_int[0] and g_list.gastnr == genstat.gastnrmember), first=True)

                if not g_list:
                    waehrung = get_cache (Waehrung, {
                        "waehrungsnr": [(eq, genstat.wahrungsnr)]})

                    guest = get_cache (Guest, {
                        "gastnr": [(eq, genstat.gastnrmember)]})

                    gfirma = get_cache (Guest, {
                        "gastnr": [(eq, genstat.gastnr)]})
                    g_list = G_list()
                    g_list_data.append(g_list)

                    g_list.resnr = genstat.resnr  
                    g_list.gastnr = genstat.gastnrmember 
                    g_list.name = gfirma.name + ", " + gfirma.anredefirma 
                    g_list.reslinnr = genstat.res_int[0] 
                    g_list.ankunft = genstat.res_date[0] 
                    g_list.abreise = genstat.res_date[1] 
                    g_list.zinr = genstat.zinr 
                    g_list.zipreis =  to_decimal(genstat.zipreis) 
                    g_list.argt = genstat.argt 
                    g_list.lodging =  to_decimal(g_list.lodging + genstat.logis) 
                    g_list.erwachs = g_list.erwachs + genstat.erwachs 
                    g_list.kind1 = g_list.kind1 + genstat.kind1 + genstat.kind2 
                    g_list.gratis = g_list.gratis + genstat.gratis 

                    if waehrung:
                        g_list.currency = waehrung.wabkurz  

                    sourccod = get_cache (Sourccod, {
                        "source_code": [(eq, genstat.source)]})

                    if sourccod:
                        g_list.source_bez = Sourccod.bezeich  

        elif to_date >= ci_date:
            for res_line in db_session.query(Res_line).filter(
            (Res_line.active_flag <= 2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.ankunft >= from_date) & (Res_line.ankunft <= to_date)).order_by(Res_line.ankunft).all():
                if curr_date != res_line.ankunft:
                    cur_date = Cur_date()
                    cur_date_data.append(cur_date)

                    cur_date.curr_date = res_line.ankunft  

                g_list = query(g_list_data, filters=(lambda g_list: g_list.resnr == res_line.resnr and g_list.reslinnr == res_line.reslinnr and g_list.gastnr == res_line.gastnrmember), first=True)

                if not g_list:
                    waehrung = get_cache (Waehrung, {
                        "waehrungsnr": [(eq, res_line.betriebsnr)]})

                    guest = get_cache (Guest, {
                        "gastnr": [(eq, res_line.gastnrmember)]})

                    gfirma = get_cache (Guest, {
                        "gastnr": [(eq, res_line.gastnr)]})
                    g_list = G_list()
                    g_list_data.append(g_list)

                    g_list.resnr = res_line.resnr 
                    g_list.gastnr = res_line.gastnrmember 
                    g_list.name = gfirma.name + ", " + gfirma.anredefirma 
                    g_list.reslinnr = res_line.reslinnr 
                    g_list.ankunft = res_line.ankunft 
                    g_list.abreise = res_line.abreise 
                    g_list.zinr = res_line.zinr 
                    g_list.zipreis =  to_decimal(res_line.zipreis) 
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

                    for datum in date_range(datum1,datum2) :
                        net_lodg =  to_decimal("0")
                        tot_breakfast =  to_decimal("0")
                        tot_lunch =  to_decimal("0")
                        tot_dinner =  to_decimal("0")
                        tot_other =  to_decimal("0")
                        curr_i = curr_i + 1


                        fnet_lodg, net_lodg, tot_breakfast, tot_lunch, tot_dinner, tot_other, tot_rmrev, tot_vat, tot_service = get_output(get_room_breakdown(res_line._recid, datum, curr_i, datum))
                        g_list.lodging =  to_decimal(g_list.lodging + net_lodg)  
                    if waehrung:
                        g_list.currency = waehrung.wabkurz 

                    reservation = get_cache (Reservation, {
                        "resnr": [(eq, res_line.resnr)]})

                    if reservation:

                        sourccod = get_cache (Sourccod, {
                            "source_code": [(eq, reservation.resart)]})

                        if sourccod:
                            g_list.source_bez = Sourccod.bezeich 
        curr_gastnr = 0
        curr_resnr = 0

        guest_obj_list = {}
        for guest in db_session.query(Guest).filter(
        ((Guest.gastnr.in_(list(set([g_list.gastnr for g_list in g_list_data])))))).order_by(g_list.gastnr, g_list.resnr).all():  # type: ignore g_list
            if guest_obj_list.get(guest._recid):
                continue
            else:
                guest_obj_list[guest._recid] = True

            g_list = query(g_list_data, (lambda g_list: (guest.gastnr == g_list.gastnr)), first=True)

            g_list = G_list()
            if curr_gastnr != g_list.gastnr:   
                repeat_list = Repeat_list()
                repeat_list_data.append(repeat_list)

                curr_gastnr = g_list.gastnr 
                curr_resnr = g_list.resnr 
                repeat_list.gastnr = g_list.gastnr 
                repeat_list.zinr = g_list.zinr 
                repeat_list.ankunft = g_list.ankunft 
                repeat_list.pax = g_list.erwachs + g_list.kind1 + g_list.gratis 
                repeat_list.source_bez = g_list.source_bez 

                if not g_list.arrFlag:  # type: ignore model g_list belum tercreate
                    repeat_list.stay = 1  # type: ignore model repeat_list belum tercreate
                else:
                    repeat_list.arrflag = True # type: ignore model repeat_list belum tercreate
                vip_flag = ""

                guestseg = db_session.query(Guestseg).filter(
                (Guestseg.gastnr == guest.gastnr) & ((Guestseg.segmentcode == vipnr1) | (Guestseg.segmentcode == vipnr2) | (Guestseg.segmentcode == vipnr3) | (Guestseg.segmentcode == vipnr4) | (Guestseg.segmentcode == vipnr5) | (Guestseg.segmentcode == vipnr6) | (Guestseg.segmentcode == vipnr7) | (Guestseg.segmentcode == vipnr8) | (Guestseg.segmentcode == vipnr9))).first()

                if guestseg:

                    segment = get_cache (Segment, {"segmentcode": [(eq, guestseg.segmentcode)]})

                    if segment:
                        vip_flag = segment.bezeich


                repeat_list.vip = vip_flag # type: ignore model repeat_list belum tercreate
                repeat_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 # type: ignore model repeat_list belum tercreate
                repeat_list.birthdate = guest.geburtdatum1 # type: ignore model repeat_list belum tercreate
                repeat_list.email = guest.email_adr # type: ignore model repeat_list belum tercreate
                repeat_list.telefon = guest.telefon # type: ignore model repeat_list belum tercreate
                repeat_list.city = guest.wohnort # type: ignore model repeat_list belum tercreate
                repeat_list.remark = guest.bemerkung # type: ignore model repeat_list belum tercreate
                repeat_list.mobil_telefon = guest.mobil_telefon # type: ignore model repeat_list belum tercreate

                nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

                if nation:
                    repeat_list.nation = nation.bezeich  # type: ignore model repeat_list belum tercreate

                res_line = get_cache (Res_line, {
                    "active_flag": [(eq, 1)],
                    "gastnrmember": [(eq, g_list.gastnr)],  # type: ignore model g_list belum tercreate
                    "resnr": [(eq, g_list.resnr)]}) # type: ignore model g_list belum tercreate

                if res_line:
                    repeat_list.flag = 2 # type: ignore model repeat_list belum tercreate
                    repeat_list.zinr = res_line.zinr # type: ignore model repeat_list belum tercreate
                    repeat_list.ankunft = res_line.ankunft # type: ignore model repeat_list belum tercreate
                    repeat_list.resname = res_line.resname # type: ignore model repeat_list belum tercreate


                else:

                    for res_line in db_session.query(Res_line).filter(
                    ((Res_line.active_flag == 0) | (Res_line.active_flag == 2)) & (Res_line.gastnrmember == g_list.gastnr) & (Res_line.resnr == g_list.resnr)).order_by(Res_line.ankunft).all():  # type: ignore model g_list belum tercreate

                        if res_line.active_flag == 2:
                            repeat_list.resname = res_line.resname # type: ignore model repeat list belum tercreate
                        else:
                            repeat_list.flag = 1  # type: ignore model repeat list belum tercreate
                            repeat_list.ankunft = res_line.ankunft # type: ignore model repeat list belum tercreate
                            repeat_list.resname = res_line.resname # type: ignore model repeat list belum tercreate


                        break
            else:

                if g_list.resnr != curr_resnr:  # type: ignore model g list belum tercreate
                    curr_resnr = g_list.resnr # type: ignore model g list belum tercreate

                    if not g_list.arrFlag: # type: ignore model g list belum tercreate
                        repeat_list.stay = repeat_list.stay + 1 # type: ignore model g list & repeat list belum tercreate
                    else:
                        repeat_list.arrflag = True  # type: ignore model repeat list belum tercreate

            if not g_list.arrFlag:  # type: ignore model g list belum tercreate
                repeat_list.rmnite = repeat_list.rmnite + g_list.abreise - g_list.ankunft # type: ignore model g list & repeat list belum tercreate


            repeat_list.lodging =  to_decimal(g_list.lodging) # type: ignore model repeat list belum tercreate

        for repeat_list in query(repeat_list_data): # type: ignore model repeat list belum tercreate

            if repeat_list.stay < 2 and not repeat_list.arrFLag:
                repeat_list_data.remove(repeat_list)


    def bed_setup():

        nonlocal g_list_data, repeat_list_data, cur_date_data, tot_payrm, tot_rm, tot_a, tot_c, tot_co, tot_avail, inactive, curr_date, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, integerflag, lvcarea, guest, zimmer, genstat, waehrung, sourccod, res_line, reservation, guestseg, segment, nation, paramtext
        nonlocal pvilanguage, from_date, to_date, ci_date, create_inhouse


        nonlocal setup_list, g_list, repeat_list, cur_date, gbuff
        nonlocal setup_list_data, g_list_data, repeat_list_data, cur_date_data


        setup_list_data.clear()
        setup_list = Setup_list()
        setup_list_data.append(setup_list)

        setup_list.nr = 1 # type: ignore model setup list belum tercreate
        setup_list.char = " " # type: ignore model setup list belum tercreate

        for paramtext in db_session.query(Paramtext).filter(
                 (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():
            setup_list = Setup_list()
            setup_list_data.append(setup_list)

            setup_list.nr = paramtext.txtnr - 9199 # type: ignore model setup list belum tercreate
            setup_list.char = substring(paramtext.notes, 0, 1) # type: ignore model setup list belum tercreate


    integerflag = get_output(htpint(700))  # type: ignore return dict unknown dari get_output

    if integerflag > 0:
        vipnr1 = integerflag
    integerflag = get_output(htpint(701)) # type: ignore return dict unknown dari get_output

    if integerflag > 0:
        vipnr2 = integerflag
    integerflag = get_output(htpint(702)) # type: ignore return dict unknown dari get_output

    if integerflag > 0:
        vipnr3 = integerflag
    integerflag = get_output(htpint(703)) # type: ignore return dict unknown dari get_output

    if integerflag > 0:
        vipnr4 = integerflag
    integerflag = get_output(htpint(704)) # type: ignore return dict unknown dari get_output

    if integerflag > 0:
        vipnr5 = integerflag
    integerflag = get_output(htpint(705)) # type: ignore return dict unknown dari get_output

    if integerflag > 0:
        vipnr6 = integerflag
    integerflag = get_output(htpint(706)) # type: ignore return dict unknown dari get_output

    if integerflag > 0:
        vipnr7 = integerflag
    integerflag = get_output(htpint(707)) # type: ignore return dict unknown dari get_output

    if integerflag > 0:
        vipnr8 = integerflag
    integerflag = get_output(htpint(708)) # type: ignore return dict unknown dari get_output

    if integerflag > 0:
        vipnr9 = integerflag
    bed_setup()
    create_inhouse()

    return generate_output()