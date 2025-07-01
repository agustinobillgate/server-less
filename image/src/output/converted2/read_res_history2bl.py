#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Res_history, Res_line, Reservation, Nebenst, Zimmer

def read_res_history2bl(case_type:int, int1:int, int2:int, int3:int, datum1:date, char1:string, char2:string):

    prepare_cache ([Res_line, Reservation, Nebenst, Zimmer])

    t_res_history_list = []
    ct:string = ""
    st:string = ""
    curr_i:int = 0
    rmno:string = ""
    wa_time:string = ""
    res_history = res_line = reservation = nebenst = zimmer = None

    t_res_history = None

    t_res_history_list, T_res_history = create_model_like(Res_history, {"gname":string, "zinr":string, "ankunft":date, "abreise":date, "grpname":string, "wa_time":string, "ack":bool, "res":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_res_history_list, ct, st, curr_i, rmno, wa_time, res_history, res_line, reservation, nebenst, zimmer
        nonlocal case_type, int1, int2, int3, datum1, char1, char2


        nonlocal t_res_history
        nonlocal t_res_history_list

        return {"t-res-history": t_res_history_list}

    if case_type == 1:

        res_history = get_cache (Res_history, {"nr": [(eq, int1)],"betriebsnr": [(ne, int2)]})

        if res_history:
            t_res_history = T_res_history()
            t_res_history_list.append(t_res_history)

            buffer_copy(res_history, t_res_history)
    elif case_type == 2:

        res_history = get_cache (Res_history, {"resnr": [(eq, int1)],"reslinnr": [(eq, int2)],"zeit": [(eq, int3)],"datum": [(eq, datum1)],"action": [(eq, "wake up call")]})

        if res_history:
            pass
            res_history.aenderung = res_history.aenderung +\
                    " Stat: ACK" + ";"


            pass
            t_res_history = T_res_history()
            t_res_history_list.append(t_res_history)

            buffer_copy(res_history, t_res_history)
    elif case_type == 3:

        for res_history in db_session.query(Res_history).filter(
                 (Res_history.resnr == int1) & (Res_history.zeit == int3) & (Res_history.datum == datum1) & (Res_history.action == ("Wake Up Call").lower())).order_by(Res_history._recid).all():
            t_res_history = T_res_history()
            t_res_history_list.append(t_res_history)

            buffer_copy(res_history, t_res_history)
    elif case_type == 4:

        for res_history in db_session.query(Res_history).filter(
                 (Res_history.zeit >= 0) & (Res_history.datum >= get_current_date() - 1) & (Res_history.action == ("Wake Up Call").lower())).order_by(Res_history._recid).all():
            t_res_history = T_res_history()
            t_res_history_list.append(t_res_history)

            buffer_copy(res_history, t_res_history)

            res_line = get_cache (Res_line, {"resnr": [(eq, res_history.resnr)],"reslinnr": [(eq, res_history.reslinnr)]})

            reservation = get_cache (Reservation, {"resnr": [(eq, res_history.resnr)]})
            t_res_history.gname = res_line.name
            t_res_history.zinr = res_line.zinr
            t_res_history.ankunft = res_line.ankunft
            t_res_history.abreise = res_line.abreise

            if reservation.groupname != "":
                t_res_history.grpname = reservation.groupname


            ct = trim(entry(0, t_res_history.aenderung, ";"))

            if matches(ct,r"*CANCEL*"):
                t_res_history.wa_time = "CANCEL"
            for curr_i in range(2,num_entries(t_res_history.aenderung, ";")  + 1) :
                ct = trim(entry(curr_i - 1, t_res_history.aenderung, ";"))
                st = substring(ct, 0, 5)

                if st == "STAT:":

                    if trim(substring(ct, 5)) == ("ACK").lower() :
                        t_res_history.ack = True
                elif st == "DayD:":
                    t_res_history.res = trim(substring(ct, 5))
    elif st == 5:

        nebenst = get_cache (Nebenst, {"nebenstelle": [(eq, char1)],"nebst_type": [(eq, 0)],"zinr": [(ne, "")]})

        if nebenst:
            rmno = nebenst.zinr
        else:

            zimmer = get_cache (Zimmer, {"nebenstelle": [(eq, char1)]})

            if not zimmer:

                zimmer = get_cache (Zimmer, {"zinr": [(eq, char1)]})

            if zimmer:
                rmno = zimmer.zinr

        if rmno != "":
            wa_time = substring(char2, 0, 2) + ":" + substring(char2, 2, 2)

            res_line = get_cache (Res_line, {"resstatus": [(eq, 6)],"zinr": [(eq, rmno)]})

            if not res_line:

                res_line = get_cache (Res_line, {"resstatus": [(eq, 13)],"l_zuordnung[2]": [(eq, 0)],"zinr": [(eq, rmno)]})

            if res_line:

                res_history = db_session.query(Res_history).filter(
                         (Res_history.action == ("Wake Up Call").lower()) & (Res_history.resnr == res_line.resnr) & (Res_history.reslinnr == res_line.reslinnr) & (Res_history.datum == datum1 - timedelta(days=1)) & (matches(Res_history.aenderung,("* " + res_line.zinr + ";*"))) & (matches(Res_history.aenderung,("*" + wa_time + ";*")))).first()

                if not res_history:

                    res_history = db_session.query(Res_history).filter(
                             (Res_history.action == ("Wake Up Call").lower()) & (Res_history.resnr == res_line.resnr) & (Res_history.reslinnr == res_line.reslinnr) & (Res_history.datum == datum1) & (matches(Res_history.aenderung,("* " + res_line.zinr + ";*"))) & (matches(Res_history.aenderung,("*" + wa_time + ";*")))).first()

                if res_history:

                    if int1 == 1:
                        res_history.aenderung = res_history.aenderung + "DayD: Answer" + ";"
                    elif int1 == 2:
                        res_history.aenderung = res_history.aenderung + "DayD: Busy" + ";"
                    elif int1 == 3:
                        res_history.aenderung = res_history.aenderung + "DayD: No Answer" + ";"
                    elif int1 == 4:
                        res_history.aenderung = res_history.aenderung + "DayD: Block" + ";"
                    elif int1 == 5:
                        res_history.aenderung = res_history.aenderung + "DayD: Call Termination" + ";"
                    pass

    return generate_output()