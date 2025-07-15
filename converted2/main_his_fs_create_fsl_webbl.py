#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import B_history, Bk_veran, Guest, B_storno, Bk_reser

def main_his_fs_create_fsl_webbl(inresnr:int, inresline:int):

    prepare_cache ([B_history, Bk_veran, Guest, B_storno, Bk_reser])

    curr_gastnr = 0
    bkf_data = []
    fsl_data = []
    flag_his = True
    b_history = bk_veran = guest = b_storno = bk_reser = None

    bkf = fsl = None

    bkf_data, Bkf = create_model_like(B_history)
    fsl_data, Fsl = create_model_like(B_history, {"cutoff":date, "grund":[string,18], "in_sales":string, "in_conv":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal curr_gastnr, bkf_data, fsl_data, flag_his, b_history, bk_veran, guest, b_storno, bk_reser
        nonlocal inresnr, inresline


        nonlocal bkf, fsl
        nonlocal bkf_data, fsl_data

        return {"curr_gastnr": curr_gastnr, "bkf": bkf_data, "fsl": fsl_data, "flag_his": flag_his}


    for b_history in db_session.query(B_history).filter(
             (B_history.veran_nr == inresnr) & (B_history.veran_seite == inresline)).order_by(B_history._recid).all():
        bkf = Bkf()
        bkf_data.append(bkf)

        bkf.veran_nr = b_history.veran_nr
        bkf.veran_seite = b_history.veran_seite
        bkf.zweck[0] = entry(0, b_history.zweck[0], chr_unicode(2))
        bkf.datum = b_history.datum
        bkf.uhrzeit = b_history.uhrzeit
        bkf.r_resstatus[0] = b_history.r_resstatus[0]
        bkf.c_resstatus[0] = b_history.c_resstatus[0]
        bkf.raeume[0] = b_history.raeume[0]
        bkf.uhrzeiten[0] = b_history.uhrzeiten[0]
        bkf.rpersonen[0] = b_history.rpersonen[0]
        bkf.tischform[0] = b_history.tischform[0]
        bkf.rpreis[0] = b_history.rpreis[0]
        bkf.dekoration[0] = b_history.dekoration[0]

    b_history = get_cache (B_history, {"veran_nr": [(eq, inresnr)],"veran_seite": [(eq, inresline)]})

    if b_history:
        fsl = Fsl()
        fsl_data.append(fsl)

        fsl.datum = b_history.datum
        fsl.uhrzeit = b_history.uhrzeit
        fsl.veran_nr = b_history.veran_nr
        fsl.veran_seite = b_history.veran_seite
        fsl.wochentag = b_history.wochentag
        fsl.bestellt__durch = b_history.bestellt__durch
        fsl.segmentcode = b_history.segmentcode
        fsl.veranstalteranschrift[0] = b_history.veranstalteranschrift[0]
        fsl.veranstalteranschrift[1] = b_history.veranstalteranschrift[1]
        fsl.veranstalteranschrift[2] = b_history.veranstalteranschrift[2]
        fsl.veranstalteranschrift[3] = b_history.veranstalteranschrift[3]
        fsl.veranstalteranschrift[4] = b_history.veranstalteranschrift[4]
        fsl.segmentcode = b_history.segmentcode
        fsl.limit_date = b_history.limit_date
        fsl.v_kontaktperson[0] = b_history.v_kontaktperson[0]
        fsl.v_telefon = b_history.v_telefon
        fsl.v_telefax = b_history.v_telefax
        fsl.adurch = b_history.adurch
        fsl.rechnungsanschrift[0] = b_history.rechnungsanschrift[0]
        fsl.rechnungsanschrift[1] = b_history.rechnungsanschrift[1]
        fsl.rechnungsanschrift[2] = b_history.rechnungsanschrift[2]
        fsl.rechnungsanschrift[3] = b_history.rechnungsanschrift[3]
        fsl.kontaktperson[0] = b_history.kontaktperson[0]
        fsl.telefon = b_history.telefon
        fsl.telefax = b_history.telefax
        fsl.r_resstatus[0] = b_history.r_resstatus[0]
        fsl.c_resstatus[0] = b_history.c_resstatus[0]
        fsl.raeume[0] = b_history.raeume[0]
        fsl.uhrzeiten[0] = b_history.uhrzeiten[0]
        fsl.rpersonen[0] = b_history.rpersonen[0]
        fsl.tischform[0] = b_history.tischform[0]
        fsl.rpreis[0] = b_history.rpreis[0]
        fsl.dekoration[0] = b_history.dekoration[0]
        fsl.ape__getraenke[0] = b_history.ape__getraenke[0]
        fsl.ape__getraenke[1] = b_history.ape__getraenke[1]
        fsl.ape__getraenke[2] = b_history.ape__getraenke[2]
        fsl.ape__getraenke[3] = b_history.ape__getraenke[3]
        fsl.ape__getraenke[4] = b_history.ape__getraenke[4]
        fsl.ape__getraenke[5] = b_history.ape__getraenke[5]
        fsl.ape__getraenke[6] = b_history.ape__getraenke[6]
        fsl.ape__getraenke[7] = b_history.ape__getraenke[7]
        fsl.ape__getraenke[2] = b_history.ape__getraenke[2]
        fsl.bemerkung = b_history.bemerkung
        fsl.f_menu[0] = b_history.f_menu[0]
        fsl.gema = b_history.gema
        fsl.rpreis[6] = b_history.rpreis[6]
        fsl.rpreis[7] = b_history.rpreis[7]
        fsl.kartentext[0] = b_history.kartentext[0]
        fsl.kartentext[1] = b_history.kartentext[1]
        fsl.kartentext[2] = b_history.kartentext[2]
        fsl.kartentext[3] = b_history.kartentext[3]
        fsl.kartentext[4] = b_history.kartentext[4]
        fsl.kartentext[5] = b_history.kartentext[5]
        fsl.kartentext[6] = b_history.kartentext[6]
        fsl.kartentext[7] = b_history.kartentext[7]
        fsl.sonstiges[0] = b_history.sonstiges[0]
        fsl.sonstiges[1] = b_history.sonstiges[1]
        fsl.sonstiges[2] = b_history.sonstiges[2]
        fsl.sonstiges[3] = b_history.sonstiges[3]
        fsl.auf__datum = b_history.auf__datum
        fsl.vgeschrieben = b_history.vgeschrieben
        fsl.vkontrolliert = b_history.vkontrolliert
        fsl.geschenk = b_history.geschenk
        fsl.nadkarte[0] = b_history.nadkarte[0]
        fsl.deposit =  to_decimal(b_history.deposit)
        fsl.limit_date = b_history.limit_date
        fsl.deposit_payment[0] = b_history.deposit_payment[0]
        fsl.deposit_payment[1] = b_history.deposit_payment[1]
        fsl.deposit_payment[2] = b_history.deposit_payment[2]
        fsl.deposit_payment[3] = b_history.deposit_payment[3]
        fsl.deposit_payment[4] = b_history.deposit_payment[4]
        fsl.payment_date[0] = b_history.payment_date[0]
        fsl.payment_date[1] = b_history.payment_date[1]
        fsl.payment_date[2] = b_history.payment_date[2]
        fsl.payment_date[3] = b_history.payment_date[3]
        fsl.payment_date[4] = b_history.payment_date[4]
        fsl.payment_userinit[0] = b_history.payment_userinit[0]
        fsl.payment_userinit[1] = b_history.payment_userinit[1]
        fsl.payment_userinit[2] = b_history.payment_userinit[2]
        fsl.payment_userinit[3] = b_history.payment_userinit[3]
        fsl.payment_userinit[4] = b_history.payment_userinit[4]
        fsl.total_paid =  to_decimal(b_history.total_paid)
        fsl.raumbezeichnung[7] = b_history.raumbezeichnung[7]

        if num_entries(b_history.zweck[0], chr_unicode(2)) >= 2:
            fsl.zweck[0] = entry(1, b_history.zweck[0], chr_unicode(2))
        else:
            fsl.zweck[0] = b_history.zweck[0]

        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, b_history.veran_nr)]})
        curr_gastnr = bk_veran.gastnr

        guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

        if num_entries(b_history.payment_userinit[8], chr_unicode(2)) >= 2:
            fsl.in_sales = entry(0, b_history.payment_userinit[8], chr_unicode(2))
            fsl.in_conv = entry(1, b_history.payment_userinit[8], chr_unicode(2))
        else:
            fsl.in_sales = guest.phonetik3
            fsl.in_conv = guest.phonetik2

        b_storno = get_cache (B_storno, {"bankettnr": [(eq, inresnr)],"breslinnr": [(eq, inresline)]})

        if b_storno:
            fsl.grund[0] = b_storno.grund[0]
            fsl.grund[1] = b_storno.grund[1]
            fsl.grund[2] = b_storno.grund[2]
            fsl.grund[3] = b_storno.grund[3]
            fsl.grund[4] = b_storno.grund[4]
            fsl.grund[5] = b_storno.grund[5]
            fsl.grund[6] = b_storno.grund[6]
            fsl.grund[7] = b_storno.grund[7]
            fsl.grund[8] = b_storno.grund[8]
            fsl.grund[9] = b_storno.grund[9]

        bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, inresnr)]})

        if bk_reser:
            fsl.cutoff = bk_reser.limitdate

    return generate_output()