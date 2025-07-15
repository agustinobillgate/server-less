from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
import re
from models import Res_line, Zimkateg, Reslin_queasy, Res_history

def res_logbl(pvilanguage:int, inp_resnr:int, inp_reslinnr:int):
    avail_res = False
    tittle = ""
    res_log_list = []
    lvcarea:str = "res_log"
    res_line = zimkateg = reslin_queasy = res_history = None

    res_log = zimkateg1 = None

    res_log_list, Res_log = create_model("Res_log", {"flag":str, "his_recid":int, "ankunft1":date, "ankunft2":date, "abreise1":date, "abreise2":date, "qty1":int, "qty2":int, "adult1":int, "adult2":int, "child1":int, "child2":int, "comp1":int, "comp2":int, "rmcat1":str, "rmcat2":str, "zinr1":str, "zinr2":str, "argt1":str, "argt2":str, "rate1":decimal, "rate2":decimal, "fixrate1":str, "fixrate2":str, "name1":str, "name2":str, "id1":str, "id2":str, "date1":date, "date2":date, "zeit":int})

    Zimkateg1 = Zimkateg

    db_session = local_storage.db_session

    def generate_output():
        nonlocal avail_res, tittle, res_log_list, lvcarea, res_line, zimkateg, reslin_queasy, res_history
        nonlocal zimkateg1


        nonlocal res_log, zimkateg1
        nonlocal res_log_list
        return {"avail_res": avail_res, "tittle": tittle, "res-log": res_log_list}

    def create_list():

        nonlocal avail_res, tittle, res_log_list, lvcarea, res_line, zimkateg, reslin_queasy, res_history
        nonlocal zimkateg1


        nonlocal res_log, zimkateg1
        nonlocal res_log_list


        Zimkateg1 = Zimkateg

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                (func.lower(Reslin_queasy.key) == "ResChanges".lower()) &  
                (Reslin_queasy.resnr == inp_resnr) &  
                (Reslin_queasy.reslinnr == inp_reslinnr) &  
                (Reslin_queasy.char3 != None)).all():
            res_log = Res_log()
            res_log_list.append(res_log)

            if re.match(".*;.*",reslin_queasy.char3):
                res_log.ankunft1 = date_mdy(entry(0, reslin_queasy.char3, ";"))
                res_log.ankunft2 = date_mdy(entry(1, reslin_queasy.char3, ";"))
                res_log.abreise1 = date_mdy(entry(2, reslin_queasy.char3, ";"))
                res_log.abreise2 = date_mdy(entry(3, reslin_queasy.char3, ";"))
                res_log.qty1 = to_int(entry(4, reslin_queasy.char3, ";"))
                res_log.qty2 = to_int(entry(5, reslin_queasy.char3, ";"))
                res_log.Adult1 = to_int(entry(6, reslin_queasy.char3, ";"))
                res_log.adult2 = to_int(entry(7, reslin_queasy.char3, ";"))
                res_log.child1 = to_int(entry(8, reslin_queasy.char3, ";"))
                res_log.child2 = to_int(entry(9, reslin_queasy.char3, ";"))
                res_log.comp1 = to_int(entry(10, reslin_queasy.char3, ";"))
                res_log.comp2 = to_int(entry(11, reslin_queasy.char3, ";"))
                res_log.zinr1 = entry(14, reslin_queasy.char3, ";")
                res_log.zinr2 = entry(15, reslin_queasy.char3, ";")
                res_log.argt1 = entry(16, reslin_queasy.char3, ";")
                res_log.argt2 = entry(17, reslin_queasy.char3, ";")
                res_log.rate1 = decimal.Decimal(entry(18, reslin_queasy.char3, ";"))
                res_log.rate2 = decimal.Decimal(entry(19, reslin_queasy.char3, ";"))
                res_log.id1 = entry(20, reslin_queasy.char3, ";")
                res_log.id2 = entry(21, reslin_queasy.char3, ";")
                res_log.name1 = entry(24, reslin_queasy.char3, ";")
                res_log.name2 = entry(25, reslin_queasy.char3, ";")
                res_log.fixrate1 = entry(26, reslin_queasy.char3, ";")
                res_log.fixrate2 = entry(27, reslin_queasy.char3, ";")

                if trim(entry(22, reslin_queasy.char3, ";")) == "":
                    res_log.date1 = None
                else:
                    res_log.date1 = date_mdy(entry(22, reslin_queasy.char3, ";"))

                if trim(entry(23, reslin_queasy.char3, ";")) == "":
                    res_log.date2 = None
                else:
                    res_log.date2 = date_mdy(entry(23, reslin_queasy.char3, ";"))

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == to_int(entry(12, reslin_queasy.char3, ";")))).first()

                zimkateg1 = db_session.query(Zimkateg1).filter(
                        (Zimkateg1.zikatnr == to_int(entry(13, reslin_queasy.char3, ";")))).first()

                if zimkateg:
                    res_log.rmcat1 = to_string(zimkateg.kurzbez, "x(6)")

                if zimkateg1:
                    res_log.rmcat2 = to_string(zimkateg1.kurzbez, "x(6)")
            else:

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == to_int(trim(substring(reslin_queasy.char3, 50, 3))))).first()

                zimkateg1 = db_session.query(Zimkateg1).filter(
                        (Zimkateg1.zikatnr == to_int(trim(substring(reslin_queasy.char3, 53, 3))))).first()
                res_log.ankunft1 = date_mdy(substring(reslin_queasy.char3, 0, 8))
                res_log.ankunft2 = date_mdy(substring(reslin_queasy.char3, 8, 8))
                res_log.abreise1 = date_mdy(substring(reslin_queasy.char3, 16, 8))
                res_log.abreise2 = date_mdy(substring(reslin_queasy.char3, 24, 8))
                res_log.qty1 = to_int(substring(reslin_queasy.char3, 32, 3))
                res_log.qty2 = to_int(substring(reslin_queasy.char3, 35, 3))
                res_log.Adult1 = to_int(substring(reslin_queasy.char3, 38, 2))
                res_log.adult2 = to_int(substring(reslin_queasy.char3, 40, 2))
                res_log.child1 = to_int(substring(reslin_queasy.char3, 42, 2))
                res_log.child2 = to_int(substring(reslin_queasy.char3, 44, 2))
                res_log.comp1 = to_int(substring(reslin_queasy.char3, 46, 2))
                res_log.comp2 = to_int(substring(reslin_queasy.char3, 48, 2))

                if zimkateg:
                    res_log.rmcat1 = to_string(zimkateg.kurzbez, "x(6)")

                if zimkateg1:
                    res_log.rmcat2 = to_string(zimkateg1.kurzbez, "x(6)")
                res_log.zinr1 = substring(reslin_queasy.char3, 56, 4)
                res_log.zinr2 = substring(reslin_queasy.char3, 60, 4)
                res_log.argt1 = substring(reslin_queasy.char3, 64, 5)
                res_log.argt2 = substring(reslin_queasy.char3, 69, 5)
                local_storage.debugging = local_storage.debugging + ",char3:" + reslin_queasy.char3
                if reslin_queasy == "":
                    pass
                else:
                    # ----- Rudy - Need to check with team dev ---------------
                    # res_log.rate1 = decimal.Decimal(substring(reslin_queasy.char3, 74, 12))
                    # res_log.rate2 = decimal.Decimal(substring(reslin_queasy.char3, 86, 12))
                    local_storage.debugging = local_storage.debugging + ",Nochar3:" + reslin_queasy.char3

                res_log.id1 = substring(reslin_queasy.char3, 98, 2)
                res_log.id2 = substring(reslin_queasy.char3, 100, 2)
                res_log.date1 = date_mdy(substring(reslin_queasy.char3, 102, 8))

                if substring(reslin_queasy.char3, 110, 8) == "        ":
                    res_log.date2 = None
                else:
                    res_log.date2 = date_mdy(substring(reslin_queasy.char3, 110, 8))

                if len(reslin_queasy.char3) > 120:
                    res_log.name1 = substring(reslin_queasy.char3, 118, 16)
                    res_log.name2 = substring(reslin_queasy.char3, 134, 16)

                if len(reslin_queasy.char3) > 151:
                    res_log.fixrate1 = substring(reslin_queasy.char3, 150, 3)
                    res_log.fixrate2 = substring(reslin_queasy.char3, 153, 3)
            res_log.zeit = reslin_queasy.number2

            res_history = db_session.query(Res_history).filter(
                    (Res_history.resnr == inp_resnr) &  
                    (Res_history.reslinnr == inp_reslinnr) &  
                    (Res_history.datum == reslin_queasy.date2) &  
                    (Res_history.zeit == reslin_queasy.number2)).first()
            # print("ResHistory:", inp_resnr, inp_reslinnr, reslin_queasy.date2, reslin_queasy.number2)
            if res_history:
                local_storage.debugging = local_storage.debugging + ",R:" + str(res_history._recid)
                res_log.his_recid = res_history._recid
                res_log.flag = "*"
            else:
                # local_storage.debugging = local_storage.debugging + ",NoR" 
                pass

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == inp_resnr) &  (Res_line.reslinnr == inp_reslinnr)).first()

    if res_line:
        avail_res = True
        tittle = " ! " + res_line.name + " -  ResNo: " + to_string(res_line.resnr)
    create_list()

    return generate_output()