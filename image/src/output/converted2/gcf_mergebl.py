#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Guestat1, Akt_kont, Genstat, Queasy, History, Reservation, Res_line, Bill, Debitor, Zimmer, Kontline, Master, Messages, Bk_veran, Bk_func, Guest_pr, Bediener, Res_history

def gcf_mergebl(user_init:string, gastnr1:int, gastnr2:int, flag1:bool, flag2:bool):

    prepare_cache ([Akt_kont, Genstat, Queasy, History, Reservation, Res_line, Bill, Debitor, Zimmer, Kontline, Master, Messages, Bk_veran, Bk_func, Guest_pr, Bediener, Res_history])

    guest = guestat1 = akt_kont = genstat = queasy = history = reservation = res_line = bill = debitor = zimmer = kontline = master = messages = bk_veran = bk_func = guest_pr = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal guest, guestat1, akt_kont, genstat, queasy, history, reservation, res_line, bill, debitor, zimmer, kontline, master, messages, bk_veran, bk_func, guest_pr, bediener, res_history
        nonlocal user_init, gastnr1, gastnr2, flag1, flag2

        return {}

    def gcf_merge():

        nonlocal guest, guestat1, akt_kont, genstat, queasy, history, reservation, res_line, bill, debitor, zimmer, kontline, master, messages, bk_veran, bk_func, guest_pr, bediener, res_history
        nonlocal user_init, gastnr1, gastnr2, flag1, flag2

        gast = None
        gast1 = None
        gast2 = None
        gastat = None
        name1:string = ""
        name2:string = ""
        Gast =  create_buffer("Gast",Guest)
        Gast1 =  create_buffer("Gast1",Guest)
        Gast2 =  create_buffer("Gast2",Guest)
        Gastat =  create_buffer("Gastat",Guestat1)

        gast2 = db_session.query(Gast2).filter(
                 (Gast2.gastnr == gastnr2)).first()
        name2 = gast2.name

        gast1 = db_session.query(Gast1).filter(
                     (Gast1.gastnr == gastnr1)).first()
        name1 = gast1.name

        for akt_kont in db_session.query(Akt_kont).filter(
                     (Akt_kont.betrieb_gast == gastnr1)).order_by(Akt_kont._recid).all():
            akt_kont.betrieb_gast = gastnr2

        for genstat in db_session.query(Genstat).filter(
                     (Genstat.gastnr == gastnr1)).order_by(Genstat._recid).all():
            genstat.gastnr = gastnr2

        for genstat in db_session.query(Genstat).filter(
                     (Genstat.gastnrmember == gastnr1)).order_by(Genstat._recid).all():
            genstat.gastnrmember = gastnr2

        for queasy in db_session.query(Queasy).filter(
                     (Queasy.key == 14) & (Queasy.number3 == gastnr1)).order_by(Queasy._recid).all():
            queasy.number3 = gastnr2

        for history in db_session.query(History).filter(
                     (History.gastnr == gastnr1)).order_by(History._recid).all():
            history.gastnr = gastnr2

        for reservation in db_session.query(Reservation).filter(
                     (Reservation.gastnr == gastnr1)).order_by(Reservation._recid).all():
            reservation.gastnr = gastnr2
            reservation.name = gast2.name

        for reservation in db_session.query(Reservation).filter(
                     (Reservation.gastnrherk == gastnr1)).order_by(Reservation._recid).all():
            reservation.gastnrherk = gastnr2

        for res_line in db_session.query(Res_line).filter(
                     (Res_line.gastnr == gastnr1)).order_by(Res_line._recid).all():
            res_line.gastnr = gastnr2
            res_line.resname = gast2.name

        for res_line in db_session.query(Res_line).filter(
                     (Res_line.gastnrmember == gastnr1)).order_by(Res_line._recid).all():
            res_line.gastnrmember = gastnr2
            res_line.name = gast2.name + ", " + gast2.vorname1 + " " + gast2.anrede1

        for res_line in db_session.query(Res_line).filter(
                     (Res_line.gastnrpay == gastnr1)).order_by(Res_line._recid).all():
            res_line.gastnrpay = gastnr2

        for bill in db_session.query(Bill).filter(
                     (Bill.gastnr == gastnr1)).order_by(Bill._recid).all():
            bill.gastnr = gastnr2
            bill.name = gast2.name

        for debitor in db_session.query(Debitor).filter(
                     (Debitor.gastnr == gastnr1)).order_by(Debitor._recid).all():
            debitor.gastnr = gastnr2
            debitor.name = gast2.name

        for debitor in db_session.query(Debitor).filter(
                     (Debitor.gastnrmember == gastnr1)).order_by(Debitor._recid).all():
            debitor.gastnrmember = gastnr2

        for gast in db_session.query(Gast).filter(
                     (Gast.master_gastnr == gastnr1)).order_by(Gast._recid).all():
            gast.master_gastnr = gastnr2

        for guestat1 in db_session.query(Guestat1).filter(
                     (Guestat1.gastnr == gastnr1)).order_by(Guestat1._recid).all():

            gastat = db_session.query(Gastat).filter(
                         (Gastat.gastnr == gastnr2) & (Gastat.datum == guestat1.datum)).first()

            if gastat:
                gastat.zimmeranz = gastat.zimmeranz + guestat1.zimmeranz
                gastat.betriebsnr = gastat.betriebsnr + guestat1.betriebsnr
                gastat.persanz = gastat.persanz + guestat1.persanz
                gastat.logis =  to_decimal(gastat.logis) + to_decimal(guestat1.logis)
                db_session.delete(guestat1)
            else:
                guestat1.gastnr = gastnr2

        for zimmer in db_session.query(Zimmer).filter(
                     (Zimmer.owner_nr == gastnr1)).order_by(Zimmer._recid).all():
            zimmer.owner_nr = gastnr2

        for kontline in db_session.query(Kontline).filter(
                     (Kontline.gastnr == gastnr1)).order_by(Kontline._recid).all():
            kontline.gastnr = gastnr2
            kontline.gastnrpay = gastnr2
        check_global_allotment(gastnr1, gastnr2)

        for master in db_session.query(Master).filter(
                     (Master.gastnr == gastnr1)).order_by(Master._recid).all():
            master.gastnr = gastnr2
            master.gastnrpay = gastnr2

        for messages in db_session.query(Messages).filter(
                     (Messages.gastnr == gastnr1)).order_by(Messages._recid).all():
            messages.gastnr = gastnr2
            messages.name = gast2.name + ", " + gast2.vorname1 + " " + gast2.anrede1

        for bk_veran in db_session.query(Bk_veran).filter(
                     (Bk_veran.gastnr == gastnr1)).order_by(Bk_veran._recid).all():

            for bk_func in db_session.query(Bk_func).filter(
                         (Bk_func.veran_nr == bk_veran.veran_nr)).order_by(Bk_func._recid).all():
                bk_func.bestellt__durch = name2
                bk_func.adurch = name2
                bk_func.nadkarte[0] = name2
                bk_func.betriebsnr = gastnr2


            bk_veran.gastnr = gastnr2

        if flag1:

            guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, gastnr1)]})
            guest_pr.gastnr = gastnr2
            pass
        pass
        gast2.logisumsatz =  to_decimal(gast2.logisumsatz) + to_decimal(gast1.logisumsatz)
        gast2.argtumsatz =  to_decimal(gast2.argtumsatz) + to_decimal(gast1.argtumsatz)
        gast2.f_b_umsatz =  to_decimal(gast2.f_b_umsatz) + to_decimal(gast1.f_b_umsatz)
        gast2.sonst_umsatz =  to_decimal(gast2.sonst_umsatz) + to_decimal(gast1.sonst_umsatz)
        gast2.gesamtumsatz =  to_decimal(gast2.gesamtumsatz) + to_decimal(gast1.gesamtumsatz)
        gast2.zimmeranz = gast2.zimmeranz + gast1.zimmeranz
        gast2.aufenthalte = gast2.aufenthalte + gast1.aufenthalte
        gast2.logiernachte = gast2.logiernachte + gast1.logiernachte


        gast1.name = ""
        gast1.gastnr = - gast1.gastnr


        pass
        pass

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.aenderung = "Merge GuestCard: GastNo " + to_string(gastnr1) +\
                " " + name1 + "TO GastNo " + to_string(gastnr2) + " " + name2
        res_history.action = "GuestFile"


        pass
        pass


    def check_global_allotment(gastnr1:int, gastnr2:int):

        nonlocal guest, guestat1, akt_kont, genstat, queasy, history, reservation, res_line, bill, debitor, zimmer, kontline, master, messages, bk_veran, bk_func, guest_pr, bediener, res_history
        nonlocal user_init, flag1, flag2

        tokcounter:int = 0
        mesvalue:string = ""
        global_str:string = ""
        changed:bool = False
        qsy = None
        Qsy =  create_buffer("Qsy",Queasy)

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 147) & (Queasy.number1 == gastnr1)).order_by(Queasy._recid).all():
            queasy.number1 = gastnr2

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 147)).order_by(Queasy._recid).all():
            changed = False
            global_str = ""


            for tokcounter in range(1,num_entries(queasy.char3, ",")  + 1) :
                mesvalue = entry(tokcounter - 1, queasy.char3, ",")

                if mesvalue != "":

                    if to_int(mesvalue) == gastnr1:
                        changed = True
                        global_str = global_str + to_string(gastnr2) + ","


                    else:
                        global_str = global_str + mesvalue + ","

            if changed:

                qsy = get_cache (Queasy, {"_recid": [(eq, queasy._recid)]})
                qsy.char3 = global_str


                pass


    gcf_merge()

    return generate_output()