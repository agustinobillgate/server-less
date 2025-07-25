#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 25/7/2025
# gitlab: 587
# lower case Veranstalteranschrift
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Bk_func, B_storno, Bk_veran, Bk_reser, Bk_raum, Queasy, Guest, Bediener, Res_line, Zimkateg

def main_fs_create_fslbl(b1_resnr:int, b1_resline:int, bk_veran_recid:int, rsvsort:int, curr_gastnr:int):

    prepare_cache ([Bk_func, Bk_veran, Bk_reser, Bk_raum, Queasy, Guest, Bediener, Res_line, Zimkateg])

    resnr = 0
    resline = 0
    sales_id = ""
    sob = ""
    segcode = ""
    rmtype = ""
    rmno = ""
    roomrate = ""
    ci_date = None
    co_date = None
    sum_room = 0
    sum_room_cat = ""
    venue = ""
    fsl_data = []
    bkf_data = []
    bstorno_data = []
    bk_func = b_storno = bk_veran = bk_reser = bk_raum = queasy = guest = bediener = res_line = zimkateg = None

    fsl = bkf = bstorno = zinr_list = None

    fsl_data, Fsl = create_model_like(Bk_func, {"deposit":Decimal, "limit_date":date, "deposit_payment":[Decimal,9], "payment_date":[date,9], "total_paid":Decimal, "payment_userinit":[string,9], "betriebsnr2":int, "cutoff":date, "raum":string, "grund":[string,18], "in_sales":string, "in_conv":string})
    bkf_data, Bkf = create_model("Bkf", {"veran_nr":int, "veran_seite":int, "zweck":[string,6], "datum":date, "uhrzeit":string, "resstatus":int, "r_resstatus":[int,8], "c_resstatus":[string,8], "raeume":[string,6], "uhrzeiten":[string,6], "rpersonen":[int,8], "tischform":[string,6], "rpreis":[Decimal,8], "dekoration":[string,6], "begin_time":string, "ending_time":string, "begin_i":int, "ending_i":int, "bezeich":string})
    bstorno_data, Bstorno = create_model_like(B_storno)
    zinr_list_data, Zinr_list = create_model("Zinr_list", {"room_cat":string, "jml_room":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal resnr, resline, sales_id, sob, segcode, rmtype, rmno, roomrate, ci_date, co_date, sum_room, sum_room_cat, venue, fsl_data, bkf_data, bstorno_data, bk_func, b_storno, bk_veran, bk_reser, bk_raum, queasy, guest, bediener, res_line, zimkateg
        nonlocal b1_resnr, b1_resline, bk_veran_recid, rsvsort, curr_gastnr


        nonlocal fsl, bkf, bstorno, zinr_list
        nonlocal fsl_data, bkf_data, bstorno_data, zinr_list_data

        return {"resnr": resnr, "resline": resline, "sales_id": sales_id, "sob": sob, "segcode": segcode, "rmtype": rmtype, "rmno": rmno, "roomrate": roomrate, "ci_date": ci_date, "co_date": co_date, "sum_room": sum_room, "sum_room_cat": sum_room_cat, "venue": venue, "fsl": fsl_data, "bkf": bkf_data, "bstorno": bstorno_data}


    bk_veran = get_cache (Bk_veran, {"_recid": [(eq, bk_veran_recid)]})

    if not bk_veran:

        return generate_output()

    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, b1_resnr)],"veran_resnr": [(eq, b1_resline)]})

    if not bk_reser:

        return generate_output()
    resnr = bk_veran.veran_nr
    resline = bk_reser.veran_seite
    resline = bk_reser.veran_seite
    fsl_data.clear()
    bkf_data.clear()

    for bk_func in db_session.query(Bk_func).filter(
             (Bk_func.veran_nr == bk_veran.veran_nr) & (Bk_func.resstatus == rsvsort)).order_by(Bk_func._recid).all():
        bkf = Bkf()
        bkf_data.append(bkf)

        bkf.veran_nr = bk_func.veran_nr
        bkf.veran_seite = bk_func.veran_seite
        bkf.datum = bk_func.datum
        bkf.uhrzeit = bk_func.uhrzeit
        bkf.resstatus = bk_func.resstatus
        bkf.r_resstatus[0] = bk_func.r_resstatus[0]
        bkf.c_resstatus[0] = bk_func.c_resstatus[0]
        bkf.raeume[0] = bk_func.raeume[0]
        bkf.rpersonen[0] = bk_func.rpersonen[0]
        bkf.tischform[0] = bk_func.tischform[0]
        bkf.rpreis[0] = bk_func.rpreis[0]
        bkf.dekoration[0] = bk_func.dekoration[0]

        if num_entries(bk_func.zweck[0], chr_unicode(2)) >= 2:
            bkf.zweck[0] = entry(0, bk_func.zweck[0], chr_unicode(2))
        else:
            bkf.zweck[0] = bk_func.zweck[0]

        bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_func.raeume[0])]})

        if bk_raum:

            queasy = get_cache (Queasy, {"key": [(eq, 210)],"number1": [(eq, bk_func.veran_nr)],"number2": [(eq, bk_func.veran_seite)]})

            if queasy:
                bkf.bezeich = queasy.char1


            else:
                bkf.bezeich = bk_raum.bezeich

    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, resnr)]})

    guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

    bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})
    fsl = Fsl()
    fsl_data.append(fsl)

    fsl.datum = bk_func.datum
    fsl.uhrzeit = bk_func.uhrzeit
    fsl.technik[0] = bk_func.technik[0]
    fsl.technik[1] = bk_func.technik[1]
    fsl.veran_nr = bk_func.veran_nr
    fsl.veran_seite = bk_func.veran_seite
    fsl.wochentag = bk_func.wochentag
    fsl.bestellt__durch = bk_func.bestellt__durch
    fsl.veranstalteranschrift[0] = bk_func.veranstalteranschrift[0]
    fsl.veranstalteranschrift[1] = bk_func.veranstalteranschrift[1]
    fsl.veranstalteranschrift[2] = bk_func.veranstalteranschrift[2]
    fsl.veranstalteranschrift[3] = bk_func.veranstalteranschrift[3]

    # Rd, 25/7/2025
    # lower case
    # fsl.veranstalteranschrift[4] = bk_func.Veranstalteranschrift[4]
    fsl.veranstalteranschrift[4] = bk_func.veranstalteranschrift[4]
    
    fsl.v_kontaktperson[0] = bk_func.v_kontaktperson[0]
    fsl.v_telefon = bk_func.v_telefon
    fsl.v_telefax = bk_func.v_telefax
    fsl.adurch = bk_func.adurch
    fsl.rechnungsanschrift[0] = bk_func.rechnungsanschrift[0]
    fsl.rechnungsanschrift[1] = bk_func.rechnungsanschrift[1]
    fsl.rechnungsanschrift[2] = bk_func.rechnungsanschrift[2]
    fsl.rechnungsanschrift[3] = bk_func.rechnungsanschrift[3]
    fsl.kontaktperson[0] = bk_func.kontaktperson[0]
    fsl.telefon = bk_func.telefon
    fsl.telefax = bk_func.telefax
    fsl.r_resstatus[0] = bk_func.r_resstatus[0]
    fsl.c_resstatus[0] = bk_func.c_resstatus[0]
    fsl.raeume[0] = bk_func.raeume[0]
    fsl.uhrzeiten[0] = bk_func.uhrzeiten[0]
    fsl.rpersonen[0] = bk_func.rpersonen[0]
    fsl.tischform[0] = bk_func.tischform[0]
    fsl.rpreis[0] = bk_func.rpreis[0]
    fsl.dekoration[0] = bk_func.dekoration[0]
    fsl.ape__getraenke[0] = bk_func.ape__getraenke[0]
    fsl.ape__getraenke[1] = bk_func.ape__getraenke[1]
    fsl.ape__getraenke[2] = bk_func.ape__getraenke[2]
    fsl.ape__getraenke[3] = bk_func.ape__getraenke[3]
    fsl.ape__getraenke[4] = bk_func.ape__getraenke[4]
    fsl.ape__getraenke[5] = bk_func.ape__getraenke[5]
    fsl.ape__getraenke[6] = bk_func.ape__getraenke[6]
    fsl.ape__getraenke[7] = bk_func.ape__getraenke[7]
    fsl.bemerkung = bk_func.bemerkung
    fsl.f_menu[0] = bk_func.f_menu[0]
    fsl.gema = bk_func.gema
    fsl.rpreis[6] = bk_func.rpreis[6]
    fsl.rpreis[7] = bk_func.rpreis[7]
    fsl.kartentext[0] = bk_func.kartentext[0]
    fsl.kartentext[1] = bk_func.kartentext[1]
    fsl.kartentext[2] = bk_func.kartentext[2]
    fsl.kartentext[3] = bk_func.kartentext[3]
    fsl.kartentext[4] = bk_func.kartentext[4]
    fsl.kartentext[5] = bk_func.kartentext[5]
    fsl.kartentext[6] = bk_func.kartentext[6]
    fsl.kartentext[7] = bk_func.kartentext[7]
    fsl.sonstiges[0] = bk_func.sonstiges[0]
    fsl.sonstiges[1] = bk_func.sonstiges[1]
    fsl.sonstiges[2] = bk_func.sonstiges[2]
    fsl.sonstiges[3] = bk_func.sonstiges[3]
    fsl.weine[0] = bk_func.weine[0]
    fsl.weine[1] = bk_func.weine[1]
    fsl.weine[2] = bk_func.weine[2]
    fsl.weine[3] = bk_func.weine[3]
    fsl.weine[4] = bk_func.weine[4]
    fsl.weine[5] = bk_func.weine[5]
    fsl.menue[0] = bk_func.menue[0]
    fsl.menue[1] = bk_func.menue[1]
    fsl.menue[2] = bk_func.menue[2]
    fsl.menue[3] = bk_func.menue[3]
    fsl.menue[4] = bk_func.menue[4]
    fsl.menue[5] = bk_func.menue[5]
    fsl.auf__datum = bk_func.auf__datum
    fsl.vgeschrieben = bk_func.vgeschrieben
    fsl.vkontrolliert = bk_func.vkontrolliert
    fsl.geschenk = bk_func.geschenk
    fsl.nadkarte[0] = bk_func.nadkarte[0]
    fsl.deposit =  to_decimal(bk_veran.deposit)
    fsl.limit_date = bk_veran.limit_date
    fsl.deposit_payment[0] = bk_veran.deposit_payment[0]
    fsl.deposit_payment[1] = bk_veran.deposit_payment[1]
    fsl.deposit_payment[2] = bk_veran.deposit_payment[2]
    fsl.deposit_payment[3] = bk_veran.deposit_payment[3]
    fsl.deposit_payment[4] = bk_veran.deposit_payment[4]
    fsl.deposit_payment[5] = bk_veran.deposit_payment[5]
    fsl.deposit_payment[6] = bk_veran.deposit_payment[6]
    fsl.deposit_payment[7] = bk_veran.deposit_payment[7]
    fsl.deposit_payment[8] = - bk_veran.deposit_payment[8]
    fsl.payment_date[0] = bk_veran.payment_date[0]
    fsl.payment_date[1] = bk_veran.payment_date[1]
    fsl.payment_date[2] = bk_veran.payment_date[2]
    fsl.payment_date[3] = bk_veran.payment_date[3]
    fsl.payment_date[4] = bk_veran.payment_date[4]
    fsl.payment_date[5] = bk_veran.payment_date[5]
    fsl.payment_date[6] = bk_veran.payment_date[6]
    fsl.payment_date[7] = bk_veran.payment_date[7]
    fsl.payment_userinit[0] = bk_veran.payment_userinit[0]
    fsl.payment_userinit[1] = bk_veran.payment_userinit[1]
    fsl.payment_userinit[2] = bk_veran.payment_userinit[2]
    fsl.payment_userinit[3] = bk_veran.payment_userinit[3]
    fsl.payment_userinit[4] = bk_veran.payment_userinit[4]
    fsl.payment_userinit[5] = bk_veran.payment_userinit[5]
    fsl.payment_userinit[6] = bk_veran.payment_userinit[6]
    fsl.payment_userinit[7] = bk_veran.payment_userinit[7]
    fsl.total_paid =  to_decimal(bk_veran.total_paid)
    fsl.segmentcode = bk_veran.segmentcode
    fsl.raumbezeichnung[7] = bk_func.raumbezeichnung[7]

    if num_entries(bk_func.zweck[0], chr_unicode(2)) >= 2:
        fsl.zweck[0] = entry(1, bk_func.zweck[0], chr_unicode(2))
    else:
        fsl.zweck[0] = bk_func.zweck[0]

    if num_entries(bk_veran.payment_userinit[8], chr_unicode(2)) >= 2:
        fsl.in_sales = entry(0, bk_veran.payment_userinit[8], chr_unicode(2))
        fsl.in_conv = entry(1, bk_veran.payment_userinit[8], chr_unicode(2))
    else:
        fsl.in_sales = guest.phonetik3
        fsl.in_conv = guest.phonetik2

    bediener = get_cache (Bediener, {"userinit": [(eq, fsl.in_sales)]})

    if bediener:
        sales_id = bediener.username

    b_storno = get_cache (B_storno, {"bankettnr": [(eq, b1_resnr)],"breslinnr": [(eq, b1_resline)],"gastnr": [(eq, curr_gastnr)]})

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

    bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, resnr)]})

    if bk_reser:
        fsl.cutoff = bk_reser.limitdate
        fsl.raum = bk_reser.raum

    for b_storno in db_session.query(B_storno).filter(
             (B_storno.bankettnr == b1_resnr) & (B_storno.breslinnr == b1_resline) & (B_storno.gastnr == curr_gastnr)).order_by(B_storno._recid).all():
        bstorno = Bstorno()
        bstorno_data.append(bstorno)

        buffer_copy(b_storno, bstorno)

    bk_raum = get_cache (Bk_raum, {"raum": [(eq, bk_func.raeume[0])]})

    if bk_raum:
        venue = bk_raum.bezeich

    queasy = get_cache (Queasy, {"key": [(eq, 151)],"char1": [(eq, to_string(bk_func.technik[1]))]})

    if queasy:
        sob = queasy.char3

    bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, bk_func.veran_nr)]})

    if bk_veran:

        queasy = get_cache (Queasy, {"key": [(eq, 146)],"char1": [(eq, to_string(bk_veran.segmentcode))]})

        if queasy:
            segcode = queasy.char3

    for res_line in db_session.query(Res_line).filter(
             (Res_line.gastnr == bk_func.betriebsnr) & (Res_line.ankunft <= bk_func.datum) & (Res_line.abreise >= bk_func.datum)).order_by(Res_line._recid).all():
        rmno = res_line.zinr + chr_unicode(10) + rmno
        roomrate = to_string(res_line.zipreis, ">,>>>,>>>,>>9.99") + chr_unicode(10) + roomrate
        ci_date = res_line.ankunft
        co_date = res_line.abreise
        sum_room = sum_room + 1

        zimkateg = get_cache (Zimkateg, {"zikatnr": [(eq, res_line.zikatnr)]})

        if zimkateg:
            rmtype = zimkateg.kurzbez + chr_unicode(10) + rmtype

            zinr_list = query(zinr_list_data, filters=(lambda zinr_list: zinr_list.room_cat == zimkateg.kurzbez), first=True)

            if zinr_list:
                zinr_list.jml_room = zinr_list.jml_room + 1

            if not zinr_list:
                zinr_list = Zinr_list()
                zinr_list_data.append(zinr_list)

                zinr_list.room_cat = zimkateg.kurzbez
                zinr_list.jml_room = 1

    for zinr_list in query(zinr_list_data):
        sum_room_cat = to_string(zinr_list.jml_room) + chr_unicode(10) + sum_room_cat

    return generate_output()