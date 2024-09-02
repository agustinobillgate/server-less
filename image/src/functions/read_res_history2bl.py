from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Res_history, Res_line, Reservation, Nebenst, Zimmer
t_res_history_list, T_res_history = create_model_like(Res_history, {"gname":str, "zinr":str, "ankunft":date, "abreise":date, "grpname":str, "wa_time":str, "ack":bool, "res":str})

def read_res_history2bl(case_type:int, int1:int, int2:int, int3:int, datum1:date, char1:str, char2:str):
    t_res_history_list = []
    ct:str = ""
    st:str = ""
    curr_i:int = 0
    rmno:str = ""
    wa_time:str = ""
    res_history = res_line = reservation = nebenst = zimmer = None

    t_res_history = None

    
    db_session = local_storage.db_session

    def generate_output():
        nonlocal t_res_history_list, ct, st, curr_i, rmno, wa_time, res_history, res_line, reservation, nebenst, zimmer
        nonlocal t_res_history
        nonlocal t_res_history_list
        return {"t-res-history": t_res_history_list}

    if case_type == 1:

        res_history = db_session.query(Res_history).filter(
                (Res_history.nr == int1) &  (Res_history.betriebsnr != int2)).first()

        if res_history:
            t_res_history = T_res_history()
            t_res_history_list.append(t_res_history)

            buffer_copy(res_history, t_res_history)
    elif case_type == 2:

        res_history = db_session.query(Res_history).filter(
                (Res_history.resnr == int1) &  
                (Res_history.reslinnr == int2) &  
                (Res_history.zeit == int3) &  
                (Res_history.datum == datum1) &  
                (func.lower(Res_history.action) == "Wake Up Call".lower())
            ).first()

        if res_history:

            res_history = db_session.query(Res_history).first()
            res_history.aenderung = res_history.aenderung + " Stat: ACK" + ";"

            res_history = db_session.query(Res_history).first()
            t_res_history = T_res_history()
            t_res_history_list.append(t_res_history)

            buffer_copy(res_history, t_res_history)
    elif case_type == 3:

        for res_history in db_session.query(Res_history).filter(
                (Res_history.resnr == int1) &  
                (Res_history.zeit == int3) &  
                (Res_history.datum == datum1) &  
                (func.lower(Res_history.action) == "Wake Up Call".lower())
                ).all():
            t_res_history = T_res_history()
            t_res_history_list.append(t_res_history)

            buffer_copy(res_history, t_res_history)
    elif case_type == 4:
        recs = (
            db_session.query(Res_history).filter(
                (Res_history.zeit >= 0) &  
                (Res_history.datum >= get_current_date() - timedelta(days=1)) &  
                (func.lower(Res_history.action) == "Wake Up Call".lower())).all()
        )
        for res_history in recs:
            t_res_history = T_res_history()
            t_res_history_list.append(t_res_history)

            buffer_copy(res_history, t_res_history)

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == res_history.resnr) &  
                    (Res_line.reslinnr == res_history.reslinnr)).first()

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_history.resnr)).first()
            t_res_history.gname = res_line.name
            t_res_history.zinr = res_line.zinr
            t_res_history.ankunft = res_line.ankunft
            t_res_history.abreise = res_line.abreise

            if reservation.groupname != "":
                t_res_history.grpname = reservation.groupname


            ct = trim(entry(0, t_res_history.aenderung, ";"))

            if re.match(".*CANCEL.*",ct):
                t_res_history.wa_time = "CANCEL"
            for curr_i in range(2,num_entries(t_res_history.aenderung, ";")  + 1) :
                ct = trim(entry(curr_i - 1, t_res_history.aenderung, ";"))
                st = substring(ct, 0, 5)

                if st == "STAT:":

                    if trim(substring(ct, 5)) == "ACK":
                        t_res_history.ack = True
                elif st == "DayD:":
                    t_res_history.res = trim(substring(ct, 5))
    elif st == 5:

        nebenst = db_session.query(Nebenst).filter(
                (func.lower(Nebenst.nebenstelle) == (char1).lower()) &  
                (Nebenst.nebst_type == 0) &  
                (Nebenst.zinr != "")).first()

        if nebenst:
            rmno = nebenst.zinr
        else:

            zimmer = db_session.query(Zimmer).filter(
                    (func.lower(Zimmer.nebenstelle) == (char1).lower())).first()

            if not zimmer:

                zimmer = db_session.query(Zimmer).filter(
                        (func.lower(Zimmer.zinr) == (char1).lower())).first()

            if zimmer:
                rmno = zimmer.zinr

        if rmno != "":
            wa_time = substring(char2, 0, 2) + ":" + substring(char2, 2, 2)

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resstatus == 6) &  (Res_line.zinr == rmno)).first()

            if not res_line:

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resstatus == 13) &  
                        (Res_line.l_zuordnung[2] == 0) &  
                        (Res_line.zinr == rmno)
                        ).first()

            if res_line:

                res_history = db_session.query(Res_history).filter(
                        (func.lower(Res_history.action) == "Wake Up Call".lower()) &  
                        (Res_history.resnr == res_line.resnr) &  
                        (Res_history.reslinnr == res_line.reslinnr) &  
                        (Res_history.datum == datum1 - 1) &  
                        (Res_history.aenderung.op("~")(".* " + res_line.zinr + ";.*")) &  
                        (Res_history.aenderung.op("~")(".*" + wa_time + ";.*"))
                        ).first()

                if not res_history:

                    res_history = db_session.query(Res_history).filter(
                            (func.lower(Res_history.action) == "Wake Up Call".lower()) &  
                            (Res_history.resnr == res_line.resnr) &  
                            (Res_history.reslinnr == res_line.reslinnr) &  
                            (Res_history.datum == datum1) &  
                            (Res_history.aenderung.op("~")(".* " + res_line.zinr + ";.*")) &  
                            (Res_history.aenderung.op("~")(".*" + wa_time + ";.*"))
                            ).first()

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

                res_history = db_session.query(Res_history).first()

    return generate_output()