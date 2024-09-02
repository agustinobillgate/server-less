from functions.additional_functions import *
import decimal
from datetime import date
from models import Reservation, Res_line, Bresline, exrate, Waehrung, Arrangement, Zimkateg, Fixleist

def deposit_admin_1bl(case_type:int, depo_foreign:bool, lname:str, deposittype:int, sorttype:int, lresnr:int, fdate:date, exrate:decimal, bill_date:date, depo_curr:int):
    total_saldo = 0
    arriv_saldo = 0
    depo_list_list = []
    b1_list_list = []
    b1_print_list = []
    grpstr:str = ""
    reservation = res_line = bresline = exrate = waehrung = arrangement = zimkateg = fixleist = None

    b1_list = b1_print = depo_list = reservation = res_line = bresline = None

    b1_list_list, B1_list = create_model("B1_list", {"grpflag":bool, "resnr":int, "reser_name":str, "groupname":str, "resli_name":str, "ankunft":date, "limitdate":date, "depositgef":decimal, "depositbez":decimal, "depositbez2":decimal, "zahldatum":date, "zahlkonto":int, "zahldatum2":date, "zahlkonto2":int, "abreise":date, "qty":int, "rmrate":decimal, "rate_code":str, "argt_code":str, "remark":str, "stafid":str, "adult":int, "rmtype":str, "zipreis":decimal, "rsv_status":int})
    b1_print_list, B1_print = create_model_like(B1_list)
    depo_list_list, Depo_list = create_model("Depo_list", {"group_str":str, "resnr":int, "reserve_name":str, "grpname":str, "guestname":str, "ankunft":date, "depositgef":decimal, "limitdate":date, "bal":decimal, "depo1":decimal, "depositbez":decimal, "datum1":date, "depo2":decimal, "depositbez2":decimal, "datum2":date, "abreise":date, "qty":int, "rmrate":decimal, "rate_code":str, "argt_code":str, "remark":str, "stafid":str, "adult":int, "rmtype":str, "rsv_status":int})

    Reservation = Reservation
    Res_line = Res_line
    Bresline = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal total_saldo, arriv_saldo, depo_list_list, b1_list_list, b1_print_list, grpstr, reservation, res_line, bresline, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal reservation, res_line, bresline


        nonlocal b1_list, b1_print, depo_list, reservation, res_line, bresline
        nonlocal b1_list_list, b1_print_list, depo_list_list
        return {"total_saldo": total_saldo, "arriv_saldo": arriv_saldo, "depo-list": depo_list_list, "b1-list": b1_list_list, "b1-print": b1_print_list}

    def create_itlist():

        nonlocal total_saldo, arriv_saldo, depo_list_list, b1_list_list, b1_print_list, grpstr, reservation, res_line, bresline, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal reservation, res_line, bresline


        nonlocal b1_list, b1_print, depo_list, reservation, res_line, bresline
        nonlocal b1_list_list, b1_print_list, depo_list_list

        to_name:str = ""

        if lname != "":
            to_name = chr(ord(substring(lname, 0, 1)) + 1)

        if lname == "":

            if deposittype == 1:

                if sorttype == 1:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8) &  (Res_line.ankunft >= fdate)).filter(
                            (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        create_it()


                elif sorttype == 2:

                    if lresnr != 0:

                        reservation_obj_list = []
                        for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8) &  (Res_line.ankunft >= fdate)).filter(
                                (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.resnr == lresnr)).all():
                            if reservation._recid in reservation_obj_list:
                                continue
                            else:
                                reservation_obj_list.append(reservation._recid)


                            create_it()

                    else:

                        reservation_obj_list = []
                        for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8) &  (Res_line.ankunft >= fdate)).filter(
                                (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.resnr >= lresnr)).all():
                            if reservation._recid in reservation_obj_list:
                                continue
                            else:
                                reservation_obj_list.append(reservation._recid)


                            create_it()


                elif sorttype == 3:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8) &  (Res_line.ankunft >= fdate)).filter(
                            (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        create_it()


                elif sorttype == 4:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8)).filter(
                            (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.resnr >= lresnr) &  (Reservation.limitdate >= fdate)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        create_it()


            elif deposittype == 2:

                if sorttype == 1:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10))).filter(
                            (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.depositbez != 0) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)

                        bresline = db_session.query(Bresline).filter(
                                (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                        if not bresline:
                            create_it()


                if sorttype == 2:

                    if lresnr != 0:

                        reservation_obj_list = []
                        for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10))).filter(
                                (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.depositbez != 0) &  (Reservation.resnr == lresnr)).all():
                            if reservation._recid in reservation_obj_list:
                                continue
                            else:
                                reservation_obj_list.append(reservation._recid)

                            bresline = db_session.query(Bresline).filter(
                                    (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                            if not bresline:
                                create_it()

                    else:

                        reservation_obj_list = []
                        for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10))).filter(
                                (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.depositbez != 0) &  (Reservation.resnr >= lresnr)).all():
                            if reservation._recid in reservation_obj_list:
                                continue
                            else:
                                reservation_obj_list.append(reservation._recid)

                            bresline = db_session.query(Bresline).filter(
                                    (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                            if not bresline:
                                create_it()


                elif sorttype == 3:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (Res_line.ankunft >= fdate)).filter(
                            (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.depositbez != 0) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)

                        bresline = db_session.query(Bresline).filter(
                                (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                        if not bresline:
                            create_it()


                elif sorttype == 4:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10))).filter(
                            (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.resnr >= lresnr) &  (Reservation.limitdate >= fdate)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)

                        bresline = db_session.query(Bresline).filter(
                                (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                        if not bresline:
                            create_it()


            elif deposittype == 3:

                reservation_obj_list = []
                for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (Res_line.ankunft >= fdate)).filter(
                        (Reservation.activeflag <= 1) &  (Reservation.depositgef == 0) &  (Reservation.resnr >= lresnr)).all():
                    if reservation._recid in reservation_obj_list:
                        continue
                    else:
                        reservation_obj_list.append(reservation._recid)


                    create_it()

        elif lname != "":

            if deposittype == 1:

                if sorttype <= 2:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8) &  (Res_line.ankunft >= fdate)).filter(
                            (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.name.op("~")(".*" + lname + ".*")) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        create_it()

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8) &  (Res_line.ankunft >= fdate) &  (Res_line.name.op("~")(".*" + lname + ".*"))).filter(
                            (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        create_it()

                elif sorttype == 3:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8) &  (Res_line.ankunft >= fdate)).filter(
                            (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.name.op("~")(".*" + lname + ".*")) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        create_it()

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8) &  (Res_line.ankunft >= fdate) &  (Res_line.name.op("~")(".*" + lname + ".*"))).filter(
                            (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        create_it()

                elif sorttype == 4:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8)).filter(
                            (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.name.op("~")(".*" + lname + ".*")) &  (Reservation.resnr >= lresnr) &  (Reservation.limitdate >= fdate)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        create_it()

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  (Res_line.resstatus <= 8) &  (Res_line.name.op("~")(".*" + lname + ".*"))).filter(
                            (Reservation.activeflag == 0) &  (Reservation.depositgef != 0) &  (Reservation.resnr >= lresnr) &  (Reservation.limitdate >= fdate)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)


                        create_it()

            elif deposittype == 2:

                if sorttype <= 2:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10))).filter(
                            (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.depositbez != 0) &  (Reservation.name.op("~")(".*" + lname + ".*")) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)

                        bresline = db_session.query(Bresline).filter(
                                (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                        if not bresline:
                            create_it()

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (Res_line.name.op("~")(".*" + lname + ".*"))).filter(
                            (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.depositbez != 0) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)

                        bresline = db_session.query(Bresline).filter(
                                (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                        if not bresline:
                            create_it()

                elif sorttype == 3:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (Res_line.ankunft >= fdate)).filter(
                            (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.depositbez != 0) &  (Reservation.name.op("~")(".*" + lname + ".*")) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)

                        bresline = db_session.query(Bresline).filter(
                                (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                        if not bresline:
                            create_it()

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (Res_line.ankunft >= fdate) &  (Res_line.name.op("~")(".*" + lname + ".*"))).filter(
                            (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.depositbez != 0) &  (Reservation.resnr >= lresnr)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)

                        bresline = db_session.query(Bresline).filter(
                                (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                        if not bresline:
                            create_it()

                elif sorttype == 4:

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10))).filter(
                            (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.name.op("~")(".*" + lname + ".*")) &  (Reservation.resnr >= lresnr) &  (Reservation.limitdate >= fdate)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)

                        bresline = db_session.query(Bresline).filter(
                                (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                        if not bresline:
                            create_it()

                    reservation_obj_list = []
                    for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (Res_line.name.op("~")(".*" + lname + ".*"))).filter(
                            (Reservation.activeflag <= 1) &  (Reservation.depositgef != 0) &  (Reservation.resnr >= lresnr) &  (Reservation.limitdate >= fdate)).all():
                        if reservation._recid in reservation_obj_list:
                            continue
                        else:
                            reservation_obj_list.append(reservation._recid)

                        bresline = db_session.query(Bresline).filter(
                                (Bresline.resnr == res_line.resnr) &  (Bresline.reslinnr != res_line.reslinnr) &  ((Bresline.resstatus != 9) |  (Bresline.resstatus != 10))).first()

                        if not bresline:
                            create_it()

            elif deposittype == 3:

                reservation_obj_list = []
                for reservation, res_line in db_session.query(Reservation, Res_line).join(Res_line,(Res_line.resnr == Reservation.resnr) &  ((Res_line.resstatus <= 5) |  (Res_line.resstatus == 9) |  (Res_line.resstatus == 10)) &  (Res_line.ankunft >= fdate) &  (Res_line.name.op("~")(".*" + lname + ".*"))).filter(
                        (Reservation.activeflag <= 1) &  (Reservation.depositgef == 0) &  (Reservation.resnr >= lresnr)).all():
                    if reservation._recid in reservation_obj_list:
                        continue
                    else:
                        reservation_obj_list.append(reservation._recid)


                    create_it()
        total_saldo = 0
        arriv_saldo = 0

        if case_type == 1:

            if depo_foreign:

                for depo_list in query(depo_list_list):
                    total_saldo = total_saldo + depo_list.depositgef - depo_list.depositbez - depo_list.depositbez2

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == depo_list.resnr) &  (Res_line.active_flag == 1)).first()

                    if not res_line:
                        arriv_saldo = arriv_saldo + depo_list.depositbez + depo_list.depositbez2
                total_saldo = total_saldo
                arriv_saldo = arriv_saldo


            else:

                for b1_list in query(b1_list_list):
                    total_saldo = total_saldo + b1_list.depositgef - b1_list.depositbez - b1_list.depositbez2

                    res_line = db_session.query(Res_line).filter(
                            (Res_line.resnr == b1_list.resnr) &  (Res_line.active_flag == 1)).first()

                    if not res_line:
                        arriv_saldo = arriv_saldo + b1_list.depositbez + b1_list.depositbez2
                total_saldo = total_saldo * exrate
                arriv_saldo = arriv_saldo * exrate

        elif case_type == 2:

            for b1_print in query(b1_print_list):
                total_saldo = total_saldo + b1_print.depositgef - b1_print.depositbez - b1_print.depositbez2

                res_line = db_session.query(Res_line).filter(
                        (Res_line.resnr == b1_print.resnr) &  (Res_line.active_flag == 1)).first()

                if not res_line:
                    arriv_saldo = arriv_saldo + b1_print.depositbez + b1_print.depositbez2
            total_saldo = total_saldo * exrate
            arriv_saldo = arriv_saldo * exrate

    def create_it():

        nonlocal total_saldo, arriv_saldo, depo_list_list, b1_list_list, b1_print_list, grpstr, reservation, res_line, bresline, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal reservation, res_line, bresline


        nonlocal b1_list, b1_print, depo_list, reservation, res_line, bresline
        nonlocal b1_list_list, b1_print_list, depo_list_list

        if case_type == 1:

            if depo_foreign:
                create_depo()
            else:
                create_b1()
        else:
            create_b1_print()

    def create_depo():

        nonlocal total_saldo, arriv_saldo, depo_list_list, b1_list_list, b1_print_list, grpstr, reservation, res_line, bresline, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal reservation, res_line, bresline


        nonlocal b1_list, b1_print, depo_list, reservation, res_line, bresline
        nonlocal b1_list_list, b1_print_list, depo_list_list

        found_it:bool = True
        exchg_rate:decimal = 0
        exchg_rate1:decimal = 0
        loopi:int = 0
        str:str = ""

        depo_list = query(depo_list_list, filters=(lambda depo_list :depo_list.resnr == reservation.resnr), first=True)

        if depo_list:

            return
        depo_list = Depo_list()
        depo_list_list.append(depo_list)

        depo_list.group_str = grpstr[to_int(reservation.grpflag) + 1 - 1]
        depo_list.resnr = reservation.resnr
        depo_list.reserve_name = reservation.name
        depo_list.grpname = reservation.groupname
        depo_list.guestname = res_line.name
        depo_list.ankunft = res_line.ankunft
        depo_list.depositgef = reservation.depositgef
        depo_list.bal = reservation.depositgef - reservation.depositbez - reservation.depositbez2
        depo_list.limitdate = reservation.limitdate
        depo_list.datum1 = reservation.zahldatum
        depo_list.datum2 = reservation.zahldatum2
        depo_list.depositbez = reservation.depositbez
        depo_list.depositbez2 = reservation.depositbez2

        if depo_list.datum1 < bill_date and depo_list.datum1 != None:

            exrate = db_session.query(exrate).filter(
                    (exrate.artnr == depo_curr) &  (exrate.datum == depo_list.datum1)).first()

            if exrate:
                exchg_rate = exrate.betrag
            else:
                found_it = False

        elif (depo_list.datum1 >= bill_date and depo_list.datum1 != None) or not found_it:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == depo_curr)).first()

            if waehrung:
                exchg_rate = waehrung.ankauf / waehrung.einheit

        if exchg_rate == 0:
            exchg_rate = 1
        depo_list.depo1 = reservation.depositbez * exchg_rate
        found_it = True

        if depo_list.datum2 < bill_date and depo_list.datum2 != None:

            exrate = db_session.query(exrate).filter(
                    (exrate.artnr == depo_curr) &  (exrate.datum == depo_list.datum2)).first()

            if exrate:
                exchg_rate = exrate.betrag
            else:
                found_it = False

        elif (depo_list.datum2 >= bill_date and depo_list.datum2 != None) or not found_it:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == depo_curr)).first()

            if waehrung:
                exchg_rate = waehrung.ankauf / waehrung.einheit

        if exchg_rate == 0:
            exchg_rate = 1
        depo_list.depo2 = reservation.depositbez2 * exchg_rate
        found_it = True
        depo_list.abreise = res_line.abreise
        depo_list.qty = res_line.zimmeranz
        depo_list.rmrate = res_line.zipreis
        depo_list.remark = " "
        depo_list.stafid = " "
        depo_list.adult = res_line.erwach
        depo_list.rsv_status = res_line.resstatus

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == res_line.arrangement)).first()

        if arrangement:
            depo_list.argt_code = arrangement.argt_bez
        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == "$CODE$":
                depo_list.rate_code = substring(str, 6)
                return

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == res_line.zikatnr)).first()

        if zimkateg:
            depo_list.rmtype = zimkateg.bezeichnung

    def create_b1():

        nonlocal total_saldo, arriv_saldo, depo_list_list, b1_list_list, b1_print_list, grpstr, reservation, res_line, bresline, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal reservation, res_line, bresline


        nonlocal b1_list, b1_print, depo_list, reservation, res_line, bresline
        nonlocal b1_list_list, b1_print_list, depo_list_list

        loopi:int = 0
        str:str = ""
        datum:date = None
        post_it:bool = False

        b1_list = query(b1_list_list, filters=(lambda b1_list :b1_list.resnr == reservation.resnr), first=True)

        if b1_list:

            return
        b1_list = B1_list()
        b1_list_list.append(b1_list)

        b1_list.grpflag = reservation.grpflag
        b1_list.resnr = reservation.resnr
        b1_list.reser_name = reservation.name
        b1_list.groupname = reservation.groupname
        b1_list.resli_name = res_line.name
        b1_list.ankunft = res_line.ankunft
        b1_list.limitdate = reservation.limitdate
        b1_list.depositgef = reservation.depositgef
        b1_list.depositbez = reservation.depositbez
        b1_list.depositbez2 = reservation.depositbez2
        b1_list.zahldatum = reservation.zahldatum
        b1_list.zahlkonto = reservation.zahlkonto
        b1_list.zahldatum2 = reservation.zahldatum2
        b1_list.zahlkonto2 = reservation.zahlkonto2
        b1_list.abreise = res_line.abreise
        b1_list.qty = res_line.zimmeranz
        b1_list.rmrate = res_line.zipreis
        b1_list.remark = " "
        b1_list.stafid = " "
        b1_list.adult = res_line.erwach
        b1_list.zipreis = res_line.zipreis
        b1_list.rsv_status = res_line.resstatus

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == res_line.arrangement)).first()

        if arrangement:
            b1_list.argt_code = arrangement.argt_bez
        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == "$CODE$":
                b1_list.rate_code = substring(str, 6)
                return

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == res_line.zikatnr)).first()

        if zimkateg:
            b1_list.rmtype = zimkateg.bezeichnung


        for datum in range(res_line.ankunft,res_line.abreise - 1 + 1) :

            for fixleist in db_session.query(Fixleist).filter(
                    (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).all():
                post_it = check_fixleist_posted(datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                if post_it:
                    b1_list.zipreis = b1_list.zipreis + (fixleist.betrag * fixleist.number)

    def create_b1_print():

        nonlocal total_saldo, arriv_saldo, depo_list_list, b1_list_list, b1_print_list, grpstr, reservation, res_line, bresline, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal reservation, res_line, bresline


        nonlocal b1_list, b1_print, depo_list, reservation, res_line, bresline
        nonlocal b1_list_list, b1_print_list, depo_list_list

        loopi:int = 0
        str:str = ""
        datum:date = None
        post_it:bool = False

        b1_print = query(b1_print_list, filters=(lambda b1_print :b1_print.resnr == reservation.resnr), first=True)

        if b1_print:

            return
        b1_print = B1_print()
        b1_print_list.append(b1_print)

        b1_print.grpflag = reservation.grpflag
        b1_print.resnr = reservation.resnr
        b1_print.reser_name = reservation.name
        b1_print.groupname = reservation.groupname
        b1_print.resli_name = res_line.name
        b1_print.ankunft = res_line.ankunft
        b1_print.limitdate = reservation.limitdate
        b1_print.depositgef = reservation.depositgef
        b1_print.depositbez = reservation.depositbez
        b1_print.depositbez2 = reservation.depositbez2
        b1_print.zahldatum = reservation.zahldatum
        b1_print.zahlkonto = reservation.zahlkonto
        b1_print.zahldatum2 = reservation.zahldatum2
        b1_print.zahlkonto2 = reservation.zahlkonto2
        b1_print.abreise = res_line.abreise
        b1_print.qty = res_line.zimmeranz
        b1_print.rmrate = res_line.zipreis
        b1_print.remark = " "
        b1_print.stafid = " "
        b1_print.adult = res_line.erwach
        b1_print.zipreis = res_line.zipreis
        b1_print.rsv_status = res_line.resstatus

        arrangement = db_session.query(Arrangement).filter(
                (Arrangement == res_line.arrangement)).first()

        if arrangement:
            b1_print.argt_code = arrangement.argt_bez
        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == "$CODE$":
                b1_print.rate_code = substring(str, 6)
                return

        zimkateg = db_session.query(Zimkateg).filter(
                (Zimkateg.zikatnr == res_line.zikatnr)).first()

        if zimkateg:
            b1_print.rmtype = zimkateg.bezeichnung


        for datum in range(res_line.ankunft,res_line.abreise - 1 + 1) :

            for fixleist in db_session.query(Fixleist).filter(
                    (Fixleist.resnr == res_line.resnr) &  (Fixleist.reslinnr == res_line.reslinnr)).all():
                post_it = check_fixleist_posted(datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                if post_it:
                    b1_print.zipreis = b1_print.zipreis + fixleist.betrag

    def check_fixleist_posted(curr_date:date, artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal total_saldo, arriv_saldo, depo_list_list, b1_list_list, b1_print_list, grpstr, reservation, res_line, bresline, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal reservation, res_line, bresline


        nonlocal b1_list, b1_print, depo_list, reservation, res_line, bresline
        nonlocal b1_list_list, b1_print_list, depo_list_list

        post_it = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return post_it

        if fakt_modus == 1:
            post_it = True

        elif fakt_modus == 2:

            if res_line.ankunft == curr_date:
                post_it = True

        elif fakt_modus == 3:

            if (res_line.ankunft + 1) == curr_date:
                post_it = True

        elif fakt_modus == 4:

            if get_day(curr_date) == 1:
                post_it = True

        elif fakt_modus == 5:

            if get_day(curr_date + 1) == 1:
                post_it = True

        elif fakt_modus == 6:

            if lfakt == None:
                delta = 0
            else:
                delta = lfakt - res_line.ankunft

                if delta < 0:
                    delta = 0
            start_date = res_line.ankunft + delta

            if (res_line.abreise - start_date) < intervall:
                start_date = res_line.ankunft

            if curr_date <= (start_date + (intervall - 1)):
                post_it = True

            if curr_date < start_date:
                post_it = False


        return generate_inner_output()


    create_itlist()

    return generate_output()