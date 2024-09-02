from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from functions.check_timebl import check_timebl
from functions.res_overbookbl import res_overbookbl
from models import Res_line, Reslin_queasy, Bediener, Outorder, Zimkateg, Guest, Res_history

def mk_resline_go1bl(pvilanguage:int, user_init:str, specrequest:bool, c_apply:str, curr_resline:[Curr_resline]):
    msg_str = ""
    do_it:bool = False
    allflag:bool = False
    curr_i:int = 0
    ct:str = ""
    zikatstr:str = ""
    curr_msg:str = ""
    init_time:int = 0
    init_date:date = None
    ankunft1:date = None
    abreise1:date = None
    i:int = 0
    str:str = ""
    m_flight:str = ""
    overbook:bool = False
    overmax:bool = False
    overanz:int = 0
    overdate:date = None
    incl_allot:bool = False
    rmcat_ovb:int = 0
    lvcarea:str = "mk_resline"
    res_line = reslin_queasy = bediener = outorder = zimkateg = guest = res_history = None

    curr_resline = t_resline = member_list = zwunsch_rline = zwunsch_rmember = rline = rmember = rbuff = raccomp = spreqbuff = resline = rqsy = rqy = guest1 = None

    curr_resline_list, Curr_resline = create_model_like(Res_line)
    t_resline_list, T_resline = create_model_like(Res_line)
    member_list_list, Member_list = create_model("Member_list", {"reslinnr":int})
    zwunsch_rline_list, Zwunsch_rline = create_model("Zwunsch_rline", {"s_label":str, "s_value1":str, "s_value2":str, "used":bool})
    zwunsch_rmember_list, Zwunsch_rmember = create_model("Zwunsch_rmember", {"s_label":str, "s_value2":str})

    Rline = Res_line
    Rmember = Res_line
    Rbuff = Res_line
    Raccomp = Res_line
    Spreqbuff = Reslin_queasy
    Resline = Res_line
    Rqsy = Reslin_queasy
    Rqy = Reslin_queasy
    Guest1 = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, do_it, allflag, curr_i, ct, zikatstr, curr_msg, init_time, init_date, ankunft1, abreise1, i, str, m_flight, overbook, overmax, overanz, overdate, incl_allot, rmcat_ovb, lvcarea, res_line, reslin_queasy, bediener, outorder, zimkateg, guest, res_history
        nonlocal rline, rmember, rbuff, raccomp, spreqbuff, resline, rqsy, rqy, guest1


        nonlocal curr_resline, t_resline, member_list, zwunsch_rline, zwunsch_rmember, rline, rmember, rbuff, raccomp, spreqbuff, resline, rqsy, rqy, guest1
        nonlocal curr_resline_list, t_resline_list, member_list_list, zwunsch_rline_list, zwunsch_rmember_list
        return {"msg_str": msg_str}

    def check_fixrates_changes():

        nonlocal msg_str, do_it, allflag, curr_i, ct, zikatstr, curr_msg, init_time, init_date, ankunft1, abreise1, i, str, m_flight, overbook, overmax, overanz, overdate, incl_allot, rmcat_ovb, lvcarea, res_line, reslin_queasy, bediener, outorder, zimkateg, guest, res_history
        nonlocal rline, rmember, rbuff, raccomp, spreqbuff, resline, rqsy, rqy, guest1


        nonlocal curr_resline, t_resline, member_list, zwunsch_rline, zwunsch_rmember, rline, rmember, rbuff, raccomp, spreqbuff, resline, rqsy, rqy, guest1
        nonlocal curr_resline_list, t_resline_list, member_list_list, zwunsch_rline_list, zwunsch_rmember_list

        curr_date:date = None
        start_date:date = None
        start_time:int = 0
        do_it:bool = False
        chgflag:bool = False
        chg_mode:str = ""
        Rqsy = Reslin_queasy

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "fixrate_trace_record") &  (Reslin_queasy.resnr == curr_resline.resnr) &  (Reslin_queasy.reslinnr == curr_resline.reslinnr)).first()

        if reslin_queasy:
            start_date = reslin_queasy.date1
            start_time = reslin_queasy.number1

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == curr_resline.resnr) &  (Reslin_queasy.reslinnr == curr_resline.reslinnr)).all():

            if reslin_queasy.date1 < reslin_queasy.date2:
                for curr_date in range(reslin_queasy.date1 + 1,reslin_queasy.date2 + 1) :
                    rqsy = Rqsy()
                    db_session.add(rqsy)

                    buffer_copy(reslin_queasy, rqsy,except_fields=["date1","date2"])
                    rqsy.date1 = curr_date
                    rqsy.date2 = curr_date

                    rqsy = db_session.query(Rqsy).first()

                rqsy = db_session.query(Rqsy).filter(
                        (Rqsy._recid == reslin_queasy._recid)).first()
                rqsy.date2 = rqsy.date1

                rqsy = db_session.query(Rqsy).first()


        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == rmember.resnr) &  (Reslin_queasy.reslinnr == rmember.reslinnr)).all():

            if reslin_queasy.date1 < reslin_queasy.date2:
                for curr_date in range(reslin_queasy.date1 + 1,reslin_queasy.date2 + 1) :
                    rqsy = Rqsy()
                    db_session.add(rqsy)

                    buffer_copy(reslin_queasy, rqsy,except_fields=["date1","date2"])
                    rqsy.date1 = curr_date
                    rqsy.date2 = curr_date

                    rqsy = db_session.query(Rqsy).first()

                rqsy = db_session.query(Rqsy).filter(
                        (Rqsy._recid == reslin_queasy._recid)).first()
                rqsy.date2 = rqsy.date1

                rqsy = db_session.query(Rqsy).first()


        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == curr_resline.resnr) &  (Reslin_queasy.reslinnr == curr_resline.reslinnr)).all():
            do_it = (start_date < reslin_queasy.date3) or ((start_date == reslin_queasy.date3) and (start_time <= reslin_queasy.number2))

            if do_it:
                chg_mode = "CHG"

                rqsy = db_session.query(Rqsy).filter(
                        (func.lower(Rqsy.key) == "arrangement") &  (Rqsy.resnr == rmember.resnr) &  (Rqsy.reslinnr == rmember.reslinnr) &  (Rqsy.date1 == reslin_queasy.date1)).first()
                chgflag = not None != rqsy or (None != rqsy and reslin_queasy.deci1 != rqsy.deci1)

                if chgflag:

                    if not rqsy:
                        rqsy = Rqsy()
                        db_session.add(rqsy)

                        rqsy.resnr = rmember.resnr
                        rqsy.reslinnr = rmember.reslinnr
                        chg_mode = "ADD"


                    else:

                        rqsy = db_session.query(Rqsy).first()
                    fixrate_changes(chg_mode, reslin_queasy.date1, rqsy.deci1, reslin_queasy.deci1)
                    buffer_copy(reslin_queasy, rqsy,except_fields=["resnr","reslinnr"])

                    rqsy = db_session.query(Rqsy).first()

    def fixrate_changes(chg_mode:str, curr_date:date, old_rate:decimal, new_rate:decimal):

        nonlocal msg_str, do_it, allflag, curr_i, ct, zikatstr, curr_msg, init_time, init_date, ankunft1, abreise1, i, str, m_flight, overbook, overmax, overanz, overdate, incl_allot, rmcat_ovb, lvcarea, res_line, reslin_queasy, bediener, outorder, zimkateg, guest, res_history
        nonlocal rline, rmember, rbuff, raccomp, spreqbuff, resline, rqsy, rqy, guest1


        nonlocal curr_resline, t_resline, member_list, zwunsch_rline, zwunsch_rmember, rline, rmember, rbuff, raccomp, spreqbuff, resline, rqsy, rqy, guest1
        nonlocal curr_resline_list, t_resline_list, member_list_list, zwunsch_rline_list, zwunsch_rmember_list

        cid:str = ""
        cdate:str = ""
        Rqy = Reslin_queasy

        if rmember.changed != None:
            cid = rmember.changed_id
            cdate = to_string(rmember.changed)

        if chg_mode.lower()  == "CHG":
            rqy = Rqy()
            db_session.add(rqy)

            rqy.key = "ResChanges"
            rqy.resnr = rmember.resnr
            rqy.reslinnr = rmember.reslinnr
            rqy.date2 = get_current_date()
            rqy.number2 = get_current_time_in_seconds()


            rqy.char3 = to_string(rmember.ankunft) + ";" + to_string(rmember.ankunft) + ";" + to_string(rmember.abreise) + ";" + to_string(rmember.abreise) + ";" + to_string(rmember.zimmeranz) + ";" + to_string(rmember.zimmeranz) + ";" + to_string(rmember.erwachs) + ";" + to_string(rmember.erwachs) + ";" + to_string(rmember.kind1) + ";" + to_string(rmember.kind1) + ";" + to_string(rmember.gratis) + ";" + to_string(rmember.gratis) + ";" + to_string(rmember.zikatnr) + ";" + to_string(rmember.zikatnr) + ";" + to_string(rmember.zinr) + ";" + to_string(rmember.zinr) + ";" + to_string(rmember.arrangement) + ";" + to_string(rmember.arrangement) + ";" + to_string(rmember.zipreis) + ";" + to_string(rmember.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + to_string("CHG Fixrate FR:") + ";" + to_string(curr_date) + "-" + to_string(old_rate) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"

            rqy = db_session.query(Rqy).first()

        rqy = Rqy()
        db_session.add(rqy)

        rqy.key = "ResChanges"
        rqy.resnr = rmember.resnr
        rqy.reslinnr = rmember.reslinnr
        rqy.date2 = get_current_date()
        rqy.number2 = get_current_time_in_seconds()


        rqy.char3 = to_string(rmember.ankunft) + ";" + to_string(rmember.ankunft) + ";" + to_string(rmember.abreise) + ";" + to_string(rmember.abreise) + ";" + to_string(rmember.zimmeranz) + ";" + to_string(rmember.zimmeranz) + ";" + to_string(rmember.erwachs) + ";" + to_string(rmember.erwachs) + ";" + to_string(rmember.kind1) + ";" + to_string(rmember.kind1) + ";" + to_string(rmember.gratis) + ";" + to_string(rmember.gratis) + ";" + to_string(rmember.zikatnr) + ";" + to_string(rmember.zikatnr) + ";" + to_string(rmember.zinr) + ";" + to_string(rmember.zinr) + ";" + to_string(rmember.arrangement) + ";" + to_string(rmember.arrangement) + ";" + to_string(rmember.zipreis) + ";" + to_string(rmember.zipreis) + ";" + to_string(cid) + ";" + to_string(user_init) + ";" + to_string(cdate, "x(8)") + ";" + to_string(get_current_date()) + ";" + chg_mode + " " + to_string("Fixrate TO:") + ";" + to_string(curr_date) + "-" + to_string(new_rate) + ";" + to_string("YES", "x(3)") + ";" + to_string("YES", "x(3)") + ";"

        rqy = db_session.query(Rqy).first()


    def res_changes():

        nonlocal msg_str, do_it, allflag, curr_i, ct, zikatstr, curr_msg, init_time, init_date, ankunft1, abreise1, i, str, m_flight, overbook, overmax, overanz, overdate, incl_allot, rmcat_ovb, lvcarea, res_line, reslin_queasy, bediener, outorder, zimkateg, guest, res_history
        nonlocal rline, rmember, rbuff, raccomp, spreqbuff, resline, rqsy, rqy, guest1


        nonlocal curr_resline, t_resline, member_list, zwunsch_rline, zwunsch_rmember, rline, rmember, rbuff, raccomp, spreqbuff, resline, rqsy, rqy, guest1
        nonlocal curr_resline_list, t_resline_list, member_list_list, zwunsch_rline_list, zwunsch_rmember_list

        cid:str = ""
        cdate:str = ""
        heute:date = None
        zeit:int = 0
        Guest1 = Guest
        heute = get_current_date()
        zeit = get_current_time_in_seconds()

        if trim(t_resline.changed_id) != "":
            cid = t_resline.changed_id
            cdate = to_string(t_resline.changed)

        elif len(t_resline.reserve_char) >= 14:
            cid = substring(t_resline.reserve_char, 13)
        reslin_queasy = Reslin_queasy()
        db_session.add(reslin_queasy)

        reslin_queasy.key = "ResChanges"
        reslin_queasy.resnr = rbuff.resnr
        reslin_queasy.reslinnr = rbuff.reslinnr
        reslin_queasy.date2 = heute
        reslin_queasy.number2 = zeit


        pass
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

        reslin_queasy = db_session.query(Reslin_queasy).first()


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


            res_history.aenderung = t_resline.bemerk + chr(10) + chr(10) + "*** Changed to:" + chr(10) + chr(10) + rbuff.bemerk

            if bediener:
                res_history.betriebsnr = bediener.nr

            res_history = db_session.query(Res_history).first()


    def update_special_request():

        nonlocal msg_str, do_it, allflag, curr_i, ct, zikatstr, curr_msg, init_time, init_date, ankunft1, abreise1, i, str, m_flight, overbook, overmax, overanz, overdate, incl_allot, rmcat_ovb, lvcarea, res_line, reslin_queasy, bediener, outorder, zimkateg, guest, res_history
        nonlocal rline, rmember, rbuff, raccomp, spreqbuff, resline, rqsy, rqy, guest1


        nonlocal curr_resline, t_resline, member_list, zwunsch_rline, zwunsch_rmember, rline, rmember, rbuff, raccomp, spreqbuff, resline, rqsy, rqy, guest1
        nonlocal curr_resline_list, t_resline_list, member_list_list, zwunsch_rline_list, zwunsch_rmember_list


        Rqsy = Reslin_queasy

        rqsy = db_session.query(Rqsy).filter(
                (func.lower(Rqsy.key) == "specialRequest") &  (Rqsy.resnr == rmember.resnr) &  (Rqsy.reslinnr == rmember.reslinnr)).first()

        if not rqsy:
            rqsy = Rqsy()
            db_session.add(rqsy)

            rqsy.key = "specialRequest"
            rqsy.resnr = rmember.resnr
            rqsy.reslinnr = rmember.reslinnr


        rqsy.char3 = spreqBuff.char3

        rqsy = db_session.query(Rqsy).first()


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()
    t_resline = T_resline()
    t_resline_list.append(t_resline)


    curr_resline = query(curr_resline_list, first=True)

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == curr_resline.resnr) &  (Res_line.reslinnr == curr_resline.reslinnr)).first()

    if specrequest:

        spreqbuff = db_session.query(Spreqbuff).filter(
                (func.lower(Spreqbuff.key) == "specialRequest") &  (spreqBuff.resnr == curr_resline.resnr) &  (spreqBuff.reslinnr == curr_resline.reslinnr)).first()
    for i in range(1,num_entries(curr_resline.zimmer_wunsch, ";") - 1 + 1) :
        zwunsch_rline = Zwunsch_rline()
        zwunsch_rline_list.append(zwunsch_rline)

        str = entry(i - 1, curr_resline.zimmer_wunsch, ";")

        if substring(str, 0, 7) == "voucher":
            zwunsch_rline.s_label = "voucher"
            zwunsch_rline.s_value1 = substring(str, 7)

        elif substring(str, 0, 5) == "ChAge":
            zwunsch_rline.s_label = "chAge"
            zwunsch_rline.s_value1 = substring(str, 5)

        elif substring(str, 0, 10) == "$OrigCode$":
            zwunsch_rline.s_label = "$OrigCode$"
            zwunsch_rline.s_value1 = substring(str, 10)

        elif substring(str, 0, 6) == "$CODE$":
            zwunsch_rline.s_label = "$CODE$"
            zwunsch_rline.s_value1 = substring(str, 6)

        elif substring(str, 0, 5) == "DATE,":
            zwunsch_rline.s_label = "DATE,"
            zwunsch_rline.s_value1 = substring(str, 5)

        elif substring(str, 0, 8) == "SEGM__PUR":
            zwunsch_rline.s_label = "SEGM__PUR"
            zwunsch_rline.s_value1 = substring(str, 8)

        elif substring(str, 0, 6) == "ebdisc":
            zwunsch_rline.s_label = "ebdisc"
            zwunsch_rline.s_value1 = "Y"

        elif substring(str, 0, 6) == "kbdisc":
            zwunsch_rline.s_label = "kbdisc"
            zwunsch_rline.s_value1 = "Y"

        elif substring(str, 0, 10) == "restricted":
            zwunsch_rline.s_label = "restricted"
            zwunsch_rline.s_value1 = "Y"

        elif substring(str, 0, 6) == "pickup":
            zwunsch_rline.s_label = "pickup"
            zwunsch_rline.s_value1 = "Y"

        elif substring(str, 0, 14) == "drop_passanger":
            zwunsch_rline.s_label = "drop_passanger"
            zwunsch_rline.s_value1 = "Y"

        elif re.match(".*WCI_req.*",str):
            zwunsch_rline.s_label = "WCI_req"
            zwunsch_rline.s_value1 = entry(1, str, " == ")


    for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
        zwunsch_rline = Zwunsch_rline()
        zwunsch_rline_list.append(zwunsch_rline)

        str = entry(i - 1, res_line.zimmer_wunsch, ";")

        if substring(str, 0, 7) == "voucher":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "voucher"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "voucher"
            zwunsch_rline.s_value2 = substring(str, 7)

        elif substring(str, 0, 5) == "ChAge":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "ChAge"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "ChAge"
            zwunsch_rline.s_value2 = substring(str, 5)

        elif substring(str, 0, 10) == "$OrigCode$":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "voucher"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "$OrigCode$"
            zwunsch_rline.s_value2 = substring(str, 10)

        elif substring(str, 0, 6) == "$CODE$":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label == "&CODE$"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "$CODE$"
            zwunsch_rline.s_value2 = substring(str, 6)

        elif substring(str, 0, 5) == "DATE,":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "DATE,"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "DATE,"
            zwunsch_rline.s_value2 = substring(str, 5)

        elif substring(str, 0, 8) == "SEGM__PUR":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "SEGM__PUR"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "SEGM__PUR"
            zwunsch_rline.s_value2 = substring(str, 8)

        elif substring(str, 0, 6) == "ebdisc":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "ebdisc"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "ebdisc"
            zwunsch_rline.s_value2 = "Y"

        elif substring(str, 0, 6) == "kbdisc":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "kbdisx"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "kbdisc"
            zwunsch_rline.s_value2 = "Y"

        elif substring(str, 0, 10) == "restricted":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "restricted"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "restricted"
            zwunsch_rline.s_value2 = "Y"

        elif substring(str, 0, 6) == "pickup":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "pickup"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "pickup"
            zwunsch_rline.s_value2 = "Y"

        elif substring(str, 0, 14) == "drop_passanger":

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "drop_passanger"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "drop_passanger"
            zwunsch_rline.s_value2 = "Y"

        elif re.match(".*WCI_req.*",str):

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label.lower()  == "WCI_req"), first=True)

            if not zwunsch_rline:
                zwunsch_rline = Zwunsch_rline()
            zwunsch_rline_list.append(zwunsch_rline)

            zwunsch_rline.s_label = "WCI_req"
            zwunsch_rline.s_value2 = entry(1, str, " == ")

    for zwunsch_rline in query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_value1 == zwunsch_rline.s_value2)):
        zwunsch_rline_list.remove(zwunsch_rline)
    allflag = (c_apply == "ALL")

    if not allflag:
        for curr_i in range(1,num_entries(c_apply, ",")  + 1) :
            ct = trim(entry(curr_i - 1, c_apply, ","))

            if ct != "":
                member_list = Member_list()
                member_list_list.append(member_list)

                member_list.reslinnr = to_int(ct)

    resline = db_session.query(Resline).filter(
            (Resline.resnr == curr_Resline.resnr) &  (Resline.active_flag == 1) &  (Resline.reslinnr != curr_Resline.reslinnr) &  (Resline.l_zuordnung[2] == 0)).first()
    while None != resline:

        if allflag:
            do_it = True
        else:

            member_list = query(member_list_list, filters=(lambda member_list :member_list.reslinnr == resline.reslinnr), first=True)
            do_it = None != member_list

        if do_it:

            rbuff = db_session.query(Rbuff).filter(
                    (Rbuff._recid == resline._recid)).first()

            if curr_resline.bemerk != res_line.bemerk:
                rbuff.bemerk = res_line.bemerk

            rbuff = db_session.query(Rbuff).first()


        resline = db_session.query(Resline).filter(
                (Resline.resnr == curr_Resline.resnr) &  (Resline.active_flag == 1) &  (Resline.reslinnr != curr_Resline.reslinnr) &  (Resline.l_zuordnung[2] == 0)).first()

    rmember = db_session.query(Rmember).filter(
            (Rmember.resnr == curr_resline.resnr) &  (Rmember.active_flag == 0) &  (Rmember.reslinnr != curr_resline.reslinnr) &  (Rmember.l_zuordnung[2] == 0)).first()
    while None != rmember:

        if allflag:
            do_it = True
        else:

            member_list = query(member_list_list, filters=(lambda member_list :member_list.reslinnr == rmember.reslinnr), first=True)
            do_it = None != member_list

        if do_it:
            do_it, init_time, init_date = get_output(check_timebl(1, rmember.resnr, rmember.reslinnr, "res_line", None, None))

            if not do_it:
                msg_str = msg_str + "#" + to_string(rmember.reslinnr, "99") + " " + rmember.name + chr(10) + translateExtended ("Reservation being modified by other user.", lvcarea, "") + chr(10) + chr(10)

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

            if curr_resline.CODE != res_line.CODE:
                rbuff.CODE = res_line.CODE

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
                    msg_str = msg_str + "#" + to_string(rmember.reslinnr) + " " + rmember.name + chr(10) + translateExtended ("Wrong check_in/check_out date", lvcarea, "") + ": " + to_string(ankunft1) + "/" + to_string(abreise1) + chr(10) + chr(10)

                if do_it and rmember.zinr != "":

                    outorder = db_session.query(Outorder).filter(
                            (Outorder.zinr == rmember.zinr) &  (not Outorder.gespstart >= abreise1) &  (not Outorder.gespende < ankunft1)).first()
                    do_it = not None != outorder

                    if not do_it:
                        msg_str = msg_str + "#" + to_string(rmember.reslinnr) + " " + rmember.name + chr(10) + translateExtended ("O_O_O found RmNo", lvcarea, "") + " " + rmember.zinr + ": " + to_string(outorder.gespstart) + "/" + to_string(outorder.gespende) + chr(10) + chr(10)
                    else:

                        rline = db_session.query(Rline).filter(
                                (Rline.zinr == rmember.zinr) &  ((Rline.resstatus <= 2) |  (Rline.resstatus == 5)) &  (Rline._recid != rmember._recid) &  (not Rline.ankunft >= abreise1) &  (not Rline.abreise <= ankunft1)).first()
                        do_it = not None != rline

                        if not do_it:
                            msg_str = msg_str + "#" + to_string(rmember.reslinnr) + " " + rmember.name + chr(10) + translateExtended ("Overlapping with other reservation - RmNo", lvcarea, "") + " " + rmember.zinr + ": " + to_string(rline.ankunft) + "/" + to_string(rline.abreise) + chr(10) + chr(10)

                if do_it:

                    if curr_resline.zikatnr != res_line.zikatnr and curr_resline.zikatnr == rmember.zikatnr:

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == res_line.zikatnr)).first()
                    else:

                        zimkateg = db_session.query(Zimkateg).filter(
                                (Zimkateg.zikatnr == rmember.zikatnr)).first()
                    zikatstr = zimkateg.kurzbez
                    overbook, overmax, overanz, overdate, incl_allot, curr_msg, rmcat_ovb = get_output(res_overbookbl(pvilanguage, "modify", rmember.resnr, rmember.reslinnr, res_line.ankunft, res_line.abreise, 1, zikatstr, None, True))
                    do_it = not overbook

                    if not do_it:
                        msg_str = msg_str + "#" + to_string(rmember.reslinnr) + " " + rmember.name + chr(10) + translateExtended ("Overbooking found on", lvcarea, "") + " " + to_string(overdate) + chr(10) + chr(10)

                if do_it:

                    if curr_resline.ankunft != res_line.ankunft:
                        rbuff.ankunft = res_line.ankunft
                        rbuff.anztage = rbuff.abreise - rbuff.ankunft

                    if curr_resline.abreise != res_line.abreise:
                        rbuff.abreise = res_line.abreise
                        rbuff.anztage = rbuff.abreise - rbuff.ankunft

                    if curr_resline.zikatnr != res_line.zikatnr and curr_resline.zikatnr == rmember.zikatnr:
                        rbuff.zikatnr = res_line.zikatnr
                        rbuff.setup = res_line.setup
                        rbuff.zinr = ""

                    for raccomp in db_session.query(Raccomp).filter(
                            (Raccomp.resnr == rmember.resnr) &  (Raccomp.resstatus == 11) &  (Raccomp.kontakt_nr == rmember.reslinnr) &  (Raccomp.l_zuordnung[2] == 1)).all():
                        raccomp.ankunft = rbuff.ankunft
                        raccomp.abreise = rbuff.abreise
                        raccomp.zikatnr = rbuff.zikatnr
                        raccomp.zinr = rbuff.zinr

        if do_it and curr_resline.zipreis != res_line.zipreis and rmember.resstatus != 11 and rmember.resstatus != 13:
            rbuff.zipreis = res_line.zipreis

        if do_it and specrequest and spreqBuff:
            update_special_request()

        if do_it:
            for i in range(1,num_entries(rmember.zimmer_wunsch, ";") - 1 + 1) :
                zwunsch_rmember = Zwunsch_rmember()
                zwunsch_rmember_list.append(zwunsch_rmember)

                str = entry(i - 1, rmember.zimmer_wunsch, ";")

                if substring(str, 0, 7) == "voucher":
                    zwunsch_rmember.s_label = "voucher"
                    zwunsch_rmember.s_value2 = substring(str, 7)

                elif substring(str, 0, 5) == "ChAge":
                    zwunsch_rmember.s_label = "chAge"
                    zwunsch_rmember.s_value2 = substring(str, 5)

                elif substring(str, 0, 10) == "$OrigCode$":
                    zwunsch_rmember.s_label = "$OrigCode$"
                    zwunsch_rmember.s_value2 = substring(str, 10)

                elif substring(str, 0, 6) == "$CODE$":
                    zwunsch_rmember.s_label = "$CODE$"
                    zwunsch_rmember.s_value2 = substring(str, 6)

                elif substring(str, 0, 5) == "DATE,":
                    zwunsch_rmember.s_label = "DATE,"
                    zwunsch_rmember.s_value2 = substring(str, 5)

                elif substring(str, 0, 8) == "SEGM__PUR":
                    zwunsch_rmember.s_label = "SEGM__PUR"
                    zwunsch_rmember.s_value2 = substring(str, 8)

                elif substring(str, 0, 6) == "ebdisc":
                    zwunsch_rmember.s_label = "ebdisc"
                    zwunsch_rmember.s_value2 = "Y"

                elif substring(str, 0, 6) == "kbdisc":
                    zwunsch_rmember.s_label = "kbdisc"
                    zwunsch_rmember.s_value2 = "Y"

                elif substring(str, 0, 10) == "restricted":
                    zwunsch_rmember.s_label = "restricted"
                    zwunsch_rmember.s_value2 = "Y"

                elif substring(str, 0, 6) == "pickup":
                    zwunsch_rmember.s_label = "pickup"
                    zwunsch_rmember.s_value2 = "Y"

                elif substring(str, 0, 14) == "drop_passanger":
                    zwunsch_rmember.s_label = "drop_passanger"
                    zwunsch_rmember.s_value2 = "Y"

                elif re.match(".*WCI_req.*",str):
                    zwunsch_rmember.s_label = "WCI_req"
                    zwunsch_rmember.s_value2 = entry(1, str, " == ")

        for zwunsch_rmember in query(zwunsch_rmember_list):

            zwunsch_rline = query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.s_label == zwunsch_rmember.s_label), first=True)

            if zwunsch_rline:
                zwunsch_rmember.s_value2 = zwunsch_rline.s_value2
                zwunsch_rline.used = True

        for zwunsch_rline in query(zwunsch_rline_list, filters=(lambda zwunsch_rline :not zwunsch_rline.used)):
            zwunsch_rmember = Zwunsch_rmember()
            zwunsch_rmember_list.append(zwunsch_rmember)

            buffer_copy(zwunsch_rline, zwunsch_rmember)

        for zwunsch_rline in query(zwunsch_rline_list, filters=(lambda zwunsch_rline :zwunsch_rline.used)):
            zwunsch_rline.used = False
        ct = ""

        for zwunsch_rmember in query(zwunsch_rmember_list):

            if zwunsch_rmember.s_value2 != "":

                if zwunsch_rmember.s_value2.lower()  == "Y":
                    ct = ct + zwunsch_rmember.s_label + ";"
                else:
                    ct = ct + zwunsch_rmember.s_label + zwunsch_rmember.s_value2 + ";"
            zwunsch_rmember_list.remove(zwunsch_rmember)
        rbuff.zimmer_wunsch = ct

        if rmember.resstatus != 11 and rmember.resstatus != 13:
            check_fixrates_changes()

        rbuff = db_session.query(Rbuff).first()
        res_changes()
        do_it, init_time, init_date = get_output(check_timebl(2, rmember.resnr, rmember.reslinnr, "res_line", init_time, init_date))

    rmember = db_session.query(Rmember).filter(
            (Rmember.resnr == curr_resline.resnr) &  (Rmember.active_flag == 0) &  (Rmember.reslinnr != curr_resline.reslinnr) &  (Rmember.l_zuordnung[2] == 0)).first()

    return generate_output()