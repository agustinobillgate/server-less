#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Artikel, Res_line, Reservation, Exrate, Waehrung

def deposit_list3_webbl(fdate:date, tdate:date, sorttype:int):

    prepare_cache ([Htparam, Artikel, Res_line, Reservation, Exrate, Waehrung])

    depo_list_list = []
    depo_foreign:bool = False
    depo_curr:int = 0
    bill_date:date = None
    exchg_rate:Decimal = to_decimal("0.0")
    found_it:bool = True
    grpstr:List[string] = [" ", "G"]
    htparam = artikel = res_line = reservation = exrate = waehrung = None

    depo_list = None

    depo_list_list, Depo_list = create_model("Depo_list", {"group_str":string, "resnr":int, "reserve_name":string, "grpname":string, "guestname":string, "ankunft":date, "depositgef":Decimal, "limitdate":date, "bal":Decimal, "depo1":Decimal, "depositbez":Decimal, "datum1":date, "depo2":Decimal, "depositbez2":Decimal, "datum2":date, "status_rsv":string, "departure":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal depo_list_list, depo_foreign, depo_curr, bill_date, exchg_rate, found_it, grpstr, htparam, artikel, res_line, reservation, exrate, waehrung
        nonlocal fdate, tdate, sorttype


        nonlocal depo_list
        nonlocal depo_list_list

        return {"depo-list": depo_list_list}

    def create_depolist1():

        nonlocal depo_list_list, depo_foreign, depo_curr, bill_date, exchg_rate, found_it, grpstr, htparam, artikel, res_line, reservation, exrate, waehrung
        nonlocal fdate, tdate, sorttype


        nonlocal depo_list
        nonlocal depo_list_list

        reservation_obj_list = {}
        reservation = Reservation()
        res_line = Res_line()
        for reservation.grpflag, reservation.resnr, reservation.name, reservation.groupname, reservation.depositgef, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.depositbez, reservation.depositbez2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line._recid in db_session.query(Reservation.grpflag, Reservation.resnr, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.depositbez, Reservation.depositbez2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & ((Res_line.abreise >= fdate) & (Res_line.abreise <= tdate))).filter(
                 (Reservation.depositgef != 0) & (((Reservation.zahldatum >= fdate) & (Reservation.zahldatum <= tdate)) | ((Reservation.zahldatum2 >= fdate) & (Reservation.zahldatum2 <= tdate)) | ((Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)))).order_by(Res_line.abreise).all():
            if reservation_obj_list.get(reservation._recid):
                continue
            else:
                reservation_obj_list[reservation._recid] = True


            depo_list = Depo_list()
            depo_list_list.append(depo_list)

            depo_list.group_str = grpstr[to_int(reservation.grpflag) + 1 - 1]
            depo_list.resnr = reservation.resnr
            depo_list.reserve_name = reservation.name
            depo_list.grpname = reservation.groupname
            depo_list.guestname = res_line.name
            depo_list.ankunft = res_line.ankunft
            depo_list.depositgef =  to_decimal(reservation.depositgef)
            depo_list.limitdate = reservation.limitdate
            depo_list.datum1 = reservation.zahldatum
            depo_list.datum2 = reservation.zahldatum2
            depo_list.departure = res_line.abreise

            if res_line.resstatus == 6:
                depo_list.status_rsv = "Checked-In"

            elif res_line.resstatus == 8:
                depo_list.status_rsv = "Checked-Out"
            else:
                depo_list.status_rsv = "Reservation"

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
            depo_list.bal =  to_decimal(depo_list.depositgef) - to_decimal(depo_list.depo1) - to_decimal(depo_list.depo2)


    def create_depolist2():

        nonlocal depo_list_list, depo_foreign, depo_curr, bill_date, exchg_rate, found_it, grpstr, htparam, artikel, res_line, reservation, exrate, waehrung
        nonlocal fdate, tdate, sorttype


        nonlocal depo_list
        nonlocal depo_list_list

        reservation_obj_list = {}
        reservation = Reservation()
        res_line = Res_line()
        for reservation.grpflag, reservation.resnr, reservation.name, reservation.groupname, reservation.depositgef, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.depositbez, reservation.depositbez2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line._recid in db_session.query(Reservation.grpflag, Reservation.resnr, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.depositbez, Reservation.depositbez2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & ((Res_line.abreise >= fdate) & (Res_line.abreise <= tdate))).filter(
                 (Reservation.depositgef != 0) & (((Reservation.zahldatum >= fdate) & (Reservation.zahldatum <= tdate)) | ((Reservation.zahldatum2 >= fdate) & (Reservation.zahldatum2 <= tdate)) | ((Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)))).order_by(Res_line.abreise).all():
            if reservation_obj_list.get(reservation._recid):
                continue
            else:
                reservation_obj_list[reservation._recid] = True


            depo_list = Depo_list()
            depo_list_list.append(depo_list)

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
            depo_list.depo1 =  to_decimal(reservation.depositbez)
            depo_list.depo2 =  to_decimal(reservation.depositbez2)
            depo_list.departure = res_line.abreise

            if res_line.resstatus == 6:
                depo_list.status_rsv = "Checked-In"

            elif res_line.resstatus == 8:
                depo_list.status_rsv = "Checked-Out"
            else:
                depo_list.status_rsv = "Reservation"


    def create_depolist_arr1():

        nonlocal depo_list_list, depo_foreign, depo_curr, bill_date, exchg_rate, found_it, grpstr, htparam, artikel, res_line, reservation, exrate, waehrung
        nonlocal fdate, tdate, sorttype


        nonlocal depo_list
        nonlocal depo_list_list

        reservation_obj_list = {}
        reservation = Reservation()
        res_line = Res_line()
        for reservation.grpflag, reservation.resnr, reservation.name, reservation.groupname, reservation.depositgef, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.depositbez, reservation.depositbez2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line._recid in db_session.query(Reservation.grpflag, Reservation.resnr, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.depositbez, Reservation.depositbez2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & ((Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate))).filter(
                 (Reservation.depositgef != 0) & (((Reservation.zahldatum >= fdate) & (Reservation.zahldatum <= tdate)) | ((Reservation.zahldatum2 >= fdate) & (Reservation.zahldatum2 <= tdate)) | ((Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)))).order_by(Res_line.ankunft).all():
            if reservation_obj_list.get(reservation._recid):
                continue
            else:
                reservation_obj_list[reservation._recid] = True


            depo_list = Depo_list()
            depo_list_list.append(depo_list)

            depo_list.group_str = grpstr[to_int(reservation.grpflag) + 1 - 1]
            depo_list.resnr = reservation.resnr
            depo_list.reserve_name = reservation.name
            depo_list.grpname = reservation.groupname
            depo_list.guestname = res_line.name
            depo_list.ankunft = res_line.ankunft
            depo_list.depositgef =  to_decimal(reservation.depositgef)
            depo_list.limitdate = reservation.limitdate
            depo_list.datum1 = reservation.zahldatum
            depo_list.datum2 = reservation.zahldatum2
            depo_list.departure = res_line.abreise

            if res_line.resstatus == 6:
                depo_list.status_rsv = "Checked-In"

            elif res_line.resstatus == 8:
                depo_list.status_rsv = "Checked-Out"
            else:
                depo_list.status_rsv = "Reservation"

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
            depo_list.bal =  to_decimal(depo_list.depositgef) - to_decimal(depo_list.depo1) - to_decimal(depo_list.depo2)


    def create_depolist_arr2():

        nonlocal depo_list_list, depo_foreign, depo_curr, bill_date, exchg_rate, found_it, grpstr, htparam, artikel, res_line, reservation, exrate, waehrung
        nonlocal fdate, tdate, sorttype


        nonlocal depo_list
        nonlocal depo_list_list

        reservation_obj_list = {}
        reservation = Reservation()
        res_line = Res_line()
        for reservation.grpflag, reservation.resnr, reservation.name, reservation.groupname, reservation.depositgef, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.depositbez, reservation.depositbez2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line._recid in db_session.query(Reservation.grpflag, Reservation.resnr, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.depositbez, Reservation.depositbez2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8) & ((Res_line.ankunft >= fdate) & (Res_line.ankunft <= tdate))).filter(
                 (Reservation.depositgef != 0) & (((Reservation.zahldatum >= fdate) & (Reservation.zahldatum <= tdate)) | ((Reservation.zahldatum2 >= fdate) & (Reservation.zahldatum2 <= tdate)) | ((Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)))).order_by(Res_line.ankunft).all():
            if reservation_obj_list.get(reservation._recid):
                continue
            else:
                reservation_obj_list[reservation._recid] = True


            depo_list = Depo_list()
            depo_list_list.append(depo_list)

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
            depo_list.depo1 =  to_decimal(reservation.depositbez)
            depo_list.depo2 =  to_decimal(reservation.depositbez2)
            depo_list.departure = res_line.abreise

            if res_line.resstatus == 6:
                depo_list.status_rsv = "Checked-In"

            elif res_line.resstatus == 8:
                depo_list.status_rsv = "Checked-Out"
            else:
                depo_list.status_rsv = "Reservation"


    def create_depolist_dep1():

        nonlocal depo_list_list, depo_foreign, depo_curr, bill_date, exchg_rate, found_it, grpstr, htparam, artikel, res_line, reservation, exrate, waehrung
        nonlocal fdate, tdate, sorttype


        nonlocal depo_list
        nonlocal depo_list_list

        reservation_obj_list = {}
        reservation = Reservation()
        res_line = Res_line()
        for reservation.grpflag, reservation.resnr, reservation.name, reservation.groupname, reservation.depositgef, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.depositbez, reservation.depositbez2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line._recid in db_session.query(Reservation.grpflag, Reservation.resnr, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.depositbez, Reservation.depositbez2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8)).filter(
                 (Reservation.depositgef != 0) & (((Reservation.zahldatum >= fdate) & (Reservation.zahldatum <= tdate)) | ((Reservation.zahldatum2 >= fdate) & (Reservation.zahldatum2 <= tdate)) | ((Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)))).order_by(Reservation.zahldatum).all():
            if reservation_obj_list.get(reservation._recid):
                continue
            else:
                reservation_obj_list[reservation._recid] = True


            depo_list = Depo_list()
            depo_list_list.append(depo_list)

            depo_list.group_str = grpstr[to_int(reservation.grpflag) + 1 - 1]
            depo_list.resnr = reservation.resnr
            depo_list.reserve_name = reservation.name
            depo_list.grpname = reservation.groupname
            depo_list.guestname = res_line.name
            depo_list.ankunft = res_line.ankunft
            depo_list.depositgef =  to_decimal(reservation.depositgef)
            depo_list.limitdate = reservation.limitdate
            depo_list.datum1 = reservation.zahldatum
            depo_list.datum2 = reservation.zahldatum2
            depo_list.departure = res_line.abreise

            if res_line.resstatus == 6:
                depo_list.status_rsv = "Checked-In"

            elif res_line.resstatus == 8:
                depo_list.status_rsv = "Checked-Out"
            else:
                depo_list.status_rsv = "Reservation"

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
            depo_list.bal =  to_decimal(depo_list.depositgef) - to_decimal(depo_list.depo1) - to_decimal(depo_list.depo2)


    def create_depolist_dep2():

        nonlocal depo_list_list, depo_foreign, depo_curr, bill_date, exchg_rate, found_it, grpstr, htparam, artikel, res_line, reservation, exrate, waehrung
        nonlocal fdate, tdate, sorttype


        nonlocal depo_list
        nonlocal depo_list_list

        reservation_obj_list = {}
        reservation = Reservation()
        res_line = Res_line()
        for reservation.grpflag, reservation.resnr, reservation.name, reservation.groupname, reservation.depositgef, reservation.limitdate, reservation.zahldatum, reservation.zahldatum2, reservation.depositbez, reservation.depositbez2, reservation._recid, res_line.name, res_line.ankunft, res_line.abreise, res_line.resstatus, res_line._recid in db_session.query(Reservation.grpflag, Reservation.resnr, Reservation.name, Reservation.groupname, Reservation.depositgef, Reservation.limitdate, Reservation.zahldatum, Reservation.zahldatum2, Reservation.depositbez, Reservation.depositbez2, Reservation._recid, Res_line.name, Res_line.ankunft, Res_line.abreise, Res_line.resstatus, Res_line._recid).join(Res_line,(Res_line.resnr == Reservation.resnr) & (Res_line.resstatus <= 8)).filter(
                 (Reservation.depositgef != 0) & (((Reservation.zahldatum >= fdate) & (Reservation.zahldatum <= tdate)) | ((Reservation.zahldatum2 >= fdate) & (Reservation.zahldatum2 <= tdate)) | ((Reservation.limitdate >= fdate) & (Reservation.limitdate <= tdate)))).order_by(Reservation.zahldatum).all():
            if reservation_obj_list.get(reservation._recid):
                continue
            else:
                reservation_obj_list[reservation._recid] = True


            depo_list = Depo_list()
            depo_list_list.append(depo_list)

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
            depo_list.depo1 =  to_decimal(reservation.depositbez)
            depo_list.depo2 =  to_decimal(reservation.depositbez2)
            depo_list.departure = res_line.abreise

            if res_line.resstatus == 6:
                depo_list.status_rsv = "Checked-In"

            elif res_line.resstatus == 8:
                depo_list.status_rsv = "Checked-Out"
            else:
                depo_list.status_rsv = "Reservation"


    htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

    artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})
    depo_foreign = artikel.pricetab
    depo_curr = artikel.betriebsnr

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    bill_date = htparam.fdate
    depo_list_list.clear()

    if sorttype == 1:

        if depo_foreign:
            create_depolist_arr1()
        else:
            create_depolist_arr2()

    if sorttype == 2:

        if depo_foreign:
            create_depolist1()
        else:
            create_depolist2()

    if sorttype == 3:

        if depo_foreign:
            create_depolist_dep1()
        else:
            create_depolist_dep2()

    return generate_output()