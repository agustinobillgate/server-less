#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 30/7/25
# gitlab: 293
# if date1 & date2 not None
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.check_timebl import check_timebl
from functions.res_overbookbl import res_overbookbl
from models import Res_line, Reslin_queasy, Bediener, Outorder, Zimkateg, Guest, Res_history

curr_resline_data, Curr_resline = create_model_like(Res_line)

def mk_resline_go1bl(pvilanguage:int, user_init:string, specrequest:bool, c_apply:string, curr_resline_data:[Curr_resline]):

    prepare_cache ([Bediener, Zimkateg, Res_history])

    msg_str = ""
    do_it:bool = False
    allflag:bool = False
    curr_i:int = 0
    ct:string = ""
    zikatstr:string = ""
    curr_msg:string = ""
    init_time:int = 0
    init_date:date = None
    ankunft1:date = None
    abreise1:date = None
    i:int = 0
    str:string = ""
    m_flight:string = ""
    overbook:bool = False
    overmax:bool = False
    overanz:int = 0
    overdate:date = None
    incl_allot:bool = False
    rmcat_ovb:int = 0
    lvcarea:string = "mk-resline"
    res_line = reslin_queasy = bediener = outorder = zimkateg = guest = res_history = None

    curr_resline = t_resline = member_list = zwunsch_rline = zwunsch_rmember = rline = rmember = rbuff = raccomp = spreqbuff = resline = None

    t_resline_data, T_resline = create_model_like(Res_line)
    member_list_data, Member_list = create_model("Member_list", {"reslinnr":int})
    zwunsch_rline_data, Zwunsch_rline = create_model("Zwunsch_rline", {"s_label":string, "s_value1":string, "s_value2":string, "used":bool})
    zwunsch_rmember_data, Zwunsch_rmember = create_model("Zwunsch_rmember", {"s_label":string, "s_value2":string})

    Rline = create_buffer("Rline",Res_line)
    Rmember = create_buffer("Rmember",Res_line)
    Rbuff = create_buffer("Rbuff",Res_line)
    Raccomp = create_buffer("Raccomp",Res_line)
    Spreqbuff = create_buffer("Spreqbuff",Reslin_queasy)
    Resline = create_buffer("Resline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, do_it, allflag, curr_i, ct, zikatstr, curr_msg, init_time, init_date, ankunft1, abreise1, i, str, m_flight, overbook, overmax, overanz, overdate, incl_allot, rmcat_ovb, lvcarea, res_line, reslin_queasy, bediener, outorder, zimkateg, guest, res_history
        nonlocal pvilanguage, user_init, specrequest, c_apply
        nonlocal rline, rmember, rbuff, raccomp, spreqbuff, resline


        nonlocal curr_resline, t_resline, member_list, zwunsch_rline, zwunsch_rmember, rline, rmember, rbuff, raccomp, spreqbuff, resline
        nonlocal t_resline_data, member_list_data, zwunsch_rline_data, zwunsch_rmember_data

        return {"msg_str": msg_str}

    def check_fixrates_changes():

        nonlocal msg_str, allflag, curr_i, ct, zikatstr, curr_msg, init_time, init_date, ankunft1, abreise1, i, str, m_flight, overbook, overmax, overanz, overdate, incl_allot, rmcat_ovb, lvcarea, res_line, reslin_queasy, bediener, outorder, zimkateg, guest, res_history
        nonlocal pvilanguage, user_init, specrequest, c_apply
        nonlocal rline, rmember, rbuff, raccomp, spreqbuff, resline


        nonlocal curr_resline, t_resline, member_list, zwunsch_rline, zwunsch_rmember, rline, rmember, rbuff, raccomp, spreqbuff, resline
        nonlocal t_resline_data, member_list_data, zwunsch_rline_data, zwunsch_rmember_data

        rqsy = None
        curr_date:date = None
        start_date:date = None
        start_time:int = 0
        do_it:bool = False
        chgflag:bool = False
        chg_mode:string = ""
        Rqsy =  create_buffer("Rqsy",Reslin_queasy)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "fixrate-trace-record")],"resnr": [(eq, curr_resline.resnr)],"reslinnr": [(eq, curr_resline.reslinnr)]})

        if reslin_queasy:
            start_date = reslin_queasy.date1
            start_time = reslin_queasy.number1

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == curr_resline.resnr) & (Reslin_queasy.reslinnr == curr_resline.reslinnr)).order_by(Reslin_queasy.date1).all():

            # Rd 30/7/2025
            # check if not None
            if reslin_queasy.date1 and reslin_queasy.date2:
                if reslin_queasy.date1 < reslin_queasy.date2:
                    for curr_date in date_range(reslin_queasy.date1 + 1,reslin_queasy.date2) :
                        rqsy = Reslin_queasy()
                        db_session.add(rqsy)

                        buffer_copy(reslin_queasy, rqsy,except_fields=["date1","date2"])
                        rqsy.date1 = curr_date
                        rqsy.date2 = curr_date


                        pass

                    rqsy = db_session.query(Rqsy).filter(
                            (Rqsy._recid == reslin_queasy._recid)).first()
                    rqsy.date2 = rqsy.date1


                    pass
                    pass

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == rmember.resnr) & (Reslin_queasy.reslinnr == rmember.reslinnr)).order_by(Reslin_queasy.date1).all():

            # Rd 30/7/2025
            # check if not None
            if reslin_queasy.date1 and  reslin_queasy.date2:
                if reslin_queasy.date1 < reslin_queasy.date2:
                    for curr_date in date_range(reslin_queasy.date1 + 1,reslin_queasy.date2) :
                        rqsy = Reslin_queasy()
                        db_session.add(rqsy)

                        buffer_copy(reslin_queasy, rqsy,except_fields=["date1","date2"])
                        rqsy.date1 = curr_date
                        rqsy.date2 = curr_date


                        pass

                    rqsy = db_session.query(Rqsy).filter(
                            (Rqsy._recid == reslin_queasy._recid)).first()
                    rqsy.date2 = rqsy.date1


                    pass
                    pass

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == ("arrangement").lower()) & (Reslin_queasy.resnr == curr_resline.resnr) & (Reslin_queasy.reslinnr == curr_resline.reslinnr)).order_by(Reslin_queasy.date1).all():
            do_it = (start_date < reslin_queasy.date3) or ((start_date == reslin_queasy.date3) and (start_time <= reslin_queasy.number2))

            if do_it:
                chg_mode = "CHG"

                rqsy = db_session.query(Rqsy).filter(
                         (Rqsy.key == ("arrangement").lower()) & (Rqsy.resnr == rmember.resnr) & (Rqsy.reslinnr == rmember.reslinnr) & (Rqsy.date1 == reslin_queasy.date1)).first()
                chgflag = not None != rqsy or (None != rqsy and reslin_queasy.deci1 != rqsy.deci1)

                if chgflag:

                    if not rqsy:
                        rqsy = Reslin_queasy()
                        db_session.add(rqsy)

                        rqsy.resnr = rmember.resnr
                        rqsy.reslinnr = rmember.reslinnr
                        chg_mode = "ADD"


                    else:
                        pass
                    fixrate_changes(chg_mode, reslin_queasy.date1, rqsy.deci1, reslin_queasy.deci1)
                    buffer_copy(reslin_queasy, rqsy,except_fields=["resnr","reslinnr"])
                    pass


    def fixrate_changes(chg_mode:string, curr_date:date, old_rate:Decimal, new_rate:Decimal):

        nonlocal msg_str, do_it, allflag, curr_i, ct, zikatstr, curr_msg, init_time, init_date, ankunft1, abreise1, i, str, m_flight, overbook, overmax, overanz, overdate, incl_allot, rmcat_ovb, lvcarea, res_line, reslin_queasy, bediener, outorder, zimkateg, guest, res_history
        nonlocal pvilanguage, user_init, specrequest, c_apply
        nonlocal rline, rmember, rbuff, raccomp, spreqbuff, resline


        nonlocal curr_resline, t_resline, member_list, zwunsch_rline, zwunsch_rmember, rline, rmember, rbuff, raccomp, spreqbuff, resline
        nonlocal t_resline_data, member_list_data, zwunsch_rline_data, zwunsch_rmember_data

        cid:string = ""
        cdate:string = " "
        rqy = None
        Rqy =  create_buffer("Rqy",Reslin_queasy)

        if rmember.changed != None:
            cid = rmember.changed_id
            cdate = to_string(rmember.changed)

        if chg_mode.lower()  == ("CHG").lower() :
            rqy = Reslin_queasy()
            db_session.add(rqy)

            rqy.key = "ResChanges"
            rqy.resnr = rmember.resnr
            rqy.reslinnr = rmember.reslinnr
            rqy.date2 = get_current_date()
            rqy.number2 = get_current_time_in_seconds()


            rqy.char3 = to_string(rmember.ankunft) + ";" + to_string(rmember.ankunft) + ";" + to_string(rmember.abreise) + ";" + to_string(rmember.abreise) + ";" + to_string(rmember.zimmeranz) + ";" + to_string(rmember.zimmeranz) + ";" + to_string(rmember.erwachs) + ";" + to_string(rmember.erwachs) + ";" + to_string(rmember.kind1) + ";" + to_string(rmember.kind1) + ";" + to_string(rmember.gratis) + ";" + to_string(rmember.gratis) + ";" + to_string(rmember.zikatnr) + ";" + to_string(rmember.zikatnr) + ";" + to_string(rmember.zinr) + ";" + to_string(rmember.zinr) + ";" + to_string(rmember.arrangement) + ";" + to_string(rmember.arrangement) + ";" + to_string(rmember.zipreis) + ";" + to_string(rmember.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixrate FR:") + ";" + to_string(curr_date) + "-" + to_string(old_rate) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"
            pass
            pass
        rqy = Reslin_queasy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = rmember.resnr
        rqy.reslinnr = rmember.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(rmember.ankunft) + ";" + to_string(rmember.ankunft) + ";" + to_string(rmember.abreise) + ";" + to_string(rmember.abreise) + ";" + to_string(rmember.zimmeranz) + ";" + to_string(rmember.zimmeranz) + ";" + to_string(rmember.erwachs) + ";" + to_string(rmember.erwachs) + ";" + to_string(rmember.kind1) + ";" + to_string(rmember.kind1) + ";" + to_string(rmember.gratis) + ";" + to_string(rmember.gratis) + ";" + to_string(rmember.zikatnr) + ";" + to_string(rmember.zikatnr) + ";" + to_string(rmember.zinr) + ";" + to_string(rmember.zinr) + ";" + to_string(rmember.arrangement) + ";" + to_string(rmember.arrangement) + ";" + to_string(rmember.zipreis) + ";" + to_string(rmember.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + chg_mode + " " + to_string("Fixrate TO:") + ";" + to_string(curr_date) + "-" + to_string(new_rate) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"
        pass
        pass


    def res_changes():

        nonlocal msg_str, do_it, allflag, curr_i, ct, zikatstr, curr_msg, init_time, init_date, ankunft1, abreise1, i, str, m_flight, overbook, overmax, overanz, overdate, incl_allot, rmcat_ovb, lvcarea, res_line, reslin_queasy, bediener, outorder, zimkateg, guest, res_history
        nonlocal pvilanguage, user_init, specrequest, c_apply
        nonlocal rline, rmember, rbuff, raccomp, spreqbuff, resline


        nonlocal curr_resline, t_resline, member_list, zwunsch_rline, zwunsch_rmember, rline, rmember, rbuff, raccomp, spreqbuff, resline
        nonlocal t_resline_data, member_list_data, zwunsch_rline_data, zwunsch_rmember_data

        guest1 = None
        cid:string = " "
        cdate:string = " "
        heute:date = None
        zeit:int = 0
        Guest1 =  create_buffer("Guest1",Guest)
        heute = get_current_date()
        zeit = get_current_time_in_seconds()

        if trim(t_resline.changed_id) != "":
            cid = t_resline.changed_id
            cdate = to_string(t_resline.changed)

        elif length(t_resline.reserve_char) >= 14:
            cid = substring(t_resline.reserve_char, 13)
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = rbuff.resnr
        reslin_queasy.reslinnr = rbuff.reslinnr
        reslin_queasy.date2 = heute
        reslin_queasy.number2 = zeit

        reslin_queasy.char3 = to_string(t_resline.ankunft) + ";" + to_string(rbuff.ankunft) + ";" + to_string(t_resline.abreise) + ";" + to_string(rbuff.abreise) + ";" + to_string(t_resline.zimmeranz) + ";" + to_string(rbuff.zimmeranz) + ";" + to_string(t_resline.erwachs) + ";" + to_string(rbuff.erwachs) + ";" + to_string(t_resline.kind1) + ";" + to_string(rbuff.kind1) + ";" + to_string(t_resline.gratis) + ";" + to_string(rbuff.gratis) + ";" + to_string(t_resline.zikatnr) + ";" + to_string(rbuff.zikatnr) + ";" + to_string(t_resline.zinr) + ";" + to_string(rbuff.zinr) + ";"

        if rbuff.reserve_int == t_resline.reserve_int:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(t_resline.arrangement) + ";" + to_string(rbuff.arrangement) + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string(t_resline.arrangement) + ";" + to_string(t_resline.reserve_int) + ";"
        reslin_queasy.char3 = reslin_queasy.char3 + to_string(t_resline.zipreis) + ";" + to_string(rbuff.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(heute) + ";" + to_string(t_resline.name) + ";" + to_string(t_resline.bemerk) + ";"

        if rbuff.was_status == 0:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("NO", "x(3)") + ";"
        else:
            reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES", "x(3)") + ";"
        reslin_queasy.char3 = reslin_queasy.char3 + to_string("YES", "x(3)") + ";"
        pass
        pass

        if t_resline.bemerk != rbuff.bemerk:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.resnr = t_resline.resnr
            res_history.reslinnr = t_resline.reslinnr
            res_history.datum = heute
            res_history.zeit = zeit
            res_history.aenderung = t_resline.bemerk
            res_history.action = "Remark"


            res_history.aenderung = t_resline.bemerk + chr_unicode(10) + chr_unicode(10) + "*** Changed to:" + chr_unicode(10) + chr_unicode(10) + rbuff.bemerk

            if bediener:
                res_history.betriebsnr = bediener.nr
            pass
            pass


    def update_special_request():

        nonlocal msg_str, do_it, allflag, curr_i, ct, zikatstr, curr_msg, init_time, init_date, ankunft1, abreise1, i, str, m_flight, overbook, overmax, overanz, overdate, incl_allot, rmcat_ovb, lvcarea, res_line, reslin_queasy, bediener, outorder, zimkateg, guest, res_history
        nonlocal pvilanguage, user_init, specrequest, c_apply
        nonlocal rline, rmember, rbuff, raccomp, spreqbuff, resline


        nonlocal curr_resline, t_resline, member_list, zwunsch_rline, zwunsch_rmember, rline, rmember, rbuff, raccomp, spreqbuff, resline
        nonlocal t_resline_data, member_list_data, zwunsch_rline_data, zwunsch_rmember_data

        rqsy = None
        Rqsy =  create_buffer("Rqsy",Reslin_queasy)

        rqsy = db_session.query(Rqsy).filter(
                 (Rqsy.key == ("specialRequest").lower()) & (Rqsy.resnr == rmember.resnr) & (Rqsy.reslinnr == rmember.reslinnr)).first()

        if not rqsy:
            rqsy = Reslin_queasy()
            db_session.add(rqsy)

            rqsy.key = "specialRequest"
            rqsy.resnr = rmember.resnr
            rqsy.reslinnr = rmember.reslinnr


        rqsy.char3 = spreqBuff.char3


        pass
        pass


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
    t_resline = T_resline()
    t_resline_data.append(t_resline)


    curr_resline = query(curr_resline_data, first=True)

    res_line = get_cache (Res_line, {"resnr": [(eq, curr_resline.resnr)],"reslinnr": [(eq, curr_resline.reslinnr)]})

    if not res_line:

        return generate_output()

    if specrequest:

        spreqbuff = db_session.query(Spreqbuff).filter(
                 (spreqBuff.key == ("specialRequest").lower()) & (spreqBuff.resnr == curr_resline.resnr) & (spreqBuff.reslinnr == curr_resline.reslinnr)).first()
    for i in range(1,num_entries(curr_resline.zimmer_wunsch, ";") - 1 + 1) :
        zwunsch_rline = Zwunsch_rline()
        zwunsch_rline_data.append(zwunsch_rline)

        str = entry(i - 1, curr_resline.zimmer_wunsch, ";")

        if substring(str, 0, 7) == ("voucher").lower() :
            zwunsch_rline.s_label = "voucher"
            zwunsch_rline.s_value1 = substring(str, 7)

        elif substring(str, 0, 5) == ("ChAge").lower() :
            zwunsch_rline.s_label = "chAge"
            zwunsch_rline.s_value1 = substring(str, 5)

        elif substring(str, 0, 10) == ("$OrigCode$").lower() :
            zwunsch_rline.s_label = "$OrigCode$"
            zwunsch_rline.s_value1 = substring(str, 10)

        elif substring(str, 0, 6) == ("$CODE$").lower() :
            zwunsch_rline.s_label = "$CODE$"
            zwunsch_rline.s_value1 = substring(str, 6)

        elif substring(str, 0, 5) == ("DATE,").lower() :
            zwunsch_rline.s_label = "DATE,"
            zwunsch_rline.s_value1 = substring(str, 5)

        elif substring(str, 0, 8) == ("SEGM_PUR").lower() :
            zwunsch_rline.s_label = "SEGM_PUR"
            zwunsch_rline.s_value1 = substring(str, 8)

        elif substring(str, 0, 6) == ("ebdisc").lower() :
            zwunsch_rline.s_label = "ebdisc"
            zwunsch_rline.s_value1 = "Y"

        elif substring(str, 0, 6) == ("kbdisc").lower() :
            zwunsch_rline.s_label = "kbdisc"
            zwunsch_rline.s_value1 = "Y"

        elif substring(str, 0, 10) == ("restricted").lower() :
            zwunsch_rline.s_label = "restricted"
            zwunsch_rline.s_value1 = "Y"

        elif substring(str, 0, 6) == ("pickup").lower() :
            zwunsch_rline.s_label = "pickup"
            zwunsch_rline.s_value1 = "Y"

        elif substring(str, 0, 14) == ("drop-passanger").lower() :
            zwunsch_rline.s_label = "drop-passanger"
            zwunsch_rline.s_value1 = "Y"

        elif matches(str,r"*WCI-req*"):
            zwunsch_rline.s_label = "WCI-req"
            zwunsch_rline.s_value1 = entry(1, str, "=")


    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
        zwunsch_rline = Zwunsch_rline()
        zwunsch_rline_data.append(zwunsch_rline)

        str = entry(i - 1, res_line.zimmer_wunsch, ";")

        if substring(str, 0, 7) == ("voucher").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("voucher").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "voucher"
            zwunsch_rline.s_value2 = substring(str, 7)

        elif substring(str, 0, 5) == ("ChAge").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("ChAge").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "ChAge"
            zwunsch_rline.s_value2 = substring(str, 5)

        elif substring(str, 0, 10) == ("$OrigCode$").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("voucher").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "$OrigCode$"
            zwunsch_rline.s_value2 = substring(str, 10)

        elif substring(str, 0, 6) == ("$CODE$").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("&CODE$").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "$CODE$"
            zwunsch_rline.s_value2 = substring(str, 6)

        elif substring(str, 0, 5) == ("DATE,").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("DATE,").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "DATE,"
            zwunsch_rline.s_value2 = substring(str, 5)

        elif substring(str, 0, 8) == ("SEGM_PUR").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("SEGM_PUR").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "SEGM_PUR"
            zwunsch_rline.s_value2 = substring(str, 8)

        elif substring(str, 0, 6) == ("ebdisc").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("ebdisc").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "ebdisc"
            zwunsch_rline.s_value2 = "Y"

        elif substring(str, 0, 6) == ("kbdisc").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("kbdisx").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "kbdisc"
            zwunsch_rline.s_value2 = "Y"

        elif substring(str, 0, 10) == ("restricted").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("restricted").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "restricted"
            zwunsch_rline.s_value2 = "Y"

        elif substring(str, 0, 6) == ("pickup").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("pickup").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "pickup"
            zwunsch_rline.s_value2 = "Y"

        elif substring(str, 0, 14) == ("drop-passanger").lower() :

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("drop-passanger").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "drop-passanger"
            zwunsch_rline.s_value2 = "Y"

        elif matches(str,r"*WCI-req*"):

            zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label.lower()  == ("WCI-req").lower()), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
                zwunsch_rline_data.append(zwunsch_rline)

            zwunsch_rline.s_label = "WCI-req"
            zwunsch_rline.s_value2 = entry(1, str, "=")

    for zwunsch_rline in query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_value1 == zwunsch_rline.s_value2)):
        zwunsch_rline_data.remove(zwunsch_rline)
    allflag = (c_apply == "ALL")

    if not allflag:
        for curr_i in range(1,num_entries(c_apply, ",")  + 1) :
            ct = trim(entry(curr_i - 1, c_apply, ","))

            if ct != "":
                member_list = Member_list()
                member_list_data.append(member_list)

                member_list.reslinnr = to_int(ct)

    resline = db_session.query(Resline).filter(
             (Resline.resnr == curr_resline.resnr) & (Resline.active_flag == 1) & (Resline.reslinnr != curr_resline.reslinnr) & (Resline.l_zuordnung[inc_value(2)] == 0)).first()
    while None != resline:

        if allflag:
            do_it = True
        else:

            member_list = query(member_list_data, filters=(lambda member_list: member_list.reslinnr == resline.reslinnr), first=True)
            do_it = None != member_list

        if do_it:

            rbuff = db_session.query(Rbuff).filter(
                     (Rbuff._recid == resline._recid)).first()

            if curr_resline.bemerk != res_line.bemerk:
                rbuff.bemerk = res_line.bemerk

            rbuff = db_session.query(Rbuff).first()
            pass

        curr_recid = resline._recid
        resline = db_session.query(Resline).filter(
                 (Resline.resnr == curr_resline.resnr) & (Resline.active_flag == 1) & (Resline.reslinnr != curr_resline.reslinnr) & (Resline.l_zuordnung[inc_value(2)] == 0) & (Resline._recid > curr_recid)).first()

    rmember = db_session.query(Rmember).filter(
             (Rmember.resnr == curr_resline.resnr) & (Rmember.active_flag == 0) & (Rmember.reslinnr != curr_resline.reslinnr) & (Rmember.l_zuordnung[inc_value(2)] == 0)).first()
    while None != rmember:

        if allflag:
            do_it = True
        else:

            member_list = query(member_list_data, filters=(lambda member_list: member_list.reslinnr == rmember.reslinnr), first=True)
            do_it = None != member_list

        if do_it:
            do_it, init_time, init_date = get_output(check_timebl(1, rmember.resnr, rmember.reslinnr, "res-line", None, None))

            if not do_it:
                msg_str = msg_str + "#" + to_string(rmember.reslinnr, "99") + " " + rmember.name + chr_unicode(10) + translateExtended ("Reservation being modified by other user.", lvcarea, "") + chr_unicode(10) + chr_unicode(10)

        if do_it:
            buffer_copy(rmember, t_resline)

            rbuff = db_session.query(Rbuff).filter(
                     (Rbuff._recid == rmember._recid)).first()
            m_flight = ""

            if substring(curr_resline.flight_nr, 0, 6) != substring(res_line.flight_nr, 0, 6):
                m_flight = substring(res_line.flight_nr, 0, 6)
            else:
                m_flight = substring(rmember.flight_nr, 0, 6)

            if substring(curr_resline.flight_nr, 6, 5) != substring(res_line.flight_nr, 6, 5):
                m_flight = m_flight + substring(res_line.flight_nr, 6, 5)
            else:
                m_flight = m_flight + substring(rmember.flight_nr, 6, 5)

            if substring(curr_resline.flight_nr, 11, 6) != substring(res_line.flight_nr, 11, 6):
                m_flight = m_flight + substring(res_line.flight_nr, 11, 6)
            else:
                m_flight = m_flight + substring(rmember.flight_nr, 11, 6)

            if substring(curr_resline.flight_nr, 17, 5) != substring(res_line.flight_nr, 17, 5):
                m_flight = m_flight + substring(res_line.flight_nr, 17, 5)
            else:
                m_flight = m_flight + substring(rmember.flight_nr, 17, 5)
            rmember.flight_nr = m_flight

            if curr_resline.code != res_line.code:
                rbuff.code = res_line.code

            if curr_resline.l_zuordnung[0] != res_line.l_zuordnung[0] and curr_resline.zikatnr == rmember.zikatnr:
                rbuff.l_zuordnung[0] = res_line.l_zuordnung[0]

            if curr_resline.gastnrpay != res_line.gastnrpay:
                rbuff.gastnrpay = res_line.gastnrpay

            if curr_resline.arrangement != res_line.arrangement:
                rbuff.arrangement = res_line.arrangement

            if curr_resline.kontignr != res_line.kontignr:
                rbuff.kontignr = res_line.kontignr

            if curr_resline.betriebsnr != res_line.betriebsnr:
                rbuff.betriebsnr = res_line.betriebsnr

            if curr_resline.reserve_int != res_line.reserve_int:
                rbuff.reserve_int = res_line.reserve_int

            if curr_resline.bemerk != res_line.bemerk:
                rbuff.bemerk = res_line.bemerk

            if curr_resline.erwachs != res_line.erwachs and res_line.erwachs > 0 and rmember.resstatus != 11:
                rbuff.erwachs = res_line.erwachs

            if curr_resline.resstatus != res_line.resstatus and (curr_resline.resstatus <= 2 or curr_resline.resstatus == 5) and (res_line.resstatus <= 2 or res_line.resstatus == 5):
                rbuff.resstatus = res_line.resstatus

            if (curr_resline.ankunft != res_line.ankunft) or (curr_resline.abreise != res_line.abreise) or (curr_resline.zikatnr != res_line.zikatnr):
                ankunft1 = rmember.ankunft

                if curr_resline.ankunft != res_line.ankunft:
                    ankunft1 = res_line.ankunft
                abreise1 = rmember.abreise

                if curr_resline.abreise != res_line.abreise:
                    abreise1 = res_line.abreise
                do_it = abreise1 >= ankunft1

                if not do_it:
                    msg_str = msg_str + "#" + to_string(rmember.reslinnr) + " " + rmember.name + chr_unicode(10) + translateExtended ("Wrong check-in/check-out date", lvcarea, "") + ": " + to_string(ankunft1) + "/" + to_string(abreise1) + chr_unicode(10) + chr_unicode(10)

                if do_it and rmember.zinr != "":

                    outorder = get_cache (Outorder, {"zinr": [(eq, rmember.zinr)],"gespstart": [(ge, abreise1)],"gespende": [(lt, ankunft1)]})
                    do_it = not None != outorder

                    if not do_it:
                        msg_str = msg_str + "#" + to_string(rmember.reslinnr) + " " + rmember.name + chr_unicode(10) + translateExtended ("O-O-O found RmNo", lvcarea, "") + " " + rmember.zinr + ": " + to_string(outorder.gespstart) + "/" + to_string(outorder.gespende) + chr_unicode(10) + chr_unicode(10)
                    else:

                        rline = db_session.query(Rline).filter(
                                 (Rline.zinr == rmember.zinr) & ((Rline.resstatus <= 2) | (Rline.resstatus == 5)) & (Rline._recid != rmember._recid) & not_ (Rline.ankunft >= abreise1) & not_ (Rline.abreise <= ankunft1)).first()
                        do_it = not None != rline

                        if not do_it:
                            msg_str = msg_str + "#" + to_string(rmember.reslinnr) + " " + rmember.name + chr_unicode(10) + translateExtended ("Overlapping with other reservation - RmNo", lvcarea, "") + " " + rmember.zinr + ": " + to_string(rline.ankunft) + "/" + to_string(rline.abreise) + chr_unicode(10) + chr_unicode(10)

                if do_it:

                    if curr_resline.zikatnr != res_line.zikatnr and curr_resline.zikatnr == rmember.zikatnr:

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
                    else:

                        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, rmember.zikatnr)]})
                    zikatstr = zimkateg.kurzbez
                    overbook, overmax, overanz, overdate, incl_allot, curr_msg, rmcat_ovb = get_output(res_overbookbl(pvilanguage, "modify", rmember.resnr, rmember.reslinnr, res_line.ankunft, res_line.abreise, 1, zikatstr, None, True))
                    do_it = not overbook

                    if not do_it:
                        msg_str = msg_str + "#" + to_string(rmember.reslinnr) + " " + rmember.name + chr_unicode(10) + translateExtended ("Overbooking found on", lvcarea, "") + " " + to_string(overdate) + chr_unicode(10) + chr_unicode(10)

                if do_it:

                    if curr_resline.ankunft != res_line.ankunft:
                        rbuff.ankunft = res_line.ankunft
                        rbuff.anztage = (rbuff.abreise - rbuff.ankunft).days

                    if curr_resline.abreise != res_line.abreise:
                        rbuff.abreise = res_line.abreise
                        rbuff.anztage = (rbuff.abreise - rbuff.ankunft).days

                    if curr_resline.zikatnr != res_line.zikatnr and curr_resline.zikatnr == rmember.zikatnr:
                        rbuff.zikatnr = res_line.zikatnr
                        rbuff.setup = res_line.setup
                        rbuff.zinr = ""

                    for raccomp in db_session.query(Raccomp).filter(
                             (Raccomp.resnr == rmember.resnr) & (Raccomp.resstatus == 11) & (Raccomp.kontakt_nr == rmember.reslinnr) & (Raccomp.l_zuordnung[inc_value(2)] == 1)).order_by(Raccomp._recid).all():
                        raccomp.ankunft = rbuff.ankunft
                        raccomp.abreise = rbuff.abreise
                        raccomp.zikatnr = rbuff.zikatnr
                        raccomp.zinr = rbuff.zinr

            if do_it and curr_resline.zipreis != res_line.zipreis and rmember.resstatus != 11 and rmember.resstatus != 13:
                rbuff.zipreis =  to_decimal(res_line.zipreis)

            if do_it and specrequest and spreqBuff:
                update_special_request()

            if do_it:
                for i in range(1,num_entries(rmember.zimmer_wunsch, ";") - 1 + 1) :
                    zwunsch_rmember = Zwunsch_rmember()
                    zwunsch_rmember_data.append(zwunsch_rmember)

                    str = entry(i - 1, rmember.zimmer_wunsch, ";")

                    if substring(str, 0, 7) == ("voucher").lower() :
                        zwunsch_rmember.s_label = "voucher"
                        zwunsch_rmember.s_value2 = substring(str, 7)

                    elif substring(str, 0, 5) == ("ChAge").lower() :
                        zwunsch_rmember.s_label = "chAge"
                        zwunsch_rmember.s_value2 = substring(str, 5)

                    elif substring(str, 0, 10) == ("$OrigCode$").lower() :
                        zwunsch_rmember.s_label = "$OrigCode$"
                        zwunsch_rmember.s_value2 = substring(str, 10)

                    elif substring(str, 0, 6) == ("$CODE$").lower() :
                        zwunsch_rmember.s_label = "$CODE$"
                        zwunsch_rmember.s_value2 = substring(str, 6)

                    elif substring(str, 0, 5) == ("DATE,").lower() :
                        zwunsch_rmember.s_label = "DATE,"
                        zwunsch_rmember.s_value2 = substring(str, 5)

                    elif substring(str, 0, 8) == ("SEGM_PUR").lower() :
                        zwunsch_rmember.s_label = "SEGM_PUR"
                        zwunsch_rmember.s_value2 = substring(str, 8)

                    elif substring(str, 0, 6) == ("ebdisc").lower() :
                        zwunsch_rmember.s_label = "ebdisc"
                        zwunsch_rmember.s_value2 = "Y"

                    elif substring(str, 0, 6) == ("kbdisc").lower() :
                        zwunsch_rmember.s_label = "kbdisc"
                        zwunsch_rmember.s_value2 = "Y"

                    elif substring(str, 0, 10) == ("restricted").lower() :
                        zwunsch_rmember.s_label = "restricted"
                        zwunsch_rmember.s_value2 = "Y"

                    elif substring(str, 0, 6) == ("pickup").lower() :
                        zwunsch_rmember.s_label = "pickup"
                        zwunsch_rmember.s_value2 = "Y"

                    elif substring(str, 0, 14) == ("drop-passanger").lower() :
                        zwunsch_rmember.s_label = "drop-passanger"
                        zwunsch_rmember.s_value2 = "Y"

                    elif matches(str,r"*WCI-req*"):
                        zwunsch_rmember.s_label = "WCI-req"
                        zwunsch_rmember.s_value2 = entry(1, str, "=")

            for zwunsch_rmember in query(zwunsch_rmember_data):

                zwunsch_rline = query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.s_label == zwunsch_rmember.s_label), first=True)

                if zwunsch_rline:
                    zwunsch_rmember.s_value2 = zwunsch_rline.s_value2
                    zwunsch_rline.used = True

            for zwunsch_rline in query(zwunsch_rline_data, filters=(lambda zwunsch_rline: not zwunsch_rline.used)):
                zwunsch_rmember = Zwunsch_rmember()
                zwunsch_rmember_data.append(zwunsch_rmember)

                buffer_copy(zwunsch_rline, zwunsch_rmember)

            for zwunsch_rline in query(zwunsch_rline_data, filters=(lambda zwunsch_rline: zwunsch_rline.used)):
                zwunsch_rline.used = False
            ct = ""

            for zwunsch_rmember in query(zwunsch_rmember_data):

                if zwunsch_rmember.s_value2 != "":

                    if zwunsch_rmember.s_value2.lower()  == ("Y").lower() :
                        ct = ct + zwunsch_rmember.s_label + ";"
                    else:
                        ct = ct + zwunsch_rmember.s_label + zwunsch_rmember.s_value2 + ";"
                zwunsch_rmember_data.remove(zwunsch_rmember)
            rbuff.zimmer_wunsch = ct

            if rmember.resstatus != 11 and rmember.resstatus != 13:
                check_fixrates_changes()
            pass
            res_changes()
            do_it, init_time, init_date = get_output(check_timebl(2, rmember.resnr, rmember.reslinnr, "res-line", init_time, init_date))

        curr_recid = rmember._recid
        rmember = db_session.query(Rmember).filter(
                 (Rmember.resnr == curr_resline.resnr) & (Rmember.active_flag == 0) & (Rmember.reslinnr != curr_resline.reslinnr) & (Rmember.l_zuordnung[inc_value(2)] == 0) & (Rmember._recid > curr_recid)).first()

    return generate_output()