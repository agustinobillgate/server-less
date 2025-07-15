#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.get_vipnrbl import get_vipnrbl
from models import Paramtext, Guest, Res_line, Waehrung, Reservation, Zimkateg, Kontline, Gentable, Mc_guest, Htparam, Reslin_queasy, Zimmer, Queasy

def arl_list_update_browsebl(show_rate:bool, recid_resline:int, long_stay:int, ci_date:date):

    prepare_cache ([Paramtext, Guest, Res_line, Waehrung, Reservation, Zimkateg, Kontline, Htparam, Reslin_queasy, Zimmer, Queasy])

    arl_list_data = []
    vipnr1:int = 999999999
    vipnr2:int = 999999999
    vipnr3:int = 999999999
    vipnr4:int = 999999999
    vipnr5:int = 999999999
    vipnr6:int = 999999999
    vipnr7:int = 999999999
    vipnr8:int = 999999999
    vipnr9:int = 999999999
    all_inclusive:string = ""
    loopi:int = 0
    loopj:int = 0
    loopk:int = 0
    loopl:int = 0
    ratecodestr:string = ""
    str1:string = ""
    str2:string = ""
    web_com:string = ""
    paramtext = guest = res_line = waehrung = reservation = zimkateg = kontline = gentable = mc_guest = htparam = reslin_queasy = zimmer = queasy = None

    setup_list = gbuff = arl_list = None

    setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})
    arl_list_data, Arl_list = create_model("Arl_list", {"resnr":int, "reslinnr":int, "resline_wabkurz":string, "voucher_nr":string, "grpflag":bool, "verstat":int, "l_zuordnung2":int, "kontignr":int, "firmen_nr":int, "steuernr":string, "rsv_name":string, "zinr":string, "setup_list_char":string, "resline_name":string, "waehrung_wabkurz":string, "segmentcode":int, "ankunft":date, "abreise":date, "zimmeranz":int, "kurzbez":string, "arrangement":string, "zipreis":Decimal, "anztage":int, "erwachs":int, "kind1":int, "kind2":int, "gratis":int, "l_zuordnung4":int, "resstatus":int, "l_zuordnung3":int, "flight_nr":string, "ankzeit":int, "abreisezeit":int, "betrieb_gast":int, "resdat":date, "useridanlage":string, "reserve_dec":Decimal, "cancelled_id":string, "changed_id":string, "groupname":string, "active_flag":int, "gastnr":int, "gastnrmember":int, "karteityp":int, "reserve_int":int, "zikatnr":int, "betrieb_gastmem":int, "pseudofix":bool, "reserve_char":string, "bemerk":string, "depositbez":Decimal, "depositbez2":Decimal, "bestat_dat":date, "briefnr":int, "rsv_gastnr":int, "rsv_resnr":int, "rsv_bemerk":string, "rsv_grpflag":bool, "recid_resline":int, "address":string, "city":string, "comments":string, "resnr_fgcol":int, "mc_str_fgcol":int, "mc_str_bgcol":int, "rsv_name_fgcol":int, "rsv_name_bgcol":int, "zinr_fgcol":int, "reslin_name_fgcol":int, "ankunft_fgcol":int, "anztage_fgcol":int, "abreise_fgcol":int, "segmentcode_fgcol":int, "reslin_name_bgcol":int, "segmentcode_bgcol":int, "zinr_bgcol":int, "webci":string, "webci_flag":string, "voucher_flag":string, "kontignr_flag":string, "ratecode":string}, {"resnr_fgcol": -1, "mc_str_fgcol": -1, "mc_str_bgcol": -1, "rsv_name_fgcol": -1, "rsv_name_bgcol": -1, "zinr_fgcol": -1, "reslin_name_fgcol": -1, "ankunft_fgcol": -1, "anztage_fgcol": -1, "abreise_fgcol": -1, "segmentcode_fgcol": -1, "reslin_name_bgcol": -1, "segmentcode_bgcol": -1, "zinr_bgcol": -1})

    Gbuff = create_buffer("Gbuff",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, all_inclusive, loopi, loopj, loopk, loopl, ratecodestr, str1, str2, web_com, paramtext, guest, res_line, waehrung, reservation, zimkateg, kontline, gentable, mc_guest, htparam, reslin_queasy, zimmer, queasy
        nonlocal show_rate, recid_resline, long_stay, ci_date
        nonlocal gbuff


        nonlocal setup_list, gbuff, arl_list
        nonlocal setup_list_data, arl_list_data

        return {"arl-list": arl_list_data}


    setup_list = Setup_list()
    setup_list_data.append(setup_list)

    setup_list.nr = 1
    setup_list.char = " "

    for paramtext in db_session.query(Paramtext).filter(
             (Paramtext.txtnr >= 9201) & (Paramtext.txtnr <= 9299)).order_by(Paramtext._recid).all():
        setup_list = Setup_list()
        setup_list_data.append(setup_list)

        setup_list.nr = paramtext.txtnr - 9199
        setup_list.char = substring(paramtext.notes, 0, 1)

    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())

    res_line = get_cache (Res_line, {"_recid": [(eq, recid_resline)]})

    gbuff = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

    reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

    setup_list = query(setup_list_data, filters=(lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)

    if matches(res_line.zimmer_wunsch,r"*$CODE$*"):
        ratecodestr = entry(0, substring (res_line.zimmer_wunsch, get_index(res_line.zimmer_wunsch, "$CODE$") + 6 - 1) , ";")
    else:
        ratecodestr = ""
    arl_list = Arl_list()
    arl_list_data.append(arl_list)

    arl_list.resnr = res_line.resnr
    arl_list.reslinnr = res_line.reslinnr
    arl_list.resline_wabkurz = res_line.wabkurz
    arl_list.voucher_nr = res_line.voucher_nr
    arl_list.grpflag = reservation.grpflag
    arl_list.verstat = reservation.verstat
    arl_list.l_zuordnung2 = res_line.l_zuordnung[1]
    arl_list.kontignr = res_line.kontignr
    arl_list.firmen_nr = gbuff.firmen_nr
    arl_list.steuernr = gbuff.steuernr
    arl_list.rsv_name = reservation.name
    arl_list.zinr = res_line.zinr
    arl_list.setup_list_char = setup_list.char
    arl_list.resline_name = res_line.name
    arl_list.waehrung_wabkurz = waehrung.wabkurz
    arl_list.segmentcode = reservation.segmentcode
    arl_list.ankunft = res_line.ankunft
    arl_list.abreise = res_line.abreise
    arl_list.zimmeranz = res_line.zimmeranz
    arl_list.kurzbez = zimkateg.kurzbez
    arl_list.arrangement = res_line.arrangement
    arl_list.zipreis =  to_decimal(res_line.zipreis)
    arl_list.anztage = res_line.anztage
    arl_list.erwachs = res_line.erwachs
    arl_list.kind1 = res_line.kind1
    arl_list.kind2 = res_line.kind2
    arl_list.gratis = res_line.gratis
    arl_list.l_zuordnung4 = res_line.l_zuordnung[3]
    arl_list.resstatus = res_line.resstatus
    arl_list.l_zuordnung3 = res_line.l_zuordnung[2]
    arl_list.flight_nr = res_line.flight_nr
    arl_list.ankzeit = res_line.ankzeit
    arl_list.abreisezeit = res_line.abreisezeit
    arl_list.betrieb_gast = res_line.betrieb_gast
    arl_list.resdat = reservation.resdat
    arl_list.useridanlage = reservation.useridanlage
    arl_list.reserve_dec =  to_decimal(res_line.reserve_dec)
    arl_list.cancelled_id = res_line.cancelled_id
    arl_list.changed_id = res_line.changed_id
    arl_list.groupname = reservation.groupname
    arl_list.active_flag = res_line.active_flag
    arl_list.gastnr = res_line.gastnr
    arl_list.gastnrmember = res_line.gastnrmember
    arl_list.reserve_int = res_line.reserve_int
    arl_list.zikatnr = res_line.zikatnr
    arl_list.betrieb_gastmem = res_line.betrieb_gastmem
    arl_list.pseudofix = res_line.pseudofix
    arl_list.reserve_char = res_line.reserve_char
    arl_list.bemerk = res_line.bemerk
    arl_list.depositbez =  to_decimal(reservation.depositbez)
    arl_list.depositbez2 =  to_decimal(reservation.depositbez2)
    arl_list.bestat_dat = reservation.bestat_datum
    arl_list.briefnr = reservation.briefnr
    arl_list.rsv_gastnr = reservation.gastnr
    arl_list.rsv_resnr = reservation.resnr
    arl_list.rsv_bemerk = reservation.bemerk
    arl_list.rsv_grpflag = reservation.grpflag
    arl_list.recid_resline = res_line._recid
    arl_list.ratecode = ratecodestr

    if res_line:

        guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
        arl_list.address = guest.adresse1
        arl_list.city = guest.wohnort + " " + guest.plz

    if res_line.kontignr > 0:

        kontline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})

        if kontline:
            arl_list.comments = "ALLOTMENT: " + kontline.kontcode + chr_unicode(10)

    elif res_line.kontignr < 0:

        kontline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

        if kontline:
            arl_list.comments = "GLOBAL RES: " + kontline.kontcode + chr_unicode(10)

    if reservation.bemerk != "":
        comments = reservation.bemerk + chr_unicode(10)

    if res_line.bemerk != "":
        arl_list.comments = arl_list.comments + res_line.bemerk

    if res_line:

        gentable = get_cache (Gentable, {"key": [(eq, "reservation")],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

        if gentable:
            arl_list.resnr_fgcol = 12

    if res_line and show_rate:

        mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, res_line.gastnrmember)],"activeflag": [(eq, True)]})

        if mc_guest:
            arl_list.mc_str_fgcol = 15


            arl_list.mc_str_bgcol = 6

    if res_line and res_line.resstatus >= 11:

        if res_line.l_zuordnung[2] == 0:
            arl_list.rsv_name_fgcol = 9


        else:
            arl_list.rsv_name_bgcol = 9
            arl_list.rsv_name_fgcol = 15

    if res_line and (res_line.betrieb_gastmem == vipnr1 or res_line.betrieb_gastmem == vipnr2 or res_line.betrieb_gastmem == vipnr3 or res_line.betrieb_gastmem == vipnr4 or res_line.betrieb_gastmem == vipnr5 or res_line.betrieb_gastmem == vipnr6 or res_line.betrieb_gastmem == vipnr7 or res_line.betrieb_gastmem == vipnr8 or res_line.betrieb_gastmem == vipnr9):
        arl_list.zinr_fgcol = 12
        arl_list.reslin_name_fgcol = 12
        arl_list.ankunft_fgcol = 12
        arl_list.anztage_fgcol = 12
        arl_list.abreise_fgcol = 12
        arl_list.segmentcode_fgcol = 12

    htparam = get_cache (Htparam, {"paramnr": [(eq, 496)]})
    all_inclusive = ";" + htparam.fchar + ";"

    if res_line and matches(all_inclusive,r"*;" + res_line.arrangement + r";*"):
        arl_list.reslin_name_bgcol = 2
        arl_list.reslin_name_fgcol = 15
        arl_list.segmentcode_bgcol = 2
        arl_list.segmentcode_fgcol = 15

    if res_line and res_line.active_flag == 1 and long_stay > 0 and (res_line.abreise - res_line.ankunft) >= long_stay and res_line.erwachs > 0:
        arl_list.reslin_name_fgcol = 15
        arl_list.reslin_name_bgcol = 9

    if res_line and res_line.active_flag <= 1 and res_line.abreise == res_line.ankunft:
        arl_list.reslin_name_fgcol = 0
        arl_list.reslin_name_bgcol = 14

    if res_line and res_line.pseudofix:
        arl_list.reslin_name_bgcol = 12
        arl_list.reslin_name_fgcol = 15

    if res_line:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"betriebsnr": [(eq, 0)]})

        if reslin_queasy:

            if (reslin_queasy.char1 != "" and reslin_queasy.deci1 == 0) or (reslin_queasy.char2 != "" and reslin_queasy.deci2 == 0) or (reslin_queasy.char3 != "" and reslin_queasy.deci3 == 0):
                arl_list.zinr_bgcol = 1
                arl_list.zinr_fgcol = 15


            else:
                arl_list.zinr_bgcol = 9
                arl_list.zinr_fgcol = 15

        if res_line.active_flag == 0 and res_line.zinr != "" and res_line.ankunft == ci_date:

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if zimmer.zistatus == 1:
                arl_list.zinr_fgcol = 0


                arl_list.zinr_bgcol = 11

            elif zimmer.zistatus == 2:
                arl_list.zinr_fgcol = 0


                arl_list.zinr_bgcol = 10

            elif zimmer.zistatus == 3:
                arl_list.zinr_fgcol = 12


                arl_list.zinr_bgcol = 14


    for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :

        if entry(loopi - 1, res_line.zimmer_wunsch, ";") == ("WCI-flag").lower() :
            arl_list.webci = entry(loopi - 1, res_line.zimmer_wunsch, ";")


            break

    if arl_list.voucher_nr != "":
        arl_list.voucher_flag = "L"

    if arl_list.kontignr > 0:
        arl_list.kontignr_flag = "A "

    if arl_list.webci != "":
        for loopj in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str1 = entry(loopj - 1, res_line.zimmer_wunsch, ";")

            if matches(str1,r"*WCI-req*"):
                str2 = entry(1, str1, "=")
                for loopk in range(1,num_entries(str2, ",")  + 1) :

                    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, to_int(entry(loopk - 1, str2, ",")))]})

                    if queasy:
                        for loopl in range(1,num_entries(queasy.char1, ";")  + 1) :

                            if matches(entry(loopl - 1, queasy.char1, ";"),r"*en*"):
                                web_com = entry(1, entry(loopl - 1, queasy.char1, ";") , "=") + ", " + web_com


                                break
                arl_list.comments = "-WEB C/I PREFERENCE-" + chr_unicode(10) + web_com + chr_unicode(10) + arl_list.comments


        arl_list.webci_flag = "W"

    return generate_output()