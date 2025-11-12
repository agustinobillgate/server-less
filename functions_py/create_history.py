#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 29/10/2025
# tambah user_init di create_history
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Res_line, Bill, History, Guest, Bediener, Reservation, Zimkateg, Htparam, Akt_kont, Bill_line, Artikel, Res_history

# Rd 29/10/2025
# tambah user_init di create_history
def create_history(resnr:int, reslinnr:int, old_zinr:string, res_mode:string, user_init:string):

    prepare_cache ([Res_line, Bill, History, Guest, Bediener, Reservation, Zimkateg, Htparam, Akt_kont, Artikel, Res_history])

    lvcarea:string = "create-history"
    variable = None
    parent_nr:int = 0
    tot_umsatz:Decimal = to_decimal("0.0")
    found:bool = False
    ziwechsel_str:string = ""
    res_line = bill = history = guest = bediener = reservation = zimkateg = htparam = akt_kont = bill_line = artikel = res_history = None

    rline = bill1 = history1 = rguest = None

    Rline = create_buffer("Rline",Res_line)
    Bill1 = create_buffer("Bill1",Bill)
    History1 = create_buffer("History1",History)
    Rguest = create_buffer("Rguest",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, variable, parent_nr, tot_umsatz, found, ziwechsel_str, res_line, bill, history, guest, bediener, reservation, zimkateg, htparam, akt_kont, bill_line, artikel, res_history
        nonlocal resnr, reslinnr, old_zinr, res_mode
        nonlocal rline, bill1, history1, rguest


        nonlocal rline, bill1, history1, rguest

        return {}


    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})

    reservation = get_cache (Reservation, {"resnr": [(eq, resnr)]})

    zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

    guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if res_mode.lower()  == ("checkout").lower() :
        history = History()
        db_session.add(history)


        rguest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})
        history.bemerk = history.bemerk + "RSV:" + rguest.name + chr_unicode(10)

        if res_line.l_zuordnung[2] == 0 and res_line.resstatus == 6:

            for rline in db_session.query(Rline).filter(
                     (Rline.resnr == res_line.resnr) & (Rline.l_zuordnung[inc_value(2)] == 1) & (Rline.kontakt_nr == res_line.reslinnr)).order_by(Rline._recid).all():
                history.bemerk = history.bemerk + "AG:" + rline.name + chr_unicode(10)

                rguest = get_cache (Guest, {"gastnr": [(eq, rline.gastnrmember)]})

                if rguest.date1 != rline.ankunft or rguest.date2 != rline.abreise:
                    pass
                    rguest.date1 = rline.ankunft
                    rguest.date2 = rline.abreise
                    rguest.resflag = 0


                    pass

            for rline in db_session.query(Rline).filter(
                     (Rline.resnr == res_line.resnr) & (Rline.reslinnr != res_line.reslinnr) & (Rline.zinr == res_line.zinr) & (Rline.l_zuordnung[inc_value(2)] == 0) & ((Rline.resstatus == 13) | (Rline.resstatus == 8))).order_by(Rline._recid).all():
                history.bemerk = history.bemerk + "SH:" + rline.name + chr_unicode(10)

        elif res_line.l_zuordnung[2] == 0 and res_line.resstatus == 13:

            rline = db_session.query(Rline).filter(
                     (Rline.resnr == res_line.resnr) & (Rline.reslinnr != res_line.reslinnr) & (Rline.zinr == res_line.zinr) & (Rline.l_zuordnung[inc_value(2)] == 0) & ((Rline.resstatus == 6) | (Rline.resstatus == 8))).first()

            if rline:
                history.bemerk = history.bemerk + "MG:" + rline.name + chr_unicode(10)

        elif res_line.l_zuordnung[2] == 1:

            rline = get_cache (Res_line, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, res_line.kontakt_nr)]})

            if rline:
                history.bemerk = history.bemerk + "MG:" + rline.name + chr_unicode(10)

        if reservation.kontakt_nr != 0:

            akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, reservation.gastnr)],"kontakt_nr": [(eq, reservation.kontakt_nr)]})

            if akt_kont:
                history.bemerk = history.bemerk + "CT:" + akt_kont.name +\
                    ", " + akt_kont.vorname + chr_unicode(10)


        history.gastnr = res_line.gastnrmember
        history.ankunft = res_line.ankunft
        history.abreise = htparam.fdate
        history.zimmeranz = res_line.zimmeranz
        history.zikateg = zimkateg.kurzbez
        history.zinr = res_line.zinr
        history.erwachs = res_line.erwachs
        history.gratis = res_line.gratis
        history.zipreis =  to_decimal(res_line.zipreis)
        history.arrangement = res_line.arrangement
        history.guestnrcom = res_line.reserve_int
        history.gastinfo = res_line.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.abreisezeit = to_string(get_current_time_in_seconds(), "HH:MM")
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = False
        history.resnr = res_line.resnr
        history.reslinnr = res_line.reslinnr
        history.betriebsnr = to_int(res_line.pseudofix)

        if res_line.bemerk != "":
            history.bemerk = history.bemerk + "RL:" + res_line.bemerk + chr_unicode(10)

        if reservation.bemerk != "":
            history.bemerk = history.bemerk + "R:" + reservation.bemerk + chr_unicode(10)

        bill1 = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)]})

        if bill1:
            history.bemerk = history.bemerk + "M:" + to_string(bill1.rechnr) + chr_unicode(10)
        found = False

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == res_line.resnr) & (Bill1.parent_nr == res_line.reslinnr) & (Bill1.zinr == res_line.zinr) & (Bill1.rechnr > 0)).order_by(Bill1._recid).all():

            if not found:
                history.bemerk = history.bemerk + "B:"
            else:
                history.bemerk = history.bemerk + "/"
            history.bemerk = history.bemerk + to_string(bill1.rechnr)
            found = True

        if found:
            history.bemerk = history.bemerk + chr_unicode(10)
        history.bemerk = history.bemerk + "C/O: " + user_init + chr_unicode(10)

        if res_line.gastnr != res_line.gastnrmember:

            history1 = get_cache (History, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 999)]})

            if not history1:
                history1 = History()
                db_session.add(history1)


                if akt_kont:
                    history1.bemerk = history1.bemerk + "CT:" + akt_kont.name +\
                        ", " + akt_kont.vorname + chr_unicode(10)


                history1.gastnr = res_line.gastnr
                history1.resnr = res_line.resnr
                history1.reslinnr = 999
                history1.ankunft = res_line.ankunft
                history1.abreise = res_line.abreise
                history1.arrangement = res_line.arrangement
                history1.gastinfo = res_line.resname
                history1.segmentcode = reservation.segmentcode

                if reservation.bemerk != "":
                    history1.bemerk = history1.bemerk + "R:" + reservation.bemerk + chr_unicode(10)

                bill1 = get_cache (Bill, {"resnr": [(eq, res_line.resnr)],"reslinnr": [(eq, 0)]})

                if bill1:
                    history1.bemerk = history1.bemerk + "M:" + to_string(bill1.rechnr) + chr_unicode(10)

                bill1 = get_cache (Bill, {"resnr": [(eq, resnr)],"reslinnr": [(eq, 0)],"flag": [(eq, 0)]})

                if bill1:
                    history1.logisumsatz =  to_decimal(bill1.logisumsatz)
                    history1.argtumsatz =  to_decimal(bill1.argtumsatz)
                    history1.f_b_umsatz =  to_decimal(bill1.f_b_umsatz)
                    history1.sonst_umsatz =  to_decimal(bill1.sonst_umsatz)
                    history1.gesamtumsatz =  to_decimal(bill1.gesamtumsatz)
            history1.zimmeranz = history1.zimmeranz + res_line.zimmeranz

            if history1.zipreis == 0 and res_line.zipreis != 0:
                history1.zikateg = zimkateg.kurzbez
                history1.zipreis =  to_decimal(res_line.zipreis)
                history1.abreisezeit = to_string(get_current_time_in_seconds(), "HH:MM")

        for bill1 in db_session.query(Bill1).filter(
                 (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.flag == 1) & (Bill1.zinr == res_line.zinr)).order_by(Bill1._recid).all():
            tot_umsatz =  to_decimal(tot_umsatz) + to_decimal(bill1.gesamtumsatz)

        if tot_umsatz != 0:

            for bill1 in db_session.query(Bill1).filter(
                     (Bill1.resnr == resnr) & (Bill1.parent_nr == reslinnr) & (Bill1.flag == 1) & (Bill1.zinr == res_line.zinr)).order_by(Bill1._recid).all():
                history.logisumsatz =  to_decimal(history.logisumsatz) + to_decimal(bill1.logisumsatz)
                history.argtumsatz =  to_decimal(history.argtumsatz) + to_decimal(bill1.argtumsatz)
                history.f_b_umsatz =  to_decimal(history.f_b_umsatz) + to_decimal(bill1.f_b_umsatz)
                history.sonst_umsatz =  to_decimal(history.sonst_umsatz) + to_decimal(bill1.sonst_umsatz)
                history.gesamtumsatz =  to_decimal(history.gesamtumsatz) + to_decimal(bill1.gesamtumsatz)

                if history1 and history1.gastnr == bill1.gastnr:
                    history1.logisumsatz =  to_decimal(history1.logisumsatz) + to_decimal(bill1.logisumsatz)
                    history1.argtumsatz =  to_decimal(history1.argtumsatz) + to_decimal(bill1.argtumsatz)
                    history1.f_b_umsatz =  to_decimal(history1.f_b_umsatz) + to_decimal(bill1.f_b_umsatz)
                    history1.sonst_umsatz =  to_decimal(history1.sonst_umsatz) + to_decimal(bill1.sonst_umsatz)
                    history1.gesamtumsatz =  to_decimal(history1.gesamtumsatz) + to_decimal(bill1.gesamtumsatz)

                bill_line = get_cache (Bill_line, {"rechnr": [(eq, bill1.rechnr)]})
                found = False
                while None != bill_line and not found:

                    artikel = db_session.query(Artikel).filter(
                             (Artikel.artnr == bill_line.artnr) & (Artikel.departement == bill_line.departement) & ((Artikel.artart == 2) | (Artikel.artart == 4) | (Artikel.artart == 6) | (Artikel.artart == 7))).first()

                    if artikel:
                        found = True
                        history.zahlungsart = artikel.artnr

                    curr_recid = bill_line._recid
                    bill_line = db_session.query(Bill_line).filter(
                             (Bill_line.rechnr == bill1.rechnr) & (Bill_line._recid > curr_recid)).first()

        if history1:
            pass

    elif res_mode.lower()  == ("roomchg").lower() :
        history = History()
        db_session.add(history)

        history.gastnr = res_line.gastnrmember
        history.ankunft = res_line.ankunft
        history.abreise = res_line.abreise
        history.zimmeranz = res_line.zimmeranz
        history.zikateg = zimkateg.kurzbez
        history.zinr = old_zinr
        history.erwachs = res_line.erwachs
        history.gratis = res_line.gratis
        history.zipreis =  to_decimal(res_line.zipreis)
        history.arrangement = res_line.arrangement
        history.abreisezeit = to_string(get_current_time_in_seconds(), "HH:MM")
        history.gastinfo = res_line.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = True
        history.resnr = res_line.resnr
        history.reslinnr = res_line.reslinnr
        history.betriebsnr = to_int(res_line.pseudofix)


        history.bemerk = to_string(htparam.fdate) + translateExtended (": Moved to", lvcarea, "") + " " + res_line.zinr + chr_unicode(10) + ziwechsel_str
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = old_zinr + " -> " + res_line.zinr +\
                chr_unicode(10) + ziwechsel_str
        res_history.action = "RoomChange"


        pass
        pass

    elif res_mode.lower()  == ("HK-preference").lower() :
        history = History()
        db_session.add(history)

        history.gastnr = res_line.gastnrmember
        history.ankunft = res_line.ankunft
        history.abreise = res_line.abreise
        history.zimmeranz = res_line.zimmeranz
        history.zikateg = zimkateg.kurzbez
        history.zinr = trim(entry(0, old_zinr, ";"))
        history.erwachs = res_line.erwachs
        history.gratis = res_line.gratis
        history.zipreis =  to_decimal(res_line.zipreis)
        history.arrangement = res_line.arrangement
        history.abreisezeit = to_string(get_current_time_in_seconds(), "HH:MM")
        history.gastinfo = res_line.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = False
        history.resnr = res_line.resnr
        history.reslinnr = res_line.reslinnr
        history.betriebsnr = to_int(res_line.pseudofix)


        history.bemerk = translateExtended ("HK-Preference", lvcarea, "") +\
                ":=" + trim(entry(1, old_zinr, ";"))


        pass

    return generate_output()