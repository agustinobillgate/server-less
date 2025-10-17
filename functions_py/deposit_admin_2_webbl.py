#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 31/7/2025
# gitlab: 860
# endpoint baru: vhpFOC/depositAdmin2 
# b1_print.adult = res_line.erwach -> erwachs
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from models import Res_line, Reservation, Exrate, Waehrung, Arrangement, Zimkateg, Fixleist

def deposit_admin_2_webbl(case_type:int, depo_foreign:bool, lname:string, deposittype:int, sorttype:int, lresnr:int, fdate:date, xchange_rate:Decimal, bill_date:date, depo_curr:int, flag:int, tdate:date):

    prepare_cache ([Res_line, Reservation, Exrate, Waehrung, Arrangement, Zimkateg, Fixleist])

    total_saldo = to_decimal("0.0")
    arriv_saldo = to_decimal("0.0")
    depo_list_data = []
    b1_list_data = []
    b1_print_data = []
    grpstr:List[string] = [" ", "G"]
    res_line = reservation = exrate = waehrung = arrangement = zimkateg = fixleist = None

    b1_list = b1_print = depo_list = bresline = None

    b1_list_data, B1_list = create_model("B1_list", {"grpflag":bool, "resnr":int, "reser_name":string, "groupname":string, "resli_name":string, "ankunft":date, "limitdate":date, "depositgef":Decimal, "depositbez":Decimal, "depositbez2":Decimal, "zahldatum":date, "zahlkonto":int, "zahldatum2":date, "zahlkonto2":int, "abreise":date, "qty":int, "rmrate":Decimal, "rate_code":string, "argt_code":string, "remark":string, "stafid":string, "adult":int, "rmtype":string, "zipreis":Decimal, "rsv_status":int})
    b1_print_data, B1_print = create_model_like(B1_list)
    depo_list_data, Depo_list = create_model("Depo_list", {"group_str":string, "resnr":int, "reserve_name":string, "grpname":string, "guestname":string, "ankunft":date, "depositgef":Decimal, "limitdate":date, "bal":Decimal, "depo1":Decimal, "depositbez":Decimal, "datum1":date, "depo2":Decimal, "depositbez2":Decimal, "datum2":date, "abreise":date, "qty":int, "rmrate":Decimal, "rate_code":string, "argt_code":string, "remark":string, "stafid":string, "adult":int, "rmtype":string, "rsv_status":int})

    Bresline = create_buffer("Bresline",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal total_saldo, arriv_saldo, depo_list_data, b1_list_data, b1_print_data, grpstr, res_line, reservation, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal case_type, depo_foreign, lname, deposittype, sorttype, lresnr, fdate, xchange_rate, bill_date, depo_curr, flag, tdate
        nonlocal bresline


        nonlocal b1_list, b1_print, depo_list, bresline
        nonlocal b1_list_data, b1_print_data, depo_list_data

        return {"total_saldo": total_saldo, "arriv_saldo": arriv_saldo, "depo-list": depo_list_data, "b1-list": b1_list_data, "b1-print": b1_print_data}

    def create_itlist():

        nonlocal total_saldo, arriv_saldo, depo_list_data, b1_list_data, b1_print_data, grpstr, res_line, reservation, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal case_type, depo_foreign, lname, deposittype, sorttype, lresnr, fdate, xchange_rate, bill_date, depo_curr, flag, tdate
        nonlocal bresline


        nonlocal b1_list, b1_print, depo_list, bresline
        nonlocal b1_list_data, b1_print_data, depo_list_data

        to_name:string = ""

        if lname != "":
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if lname == "":

            if deposittype == 1:

                if sorttype == 1:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.name, Reservation.resnr).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                elif sorttype == 2:

                    if lresnr != 0:

                        reservation_obj_list = {}
                        reservation = Reservation()
                        res_line = Res_line()
                        for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate)).filter(
                                 (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr == lresnr)).order_by(Reservation.resnr, Reservation.name).all():
                            if reservation_obj_list.get(reservation._recid):
                                continue
                            else:
                                reservation_obj_list[reservation._recid] = True


                            create_it()

                    else:

                        reservation_obj_list = {}
                        reservation = Reservation()
                        res_line = Res_line()
                        for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate)).filter(
                                 (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.resnr, Reservation.name).all():
                            if reservation_obj_list.get(reservation._recid):
                                continue
                            else:
                                reservation_obj_list[reservation._recid] = True


                            create_it()


                elif sorttype == 3:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                elif sorttype == 4:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.limitdate >= fdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                elif sorttype == 5:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


            elif deposittype == 2:

                if sorttype == 1:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.name, Reservation.resnr).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                if sorttype == 2:

                    if lresnr != 0:

                        reservation_obj_list = {}
                        reservation = Reservation()
                        res_line = Res_line()
                        for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                                 (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr == lresnr)).order_by(Reservation.resnr, Reservation.name).all():
                            if reservation_obj_list.get(reservation._recid):
                                continue
                            else:
                                reservation_obj_list[reservation._recid] = True


                            create_it()

                    else:

                        reservation_obj_list = {}
                        reservation = Reservation()
                        res_line = Res_line()
                        for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                                 (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.resnr, Reservation.name).all():
                            if reservation_obj_list.get(reservation._recid):
                                continue
                            else:
                                reservation_obj_list[reservation._recid] = True


                            create_it()


                elif sorttype == 3:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate)).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                elif sorttype == 4:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.limitdate >= fdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                elif sorttype == 5:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate)).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


            elif deposittype == 3:

                reservation_obj_list = {}
                reservation = Reservation()
                res_line = Res_line()
                for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate)).filter(
                         (Reservation.activeflag <= 1) & (Reservation.depositgef == 0) & (Reservation.resnr >= lresnr)).order_by(Res_line.ankunft).all():
                    if reservation_obj_list.get(reservation._recid):
                        continue
                    else:
                        reservation_obj_list[reservation._recid] = True


                    create_it()

        elif lname != "":

            if deposittype == 1:

                if sorttype <= 2:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr)).order_by(Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 3:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 4:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr) & (Reservation.limitdate >= fdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.limitdate >= fdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 5:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

            elif deposittype == 2:

                if sorttype <= 2:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr)).order_by(Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 3:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate)).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 4:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr) & (Reservation.limitdate >= fdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.limitdate >= fdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 5:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate)).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

            elif deposittype == 3:

                reservation_obj_list = {}
                reservation = Reservation()
                res_line = Res_line()
                for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                         (Reservation.activeflag <= 1) & (Reservation.depositgef == 0) & (Reservation.resnr >= lresnr)).order_by(Res_line.ankunft).all():
                    if reservation_obj_list.get(reservation._recid):
                        continue
                    else:
                        reservation_obj_list[reservation._recid] = True


                    create_it()
        total_saldo =  to_decimal("0")
        arriv_saldo =  to_decimal("0")

        if case_type == 1:

            if depo_foreign:

                for depo_list in query(depo_list_data):
                    total_saldo =  to_decimal(total_saldo) + to_decimal(depo_list.depositgef) - to_decimal(depo_list.depositbez) - to_decimal(depo_list.depositbez2)

                    res_line = get_cache (Res_line, {"resnr": [(eq, depo_list.resnr)],"active_flag": [(eq, 1)]})

                    if not res_line:
                        arriv_saldo =  to_decimal(arriv_saldo) + to_decimal(depo_list.depositbez) + to_decimal(depo_list.depositbez2)
                total_saldo =  to_decimal(total_saldo)
                arriv_saldo =  to_decimal(arriv_saldo)


            else:

                for b1_list in query(b1_list_data):
                    total_saldo =  to_decimal(total_saldo) + to_decimal(b1_list.depositgef) - to_decimal(b1_list.depositbez) - to_decimal(b1_list.depositbez2)

                    res_line = get_cache (Res_line, {"resnr": [(eq, b1_list.resnr)],"active_flag": [(eq, 1)]})

                    if not res_line:
                        arriv_saldo =  to_decimal(arriv_saldo) + to_decimal(b1_list.depositbez) + to_decimal(b1_list.depositbez2)
                total_saldo =  to_decimal(total_saldo) * to_decimal(xchange_rate)
                arriv_saldo =  to_decimal(arriv_saldo) * to_decimal(xchange_rate)

        elif case_type == 2:

            for b1_print in query(b1_print_data):
                total_saldo =  to_decimal(total_saldo) + to_decimal(b1_print.depositgef) - to_decimal(b1_print.depositbez) - to_decimal(b1_print.depositbez2)

                res_line = get_cache (Res_line, {"resnr": [(eq, b1_print.resnr)],"active_flag": [(eq, 1)]})

                if not res_line:
                    arriv_saldo =  to_decimal(arriv_saldo) + to_decimal(b1_print.depositbez) + to_decimal(b1_print.depositbez2)
            total_saldo =  to_decimal(total_saldo) * to_decimal(xchange_rate)
            arriv_saldo =  to_decimal(arriv_saldo) * to_decimal(xchange_rate)


    def create_itlist2():

        nonlocal total_saldo, arriv_saldo, depo_list_data, b1_list_data, b1_print_data, grpstr, res_line, reservation, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal case_type, depo_foreign, lname, deposittype, sorttype, lresnr, fdate, xchange_rate, bill_date, depo_curr, flag, tdate
        nonlocal bresline


        nonlocal b1_list, b1_print, depo_list, bresline
        nonlocal b1_list_data, b1_print_data, depo_list_data

        to_name:string = ""

        if lname != "":
            to_name = chr_unicode(asc(substring(lname, 0, 1)) + 1)

        if lname == "":

            if deposittype == 1:

                if sorttype == 1:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.name, Reservation.resnr).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                elif sorttype == 2:

                    if lresnr != 0:

                        reservation_obj_list = {}
                        reservation = Reservation()
                        res_line = Res_line()
                        for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                                 (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr == lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.resnr, Reservation.name).all():
                            if reservation_obj_list.get(reservation._recid):
                                continue
                            else:
                                reservation_obj_list[reservation._recid] = True


                            create_it()

                    else:

                        reservation_obj_list = {}
                        reservation = Reservation()
                        res_line = Res_line()
                        for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                                 (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.resnr, Reservation.name).all():
                            if reservation_obj_list.get(reservation._recid):
                                continue
                            else:
                                reservation_obj_list[reservation._recid] = True


                            create_it()


                elif sorttype == 3:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                elif sorttype == 4:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None) & (Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                elif sorttype == 5:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


            elif deposittype == 2:

                if sorttype == 1:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.name, Reservation.resnr).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                if sorttype == 2:

                    if lresnr != 0:

                        reservation_obj_list = {}
                        reservation = Reservation()
                        res_line = Res_line()
                        for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                                 (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr == lresnr)).order_by(Reservation.resnr, Reservation.name).all():
                            if reservation_obj_list.get(reservation._recid):
                                continue
                            else:
                                reservation_obj_list[reservation._recid] = True


                            create_it()

                    else:

                        reservation_obj_list = {}
                        reservation = Reservation()
                        res_line = Res_line()
                        for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                                 (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.resnr, Reservation.name).all():
                            if reservation_obj_list.get(reservation._recid):
                                continue
                            else:
                                reservation_obj_list[reservation._recid] = True


                            create_it()


                elif sorttype == 3:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                elif sorttype == 4:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None) & (Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)).order_by(Reservation.limitdate).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


                elif sorttype == 5:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()


            elif deposittype == 3:

                reservation_obj_list = {}
                reservation = Reservation()
                res_line = Res_line()
                for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate)).filter(
                         (Reservation.activeflag <= 1) & (Reservation.depositgef == 0) & (Reservation.resnr >= lresnr)).order_by(Res_line.ankunft).all():
                    if reservation_obj_list.get(reservation._recid):
                        continue
                    else:
                        reservation_obj_list[reservation._recid] = True


                    create_it()

        elif lname != "":

            if deposittype == 1:

                if sorttype <= 2:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (matches(Res_line.name,("*" + lname + "*"))) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 3:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (matches(Res_line.name,("*" + lname + "*"))) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 4:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None) & (Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None) & (Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 5:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & (matches(Res_line.name,("*" + lname + "*"))) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag == 0) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

            elif deposittype == 2:

                if sorttype <= 2:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr)).order_by(Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr)).order_by(Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 3:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (matches(Res_line.name,("*" + lname + "*"))) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Res_line.ankunft).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 4:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None) & (Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None) & (Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)).order_by(Reservation.limitdate, Reservation.name).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                elif sorttype == 5:

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (matches(Reservation.name,("*" + lname + "*"))) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

                    reservation_obj_list = {}
                    reservation = Reservation()
                    res_line = Res_line()
                    for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (matches(Res_line.name,("*" + lname + "*"))) & (Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate)).filter(
                             (Reservation.activeflag <= 1) & (Reservation.depositgef != 0) & (Reservation.depositbez != 0) & (Reservation.resnr >= lresnr) & (Reservation.zahldatum != None)).order_by(Reservation.zahldatum).all():
                        if reservation_obj_list.get(reservation._recid):
                            continue
                        else:
                            reservation_obj_list[reservation._recid] = True


                        create_it()

            elif deposittype == 3:

                reservation_obj_list = {}
                reservation = Reservation()
                res_line = Res_line()
                for reservation.resnr, reservation.grpflag, reservation.name, reservation.groupname, reservation.depositgef, reservation.depositbez, reservation.depositbez2, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.zahlkonto, reservation.zahlkonto2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.zimmeranz, res_line.zipreis, res_line.erwachs, res_line.resstatus, res_line.arrangement, res_line.zimmer_wunsch, res_line.zikatnr, res_line.resnr, res_line.reslinnr, res_line._recid in db_session.query(Reservation.resnr, Reservation.grpflag, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.depositbez, Reservation.depositbez2, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.zahlkonto, Reservation.zahlkonto2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.zimmeranz, Res_line.zipreis, Res_line.erwachs, Res_line.resstatus, Res_line.arrangement, Res_line.zimmer_wunsch, Res_line.zikatnr, Res_line.resnr, Res_line.reslinnr, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & ((Res_line.resstatus <= 5) | (Res_line.resstatus == 9) | (Res_line.resstatus == 10)) & (Res_line.ankunft >= fdate) & (matches(Res_line.name,("*" + lname + "*")))).filter(
                         (Reservation.activeflag <= 1) & (Reservation.depositgef == 0) & (Reservation.resnr >= lresnr)).order_by(Res_line.ankunft).all():
                    if reservation_obj_list.get(reservation._recid):
                        continue
                    else:
                        reservation_obj_list[reservation._recid] = True


                    create_it()
        total_saldo =  to_decimal("0")
        arriv_saldo =  to_decimal("0")

        if case_type == 1:

            if depo_foreign:

                for depo_list in query(depo_list_data):
                    total_saldo =  to_decimal(total_saldo) + to_decimal(depo_list.depositgef) - to_decimal(depo_list.depositbez) - to_decimal(depo_list.depositbez2)

                    res_line = get_cache (Res_line, {"resnr": [(eq, depo_list.resnr)],"active_flag": [(eq, 1)]})

                    if not res_line:
                        arriv_saldo =  to_decimal(arriv_saldo) + to_decimal(depo_list.depositbez) + to_decimal(depo_list.depositbez2)
                total_saldo =  to_decimal(total_saldo)
                arriv_saldo =  to_decimal(arriv_saldo)


            else:

                for b1_list in query(b1_list_data):
                    total_saldo =  to_decimal(total_saldo) + to_decimal(b1_list.depositgef) - to_decimal(b1_list.depositbez) - to_decimal(b1_list.depositbez2)

                    res_line = get_cache (Res_line, {"resnr": [(eq, b1_list.resnr)],"active_flag": [(eq, 1)]})

                    if not res_line:
                        arriv_saldo =  to_decimal(arriv_saldo) + to_decimal(b1_list.depositbez) + to_decimal(b1_list.depositbez2)
                total_saldo =  to_decimal(total_saldo) * to_decimal(xchange_rate)
                arriv_saldo =  to_decimal(arriv_saldo) * to_decimal(xchange_rate)

        elif case_type == 2:

            for b1_print in query(b1_print_data):
                total_saldo =  to_decimal(total_saldo) + to_decimal(b1_print.depositgef) - to_decimal(b1_print.depositbez) - to_decimal(b1_print.depositbez2)

                res_line = get_cache (Res_line, {"resnr": [(eq, b1_print.resnr)],"active_flag": [(eq, 1)]})

                if not res_line:
                    arriv_saldo =  to_decimal(arriv_saldo) + to_decimal(b1_print.depositbez) + to_decimal(b1_print.depositbez2)
            total_saldo =  to_decimal(total_saldo) * to_decimal(xchange_rate)
            arriv_saldo =  to_decimal(arriv_saldo) * to_decimal(xchange_rate)


    def create_it():

        nonlocal total_saldo, arriv_saldo, depo_list_data, b1_list_data, b1_print_data, grpstr, res_line, reservation, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal case_type, depo_foreign, lname, deposittype, sorttype, lresnr, fdate, xchange_rate, bill_date, depo_curr, flag, tdate
        nonlocal bresline


        nonlocal b1_list, b1_print, depo_list, bresline
        nonlocal b1_list_data, b1_print_data, depo_list_data

        if case_type == 1:

            if depo_foreign:
                create_depo()
            else:
                create_b1()
        else:
            create_b1_print()


    def create_depo():

        nonlocal total_saldo, arriv_saldo, depo_list_data, b1_list_data, b1_print_data, grpstr, res_line, reservation, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal case_type, depo_foreign, lname, deposittype, sorttype, lresnr, fdate, xchange_rate, bill_date, depo_curr, flag, tdate
        nonlocal bresline


        nonlocal b1_list, b1_print, depo_list, bresline
        nonlocal b1_list_data, b1_print_data, depo_list_data

        found_it:bool = True
        exchg_rate:Decimal = to_decimal("0.0")
        exchg_rate1:Decimal = to_decimal("0.0")
        loopi:int = 0
        str:string = ""

        depo_list = query(depo_list_data, filters=(lambda depo_list: depo_list.resnr == reservation.resnr), first=True)

        if depo_list:

            return
        depo_list = Depo_list()
        depo_list_data.append(depo_list)

        depo_list.group_str = grpstr[to_int(reservation.grpflag) + 1 - 1]
        depo_list.resnr = reservation.resnr
        depo_list.reserve_name = reservation.name
        depo_list.grpname = reservation.groupname
        depo_list.guestname = res_line.name
        depo_list.ankunft = res_line.ankunft
        depo_list.depositgef =  to_decimal(reservation.depositgef)
        depo_list.bal =  to_decimal(reservation.depositgef) - to_decimal(reservation.depositbez) - to_decimal(reservation.depositbez2)
        depo_list.limitdate = reservation.limitdate
        depo_list.datum1 = reservation.zahldatum
        depo_list.datum2 = reservation.zahldatum2
        depo_list.depositbez =  to_decimal(reservation.depositbez)
        depo_list.depositbez2 =  to_decimal(reservation.depositbez2)

        if depo_list.datum1 < bill_date and depo_list.datum1 != None:

            exrate = get_cache (Exrate, {"artnr": [(eq, depo_curr)],"datum": [(eq, depo_list.datum1)]})

            if exrate:
                exchg_rate =  to_decimal(exrate.betrag)
            else:
                found_it = False

        elif (depo_list.datum1 >= bill_date and depo_list.datum1 != None) or not found_it:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, depo_curr)]})

            if waehrung:
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        if exchg_rate == 0:
            exchg_rate =  to_decimal("1")
        depo_list.depo1 =  to_decimal(reservation.depositbez) * to_decimal(exchg_rate)
        found_it = True

        if depo_list.datum2 < bill_date and depo_list.datum2 != None:

            exrate = get_cache (Exrate, {"artnr": [(eq, depo_curr)],"datum": [(eq, depo_list.datum2)]})

            if exrate:
                exchg_rate =  to_decimal(exrate.betrag)
            else:
                found_it = False

        elif (depo_list.datum2 >= bill_date and depo_list.datum2 != None) or not found_it:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, depo_curr)]})

            if waehrung:
                exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)

        if exchg_rate == 0:
            exchg_rate =  to_decimal("1")
        depo_list.depo2 =  to_decimal(reservation.depositbez2) * to_decimal(exchg_rate)
        found_it = True
        depo_list.abreise = res_line.abreise
        depo_list.qty = res_line.zimmeranz
        depo_list.rmrate =  to_decimal(res_line.zipreis)
        depo_list.remark = " "
        depo_list.stafid = " "
        # Rd 15/8/2025
        # depo_list.adult = res_line.erwach
        depo_list.adult = res_line.erwachs
        depo_list.rsv_status = res_line.resstatus

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if arrangement:
            depo_list.argt_code = arrangement.argt_bez
        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == ("$CODE$").lower() :
                depo_list.rate_code = substring(str, 6)
                return

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            depo_list.rmtype = zimkateg.bezeichnung


    def create_b1():

        nonlocal total_saldo, arriv_saldo, depo_list_data, b1_list_data, b1_print_data, grpstr, res_line, reservation, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal case_type, depo_foreign, lname, deposittype, sorttype, lresnr, fdate, xchange_rate, bill_date, depo_curr, flag, tdate
        nonlocal bresline


        nonlocal b1_list, b1_print, depo_list, bresline
        nonlocal b1_list_data, b1_print_data, depo_list_data

        loopi:int = 0
        str:string = ""
        datum:date = None
        post_it:bool = False

        b1_list = query(b1_list_data, filters=(lambda b1_list: b1_list.resnr == reservation.resnr), first=True)

        if b1_list:

            return
        b1_list = B1_list()
        b1_list_data.append(b1_list)

        b1_list.grpflag = reservation.grpflag
        b1_list.resnr = reservation.resnr
        b1_list.reser_name = reservation.name
        b1_list.groupname = reservation.groupname
        b1_list.resli_name = res_line.name
        b1_list.ankunft = res_line.ankunft
        b1_list.limitdate = reservation.limitdate
        b1_list.depositgef =  to_decimal(reservation.depositgef)
        b1_list.depositbez =  to_decimal(reservation.depositbez)
        b1_list.depositbez2 =  to_decimal(reservation.depositbez2)
        b1_list.zahldatum = reservation.zahldatum
        b1_list.zahlkonto = reservation.zahlkonto
        b1_list.zahldatum2 = reservation.zahldatum2
        b1_list.zahlkonto2 = reservation.zahlkonto2
        b1_list.abreise = res_line.abreise
        b1_list.qty = res_line.zimmeranz
        b1_list.rmrate =  to_decimal(res_line.zipreis)
        b1_list.remark = " "
        b1_list.stafid = " "
        # Rd 15/8/2025
        # b1_list.adult = res_line.erwach
        b1_list.adult = res_line.erwachs
        b1_list.zipreis =  to_decimal(res_line.zipreis)
        b1_list.rsv_status = res_line.resstatus

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if arrangement:
            b1_list.argt_code = arrangement.argt_bez
        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == ("$CODE$").lower() :
                b1_list.rate_code = substring(str, 6)
                return

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            b1_list.rmtype = zimkateg.bezeichnung

        # Rd, 31/7/2025
        # date timedelta
        # for datum in date_range(res_line.ankunft,res_line.abreise - timedelta(days=1)) :
        tmpdate = res_line.abreise - timedelta(days=1)
        for datum in date_range(res_line.ankunft, tmpdate) :

            for fixleist in db_session.query(Fixleist).filter(
                     (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                post_it = check_fixleist_posted(datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                if post_it:
                    b1_list.zipreis =  to_decimal(b1_list.zipreis) + to_decimal((fixleist.betrag) * to_decimal(fixleist.number))


    def create_b1_print():

        nonlocal total_saldo, arriv_saldo, depo_list_data, b1_list_data, b1_print_data, grpstr, res_line, reservation, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal case_type, depo_foreign, lname, deposittype, sorttype, lresnr, fdate, xchange_rate, bill_date, depo_curr, flag, tdate
        nonlocal bresline


        nonlocal b1_list, b1_print, depo_list, bresline
        nonlocal b1_list_data, b1_print_data, depo_list_data

        loopi:int = 0
        str:string = ""
        datum:date = None
        post_it:bool = False

        b1_print = query(b1_print_data, filters=(lambda b1_print: b1_print.resnr == reservation.resnr), first=True)

        if b1_print:

            return
        b1_print = B1_print()
        b1_print_data.append(b1_print)

        b1_print.grpflag = reservation.grpflag
        b1_print.resnr = reservation.resnr
        b1_print.reser_name = reservation.name
        b1_print.groupname = reservation.groupname
        b1_print.resli_name = res_line.name
        b1_print.ankunft = res_line.ankunft
        b1_print.limitdate = reservation.limitdate
        b1_print.depositgef =  to_decimal(reservation.depositgef)
        b1_print.depositbez =  to_decimal(reservation.depositbez)
        b1_print.depositbez2 =  to_decimal(reservation.depositbez2)
        b1_print.zahldatum = reservation.zahldatum
        b1_print.zahlkonto = reservation.zahlkonto
        b1_print.zahldatum2 = reservation.zahldatum2
        b1_print.zahlkonto2 = reservation.zahlkonto2
        b1_print.abreise = res_line.abreise
        b1_print.qty = res_line.zimmeranz
        b1_print.rmrate =  to_decimal(res_line.zipreis)
        b1_print.remark = " "
        b1_print.stafid = " "
        # Rd, 31/7/2025
        # b1_print.adult = res_line.erwach
        b1_print.adult = res_line.erwachs

        b1_print.zipreis =  to_decimal(res_line.zipreis)
        b1_print.rsv_status = res_line.resstatus

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if arrangement:
            b1_print.argt_code = arrangement.argt_bez
        for loopi in range(1,num_entries(res_line.zimmer_wunsch, ";") - 1 + 1) :
            str = entry(loopi - 1, res_line.zimmer_wunsch, ";")

            if substring(str, 0, 6) == ("$CODE$").lower() :
                b1_print.rate_code = substring(str, 6)
                return

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            b1_print.rmtype = zimkateg.bezeichnung

        # Rd, 31/7/2025
        # date timedelta
        # for datum in date_range(res_line.ankunft,res_line.abreise - timedelta(days=1)) :
        tmpdate = res_line.abreise - timedelta(days=1)
        for datum in date_range(res_line.ankunft, tmpdate ) :

            for fixleist in db_session.query(Fixleist).filter(
                     (Fixleist.resnr == res_line.resnr) & (Fixleist.reslinnr == res_line.reslinnr)).order_by(Fixleist._recid).all():
                post_it = check_fixleist_posted(datum, fixleist.artnr, fixleist.departement, fixleist.sequenz, fixleist.dekade, fixleist.lfakt)

                if post_it:
                    b1_print.zipreis =  to_decimal(b1_print.zipreis) + to_decimal(fixleist.betrag)


    def check_fixleist_posted(curr_date:date, artnr:int, dept:int, fakt_modus:int, intervall:int, lfakt:date):

        nonlocal total_saldo, arriv_saldo, depo_list_data, b1_list_data, b1_print_data, grpstr, res_line, reservation, exrate, waehrung, arrangement, zimkateg, fixleist
        nonlocal case_type, depo_foreign, lname, deposittype, sorttype, lresnr, fdate, xchange_rate, bill_date, depo_curr, flag, tdate
        nonlocal bresline


        nonlocal b1_list, b1_print, depo_list, bresline
        nonlocal b1_list_data, b1_print_data, depo_list_data

        post_it = False
        delta:int = 0
        start_date:date = None

        def generate_inner_output():
            return (post_it)


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
                delta = (lfakt - res_line.ankunft).days

                if delta < 0:
                    delta = 0
            start_date = res_line.ankunft + timedelta(days=delta)

            if (res_line.abreise - start_date) < intervall:
                start_date = res_line.ankunft

            if curr_date <= (start_date + timedelta(days=(intervall - 1))):
                post_it = True

            if curr_date < start_date:
                post_it = False

        return generate_inner_output()


    if flag == 1:
        create_itlist()
    else:
        create_itlist2()

    return generate_output()