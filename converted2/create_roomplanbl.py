#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Zimmer, Zimkateg, Resplan, Zimplan, Bill

na_list_data, Na_list = create_model("Na_list", {"reihenfolge":int, "flag":int, "bezeich":string, "anz":int})

def create_roomplanbl(na_list_data:[Na_list], ci_date:date):

    prepare_cache ([Res_line, Zimkateg, Resplan, Zimplan, Bill])

    i = 0
    res_line = zimmer = zimkateg = resplan = zimplan = bill = None

    na_list = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, res_line, zimmer, zimkateg, resplan, zimplan, bill
        nonlocal ci_date


        nonlocal na_list

        return {"na-list": na_list_data, "i": i}

    def create_roomplan():

        nonlocal i, res_line, zimmer, zimkateg, resplan, zimplan, bill
        nonlocal ci_date


        nonlocal na_list

        j:int = 0
        anz:int = 0
        beg_datum:date = None
        end_datum:date = None
        curr_date:date = None
        answer:bool = True

        na_list = query(na_list_data, filters=(lambda na_list: na_list.reihenfolge == 2), first=True)

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.gastnr > 0) & (Res_line.resstatus >= 1) & (Res_line.resstatus <= 4) & (Res_line.ankunft >= ci_date) & (Res_line.active_flag == 0)).order_by(Res_line._recid).all():

            zimmer = get_cache (Zimmer, {"zinr": [(eq, res_line.zinr)]})

            if not zimmer or (zimmer and zimmer.sleeping):
                j = res_line.resstatus

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
                beg_datum = res_line.ankunft
                end_datum = res_line.abreise - timedelta(days=1)
                for curr_date in date_range(beg_datum,end_datum) :

                    resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})

                    if not resplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        resplan = Resplan()
                        db_session.add(resplan)

                        resplan.datum = curr_date
                        resplan.zikatnr = zimkateg.zikatnr


                    anz = resplan.anzzim[j - 1] + res_line.zimmeranz
                    pass
                    resplan.anzzim[j - 1] = anz
                    pass

            if res_line.zinr != "":
                for curr_date in date_range(beg_datum,end_datum) :

                    zimplan = get_cache (Zimplan, {"datum": [(eq, curr_date)],"zinr": [(eq, res_line.zinr)]})

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


                        pass

        res_line_obj_list = {}
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                 (Res_line.active_flag == 1) & (Res_line.abreise > ci_date) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).order_by(Res_line._recid).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            if zimmer.sleeping:
                j = res_line.resstatus

                zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})
                beg_datum = ci_date
                end_datum = res_line.abreise - timedelta(days=1)
                for curr_date in date_range(beg_datum,end_datum) :

                    resplan = get_cache (Resplan, {"zikatnr": [(eq, zimkateg.zikatnr)],"datum": [(eq, curr_date)]})

                    if not resplan:
                        i = i + 1
                        na_list.anz = na_list.anz + 1
                        resplan = Resplan()
                        db_session.add(resplan)

                        resplan.datum = curr_date
                        resplan.zikatnr = zimkateg.zikatnr


                    anz = resplan.anzzim[j - 1] + res_line.zimmeranz
                    pass
                    resplan.anzzim[j - 1] = anz
                    pass

            if res_line.resstatus == 6:
                for curr_date in date_range(beg_datum,end_datum) :

                    zimplan = get_cache (Zimplan, {"datum": [(eq, curr_date)],"zinr": [(eq, res_line.zinr)]})

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


                        pass


    def check_co_guestbill():

        nonlocal i, res_line, zimmer, zimkateg, resplan, zimplan, bill
        nonlocal ci_date


        nonlocal na_list

        bbuff = None
        Bbuff =  create_buffer("Bbuff",Bill)

        bill = get_cache (Bill, {"resnr": [(gt, 0)],"reslinnr": [(gt, 0)],"flag": [(eq, 0)],"saldo": [(eq, 0)]})
        while None != bill:

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})

            if not res_line:

                bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                bbuff.flag = 1
                pass
                pass

            elif res_line.active_flag == 2:

                bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                bbuff.flag = 1
                pass
                pass

            curr_recid = bill._recid
            bill = db_session.query(Bill).filter(
                     (Bill.resnr > 0) & (Bill.reslinnr > 0) & (Bill.flag == 0) & (Bill.saldo == 0) & (Bill._recid > curr_recid)).first()

        for res_line in db_session.query(Res_line).filter(
                 (Res_line.active_flag == 1) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():

            bill = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"parent_nr": [(eq, res_line.reslinnr)]})
            while None != bill:

                if bill.zinr != res_line.zinr:

                    bbuff = get_cache (Bill, {"_recid": [(eq, bill._recid)]})
                    bbuff.zinr = res_line.zinr
                    pass
                    pass

                curr_recid = bill._recid
                bill = db_session.query(Bill).filter(
                         (Bill.resnr == res_line.resnr) & (Bill.parent_nr == res_line.reslinnr) & (Bill._recid > curr_recid)).first()

    create_roomplan()
    check_co_guestbill()

    return generate_output()