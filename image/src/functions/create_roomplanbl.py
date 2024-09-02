from functions.additional_functions import *
import decimal
from datetime import date
from models import Res_line, Zimmer, Zimkateg, Resplan, Zimplan, Bill

def create_roomplanbl(na_list:[Na_list], ci_date:date):
    i = 0
    res_line = zimmer = zimkateg = resplan = zimplan = bill = None

    na_list = bbuff = None

    na_list_list, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "bezeich":str, "anz":int})

    Bbuff = Bill

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, res_line, zimmer, zimkateg, resplan, zimplan, bill
        nonlocal bbuff


        nonlocal na_list, bbuff
        nonlocal na_list_list
        return {"i": i}

    def create_roomplan():

        nonlocal i, res_line, zimmer, zimkateg, resplan, zimplan, bill
        nonlocal bbuff


        nonlocal na_list, bbuff
        nonlocal na_list_list

        j:int = 0
        anz:int = 0
        beg_datum:date = None
        end_datum:date = None
        curr_date:date = None
        answer:bool = True

        na_list = query(na_list_list, filters=(lambda na_list :na_list.reihenfolge == 2), first=True)

        for res_line in db_session.query(Res_line).filter(
                (Res_line.gastnr > 0) &  (Res_line.resstatus >= 1) &  (Res_line.resstatus <= 4) &  (Res_line.ankunft >= ci_date) &  (Res_line.active_flag == 0)).all():

            zimmer = db_session.query(Zimmer).filter(
                    (Zimmer.zinr == res_line.zinr)).first()

            if not zimmer or (zimmer and zimmer.sleeping):
                j = res_line.resstatus

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()
                beg_datum = res_line.ankunft
                end_datum = res_line.abreise - 1
                for curr_date in range(beg_datum,end_datum + 1) :

                    resplan = db_session.query(Resplan).filter(
                                (Resplan.zikatnr == zimkateg.zikatnr) &  (Resplan.datum == curr_date)).first()

                    if not resplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        resplan = Resplan()
                        db_session.add(resplan)

                        resplan.datum = curr_date
                        resplan.zikatnr = zimkateg.zikatnr


                    anz = resplan.anzzim[j - 1] + res_line.zimmeranz

                    resplan = db_session.query(Resplan).first()
                    resplan.anzzim[j - 1] = anz

                    resplan = db_session.query(Resplan).first()


            if res_line.zinr != "":
                for curr_date in range(beg_datum,end_datum + 1) :

                    zimplan = db_session.query(Zimplan).filter(
                                (Zimplan.datum == curr_date) &  (Zimplan.zinr == res_line.zinr)).first()

                    if not zimplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        zimplan = Zimplan()
                        db_session.add(zimplan)

                        zimplan.datum = curr_date
                        zimplan.zinr = res_line.zinr
                        zimplan.res_recid = res_line._recid
                        zimplan.gastnrmember = res_line.gastnrmember
                        zimplan.bemerk = res_line.bemerk
                        zimplan.resstatus = res_line.resstatus
                        zimplan.name = res_line.name

                        zimplan = db_session.query(Zimplan).first()


        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                (Res_line.active_flag == 1) &  (Res_line.abreise > ci_date) &  ((Res_line.resstatus == 6) |  (Res_line.resstatus == 13))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            if zimmer.sleeping:
                j = res_line.resstatus

                zimkateg = db_session.query(Zimkateg).filter(
                        (Zimkateg.zikatnr == res_line.zikatnr)).first()
                beg_datum = ci_date
                end_datum = res_line.abreise - 1
                for curr_date in range(beg_datum,end_datum + 1) :

                    resplan = db_session.query(Resplan).filter(
                                (Resplan.zikatnr == zimkateg.zikatnr) &  (Resplan.datum == curr_date)).first()

                    if not resplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        resplan = Resplan()
                        db_session.add(resplan)

                        resplan.datum = curr_date
                        resplan.zikatnr = zimkateg.zikatnr


                    anz = resplan.anzzim[j - 1] + res_line.zimmeranz

                    resplan = db_session.query(Resplan).first()
                    resplan.anzzim[j - 1] = anz

                    resplan = db_session.query(Resplan).first()


            if res_line.resstatus == 6:
                for curr_date in range(beg_datum,end_datum + 1) :

                    zimplan = db_session.query(Zimplan).filter(
                                (Zimplan.datum == curr_date) &  (Zimplan.zinr == res_line.zinr)).first()

                    if not zimplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        zimplan = Zimplan()
                        db_session.add(zimplan)

                        zimplan.datum = curr_date
                        zimplan.zinr = res_line.zinr
                        zimplan.res_recid = res_line._recid
                        zimplan.gastnrmember = res_line.gastnrmember
                        zimplan.bemerk = res_line.bemerk
                        zimplan.resstatus = res_line.resstatus
                        zimplan.name = res_line.name

                        zimplan = db_session.query(Zimplan).first()


    def check_co_guestbill():

        nonlocal i, res_line, zimmer, zimkateg, resplan, zimplan, bill
        nonlocal bbuff


        nonlocal na_list, bbuff
        nonlocal na_list_list


        Bbuff = Bill

        bill = db_session.query(Bill).filter(
                (Bill.resnr > 0) &  (Bill.reslinnr > 0) &  (Bill.flag == 0) &  (Bill.saldo == 0)).first()
        while None != bill:

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.parent_nr)).first()

            if not res_line:

                bbuff = db_session.query(Bbuff).filter(
                        (Bbuff._recid == bill._recid)).first()
                bbuff.flag = 1

                bbuff = db_session.query(Bbuff).first()


            elif res_line.active_flag == 2:

                bbuff = db_session.query(Bbuff).filter(
                        (Bbuff._recid == bill._recid)).first()
                bbuff.flag = 1

                bbuff = db_session.query(Bbuff).first()


            bill = db_session.query(Bill).filter(
                    (Bill.resnr > 0) &  (Bill.reslinnr > 0) &  (Bill.flag == 0) &  (Bill.saldo == 0)).first()

        for res_line in db_session.query(Res_line).filter(
                (Res_line.active_flag == 1) &  (Res_line.l_zuordnung[2] == 0)).all():

            bill = db_session.query(Bill).filter(
                    (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr)).first()
            while None != bill:

                if bill.zinr != res_line.zinr:

                    bbuff = db_session.query(Bbuff).filter(
                            (Bbuff._recid == bill._recid)).first()
                    bbuff.zinr = res_line.zinr

                    bbuff = db_session.query(Bbuff).first()


                bill = db_session.query(Bill).filter(
                        (Bill.resnr == res_line.resnr) &  (Bill.parent_nr == res_line.reslinnr)).first()


    create_roomplan()
    check_co_guestbill()

    return generate_output()