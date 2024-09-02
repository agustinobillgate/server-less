from functions.additional_functions import *
import decimal
from functions.ziwechsel_str import ziwechsel_str
from models import Res_line, Bill, History, Guest, Bediener, Reservation, Zimkateg, Htparam, Akt_kont, Bill_line, Artikel, Res_history

def create_history(resnr:int, reslinnr:int, old_zinr:str, res_mode:str):
    lvcarea:str = "create_history"
    variable: = None
    parent_nr:int = 0
    tot_umsatz:decimal = 0
    found:bool = False
    ziwechsel_str:str = ""
    res_line = bill = history = guest = bediener = reservation = zimkateg = htparam = akt_kont = bill_line = artikel = res_history = None

    rline = bill1 = history1 = rguest = None

    Rline = Res_line
    Bill1 = Bill
    History1 = History
    Rguest = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal lvcarea, variable, parent_nr, tot_umsatz, found, ziwechsel_str, res_line, bill, history, guest, bediener, reservation, zimkateg, htparam, akt_kont, bill_line, artikel, res_history
        nonlocal rline, bill1, history1, rguest


        nonlocal rline, bill1, history1, rguest
        return {}


    bediener = db_session.query(Bediener).filter(
            (Bediener.userinit == user_init)).first()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == resnr) &  (Res_line.reslinnr == reslinnr)).first()

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == resnr)).first()

    zimkateg = db_session.query(Zimkateg).filter(
            (Zimkateg.zikatnr == res_line.zikatnr)).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == res_line.gastnrmember)).first()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 87)).first()

    if res_mode.lower()  == "checkout":
        history = History()
        db_session.add(history)


        rguest = db_session.query(Rguest).filter(
                (Rguest.gastnr == res_line.gastnr)).first()
        history.bemerk = history.bemerk + "RSV:" + rguest.name + chr(10)

        if res_line.l_zuordnung[2] == 0 and res_line.resstatus == 6:

            for rline in db_session.query(Rline).filter(
                    (Rline.resnr == res_line.resnr) &  (Rline.l_zuordnung[2] == 1) &  (Rline.kontakt_nr == res_line.reslinnr)).all():
                history.bemerk = history.bemerk + "AG:" + rline.name + chr(10)

                rguest = db_session.query(Rguest).filter(
                        (Rguest.gastnr == rline.gastnrmember)).first()

                if rguest.date1 != rline.ankunft or rguest.date2 != rline.abreise:

                    rguest = db_session.query(Rguest).first()
                    rguest.date1 = rline.ankunft
                    rguest.date2 = rline.abreise
                    rguest.resflag = 0

                    rguest = db_session.query(Rguest).first()

            for rline in db_session.query(Rline).filter(
                    (Rline.resnr == res_line.resnr) &  (Rline.reslinnr != res_line.reslinnr) &  (Rline.zinr == res_line.zinr) &  (Rline.l_zuordnung[2] == 0) &  ((Rline.resstatus == 13) |  (Rline.resstatus == 8))).all():
                history.bemerk = history.bemerk + "SH:" + rline.name + chr(10)

        elif res_line.l_zuordnung[2] == 0 and res_line.resstatus == 13:

            rline = db_session.query(Rline).filter(
                    (Rline.resnr == res_line.resnr) &  (Rline.reslinnr != res_line.reslinnr) &  (Rline.zinr == res_line.zinr) &  (Rline.l_zuordnung[2] == 0) &  ((Rline.resstatus == 6) |  (Rline.resstatus == 8))).first()

            if rline:
                history.bemerk = history.bemerk + "MG:" + rline.name + chr(10)

        elif res_line.l_zuordnung[2] == 1:

            rline = db_session.query(Rline).filter(
                    (Rline.resnr == res_line.resnr) &  (Rline.reslinnr == res_line.kontakt_nr)).first()

            if rline:
                history.bemerk = history.bemerk + "MG:" + rline.name + chr(10)

        if reservation.kontakt_nr != 0:

            akt_kont = db_session.query(Akt_kont).filter(
                    (Akt_kont.gastnr == reservation.gastnr) &  (Akt_kont.kontakt_nr == reservation.kontakt_nr)).first()

            if akt_kont:
                history.bemerk = history.bemerk + "CT:" + akt_kont.name +\
                    ", " + akt_kont.vorname + chr(10)


        history.gastnr = res_line.gastnrmember
        history.ankunft = res_line.ankunft
        history.abreise = htparam.fdate
        history.zimmeranz = res_line.zimmeranz
        history.zikateg = zimkateg.kurzbez
        history.zinr = res_line.zinr
        history.erwachs = res_line.erwachs
        history.gratis = res_line.gratis
        history.zipreis = res_line.zipreis
        history.arrangement = res_line.arrangement
        history.guestnrcom = res_line.reserve_int
        history.gastinfo = res_line.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.abreisezeit = to_string(time, "HH:MM")
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = False
        history.resnr = res_line.resnr
        history.reslinnr = res_line.reslinnr
        history.betriebsnr = to_int(res_line.pseudofix)

        if res_line.bemerk != "":
            history.bemerk = history.bemerk + "RL:" + res_line.bemerk + chr(10)

        if reservation.bemerk != "":
            history.bemerk = history.bemerk + "R:" + reservation.bemerk + chr(10)

        bill1 = db_session.query(Bill1).filter(
                (Bill1.resnr == res_line.resnr) &  (Bill1.reslinnr == 0)).first()

        if bill1:
            history.bemerk = history.bemerk + "M:" + to_string(bill1.rechnr) + chr(10)
        found = False

        for bill1 in db_session.query(Bill1).filter(
                (Bill1.resnr == res_line.resnr) &  (Bill1.parent_nr == res_line.reslinnr) &  (Bill1.zinr == res_line.zinr) &  (Bill1.rechnr > 0)).all():

            if not found:
                history.bemerk = history.bemerk + "B:"
            else:
                history.bemerk = history.bemerk + "/"
            history.bemerk = history.bemerk + to_string(bill1.rechnr)
            found = True

        if found:
            history.bemerk = history.bemerk + chr(10)
        history.bemerk = history.bemerk + "C/O: " + user_init + chr(10)

        if res_line.gastnr != res_line.gastnrmember:

            history1 = db_session.query(History1).filter(
                    (History1.resnr == res_line.resnr) &  (History1.reslinnr == 999)).first()

            if not history1:
                history1 = History1()
                db_session.add(history1)


                if akt_kont:
                    history1.bemerk = history1.bemerk + "CT:" + akt_kont.name +\
                        ", " + akt_kont.vorname + chr(10)


                history1.gastnr = res_line.gastnr
                history1.resnr = res_line.resnr
                history1.reslinnr = 999
                history1.ankunft = res_line.ankunft
                history1.abreise = res_line.abreise
                history1.arrangement = res_line.arrangement
                history1.gastinfo = res_line.resname
                history1.segmentcode = reservation.segmentcode

                if reservation.bemerk != "":
                    history1.bemerk = history1.bemerk + "R:" + reservation.bemerk + chr(10)

                bill1 = db_session.query(Bill1).filter(
                        (Bill1.resnr == res_line.resnr) &  (Bill1.reslinnr == 0)).first()

                if bill1:
                    history1.bemerk = history1.bemerk + "M:" + to_string(bill1.rechnr) + chr(10)

                bill1 = db_session.query(Bill1).filter(
                        (Bill1.resnr == resnr) &  (Bill1.reslinnr == 0) &  (Bill1.flag == 0)).first()

                if bill1:
                    history1.logisumsatz = bill1.logisumsatz
                    history1.argtumsatz = bill1.argtumsatz
                    history1.f_b_umsatz = bill1.f_b_umsatz
                    history1.sonst_umsatz = bill1.sonst_umsatz
                    history1.gesamtumsatz = bill1.gesamtumsatz
            history1.zimmeranz = history1.zimmeranz + res_line.zimmeranz

            if history1.zipreis == 0 and res_line.zipreis != 0:
                history1.zikateg = zimkateg.kurzbez
                history1.zipreis = res_line.zipreis
                history1.abreisezeit = to_string(time, "HH:MM")

        for bill1 in db_session.query(Bill1).filter(
                (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (Bill1.flag == 1) &  (Bill1.zinr == res_line.zinr)).all():
            tot_umsatz = tot_umsatz + bill1.gesamtumsatz

        if tot_umsatz != 0:

            for bill1 in db_session.query(Bill1).filter(
                    (Bill1.resnr == resnr) &  (Bill1.parent_nr == reslinnr) &  (Bill1.flag == 1) &  (Bill1.zinr == res_line.zinr)).all():
                history.logisumsatz = history.logisumsatz + bill1.logisumsatz
                history.argtumsatz = history.argtumsatz + bill1.argtumsatz
                history.f_b_umsatz = history.f_b_umsatz + bill1.f_b_umsatz
                history.sonst_umsatz = history.sonst_umsatz + bill1.sonst_umsatz
                history.gesamtumsatz = history.gesamtumsatz + bill1.gesamtumsatz

                if history1 and history1.gastnr == bill1.gastnr:
                    history1.logisumsatz = history1.logisumsatz + bill1.logisumsatz
                    history1.argtumsatz = history1.argtumsatz + bill1.argtumsatz
                    history1.f_b_umsatz = history1.f_b_umsatz + bill1.f_b_umsatz
                    history1.sonst_umsatz = history1.sonst_umsatz + bill1.sonst_umsatz
                    history1.gesamtumsatz = history1.gesamtumsatz + bill1.gesamtumsatz

                bill_line = db_session.query(Bill_line).filter(
                        (Bill_line.rechnr == bill1.rechnr)).first()
                found = False
                while None != bill_line and not found:

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == bill_line.artnr) &  (Artikel.departement == bill_line.departement) &  ((Artikel.artart == 2) |  (Artikel.artart == 4) |  (Artikel.artart == 6) |  (Artikel.artart == 7))).first()

                    if artikel:
                        found = True
                        history.zahlungsart = artikel.artnr

                    bill_line = db_session.query(Bill_line).filter(
                            (Bill_line.rechnr == bill1.rechnr)).first()

        if history1:

            history1 = db_session.query(History1).first()

    elif res_mode.lower()  == "roomchg":
        ziwechsel_str = get_output(ziwechsel_str())
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
        history.zipreis = res_line.zipreis
        history.arrangement = res_line.arrangement
        history.abreisezeit = to_string(time, "HH:MM")
        history.gastinfo = res_line.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = True
        history.resnr = res_line.resnr
        history.reslinnr = res_line.reslinnr
        history.betriebsnr = to_int(res_line.pseudofix)


        history.bemerk = to_string(htparam.fdate) + translateExtended (": Moved to", lvcarea, "") + " " + res_line.zinr + chr(10) + ziwechsel_str
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = old_zinr + " -> " + res_line.zinr +\
                chr(10) + ziwechsel_str
        res_history.action = "RoomChange"

        res_history = db_session.query(Res_history).first()


    elif res_mode.lower()  == "HK_preference":
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
        history.zipreis = res_line.zipreis
        history.arrangement = res_line.arrangement
        history.abreisezeit = to_string(time, "HH:MM")
        history.gastinfo = res_line.name + " - " +\
                guest.adresse1 + ", " + guest.wohnort
        history.segmentcode = reservation.segmentcode
        history.zi_wechsel = False
        history.resnr = res_line.resnr
        history.reslinnr = res_line.reslinnr
        history.betriebsnr = to_int(res_line.pseudofix)


        history.bemerk = translateExtended ("HK_Preference", lvcarea, "") +\
                ": == " + trim(entry(1, old_zinr, ";"))

        history = db_session.query(History).first()

    return generate_output()