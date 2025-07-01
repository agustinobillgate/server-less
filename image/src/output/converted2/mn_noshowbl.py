#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Zimplan, Zinrstat, Guest, Reservation, Artikel, Counters, Bill, Bill_line, Billjournal, Umsatz, Waehrung, Exrate

def mn_noshowbl(pvilanguage:int):

    prepare_cache ([Htparam, Zinrstat, Guest, Reservation, Artikel, Counters, Bill, Bill_line, Billjournal, Umsatz, Waehrung, Exrate])

    i = 0
    msg_str = ""
    lvcarea:string = "mn-start"
    ci_date:date = None
    htparam = res_line = zimplan = zinrstat = guest = reservation = artikel = counters = bill = bill_line = billjournal = umsatz = waehrung = exrate = None

    reslist = None

    reslist_list, Reslist = create_model("Reslist", {"resnr":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, msg_str, lvcarea, ci_date, htparam, res_line, zimplan, zinrstat, guest, reservation, artikel, counters, bill, bill_line, billjournal, umsatz, waehrung, exrate
        nonlocal pvilanguage


        nonlocal reslist
        nonlocal reslist_list

        return {"i": i, "msg_str": msg_str}

    def noshow():

        nonlocal i, msg_str, lvcarea, ci_date, htparam, res_line, zimplan, zinrstat, guest, reservation, artikel, counters, bill, bill_line, billjournal, umsatz, waehrung, exrate
        nonlocal pvilanguage


        nonlocal reslist
        nonlocal reslist_list

        res_recid1:int = 0
        rline = None
        Rline =  create_buffer("Rline",Res_line)

        res_line = get_cache (Res_line, {"active_flag": [(eq, 0)],"resstatus": [(le, 5)],"ankunft": [(lt, ci_date)]})
        while None != res_line:
            i = i + 1

            reslist = query(reslist_list, filters=(lambda reslist: reslist.resnr == res_line.resnr), first=True)

            if not reslist:
                reslist = Reslist()
                reslist_list.append(reslist)

                reslist.resnr = res_line.resnr

            if res_line.zinr != "":
                res_recid1 = res_line._recid

                for zimplan in db_session.query(Zimplan).filter(
                             (Zimplan.zinr == res_line.zinr) & (Zimplan.datum >= ci_date) & (Zimplan.datum <= res_line.abreise) & (Zimplan.res_recid == res_recid1)).order_by(Zimplan._recid).all():
                    db_session.delete(zimplan)
            check_noshow_deposit(res_line.resnr)
            pass

            if (res_line.resstatus <= 2 or res_line.resstatus == 5):
                res_line.betrieb_gastpay = res_line.resstatus
                res_line.resstatus = 10
                res_line.active_flag = 2


                pass

                for rline in db_session.query(Rline).filter(
                             (Rline.resnr == res_line.resnr) & (Rline.resstatus == 11) & (Rline.kontakt_nr == res_line.reslinnr)).order_by(Rline._recid).all():
                    rline.zimmerfix = True
                    rline.resstatus = 10
                    rline.active_flag = 2


                zinrstat = get_cache (Zinrstat, {"zinr": [(eq, "no-show")],"datum": [(eq, res_line.ankunft)]})

                if not zinrstat:
                    zinrstat = Zinrstat()
                    db_session.add(zinrstat)

                    zinrstat.datum = res_line.ankunft
                    zinrstat.zinr = "No-Show"


                zinrstat.zimmeranz = zinrstat.zimmeranz + res_line.zimmeranz
                zinrstat.personen = zinrstat.personen + res_line.erwachs

                guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

                if guest:
                    guest.noshows = guest.noshows + 1
                    pass
            else:
                res_line.betrieb_gastpay = res_line.resstatus
                res_line.resstatus = 9
                res_line.cancelled_id = "$$" +\
                        ";" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS")
                res_line.active_flag = 2


                pass

                for rline in db_session.query(Rline).filter(
                             (Rline.resnr == res_line.resnr) & (Rline.resstatus == 11) & (Rline.kontakt_nr == res_line.reslinnr)).order_by(Rline._recid).all():
                    rline.zimmerfix = True
                    rline.resstatus = 9
                    res_line.cancelled_id = "$$" +\
                            ";" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS")
                    rline.active_flag = 2

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag == 0) & (Res_line.resstatus <= 5) & (Res_line.ankunft < ci_date) & (Res_line._recid > curr_recid)).first()

        res_line = get_cache (Res_line, {"active_flag": [(eq, 0)],"resstatus": [(eq, 11)],"ankunft": [(lt, ci_date)]})
        while None != res_line:
            i = i + 1
            pass
            res_line.betrieb_gastpay = res_line.resstatus
            res_line.resstatus = 10
            res_line.active_flag = 2


            pass

            curr_recid = res_line._recid
            res_line = db_session.query(Res_line).filter(
                     (Res_line.active_flag == 0) & (Res_line.resstatus == 11) & (Res_line.ankunft < ci_date) & (Res_line._recid > curr_recid)).first()

        for reslist in query(reslist_list):

            res_line = get_cache (Res_line, {"resnr": [(eq, reslist.resnr)],"active_flag": [(lt, 2)]})

            if not res_line:

                reservation = get_cache (Reservation, {"resnr": [(eq, reslist.resnr)]})
                reservation.activeflag = 1
                pass
            reslist_list.remove(reslist)


    def check_noshow_deposit(resno:int):

        nonlocal i, msg_str, lvcarea, ci_date, htparam, res_line, zimplan, zinrstat, guest, reservation, artikel, counters, bill, bill_line, billjournal, umsatz, waehrung, exrate
        nonlocal pvilanguage


        nonlocal reslist
        nonlocal reslist_list

        bill_date:date = None
        deposit:Decimal = to_decimal("0.0")
        deposit_foreign:Decimal = to_decimal("0.0")
        sys_id:string = ""
        depoart = None
        art1 = None
        gbuff = None
        Depoart =  create_buffer("Depoart",Artikel)
        Art1 =  create_buffer("Art1",Artikel)
        Gbuff =  create_buffer("Gbuff",Guest)

        reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

        if reservation.depositbez == 0 or reservation.bestat_datum != None:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

        depoart = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if not depoArt:

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 104)]})
        sys_id = htparam.fchar

        htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
        bill_date = htparam.fdate

        art1 = get_cache (Artikel, {"artnr": [(eq, reservation.zahlkonto)],"departement": [(eq, 0)]})
        pass
        reservation.bestat_datum = bill_date


        pass
        deposit, deposit_foreign = calculate_deposit_amount(bill_date)

        counters = get_cache (Counters, {"counter_no": [(eq, 3)]})
        counters.counter = counters.counter + 1
        pass

        gbuff = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})
        bill = Bill()
        db_session.add(bill)

        bill.gastnr = reservation.gastnr
        bill.rechnr = counters.counter
        bill.datum = bill_date
        bill.billtyp = 0
        bill.name = gbuff.name + ", " + gbuff.vorname1 + gbuff.anredefirma
        bill.bilname = bill.name
        bill.resnr = 0
        bill.reslinnr = 1
        bill.saldo =  to_decimal(deposit)
        bill.mwst[98] = deposit_foreign
        bill.rgdruck = 0


        pass

        art1 = get_cache (Artikel, {"artnr": [(eq, reservation.zahlkonto)],"departement": [(eq, 0)]})
        bill_line = Bill_line()
        db_session.add(bill_line)

        bill_line.rechnr = bill.rechnr
        bill_line.artnr = depoArt.artnr
        bill_line.bezeich = depoArt.bezeich
        bill_line.anzahl = 1
        bill_line.betrag =  to_decimal(deposit)
        bill_line.fremdwbetrag =  to_decimal(deposit_foreign)
        bill_line.zeit = get_current_time_in_seconds()
        bill_line.userinit = sys_id
        bill_line.zinr = res_line.zinr
        bill_line.massnr = res_line.resnr
        bill_line.billin_nr = res_line.reslinnr
        bill_line.arrangement = res_line.arrangement
        bill_line.bill_datum = bill_date

        if art1:
            bill_line.bezeich = bill_line.bezeich + " [" + art1.bezeich + "]"
        pass
        billjournal = Billjournal()
        db_session.add(billjournal)

        billjournal.rechnr = bill.rechnr
        billjournal.artnr = depoArt.artnr
        billjournal.anzahl = 1
        billjournal.fremdwaehrng =  to_decimal(deposit_foreign)
        billjournal.betrag =  to_decimal(deposit)
        billjournal.bezeich = depoArt.bezeich + " " +\
                to_string(reservation.resnr)
        billjournal.zinr = res_line.zinr
        billjournal.epreis =  to_decimal("0")
        billjournal.zinr = res_line.zinr
        billjournal.zeit = get_current_time_in_seconds()
        billjournal.userinit = sys_id
        billjournal.bill_datum = bill_date

        if art1:
            billjournal.bezeich = billjournal.bezeich + " [" + art1.bezeich + "]"
        pass

        umsatz = get_cache (Umsatz, {"artnr": [(eq, depoart.artnr)],"departement": [(eq, 0)],"datum": [(eq, bill_date)]})

        if not umsatz:
            umsatz = Umsatz()
            db_session.add(umsatz)

            umsatz.artnr = depoArt.artnr
            umsatz.datum = bill_date
        umsatz.anzahl = umsatz.anzahl + 1
        umsatz.betrag =  to_decimal(umsatz.betrag) + to_decimal(deposit)
        pass
        msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("No-show guest with PAID deposit found:", lvcarea, "") + chr_unicode(10) + to_string(res_line.resnr) + " - " + res_line.name + chr_unicode(10) + translateExtended ("deposit amount automatically posted to bill number", lvcarea, "") + " " + to_string(bill.rechnr)


    def calculate_deposit_amount(bill_date:date):

        nonlocal i, msg_str, lvcarea, ci_date, htparam, res_line, zimplan, zinrstat, guest, reservation, artikel, counters, bill, bill_line, billjournal, umsatz, waehrung, exrate
        nonlocal pvilanguage


        nonlocal reslist
        nonlocal reslist_list

        deposit = to_decimal("0.0")
        deposit_foreign = to_decimal("0.0")
        deposit_exrate:Decimal = 1
        exchg_rate:Decimal = to_decimal("0.0")

        def generate_inner_output():
            return (deposit, deposit_foreign)


        htparam = get_cache (Htparam, {"paramnr": [(eq, 120)]})

        artikel = get_cache (Artikel, {"artnr": [(eq, htparam.finteger)],"departement": [(eq, 0)]})

        if not artikel.pricetab:
            deposit =  - to_decimal(reservation.depositbez) - to_decimal(reservation.depositbez2)


        else:
            deposit_exrate =  to_decimal("1")

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, artikel.betriebsnr)]})

            if reservation.zahldatum == bill_date:

                if waehrung:
                    deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            else:

                exrate = get_cache (Exrate, {"artnr": [(eq, artikel.betriebsnr)],"datum": [(eq, reservation.zahldatum)]})

                if exrate:
                    deposit_exrate =  to_decimal(exrate.betrag)

                elif waehrung:
                    deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            deposit =  - to_decimal(reservation.depositbez) * to_decimal(deposit_exrate)

            if reservation.depositbez2 != 0:
                deposit_exrate =  to_decimal("1")

                if reservation.zahldatum == bill_date:

                    if waehrung:
                        deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
                else:

                    exrate = get_cache (Exrate, {"artnr": [(eq, artikel.betriebsnr)],"datum": [(eq, reservation.zahldatum2)]})

                    if exrate:
                        deposit_exrate =  to_decimal(exrate.betrag)

                    elif waehrung:
                        deposit_exrate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
            deposit =  to_decimal(deposit) - to_decimal(reservation.depositbez2) * to_decimal(deposit_exrate)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

        waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

        if waehrung:
            exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
        deposit_foreign = to_decimal(round(deposit / exchg_rate , 2))

        return generate_inner_output()


    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate
    noshow()

    return generate_output()