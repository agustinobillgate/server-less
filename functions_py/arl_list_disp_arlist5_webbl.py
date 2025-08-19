#using conversion tools version: 1.0.0.118

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.htpint import htpint
from functions.get_vipnrbl import get_vipnrbl
from sqlalchemy import func
from functions.prepare_gcf_history_1bl import prepare_gcf_history_1bl
# from functions.gcf_history_4blho import gcf_history_4blho # Oscar - skip because using HServer on Progress
from models import Guest, History, Paramtext, Htparam, Res_line, Waehrung, Reservation, Zimkateg, Bresline, Guestseg, Master, Messages, Kontline, Gentable, Mc_guest, Reslin_queasy, Zimmer, Queasy, Fixleist

t_payload_list_data, T_payload_list = create_model("T_payload_list", {"argt_str":string})

def arl_list_disp_arlist5_webbl(t_payload_list_data:[T_payload_list], show_rate:bool, last_sort:int, lresnr:int, long_stay:int, ci_date:date, grpflag:bool, room:string, lname:string, sorttype:int, fdate1:date, fdate2:date, fdate:date, excl_rmshare:bool, voucher_no:string, nation_str:string):

    prepare_cache ([Guest, Paramtext, Htparam, Waehrung, Reservation, Zimkateg, Bresline, Kontline, Reslin_queasy, Zimmer, Queasy])

    rmlen = 0
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
    vipnr10:int = 999999999
    done_flag:bool = False
    curr_resnr:int = 0
    curr_resline:int = 0
    today_str:string = ""
    reserve_str:string = ""
    created_time:int = 0
    do_it:bool = True
    loop_i:int = 0
    comment_str:string = ""
    all_inclusive:string = ""
    res_mode:string = ""
    checkin_flag:bool = False
    tmpdate:date = None
    tmpint:int = 0
    stay:int = 0
    resbemerk:string = ""
    rescomment:string = ""
    rsvbemerk:string = ""
    blacklist_int:int = 0
    arl_list_reslin_name_fgcol:int = 0
    arl_list_reslin_name_bgcol:int = 0
    htl_name:string = ""
    vhost:string = ""
    vservice:string = ""
    hoappparam:string = ""
    lreturn:bool = False
    centralized_flag:bool = False
    guest = history = paramtext = htparam = res_line = waehrung = reservation = zimkateg = bresline = guestseg = master = messages = kontline = gentable = mc_guest = reslin_queasy = zimmer = queasy = fixleist = None

    setup_list = gbuff = gbuffmember = arl_list = b_arl_list = t_payload_list = ghistory = summ_list = gmember = None

    setup_list_data, Setup_list = create_model("Setup_list", {"nr":int, "char":string})
    arl_list_data, Arl_list = create_model("Arl_list", {"resnr":int, "reslinnr":int, "resline_wabkurz":string, "voucher_nr":string, "grpflag":bool, "verstat":int, "l_zuordnung2":int, "kontignr":int, "firmen_nr":int, "steuernr":string, "rsv_name":string, "zinr":string, "setup_list_char":string, "resline_name":string, "waehrung_wabkurz":string, "segmentcode":int, "ankunft":date, "abreise":date, "zimmeranz":int, "kurzbez":string, "arrangement":string, "zipreis":Decimal, "anztage":int, "erwachs":int, "kind1":int, "kind2":int, "gratis":int, "l_zuordnung4":int, "resstatus":int, "l_zuordnung3":int, "flight_nr":string, "ankzeit":int, "abreisezeit":int, "betrieb_gast":int, "resdat":date, "useridanlage":string, "reserve_dec":Decimal, "cancelled_id":string, "changed_id":string, "groupname":string, "active_flag":int, "gastnr":int, "gastnrmember":int, "karteityp":int, "reserve_int":int, "zikatnr":int, "betrieb_gastmem":int, "pseudofix":bool, "reserve_char":string, "bemerk":string, "depositbez":Decimal, "depositbez2":Decimal, "bestat_dat":date, "briefnr":int, "rsv_gastnr":int, "rsv_resnr":int, "rsv_bemerk":string, "rsv_grpflag":bool, "recid_resline":int, "address":string, "city":string, "comments":string, "resnr_fgcol":int, "mc_str_fgcol":int, "mc_str_bgcol":int, "mc_flag":bool, "rsv_name_fgcol":int, "rsv_name_bgcol":int, "zinr_fgcol":int, "reslin_name_fgcol":int, "ankunft_fgcol":int, "anztage_fgcol":int, "abreise_fgcol":int, "segmentcode_fgcol":int, "reslin_name_bgcol":int, "segmentcode_bgcol":int, "zinr_bgcol":int, "webci":string, "webci_flag":string, "voucher_flag":string, "kontignr_flag":string, "birthday_flag":bool, "sharer_no":int, "guest_blacklist":bool, "fixcost_flag":bool, "gastmobileno":string, "special_request":string}, {"resnr_fgcol": -1, "mc_str_fgcol": -1, "mc_str_bgcol": -1, "rsv_name_fgcol": -1, "rsv_name_bgcol": -1, "zinr_fgcol": -1, "reslin_name_fgcol": -1, "ankunft_fgcol": -1, "anztage_fgcol": -1, "abreise_fgcol": -1, "segmentcode_fgcol": -1, "reslin_name_bgcol": -1, "segmentcode_bgcol": -1, "zinr_bgcol": -1})
    b_arl_list_data, B_arl_list = create_model("B_arl_list", {"resnr":int, "reslinnr":int, "resline_wabkurz":string, "voucher_nr":string, "grpflag":bool, "verstat":int, "l_zuordnung2":int, "kontignr":int, "firmen_nr":int, "steuernr":string, "rsv_name":string, "zinr":string, "setup_list_char":string, "resline_name":string, "waehrung_wabkurz":string, "segmentcode":int, "ankunft":date, "abreise":date, "zimmeranz":int, "kurzbez":string, "arrangement":string, "zipreis":Decimal, "anztage":int, "erwachs":int, "kind1":int, "kind2":int, "gratis":int, "l_zuordnung4":int, "resstatus":int, "l_zuordnung3":int, "flight_nr":string, "ankzeit":int, "abreisezeit":int, "betrieb_gast":int, "resdat":date, "useridanlage":string, "reserve_dec":Decimal, "cancelled_id":string, "changed_id":string, "groupname":string, "active_flag":int, "gastnr":int, "gastnrmember":int, "karteityp":int, "reserve_int":int, "zikatnr":int, "betrieb_gastmem":int, "pseudofix":bool, "reserve_char":string, "bemerk":string, "depositbez":Decimal, "depositbez2":Decimal, "bestat_dat":date, "briefnr":int, "rsv_gastnr":int, "rsv_resnr":int, "rsv_bemerk":string, "rsv_grpflag":bool, "recid_resline":int, "address":string, "city":string, "comments":string, "resnr_fgcol":int, "mc_str_fgcol":int, "mc_str_bgcol":int, "mc_flag":bool, "rsv_name_fgcol":int, "rsv_name_bgcol":int, "zinr_fgcol":int, "reslin_name_fgcol":int, "ankunft_fgcol":int, "anztage_fgcol":int, "abreise_fgcol":int, "segmentcode_fgcol":int, "reslin_name_bgcol":int, "segmentcode_bgcol":int, "zinr_bgcol":int, "webci":string, "webci_flag":string, "voucher_flag":string, "kontignr_flag":string, "birthday_flag":bool, "sharer_no":int, "guest_blacklist":bool, "fixcost_flag":bool, "gastmobileno":string, "special_request":string}, {"resnr_fgcol": -1, "mc_str_fgcol": -1, "mc_str_bgcol": -1, "rsv_name_fgcol": -1, "rsv_name_bgcol": -1, "zinr_fgcol": -1, "reslin_name_fgcol": -1, "ankunft_fgcol": -1, "anztage_fgcol": -1, "abreise_fgcol": -1, "segmentcode_fgcol": -1, "reslin_name_bgcol": -1, "segmentcode_bgcol": -1, "zinr_bgcol": -1})
    ghistory_data, Ghistory = create_model_like(History, {"hname":string, "gname":string, "address":string, "s_recid":int, "vcrnr":string, "mblnr":string, "email":string})
    summ_list_data, Summ_list = create_model_like(History)

    Gbuff = create_buffer("Gbuff",Guest)
    Gbuffmember = create_buffer("Gbuffmember",Guest)
    Gmember = create_buffer("Gmember",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        return {"fdate1": fdate1, "fdate2": fdate2, "rmlen": rmlen, "arl-list": arl_list_data}

    def get_toname(lname:string):

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data


        return chr_unicode(asc(substring(lname, 0, 1)) + 1)


    def fixing_blank_resname():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        rline = None
        Rline =  create_buffer("Rline",Res_line)

        res_line = get_cache (Res_line, {"active_flag": [(le, 1)],"resstatus": [(ne, 12)],"resname": [(eq, "")]})
        while None != res_line:

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

            rline = db_session.query(Rline).filter(
                         (Rline._recid == res_line._recid)).first()

            if rline:
                rline.resname = guest.name


                pass
                pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag <= 1) & (Res_line.resstatus != 12) & (Res_line.resname == "") & (Res_line._recid > curr_recid)).first()


    def disp_arlist1():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        to_name:string = ""
        igrpname:int = 0
        igrpname = to_int(grpflag)
        rmlen = length(room)

        if lname != "":

            if substring(lname, 0, 1) == ("*").lower() :

                if substring(lname, length(lname) - 1, 1) != ("*").lower() :
                    lname = lname + "*"
            else:
                to_name = get_toname (lname)

        if sorttype == 1:
            disp_arrivea()

        elif sorttype == 2:

            if last_sort == 1:

                if room != "":

                    if lname == "":

                        res_line_obj_list = {}
                        for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                            setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                            if not setup_list:
                                continue

                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            create_it()


                    elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                        res_line_obj_list = {}
                        for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (matches(Res_line.name,("*" + lname + "*"))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                            setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                            if not setup_list:
                                continue

                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            create_it()


                    elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                        res_line_obj_list = {}
                        for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (matches(Res_line.name,(lname))) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                            setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                            if not setup_list:
                                continue

                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            create_it()


                elif room == "":

                    if lname == "":

                        res_line_obj_list = {}
                        for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                            setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                            if not setup_list:
                                continue

                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            create_it()


                    elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                        res_line_obj_list = {}
                        for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (matches(Res_line.name,("*" + lname + "*"))) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.name).all():
                            setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                            if not setup_list:
                                continue

                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            create_it()


                    elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                        res_line_obj_list = {}
                        for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (matches(Res_line.name,(lname))) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.name).all():
                            setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                            if not setup_list:
                                continue

                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            create_it()


            if last_sort == 2:
                sqry2()

            elif last_sort == 3:
                sqry3()

            elif last_sort == 4:
                sqry4()

            elif last_sort == 5:
                sqry5()

            elif last_sort == 6:
                sqry6()

            elif last_sort == 7:
                sqry7()

            elif last_sort == 8:
                sqry8()

        elif sorttype == 3:

            if last_sort == 1:

                if lname == "":

                    if room == "":

                        res_line_obj_list = {}
                        for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                                 (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                            setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                            if not setup_list:
                                continue

                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            create_it()


                    elif room != "":

                        res_line_obj_list = {}
                        for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                                 (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                            setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                            if not setup_list:
                                continue

                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            create_it()


                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (matches(Res_line.name,("*" + lname + "*"))) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.name, Res_line.zinr).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


                elif substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (matches(Res_line.name,(lname))) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.name, Res_line.zinr).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


            elif last_sort == 2:
                sqry2()

            elif last_sort == 3:
                sqry3()

            elif last_sort == 4:
                sqry4()

            elif last_sort == 5:
                sqry5()

            elif last_sort == 6:
                sqry6()

            elif last_sort == 7:
                sqry7()

            elif last_sort == 8:
                sqry8()

        elif sorttype == 4:

            if last_sort == 1:

                if lname == "":

                    if room == "":

                        res_line_obj_list = {}
                        for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                            setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                            if not setup_list:
                                continue

                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            create_it()


                    elif room != "":

                        res_line_obj_list = {}
                        for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                                 (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                            setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                            if not setup_list:
                                continue

                            if res_line_obj_list.get(res_line._recid):
                                continue
                            else:
                                res_line_obj_list[res_line._recid] = True


                            create_it()


                elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & (matches(Res_line.name,("*" + lname + "*"))) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.name, Res_line.zinr).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


                elif substring(lname, 0, 1) == ("*").lower() :

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & (matches(Res_line.name,(lname))) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.name, Res_line.zinr).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


            elif last_sort == 2:
                sqry2()

            elif last_sort == 3:
                sqry3()

            elif last_sort == 4:
                sqry4()

            elif last_sort == 5:
                sqry5()

            elif last_sort == 6:
                sqry6()

            elif last_sort == 7:
                sqry7()

            elif last_sort == 8:
                sqry8()


    def disp_arrivea():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        to_name:string = ""
        igrpname:int = 0
        igrpname = to_int(grpflag)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = get_toname (lname)

        if last_sort == 1:

            if fdate1 == None or fdate2 == None:
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=365)

            if lname == "":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


            elif substring(lname, 0, 1) != ("*").lower()  and lname != "":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & (matches(Res_line.name,("*" + lname + "*")))).order_by(Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (matches(Res_line.name,(lname))) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


        elif last_sort == 2:

            if fdate1 == None or fdate2 == None:
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=365)

            if lname == "":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Reservation.name, Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


            elif substring(lname, 0, 1) == ("*").lower()  and lname != "":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname) & (matches(Reservation.name,(lname)))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Reservation.name, Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname) & (matches(Reservation.name,("*" + lname + "*")))).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Reservation.name, Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


        elif last_sort == 3:
            tmpdate = ci_date + timedelta(days=30)

            if lresnr == 0:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft >= ci_date) & (Res_line.ankunft <= tmpdate) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & ((Res_line.resnr == lresnr) | (Res_line.l_zuordnung[inc_value(4)] == lresnr)) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


        elif last_sort == 4:

            if (fdate1 == None) or (fdate2 == None):
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=365)

            res_line_obj_list = {}
            for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.ankunft, Reservation.name, Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                if not setup_list:
                    continue

                if res_line_obj_list.get(res_line._recid):
                    continue
                else:
                    res_line_obj_list[res_line._recid] = True


                create_it()

        elif last_sort == 5:
            sqry5()

        elif last_sort == 6:
            sqry6()

        elif last_sort == 7:
            sqry7()

        elif last_sort == 8:
            sqry8()


    def sqry2():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        to_name:string = ""
        igrpname:int = 0
        igrpname = to_int(grpflag)
        rmlen = length(room)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = get_toname (lname)

        if sorttype == 2:

            if lname == "":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (Reservation.name >= (lname).lower()) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date) & (Res_line.resname >= (lname).lower())).order_by(Reservation.name, Reservation.groupname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (matches(Reservation.name,("*" + lname + "*"))) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Reservation.name, Reservation.groupname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (matches(Reservation.name,(lname))) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Reservation.name, Reservation.groupname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


        elif sorttype == 3:

            if lname == "":

                if room == "":

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Reservation.name, Reservation.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


                elif room != "":

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, Reservation.name, Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


            elif substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (matches(Reservation.name,(lname))) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Reservation.name, Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


            elif substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (matches(Reservation.name,("*" + lname + "*"))) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Reservation.name, Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


        elif sorttype == 4:

            if lname == "":

                if room == "":

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Reservation.name, Reservation.groupname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


                elif room != "":

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, Reservation.name, Reservation.groupname, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


            elif substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (matches(Reservation.name,(lname))) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Reservation.name, Reservation.groupname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


            elif substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (matches(Reservation.name,("*" + lname + "*"))) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Reservation.name, Reservation.groupname, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

    def sqry3():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        igrpname:int = 0
        igrpname = to_int(grpflag)

        if sorttype == 2:

            if lresnr == 0:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((Res_line.resnr == lresnr) | (Res_line.l_zuordnung[inc_value(4)] == lresnr))).order_by(Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


        elif sorttype == 3:

            if lresnr == 0:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & ((Res_line.resnr == lresnr) | (Res_line.l_zuordnung[inc_value(4)] == lresnr))).order_by(Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


        elif sorttype == 4:

            if lresnr == 0:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate)).order_by(Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((Res_line.resnr == lresnr) | (Res_line.l_zuordnung[inc_value(4)] == lresnr))).order_by(Res_line.l_zuordnung[inc_value(4)], Res_line.resnr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

    def sqry4():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        to_name:string = ""
        igrpname:int = 0
        igrpname = to_int(grpflag)
        rmlen = length(room)

        if lname != "" and substring(lname, 0, 1) != ("*").lower() :
            to_name = get_toname (lname)

        if sorttype == 2:

            if fdate != None:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.ankunft >= fdate) & (Res_line.abreise >= ci_date)).order_by(Res_line.ankunft, Reservation.name, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.ankunft, Reservation.name, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


        elif sorttype == 3:

            if lname == "":

                if room == "":

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 99) & (Res_line.resstatus != 10) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


                elif room != "":

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower())).order_by(Res_line.name, Res_line.zinr).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (matches(Res_line.name,(lname)))).order_by(Res_line.name, Res_line.zinr).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


        elif sorttype == 4:

            if lname == "":

                if room == "":

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


                elif room != "":

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()


            elif lname != "" and substring(lname, 0, 1) != ("*").lower() :

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.name >= (lname).lower()) & (Res_line.name <= (to_name).lower())).order_by(Res_line.name, Res_line.zinr).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


            elif lname != "" and substring(lname, 0, 1) == ("*").lower() :

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (matches(Res_line.name,(lname)))).order_by(Res_line.name, Res_line.zinr).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

    def sqry5():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        igrpname:int = 0
        igrpname = to_int(grpflag)


        rmlen = length(room)

        if sorttype == 1:

            if (fdate1 == None) or (fdate2 == None):
                fdate1 = ci_date
                fdate2 = ci_date + timedelta(days=365)

            if room != "":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.zinr == (room).lower()) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.zinr == (room).lower()) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

        elif sorttype == 2:

            if fdate != None:

                if room != "":

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date) & (substring(Res_line.zinr, 0, to_int(rmlen)) == (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()
                else:

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.zinr >= (room).lower()) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()
            else:

                if room != "":

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date) & (substring(Res_line.zinr, 0, to_int(rmlen)) == (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()
                else:

                    res_line_obj_list = {}
                    for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                             (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date) & (Res_line.zinr >= (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                        setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                        if not setup_list:
                            continue

                        if res_line_obj_list.get(res_line._recid):
                            continue
                        else:
                            res_line_obj_list[res_line._recid] = True


                        create_it()

        elif sorttype == 3:

            if room != "":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & (Res_line.resname >= (lname).lower()) & (substring(Res_line.zinr, 0, to_int(rmlen)) == (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & (Res_line.resname >= (lname).lower()) & (Res_line.zinr >= (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

        elif sorttype == 4:

            if room != "":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & (Res_line.resname >= (lname).lower()) & (substring(Res_line.zinr, 0, to_int(rmlen)) == (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & (Res_line.resname >= (lname).lower()) & (Res_line.zinr >= (room).lower())).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


    def sqry6():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        igrpname:int = 0
        i:int = 0
        str:string = ""
        igrpname = to_int(grpflag)

        if sorttype == 1:

            if voucher_no != "" and voucher_no != None:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & (matches(Res_line.zimmer_wunsch,("*Voucher*")))).order_by(Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    if reservation.vesrdepot.lower()  == (voucher_no).lower() :
                        create_it()
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 7) == ("voucher").lower()  and substring(str, 7) == (voucher_no).lower() :
                                i = 999
                                create_it()

        elif sorttype == 2:

            if voucher_no != "" and voucher_no != None:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    if reservation.vesrdepot.lower()  == (voucher_no).lower() :
                        create_it()
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 7) == ("voucher").lower()  and substring(str, 7) == (voucher_no).lower() :
                                i = 999
                                create_it()

        elif sorttype == 3:

            if voucher_no != "" and voucher_no != None:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    if reservation.vesrdepot.lower()  == (voucher_no).lower() :
                        create_it()
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 7) == ("voucher").lower()  and substring(str, 7) == (voucher_no).lower() :
                                i = 999
                                create_it()

        elif sorttype == 4:

            if voucher_no != "" and voucher_no != None:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    if reservation.vesrdepot.lower()  == (voucher_no).lower() :
                        create_it()
                    else:
                        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
                            str = entry(i - 1, res_line.zimmer_wunsch, ";")

                            if substring(str, 0, 7) == ("voucher").lower()  and substring(str, 7) == (voucher_no).lower() :
                                i = 999
                                create_it()


    def sqry7():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        igrpname:int = 0
        i:int = 0
        str:string = ""
        igrpname = to_int(grpflag)

        if sorttype == 1:

            if nation_str == " ":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)],"nation1": [(eq, nation_str)]})

                    if guest:
                        create_it()

        elif sorttype == 2:

            if nation_str == " ":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)],"nation1": [(eq, nation_str)]})

                    if guest:
                        create_it()

        elif sorttype == 3:

            if nation_str == " ":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)],"nation1": [(eq, nation_str)]})

                    if guest:
                        create_it()

        elif sorttype == 4:

            if nation_str == " ":

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True

                    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)],"nation1": [(eq, nation_str)]})

                    if guest:
                        create_it()


    def sqry8():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        igrpname:int = 0

        t_payload_list = query(t_payload_list_data, first=True)
        igrpname = to_int(grpflag)

        if fdate1 == None or fdate2 == None:
            fdate1 = ci_date
            fdate2 = ci_date + timedelta(days=365)

        if sorttype == 1:

            if t_payload_list.argt_str == " " or t_payload_list.argt_str == None:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft >= fdate1) & (Res_line.ankunft <= fdate2) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & (Res_line.arrangement == t_payload_list.argt_str)).order_by((Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

        elif sorttype == 2:

            if t_payload_list.argt_str == " " or t_payload_list.argt_str == None:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.ankunft <= ci_date) & (Res_line.abreise >= ci_date) & (Res_line.arrangement == t_payload_list.argt_str)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

        elif sorttype == 3:

            if t_payload_list.argt_str == " " or t_payload_list.argt_str == None:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 0) & (Res_line.ankunft == ci_date) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.resstatus != 99) & (Res_line.arrangement == t_payload_list.argt_str)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()

        elif sorttype == 4:

            if t_payload_list.argt_str == " " or t_payload_list.argt_str == None:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower()))).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()
            else:

                res_line_obj_list = {}
                for res_line, gbuff, waehrung, reservation, zimkateg in db_session.query(Res_line, Gbuff, Waehrung, Reservation, Zimkateg).join(Gbuff,(Gbuff.gastnr == Res_line.gastnr)).join(Waehrung,(Waehrung.waehrungsnr == Res_line.betriebsnr)).join(Reservation,(Reservation.resnr == Res_line.resnr) & (length(trim(Reservation.groupname)) >= igrpname)).join(Zimkateg,(Zimkateg.zikatnr == Res_line.zikatnr)).filter(
                         (Res_line.active_flag == 1) & (Res_line.resstatus != 12) & (Res_line.resstatus != 99) & (Res_line.resstatus != 99) & (Res_line.abreise == fdate) & ((substring(Res_line.zinr, 0, to_int(rmlen))) >= ((room).lower())) & (Res_line.arrangement == t_payload_list.argt_str)).order_by(Res_line.zinr, (Res_line.kontakt_nr * Res_line.resnr), Res_line.resstatus, Res_line.name).all():
                    setup_list = query(setup_list_data, (lambda setup_list: setup_list.nr == res_line.setup + 1), first=True)
                    if not setup_list:
                        continue

                    if res_line_obj_list.get(res_line._recid):
                        continue
                    else:
                        res_line_obj_list[res_line._recid] = True


                    create_it()


    def create_it():

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        loopi:int = 0
        loopj:int = 0
        loopk:int = 0
        loopl:int = 0
        str1:string = ""
        str2:string = ""
        web_com:string = ""
        bday:date = None
        bresline = None
        Bresline =  create_buffer("Bresline",Res_line)

        gmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})
        arl_list = Arl_list()
        arl_list_data.append(arl_list)

        arl_list.resnr = res_line.resnr
        arl_list.reslinnr = res_line.reslinnr
        arl_list.voucher_nr = res_line.voucher_nr
        arl_list.grpflag = reservation.grpflag
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
        arl_list.karteityp = gmember.karteityp
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
        arl_list.gastmobileno = gmember.mobil_telefon

        if res_line.resstatus != 11 and res_line.resstatus != 13:

            bresline = db_session.query(Bresline).filter(
                     (Bresline.resnr == res_line.resnr) & (Bresline.reslinnr != res_line.reslinnr) & (Bresline.kontakt_nr == res_line.reslinnr) & ((Bresline.resstatus == 11) | (Bresline.resstatus == 13))).first()

            if bresline:
                arl_list.sharer_no = bresline.kontakt_nr


            else:
                arl_list.sharer_no = res_line.kontakt_nr


        bday = date_mdy(get_month(gmember.geburtdatum1) , get_day(gmember.geburtdatum1) , get_year(get_current_date()))

        if bday == get_current_date():
            arl_list.birthday_flag = True

        guestseg = get_cache (Guestseg, {"gastnr": [(eq, res_line.gastnrmember)],"segmentcode": [(eq, blacklist_int)]})

        if guestseg:
            arl_list.guest_blacklist = True

        master = get_cache (Master, {"resnr": [(eq, res_line.resnr)]})

        if master and master.active:
            arl_list.verstat = 1
        else:
            arl_list.verstat = 0

        messages = get_cache (Messages, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

        if messages:
            arl_list.resline_wabkurz = "M"

        if res_line:

            guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
            arl_list.address = guest.adresse1
            arl_list.city = guest.wohnort + " " + guest.plz

        if res_line.kontignr > 0:

            kontline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"betriebsnr": [(eq, 0)],"kontstatus": [(eq, 1)]})

            if kontline:
                arl_list.comments = "ALLOTMENT: " + kontline.kontcode + chr_unicode(10)
            else:
                arl_list.comments = "ALLOTMENT: "

        elif res_line.kontignr < 0:

            kontline = get_cache (Kontline, {"kontignr": [(eq, res_line.kontignr)],"betriebsnr": [(eq, 1)],"kontstatus": [(eq, 1)]})

            if kontline:
                arl_list.comments = "GLOBAL RES: " + kontline.kontcode + chr_unicode(10)
            else:
                arl_list.comments = "GLOBAL RES: "

        if reservation.bemerk != "":

            if reservation.bemerk == None:
                arl_list.comments = " "
            else:
                arl_list.comments = reservation.bemerk + chr_unicode(10)
        else:
            arl_list.comments = " "

        if res_line.bemerk != "":

            if res_line.bemerk == None:
                arl_list.comments = arl_list.comments + " "
            else:
                arl_list.comments = arl_list.comments + res_line.bemerk
        else:
            arl_list.comments = arl_list.comments + " "
            
        for loop_i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            comment_str = entry(loop_i - 1, res_line.zimmer_wunsch, ";")

            if substring(comment_str, 0, 8) == ("$OTACOM$").lower() :
                arl_list.comments = arl_list.comments + chr_unicode(10) + "---OTA COMMENT---" + chr_unicode(10) + entry(2, comment_str, "$OTACOM$")
            else:
                arl_list.comments = arl_list.comments + " "

        if res_line:

            gentable = get_cache (Gentable, {"key": [(eq, "reservation")],"number1": [(eq, res_line.resnr)],"number2": [(eq, res_line.reslinnr)]})

            if gentable:
                arl_list.resnr_fgcol = 12

        if res_line and show_rate:

            mc_guest = get_cache (Mc_guest, {"gastnr": [(eq, res_line.gastnrmember)],"activeflag": [(eq, True)]})

            if mc_guest:
                arl_list.mc_str_fgcol = 15


                arl_list.mc_str_bgcol = 6


                arl_list.mc_flag = True

        if res_line and res_line.resstatus >= 11:

            if res_line.l_zuordnung[2] == 0:
                arl_list.rsv_name_fgcol = 9


            else:
                arl_list.rsv_name_bgcol = 9
                arl_list.rsv_name_fgcol = 15

        htparam = get_cache (Htparam, {"paramnr": [(eq, 712)]})

        if htparam and htparam.finteger != 0:
            vipnr10 = htparam.finteger

        if res_line and (res_line.betrieb_gastmem == vipnr1 or res_line.betrieb_gastmem == vipnr2 or res_line.betrieb_gastmem == vipnr3 or res_line.betrieb_gastmem == vipnr4 or res_line.betrieb_gastmem == vipnr5 or res_line.betrieb_gastmem == vipnr6 or res_line.betrieb_gastmem == vipnr7 or res_line.betrieb_gastmem == vipnr8 or res_line.betrieb_gastmem == vipnr9):
            arl_list.reslin_name_fgcol = 12

        htparam = get_cache (Htparam, {"paramnr": [(eq, 496)]})
        all_inclusive = ";" + htparam.fchar + ";"

        if res_line and matches(all_inclusive,r"*;" + res_line.arrangement + r";*"):
            arl_list.reslin_name_bgcol = 2
            arl_list.reslin_name_fgcol = 15
            arl_list.segmentcode_bgcol = 2
            arl_list.segmentcode_fgcol = 15


        tmpint = (res_line.abreise - res_line.ankunft).days

        if res_line and res_line.active_flag == 1 and long_stay > 0 and tmpint >= long_stay and res_line.erwachs > 0:
            arl_list.abreise_fgcol = 915

        if res_line and res_line.active_flag <= 1 and res_line.abreise == res_line.ankunft:
            arl_list.reslin_name_fgcol = 0
            arl_list.reslin_name_bgcol = 14

        if res_line and res_line.pseudofix:
            arl_list.reslin_name_bgcol = 12
            arl_list.reslin_name_fgcol = 15

        if res_line:
            done_flag = None

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "flag")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)],"betriebsnr": [(eq, 0)]})

            if reslin_queasy:
                done_flag = True

                for reslin_queasy in db_session.query(Reslin_queasy).filter(
                         (Reslin_queasy.key == ("flag").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.betriebsnr == 0)).order_by(Reslin_queasy._recid).all():

                    if (reslin_queasy.char1 != "" and reslin_queasy.deci1 == 0):
                        done_flag = False

                    if (reslin_queasy.char2 != "" and reslin_queasy.deci2 == 0):
                        done_flag = False

                    if (reslin_queasy.char3 != "" and reslin_queasy.deci3 == 0):
                        done_flag = False

                    if not done_flag:
                        break

                if done_flag:
                    arl_list.ankunft_fgcol = 915
                else:
                    arl_list.ankunft_fgcol = 115

            if res_line.active_flag == 0 and res_line.zinr != "" and res_line.ankunft == ci_date:

                zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

                if zimmer.zistatus == 1:
                    arl_list.zinr_fgcol = 0
                    arl_list.zinr_bgcol = 11

                elif zimmer.zistatus == 2:
                    arl_list.zinr_fgcol = 0
                    arl_list.zinr_bgcol = 10

                    queasy = get_cache (Queasy, {"key": [(eq, 162)],"char1": [(eq, zimmer.zinr)],"number1": [(eq, 0)]})

                    if queasy:
                        arl_list.zinr_fgcol = 15
                        arl_list.zinr_bgcol = 6

                elif zimmer.zistatus == 3:
                    arl_list.zinr_fgcol = 12
                    arl_list.zinr_bgcol = 14

        if res_line:

            if centralized_flag :
                arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol = centralized_guest(res_line.gastnrmember)
                arl_list.reslin_name_fgcol = arl_list_reslin_name_fgcol
                arl_list.reslin_name_bgcol = arl_list_reslin_name_bgcol

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

            if guest:

                if guest.zimmeranz >= stay and stay > 0:
                    arl_list.reslin_name_fgcol = 15
                    arl_list.reslin_name_bgcol = 3


        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :

            if entry(loopi - 1, res_line.zimmer_wunsch, ";") == ("WCI-flag").lower() :
                arl_list.webci = entry(loopi - 1, res_line.zimmer_wunsch, ";")


                return

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


                                    return
                    arl_list.comments = "-WEB C/i PREFERENCE-" + chr_unicode(10) + web_com + chr_unicode(10) + arl_list.comments


            arl_list.webci_flag = "W"

            queasy = get_cache (Queasy, {"key": [(eq, 167)],"number1": [(eq, res_line.resnr)]})

            if queasy:

                if arl_list.comments != " ":
                    arl_list.comments = arl_list.comments + chr_unicode(10) + queasy.char3


                else:
                    arl_list.comments = "-WEB C/i PREFERENCE-" + chr_unicode(10) + queasy.char3

        if arl_list.webci_flag == "":

            if matches(res_line.zimmer_wunsch,r"*PCIFLAG*"):
                arl_list.webci_flag = "W"

        fixleist = get_cache (Fixleist, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

        if fixleist:
            arl_list.fixcost_flag = True

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "specialrequest")],"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.reslinnr)]})

        if reslin_queasy:
            arl_list.special_request = reslin_queasy.char3


    def centralized_guest(res_line_gastnrmember:int):

        nonlocal rmlen, arl_list_data, vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9, vipnr10, done_flag, curr_resnr, curr_resline, today_str, reserve_str, created_time, do_it, loop_i, comment_str, all_inclusive, res_mode, checkin_flag, tmpdate, tmpint, stay, resbemerk, rescomment, rsvbemerk, blacklist_int, arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol, htl_name, vhost, vservice, hoappparam, lreturn, centralized_flag, guest, history, paramtext, htparam, res_line, waehrung, reservation, zimkateg, bresline, guestseg, master, messages, kontline, gentable, mc_guest, reslin_queasy, zimmer, queasy, fixleist
        nonlocal show_rate, last_sort, lresnr, long_stay, ci_date, grpflag, room, lname, sorttype, fdate1, fdate2, fdate, excl_rmshare, voucher_no, nation_str
        nonlocal gbuff, gbuffmember, gmember


        nonlocal setup_list, gbuff, gbuffmember, arl_list, b_arl_list, t_payload_list, ghistory, summ_list, gmember
        nonlocal setup_list_data, arl_list_data, b_arl_list_data, ghistory_data, summ_list_data

        arl_list_reslin_name_fgcol = 0
        arl_list_reslin_name_bgcol = 0
        cg_ci_date:date = None
        cg_t_tittle:string = ""
        cg_ip_port:string = ""
        cg_guest_phone:string = ""
        cg_guest_name:string = ""
        cg_guest_email:string = ""
        cg_counter:int = 0

        def generate_inner_output():
            return (arl_list_reslin_name_fgcol, arl_list_reslin_name_bgcol)


        guest = get_cache (Guest, {"gastnr": [(eq, res_line_gastnrmember)]})

        if guest:
            cg_ci_date, cg_t_tittle, cg_ip_port, cg_guest_phone, cg_guest_name, cg_guest_email = get_output(prepare_gcf_history_1bl(guest.gastnr))
            # lreturn = hServerHO:CONNECT (hoappparam, None, None, None) # Oscar - skip because using HServer on Progress
            lreturn = False

            if not lreturn:
                return generate_inner_output()
            
            local_storage.combo_flag = True
            # ghistory_data, summ_list_data = get_output(gcf_history_4blho(guest.gastnr, cg_guest_phone, cg_guest_name, cg_guest_email, None, None)) # Oscar - skip because using HServer on Progress
            local_storage.combo_flag = False

            cg_counter = 0

            for ghistory in query(ghistory_data):
                cg_counter = cg_counter + 1

            if cg_counter >= stay and stay > 0:
                arl_list_reslin_name_fgcol = 15
                arl_list_reslin_name_bgcol = 3


            # lreturn = hServerHO:DISCONNECT() # Oscar - skip because using HServer on Progress


        return generate_inner_output()


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
    blacklist_int = get_output(htpint(709))

    htparam = get_cache (Htparam, {"paramnr": [(eq, 458)]})

    if htparam:
        stay = htparam.finteger

    paramtext = get_cache (Paramtext, {"txtnr": [(eq, 200)]})

    if paramtext:
        htl_name = paramtext.ptexte

    htparam = get_cache (Htparam, {"paramnr": [(eq, 1343)]})

    if htparam:

        if htparam.fchar != "" and htparam.fchar != None:

            if num_entries(htparam.fchar, ":") > 1:
                vhost = entry(0, htparam.fchar, ":")
                vservice = entry(1, htparam.fchar, ":")
                hoappparam = " -H " + vhost + " -S " + vservice + " -DirectConnect -sessionModel Session-free"

                if vhost != None and vhost != "" and vservice != None and vservice != "":
                    centralized_flag = True


    else:
        centralized_flag = False


    fixing_blank_resname()

    if num_entries(room, chr_unicode(2)) > 1:
        do_it = False
        curr_resnr = to_int(entry(1, room, chr_unicode(2)))
        curr_resline = to_int(entry(2, room, chr_unicode(2)))
        today_str = to_string(get_current_date())
        res_mode = trim(entry(3, room, chr_unicode(2)))


        room = entry(0, room, chr_unicode(2))

        res_line = get_cache (Res_line, {"resnr": [(eq, curr_resnr)],"reslinnr": [(eq, curr_resline)]})

        if not res_line:
            do_it = True
        else:

            if res_line.active_flag == 1 and res_mode.lower()  == ("modify").lower() :
                do_it = True
            else:

                for res_line in db_session.query(Res_line).filter(
                         (Res_line.resnr == curr_resnr) & (Res_line.active_flag <= 1)).order_by(Res_line._recid).all():
                    reserve_str = res_line.reserve_char

                    if today_str == substring(reserve_str, 0, 8):
                        reserve_str = substring(reserve_str, 8)
                        created_time = to_int(substring(reserve_str, 0, 2)) * 3600 +\
                                to_int(substring(reserve_str, 3, 2)) * 60

                        if created_time >= (get_current_time_in_seconds() - 70):
                            do_it = True
                            break


    if not do_it:

        return generate_output()
    vipnr1, vipnr2, vipnr3, vipnr4, vipnr5, vipnr6, vipnr7, vipnr8, vipnr9 = get_output(get_vipnrbl())
    disp_arlist1()

    for arl_list in query(arl_list_data, sort_by=[("zinr",False),("sharer_no",False)]):
        b_arl_list = B_arl_list()
        b_arl_list_data.append(b_arl_list)

        buffer_copy(arl_list, b_arl_list)
    arl_list_data.clear()

    for b_arl_list in query(b_arl_list_data):
        arl_list = Arl_list()
        arl_list_data.append(arl_list)

        buffer_copy(b_arl_list, arl_list)
        resbemerk = b_arl_list.bemerk
        resbemerk = replace_str(resbemerk, chr_unicode(10) , "")
        resbemerk = replace_str(resbemerk, chr_unicode(13) , "")
        resbemerk = replace_str(resbemerk, "~n", "")
        resbemerk = replace_str(resbemerk, "\\n", "")
        resbemerk = replace_str(resbemerk, "~r", "")
        resbemerk = replace_str(resbemerk, "~r~n", "")
        resbemerk = replace_str(resbemerk, chr_unicode(10) + chr_unicode(13) , "")

        if length(resbemerk) < 3:
            resbemerk = replace_str(resbemerk, chr_unicode(32) , "")

        if length(resbemerk) < 3:
            resbemerk = ""

        if length(resbemerk) == None:
            resbemerk = ""
        arl_list.bemerk = trim(resbemerk)
        resbemerk = ""
        rescomment = b_arl_list.comments
        rescomment = replace_str(rescomment, chr_unicode(10) , "")
        rescomment = replace_str(rescomment, chr_unicode(13) , "")
        rescomment = replace_str(rescomment, "~n", "")
        rescomment = replace_str(rescomment, "\\n", "")
        rescomment = replace_str(rescomment, "~r", "")
        rescomment = replace_str(rescomment, "~r~n", "")
        rescomment = replace_str(rescomment, chr_unicode(10) + chr_unicode(13) , "")

        if length(rescomment) < 3:
            rescomment = replace_str(rescomment, chr_unicode(32) , "")

        if length(rescomment) < 3:
            rescomment = ""

        if length(rescomment) == None:
            rescomment = ""
        arl_list.comments = trim(rescomment)
        rescomment = ""
        rsvbemerk = b_arl_list.rsv_bemerk
        rsvbemerk = replace_str(rsvbemerk, chr_unicode(10) , "")
        rsvbemerk = replace_str(rsvbemerk, chr_unicode(13) , "")
        rsvbemerk = replace_str(rsvbemerk, "~n", "")
        rsvbemerk = replace_str(rsvbemerk, "\\n", "")
        rsvbemerk = replace_str(rsvbemerk, "~r", "")
        rsvbemerk = replace_str(rsvbemerk, "~r~n", "")
        rsvbemerk = replace_str(rsvbemerk, chr_unicode(10) + chr_unicode(13) , "")

        if length(rsvbemerk) < 3:
            rsvbemerk = replace_str(rsvbemerk, chr_unicode(32) , "")

        if length(rsvbemerk) < 3:
            rsvbemerk = ""

        if length(rsvbemerk) == None:
            rsvbemerk = ""
        arl_list.rsv_bemerk = trim(rsvbemerk)
        rsvbemerk = ""

    if excl_rmshare:

        for arl_list in query(arl_list_data, filters=(lambda arl_list: arl_list.resstatus == 11 or arl_list.resstatus == 13)):
            arl_list_data.remove(arl_list)

    return generate_output()