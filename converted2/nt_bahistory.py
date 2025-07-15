#using conversion tools version: 1.0.0.29

from functions.additional_functions import *
import decimal
from models import Bk_reser, Bk_func, Bk_veran, Htparam, B_history

def nt_bahistory():
    rechnr:int = 0
    bk_reser = bk_func = bk_veran = htparam = b_history = None

    bk_reser1 = fsl = mres = None

    Bk_reser1 = create_buffer("Bk_reser1",Bk_reser)
    Fsl = create_buffer("Fsl",Bk_func)
    Mres = create_buffer("Mres",Bk_veran)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rechnr, bk_reser, bk_func, bk_veran, htparam, b_history
        nonlocal bk_reser1, fsl, mres


        nonlocal bk_reser1, fsl, mres

        return {}


    bk_reser = db_session.query(Bk_reser).first()
    while None != bk_reser:

        bk_func = db_session.query(Bk_func).filter(
                 (Bk_func.veran_nr == bk_reser.veran_nr) & (Bk_func.veran_seite == bk_reser.veran_seite)).first()

        if bk_func and bk_func.datum != bk_reser.datum:

            fsl = db_session.query(Fsl).filter(
                     (Fsl._recid == bk_func._recid)).first()

            if fsl:
                fsl.datum = bk_reser.datum
                fsl.bis_datum = bk_reser.bis_datum


                pass

        curr_recid = bk_reser._recid
        bk_reser = db_session.query(Bk_reser).filter(Bk_reser._recid > curr_recid).first()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()

    bk_func_obj_list = []
    for bk_func, bk_veran, bk_reser in db_session.query(Bk_func, Bk_veran, Bk_reser).join(Bk_veran,(Bk_veran.veran_nr == Bk_func.veran_nr) & (Bk_veran.activeflag == 0)).join(Bk_reser,(Bk_reser.veran_nr == Bk_func.veran_nr) & (Bk_reser.veran_resnr == Bk_func.veran_seite) & (Bk_reser.resstatus <= 1)).filter(
             (Bk_func.datum < htparam.fdate) & (Bk_func.r_resstatus[inc_value(0)] <= 1)).order_by(Bk_func._recid).all():
        if bk_func._recid in bk_func_obj_list:
            continue
        else:
            bk_func_obj_list.append(bk_func._recid)

        if bk_reser.resstatus == 1:
            b_history = B_history()
            db_session.add(b_history)

            b_history.anlass[0] = bk_func.anlass[0]
            b_history.datum = bk_func.datum
            b_history.uhrzeit = bk_func.uhrzeit
            b_history.veran_nr = bk_func.veran_nr
            b_history.veran_seite = bk_func.veran_seite
            b_history.wochentag = bk_func.wochentag
            b_history.personen = bk_func.personen
            b_history.bestellt__durch = bk_func.bestellt__durch
            b_history.veranstalteranschrift[0] = bk_func.veranstalteranschrift[0]
            b_history.veranstalteranschrift[1] = bk_func.veranstalteranschrift[1]
            b_history.veranstalteranschrift[2] = bk_func.veranstalteranschrift[2]
            b_history.veranstalteranschrift[3] = bk_func.veranstalteranschrift[3]
            b_history.v_kontaktperson[0] = bk_func.v_kontaktperson[0]
            b_history.v_telefon = bk_func.v_telefon
            b_history.v_telefax = bk_func.v_telefax
            b_history.adurch = bk_func.adurch
            b_history.rechnungsanschrift[0] = bk_func.rechnungsanschrift[0]
            b_history.rechnungsanschrift[1] = bk_func.rechnungsanschrift[1]
            b_history.rechnungsanschrift[2] = bk_func.rechnungsanschrift[2]
            b_history.rechnungsanschrift[3] = bk_func.rechnungsanschrift[3]
            b_history.kontaktperson[0] = bk_func.kontaktperson[0]
            b_history.telefon = bk_func.telefon
            b_history.telefax = bk_func.telefax
            b_history.bemerkung = bk_func.bemerkung
            b_history.r_resstatus[0] = bk_func.r_resstatus[0]
            b_history.c_resstatus[0] = bk_func.c_resstatus[0]
            b_history.raeume[0] = bk_func.raeume[0]
            b_history.zweck[0] = bk_func.zweck[0]
            b_history.uhrzeiten[0] = bk_func.uhrzeiten[0]
            b_history.rpersonen[0] = bk_func.rpersonen[0]
            b_history.tischform[0] = bk_func.tischform[0]
            b_history.rpreis[0] = bk_func.rpreis[0]
            b_history.dekoration[0] = bk_func.dekoration[0]
            b_history.ape__getraenke[0] = bk_func.ape__getraenke[0]
            b_history.ape__getraenke[1] = bk_func.ape__getraenke[1]
            b_history.ape__getraenke[2] = bk_func.ape__getraenke[2]
            b_history.ape__getraenke[3] = bk_func.ape__getraenke[3]
            b_history.ape__getraenke[4] = bk_func.ape__getraenke[4]
            b_history.ape__getraenke[5] = bk_func.ape__getraenke[5]
            b_history.f_menu[0] = bk_func.f_menu[0]
            b_history.gema = bk_func.gema
            b_history.rpreis[6] = bk_func.rpreis[6]
            b_history.rpreis[7] = bk_func.rpreis[7]
            b_history.kartentext[0] = bk_func.kartentext[0]
            b_history.kartentext[1] = bk_func.kartentext[1]
            b_history.kartentext[2] = bk_func.kartentext[2]
            b_history.kartentext[3] = bk_func.kartentext[3]
            b_history.kartentext[4] = bk_func.kartentext[4]
            b_history.kartentext[5] = bk_func.kartentext[5]
            b_history.kartentext[6] = bk_func.kartentext[6]
            b_history.kartentext[7] = bk_func.kartentext[7]
            b_history.sonstiges[0] = bk_func.sonstiges[0]
            b_history.sonstiges[1] = bk_func.sonstiges[1]
            b_history.sonstiges[7] = bk_func.sonstiges[7]
            b_history.weine[0] = bk_func.weine[0]
            b_history.weine[1] = bk_func.weine[1]
            b_history.weine[2] = bk_func.weine[2]
            b_history.weine[3] = bk_func.weine[3]
            b_history.weine[4] = bk_func.weine[4]
            b_history.weine[5] = bk_func.weine[5]
            b_history.menue[0] = bk_func.menue[0]
            b_history.menue[1] = bk_func.menue[1]
            b_history.menue[2] = bk_func.menue[2]
            b_history.menue[3] = bk_func.menue[3]
            b_history.menue[4] = bk_func.menue[4]
            b_history.menue[5] = bk_func.menue[5]
            b_history.auf__datum = bk_func.auf__datum
            b_history.vgeschrieben = bk_func.vgeschrieben
            b_history.vkontrolliert = bk_func.vkontrolliert
            b_history.geschenk = bk_func.geschenk
            b_history.nadkarte[0] = bk_func.nadkarte[0]
            b_history.deposit =  to_decimal(bk_veran.deposit)
            b_history.limit_date = bk_veran.limit_date
            b_history.deposit_payment[0] = bk_veran.deposit_payment[0]
            b_history.deposit_payment[1] = bk_veran.deposit_payment[1]
            b_history.deposit_payment[2] = bk_veran.deposit_payment[2]
            b_history.deposit_payment[3] = bk_veran.deposit_payment[3]
            b_history.deposit_payment[4] = bk_veran.deposit_payment[4]
            b_history.deposit_payment[5] = bk_veran.deposit_payment[5]
            b_history.deposit_payment[6] = bk_veran.deposit_payment[6]
            b_history.deposit_payment[7] = bk_veran.deposit_payment[7]
            b_history.payment_date[0] = bk_veran.payment_date[0]
            b_history.payment_date[1] = bk_veran.payment_date[1]
            b_history.payment_date[2] = bk_veran.payment_date[2]
            b_history.payment_date[3] = bk_veran.payment_date[3]
            b_history.payment_date[4] = bk_veran.payment_date[4]
            b_history.payment_date[5] = bk_veran.payment_date[5]
            b_history.payment_date[6] = bk_veran.payment_date[6]
            b_history.payment_date[7] = bk_veran.payment_date[7]
            b_history.payment_userinit[0] = bk_veran.payment_userinit[0]
            b_history.payment_userinit[1] = bk_veran.payment_userinit[1]
            b_history.payment_userinit[2] = bk_veran.payment_userinit[2]
            b_history.payment_userinit[3] = bk_veran.payment_userinit[3]
            b_history.payment_userinit[4] = bk_veran.payment_userinit[4]
            b_history.payment_userinit[5] = bk_veran.payment_userinit[5]
            b_history.payment_userinit[6] = bk_veran.payment_userinit[6]
            b_history.payment_userinit[7] = bk_veran.payment_userinit[7]
            b_history.total_paid =  to_decimal(bk_veran.total_paid)
            b_history.betriebsnr = bk_func.betriebsnr

        bk_reser1 = db_session.query(Bk_reser1).filter(
                 (Bk_reser1._recid == bk_reser._recid)).first()
        bk_reser1.resstatus = 8

        fsl = db_session.query(Fsl).filter(
                 (Fsl._recid == bk_func._recid)).first()
        fsl.c_resstatus[0] = "I"
        fsl.r_resstatus[0] = 8

        bk_reser1 = db_session.query(Bk_reser1).filter(
                 (Bk_reser1.veran_nr == bk_func.veran_nr) & (Bk_reser1.resstatus <= 1)).first()

        if not bk_reser1:

            mres = db_session.query(Mres).filter(
                     (Mres._recid == bk_veran._recid)).first()
            mres.activeflag = 1

    return generate_output()