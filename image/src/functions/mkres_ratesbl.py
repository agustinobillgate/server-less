from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.check_bonus_nightbl import check_bonus_nightbl
from models import Res_line, Reslin_queasy, Htparam, Queasy, Zimkateg, Segment, Reservation

def mkres_ratesbl(from_date:date, user_init:str, chg_zikat:bool, chg_flag:bool, reslin_list:[Reslin_list], room_list:[Room_list], res_dynarate:[Res_dynarate]):
    ratecode_bez = ""
    new_segm = ""
    fixed_rate = False
    room_rate = 0
    resno:int = 0
    reslinno:int = 0
    ankunft:date = None
    abreise:date = None
    curr_argt:str = ""
    curr_i:int = 0
    fr_date:date = None
    checkin_date:date = None
    curr_date:date = None
    to_date:date = None
    p_493:bool = False
    res_line = reslin_queasy = htparam = queasy = zimkateg = segment = reservation = None

    reslin_list = res_dynarate = room_list = r_qsy = qsy = zbuff = None

    reslin_list_list, Reslin_list = create_model_like(Res_line)
    res_dynarate_list, Res_dynarate = create_model("Res_dynarate", {"date1":date, "date2":date, "rate":decimal, "rmcat":str, "argt":str, "prcode":str, "rcode":str, "markno":int, "setup":int, "adult":int, "child":int})
    room_list_list, Room_list = create_model("Room_list", {"avail_flag":bool, "allot_flag":bool, "zikatnr":int, "i_typ":int, "sleeping":bool, "allotment":[int, 30], "bezeich":str, "room":[int, 30], "coom":[str, 30], "rmrate":[decimal, 30], "currency":int, "wabkurz":str, "i_counter":int, "rateflag":bool, "adult":int, "child":int, "prcode":[str, 30], "rmcat":str, "argt":str, "rcode":str, "segmentcode":str, "dynarate":bool, "expired":bool, "argt_remark":str, "minstay":int, "maxstay":int, "minadvance":int, "maxadvance":int, "frdate":date, "todate":date, "marknr":int, "datum":[date, 30]}, {"sleeping": True, "frdate": None, "todate": None})

    R_qsy = Reslin_queasy
    Qsy = Queasy
    Zbuff = Zimkateg

    db_session = local_storage.db_session

    def generate_output():
        nonlocal ratecode_bez, new_segm, fixed_rate, room_rate, resno, reslinno, ankunft, abreise, curr_argt, curr_i, fr_date, checkin_date, curr_date, to_date, p_493, res_line, reslin_queasy, htparam, queasy, zimkateg, segment, reservation
        nonlocal r_qsy, qsy, zbuff


        nonlocal reslin_list, res_dynarate, room_list, r_qsy, qsy, zbuff
        nonlocal reslin_list_list, res_dynarate_list, room_list_list
        return {"ratecode_bez": ratecode_bez, "new_segm": new_segm, "fixed_rate": fixed_rate, "room_rate": room_rate}

    def update_qsy171():

        nonlocal ratecode_bez, new_segm, fixed_rate, room_rate, resno, reslinno, ankunft, abreise, curr_argt, curr_i, fr_date, checkin_date, curr_date, to_date, p_493, res_line, reslin_queasy, htparam, queasy, zimkateg, segment, reservation
        nonlocal r_qsy, qsy, zbuff


        nonlocal reslin_list, res_dynarate, room_list, r_qsy, qsy, zbuff
        nonlocal reslin_list_list, res_dynarate_list, room_list_list

        upto_date:date = None
        datum:date = None
        start_date:date = None
        i:int = 0
        iftask:str = ""
        origcode:str = ""
        newcode:str = ""
        do_it:bool = False
        cat_flag:bool = False
        roomnr:int = 0
        roomnr1:int = 0
        Qsy = Queasy
        Zbuff = Zimkateg
        for i in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            iftask = entry(i - 1, res_line.zimmer_wunsch, ";")

            if substring(iftask, 0, 10) == "$origcode$":
                origcode = substring(iftask, 10)
                return
        for i in range(1,num_entries(reslin_list.zimmer_wunsch, ";") - 1 + 1) :
            iftask = entry(i - 1, reslin_list.zimmer_wunsch, ";")

            if substring(iftask, 0, 10) == "$origcode$":
                newcode = substring(iftask, 10)
                return

        queasy = db_session.query(Queasy).filter(
                    (Queasy.key == 152)).first()

        if queasy:
            cat_flag = True

        zbuff = db_session.query(Zbuff).filter(
                    (Zbuff.zikatnr == res_line.zikatnr)).first()

        if cat_flag and zbuff:
            roomnr = zbuff.typ
            roomnr1 = zimkateg.typ

        elif zbuff:
            roomnr = zbuff.zikatnr
            roomnr1 = zimkateg.zikatnr

        if origcode.lower()  == (newcode).lower()  and res_line.zikatnr == zimkateg.zikatnr:
            pass

        elif origcode != "" or newcode != "":

            if res_line.ankunft == res_line.abreise:
                upto_date = res_line.abreise
            else:
                upto_date = res_line.abreise - 1

            if res_line.zikatnr != zimkateg.zikatnr:
                for datum in range(res_line.ankunft,upto_date + 1) :

                    queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 171) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (func.lower(Queasy.char1) == (origcode).lower())).first()

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:

                        queasy = db_session.query(Queasy).first()
                        queasy.logi2 = True

                        queasy = db_session.query(Queasy).first()


                    queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 171) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr1) &  (func.lower(Queasy.char1) == (newcode).lower())).first()

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:

                        queasy = db_session.query(Queasy).first()
                        queasy.logi2 = True

                        queasy = db_session.query(Queasy).first()


            elif res_line.zikatnr == zimkateg.zikatnr and origcode.lower()  != (newcode).lower() :
                for datum in range(res_line.ankunft,upto_date + 1) :

                    queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 171) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (func.lower(Queasy.char1) == (origcode).lower())).first()

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:

                        queasy = db_session.query(Queasy).first()
                        queasy.logi2 = True

                        queasy = db_session.query(Queasy).first()


                    queasy = db_session.query(Queasy).filter(
                                (Queasy.key == 171) &  (Queasy.date1 == datum) &  (Queasy.number1 == roomnr) &  (func.lower(Queasy.char1) == (newcode).lower())).first()

                    if queasy and queasy.logi1 == False and queasy.logi2 == False:

                        queasy = db_session.query(Queasy).first()
                        queasy.logi2 = True

                        queasy = db_session.query(Queasy).first()


    reslin_list = query(reslin_list_list, first=True)

    room_list = query(room_list_list, first=True)
    resno = reslin_list.resnr
    reslinno = reslin_list.reslinnr
    ankunft = reslin_list.ankunft
    abreise = reslin_list.abreise
    curr_argt = reslin_list.arrangement

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    checkin_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 493)).first()
    p_493 = htparam.flogical

    if p_493 :

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno)).all():
            db_session.delete(reslin_queasy)


    queasy = db_session.query(Queasy).filter(
            (Queasy.key == 2) &  (Queasy.char1 == room_list.rcode)).first()
    ratecode_bez = queasy.char1 + " - " + queasy.char2

    for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.date1 < Reslin_queasy.date2)).all():
        to_date = reslin_queasy.date2

        r_qsy = db_session.query(R_qsy).filter(
                        (R_qsy._recid == reslin_queasy._recid)).first()
        r_qsy.date2 = r_qsy.date1

        r_qsy = db_session.query(R_qsy).first()

        curr_date = reslin_queasy.date1
        for curr_i in range(2,(to_date - reslin_queasy.date1)  + 1) :
            curr_date = curr_date + 1


            r_qsy = R_qsy()
            db_session.add(r_qsy)

            buffer_copy(reslin_queasy, r_qsy,except_fields=["date1","date2"])
            r_qsy.date1 = curr_date
            r_qsy.date2 = curr_date

            r_qsy = db_session.query(R_qsy).first()

    fixed_rate = True
    fr_date = from_date


    for curr_i in range(1,(abreise - from_date)  + 1) :

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.date1 == fr_date) &  (Reslin_queasy.date2 == fr_date)).first()

        if not reslin_queasy:
            reslin_queasy = Reslin_queasy()
            db_session.add(reslin_queasy)

            reslin_queasy.key = "arrangement"
            reslin_queasy.resnr = resno
            reslin_queasy.reslinnr = reslinno
            reslin_queasy.date1 = fr_date
            reslin_queasy.date2 = fr_date
            reslin_queasy.deci1 = room_list.rmrate[curr_i - 1]
            reslin_queasy.char2 = room_list.prcode[curr_i - 1]
            reslin_queasy.char3 = user_init

            if curr_argt != room_list.argt:
                reslin_queasy.char1 = room_list.argt

        if curr_i == 1:
            room_rate = reslin_queasy.deci1

        if curr_i == 1:
            room_rate = reslin_queasy.deci1
        fr_date = fr_date + 1

    zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.kurzbez == room_list.rmcat)).first()

    res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == resno) &  (Res_line.reslinnr == reslinno)).first()
    update_qsy171()
    res_line.zimmer_wunsch = reslin_list.zimmer_wunsch
    res_line.arrangement = reslin_list.arrangement
    res_line.betriebsnr = reslin_list.betriebsnr
    res_line.zipreis = reslin_list.zipreis
    res_line.reserve_int = room_list.marknr
    res_line.zikatnr = zimkateg.zikatnr
    res_line.l_zuordnung[0] = zimkateg.zikatnr

    if chg_zikat:
        res_line.zinr = ""
        res_line.setup = 0

    res_line = db_session.query(Res_line).first()

    queasy = db_session.query(Queasy).filter(
                (Queasy.key == 2) &  (Queasy.char1 == room_list.rcode)).first()

    if entry(0, queasy.char3, ";") != "" and ((reslin_list.active_flag == 0) or (reslin_list.active_flag == 1) and (from_date == checkin_date)):

        segment = db_session.query(Segment).filter(
                    (Segment.bezeich == entry(0, queasy.char3, ";"))).first()

        if segment:

            reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == resno)).first()
            reservation.segmentcode = segmentcode
            new_segm = to_string(segmentcode) + " " +\
                    segment.bezeich

            reservation = db_session.query(Reservation).first()

    if room_list.dynarate:

        for res_dynarate in query(res_dynarate_list):

            if res_dynarate.date2 < from_date:
                1

            elif res_dynarate.date1 < checkin_date and res_dynarate.date2 >= checkin_date:
                res_dynarate.date2 = checkin_date - 1
            else:
                res_dynarate_list.remove(res_dynarate)
        fixed_rate = True
        fr_date = from_date


        for curr_i in range(1,(abreise - from_date)  + 1) :
            res_dynarate = Res_dynarate()
            res_dynarate_list.append(res_dynarate)

            res_dynarate.date1 = fr_date
            res_dynarate.date2 = fr_date
            res_dynarate.rmcat = room_list.rmcat
            res_dynarate.argt = room_list.argt
            res_dynarate.markNo = room_list.marknr
            res_dynarate.adult = room_list.adult
            res_dynarate.child = room_list.child
            res_dynarate.rcode = room_list.rcode
            res_dynarate.prcode = room_list.prcode[curr_i - 1]
            res_dynarate.rate = room_list.rmrate[curr_i - 1]

            reslin_queasy = db_session.query(Reslin_queasy).filter(
                        (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno) &  (Reslin_queasy.date1 == fr_date) &  (Reslin_queasy.date2 == fr_date)).first()

            if not reslin_queasy:
                reslin_queasy = Reslin_queasy()
                db_session.add(reslin_queasy)

                reslin_queasy.key = "arrangement"
                reslin_queasy.resnr = resno
                reslin_queasy.reslinnr = reslinno
                reslin_queasy.date1 = fr_date
                reslin_queasy.date2 = fr_date
                reslin_queasy.deci1 = room_list.rmrate[curr_i - 1]
                reslin_queasy.char2 = room_list.prcode[curr_i - 1]
                reslin_queasy.char3 = user_init

                if curr_argt != room_list.argt:

                if curr_i == 1:
                    room_rate = reslin_queasy.deci1
                fr_date = fr_date + 1
                res_dynarate.rate = reslin_queasy.deci1
                reslin_queasy.char1 = room_list.argt

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                    (func.lower(Reslin_queasy.key) == "arrangement") &  (Reslin_queasy.resnr == resno) &  (Reslin_queasy.reslinnr == reslinno)).all():

            if reslin_queasy.date2 < reslin_list.ankunft:
                db_session.delete(reslin_queasy)

            elif reslin_queasy.date1 >= reslin_list.abreise:
                db_session.delete(reslin_queasy)

    if reslin_list.active_flag == 0:
        res_dynarate_list = get_output(check_bonus_nightbl(reslin_list.ankunft, reslin_list.abreise, res_dynarate))

    return generate_output()