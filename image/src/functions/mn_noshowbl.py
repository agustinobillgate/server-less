from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Res_line, Zimplan, Zinrstat, Guest, Reservation, Artikel, Counters, Bill, Bill_line, Billjournal, Umsatz, Waehrung, Exrate

def mn_noshowbl(pvilanguage:int):
    i = 0
    msg_str = ""
    lvcarea:str = "mn_start"
    ci_date:date = None
    htparam = res_line = zimplan = zinrstat = guest = reservation = artikel = counters = bill = bill_line = billjournal = umsatz = waehrung = exrate = None

    reslist = rline = depoart = art1 = gbuff = None

    reslist_list, Reslist = create_model("Reslist", {"resnr":int})

    Rline = Res_line
    Depoart = Artikel
    Art1 = Artikel
    Gbuff = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, msg_str, lvcarea, ci_date, htparam, res_line, zimplan, zinrstat, guest, reservation, artikel, counters, bill, bill_line, billjournal, umsatz, waehrung, exrate
        nonlocal rline, depoart, art1, gbuff


        nonlocal reslist, rline, depoart, art1, gbuff
        nonlocal reslist_list
        return {"i": i, "msg_str": msg_str}

    def noshow():

        nonlocal i, msg_str, lvcarea, ci_date, htparam, res_line, zimplan, zinrstat, guest, reservation, artikel, counters, bill, bill_line, billjournal, umsatz, waehrung, exrate
        nonlocal rline, depoart, art1, gbuff


        nonlocal reslist, rline, depoart, art1, gbuff
        nonlocal reslist_list

        res_recid1:int = 0
        Rline = Res_line

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  (Res_line.resstatus <= 5) &  (Res_line.ankunft < ci_date)).first()
        while None != res_line:
            i = i + 1

            reslist = query(reslist_list, filters=(lambda reslist :reslist.resnr == res_line.resnr), first=True)

            if not reslist:
                reslist = Reslist()
                reslist_list.append(reslist)

                reslist.resnr = res_line.resnr

            if res_line.zinr != "":
                res_recid1 = res_line._recid

                for zimplan in db_session.query(Zimplan).filter(
                            (Zimplan.zinr == res_line.zinr) &  (Zimplan.datum >= ci_date) &  (Zimplan.datum <= res_line.abreise) &  (Zimplan.res_recid == res_recid1)).all():
                    db_session.delete(zimplan)
            check_noshow_deposit(res_line.resnr)

            res_line = db_session.query(Res_line).first()

            if (res_line.resstatus <= 2 or res_line.resstatus == 5):
                res_line.betrieb_gastpay = res_line.resstatus
                res_line.resstatus = 10
                res_line.active_flag = 2

                res_line = db_session.query(Res_line).first()

                for rline in db_session.query(Rline).filter(
                            (Rline.resnr == res_line.resnr) &  (Rline.resstatus == 11) &  (Rline.kontakt_nr == res_line.reslinnr)).all():
                    rline.zimmerfix = True
                    rline.resstatus = 10
                    rline.active_flag = 2


                    pass

                zinrstat = db_session.query(Zinrstat).filter(
                            (func.lower(Zinrstat.zinr) == "No_Show") &  (Zinrstat.datum == res_line.ankunft)).first()

                if not zinrstat:
                    zinrstat = Zinrstat()
                    db_session.add(zinrstat)

                    zinrstat.datum = res_line.ankunft
                    zinrstat.zinr = "No_Show"


                zinrstat.zimmeranz = zinrstat.zimmeranz + res_line.zimmeranz
                zinrstat.personen = zinrstat.personen + res_line.erwachs

                guest = db_session.query(Guest).filter(
                            (Guest.gastnr == res_line.gastnrmember)).first()

                if guest:
                    guest.noshows = guest.noshows + 1

                    guest = db_session.query(Guest).first()
            else:
                res_line.betrieb_gastpay = res_line.resstatus
                res_line.resstatus = 9
                res_line.cancelled_id = "$$" +\
                        ";" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS")
                res_line.active_flag = 2

                res_line = db_session.query(Res_line).first()

                for rline in db_session.query(Rline).filter(
                            (Rline.resnr == res_line.resnr) &  (Rline.resstatus == 11) &  (Rline.kontakt_nr == res_line.reslinnr)).all():
                    rline.zimmerfix = True
                    rline.resstatus = 9
                    res_line.cancelled_id = "$$" +\
                            ";" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS")
                    rline.active_flag = 2


            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == 0) &  (Res_line.resstatus <= 5) &  (Res_line.ankunft < ci_date)).first()

        res_line = db_session.query(Res_line).filter(
                (Res_line.active_flag == 0) &  (Res_line.resstatus == 11) &  (Res_line.ankunft < ci_date)).first()
        while None != res_line:
            i = i + 1

            res_line = db_session.query(Res_line).first()
            res_line.betrieb_gastpay = res_line.resstatus
            res_line.resstatus = 10
            res_line.active_flag = 2

            res_line = db_session.query(Res_line).first()


            res_line = db_session.query(Res_line).filter(
                    (Res_line.active_flag == 0) &  (Res_line.resstatus == 11) &  (Res_line.ankunft < ci_date)).first()

        for reslist in query(reslist_list):

            res_line = db_session.query(Res_line).filter(
                    (Res_line.resnr == reslist.resnr) &  (Res_line.active_flag < 2)).first()

            if not res_line:

                reservation = db_session.query(Reservation).filter(
                        (Reservation.resnr == reslist.resnr)).first()
                reservation.activeflag = 1

                reservation = db_session.query(Reservation).first()
            reslist_list.remove(reslist)

    def check_noshow_deposit(resno:int):

        nonlocal i, msg_str, lvcarea, ci_date, htparam, res_line, zimplan, zinrstat, guest, reservation, artikel, counters, bill, bill_line, billjournal, umsatz, waehrung, exrate
        nonlocal rline, depoart, art1, gbuff


        nonlocal reslist, rline, depoart, art1, gbuff
        nonlocal reslist_list

        bill_date:date = None
        deposit:decimal = 0
        deposit_foreign:decimal = 0
        sys_id:str = ""
        Depoart = Artikel
        Art1 = Artikel
        Gbuff = Guest

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == resno)).first()

        if reservation.depositbez == 0 or reservation.bestat_datum != None:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 120)).first()

        depoart = db_session.query(Depoart).filter(
                (depoArt.artnr == htparam.finteger) &  (depoArt.departement == 0)).first()

        if not depoArt:

            return

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 104)).first()
        sys_id = htparam.fchar

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 110)).first()
        bill_date = htparam.fdate

        art1 = db_session.query(Art1).filter(
                (Art1.artnr == reservation.zahlkonto) &  (Art1.departement == 0)).first()

        reservation = db_session.query(Reservation).first()
        reservation.bestat_dat = bill_date

        reservation = db_session.query(Reservation).first()
        deposit, deposit_foreign = calculate_deposit_amount(bill_date)

        counters = db_session.query(Counters).filter(
                (Counters.counter_no == 3)).first()
        counters = counters + 1

        counters = db_session.query(Counters).first()

        gbuff = db_session.query(Gbuff).filter(
                (Gbuff.gastnr == reservation.gastnr)).first()
        bill = Bill()
        db_session.add(bill)

        bill.gastnr = reservation.gastnr
        bill.rechnr = counters
        bill.datum = bill_date
        billtyp = 0
        bill.name = gbuff.name + ", " + gbuff.vorname1 + gbuff.anredefirma
        bill.bilname = bill.name
        bill.resnr = 0
        bill.reslinnr = 1
        bill.saldo = deposit
        bill.mwst[98] = deposit_foreign
        bill.rgdruck = 0

        bill = db_session.query(Bill).first()

        art1 = db_session.query(Art1).filter(
                (Art1.artnr == reservation.zahlkonto) &  (Art1.departement == 0)).first()
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = depoArt.artnr
        bill_line.bezeich = depoArt.bezeich
        bill_line.anzahl = 1
        bill_line.betrag = deposit
        bill_line.fremdwbetrag = deposit_foreign
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = sys_id
        bill_line.zinr = res_line.zinr
        bill_line.massnr = res_line.resnr
        bill_line.billin_nr = res_line.reslinnr
        bill_line.arrangement = res_line.arrangement
        bill_line.bill_datum = bill_date

        if art1:
            bill_line.bezeich = bill_line.bezeich + " [" + art1.bezeich + "]"

        bill_line = db_session.query(Bill_line).first()
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = depoArt.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng = deposit_foreign
        billjournal.betrag = deposit
        billjournal.bezeich = depoArt.bezeich + " " +\
                to_string(reservation.resnr)
        billjournal.zinr = res_line.zinr
        billjournal.epreis = 0
        billjournal.zinr = res_line.zinr
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = sys_id
        billjournal.bill_datum = bill_date

        if art1:
            billjournal.bezeich = billjournal.bezeich + " [" + art1.bezeich + "]"

        billjournal = db_session.query(Billjournal).first()

        umsatz = db_session.query(Umsatz).filter(
                (Umsatz.artnr == depoArt.artnr) &  (Umsatz.departement == 0) &  (Umsatz.datum == bill_date)).first()

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoArt.artnr
            umsatz.datum = bill_date
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag = umsatz.betrag + deposit

        umsatz = db_session.query(Umsatz).first()
        msg_str = msg_str + chr(2) + "&W" + translateExtended ("No_show guest with PAID deposit found:", lvcarea, "") + chr(10) + to_string(res_line.resnr) + " - " + res_line.name + chr(10) + translateExtended ("deposit amount automatically posted to bill number", lvcarea, "") + " " + to_string(bill.rechnr)

    def calculate_deposit_amount(bill_date:date):

        nonlocal i, msg_str, lvcarea, ci_date, htparam, res_line, zimplan, zinrstat, guest, reservation, artikel, counters, bill, bill_line, billjournal, umsatz, waehrung, exrate
        nonlocal rline, depoart, art1, gbuff


        nonlocal reslist, rline, depoart, art1, gbuff
        nonlocal reslist_list

        deposit = 0
        deposit_foreign = 0
        deposit_exrate:decimal = 1
        exchg_rate:decimal = 0

        def generate_inner_output():
            return deposit, deposit_foreign

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 120)).first()

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == htparam.finteger) &  (Artikel.departement == 0)).first()

        if not artikel.pricetab:
            deposit = - reservation.depositbez - reservation.depositbez2


        else:
            deposit_exrate = 1

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == artikel.betriebsnr)).first()

            if reservation.zahldatum == bill_date:

                if waehrung:
                    deposit_exrate = waehrung.ankauf / waehrung.einheit
            else:

                exrate = db_session.query(Exrate).filter(
                        (Exrate.artnr == artikel.betriebsnr) &  (Exrate.datum == reservation.zahldatum)).first()

                if exrate:
                    deposit_exrate = exrate.betrag

                elif waehrung:
                    deposit_exrate = waehrung.ankauf / waehrung.einheit
            deposit = - reservation.depositbez * deposit_exrate

            if reservation.depositbez2 != 0:
                deposit_exrate = 1

                if reservation.zahldatum == bill_date:

                    if waehrung:
                        deposit_exrate = waehrung.ankauf / waehrung.einheit
                else:

                    exrate = db_session.query(Exrate).filter(
                            (Exrate.artnr == artikel.betriebsnr) &  (Exrate.datum == reservation.zahldatum2)).first()

                    if exrate:
                        deposit_exrate = exrate.betrag

                    elif waehrung:
                        deposit_exrate = waehrung.ankauf / waehrung.einheit
            deposit = deposit - reservation.depositbez2 * deposit_exrate

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        waehrung = db_session.query(Waehrung).filter(
                (Waehrung.wabkurz == htparam.fchar)).first()

        if waehrung:
            exchg_rate = waehrung.ankauf / waehrung.einheit
        deposit_foreign = round(deposit / exchg_rate, 2)


        return generate_inner_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()
    ci_date = htparam.fdate
    noshow()

    return generate_output()