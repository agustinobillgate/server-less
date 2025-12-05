#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 25/7/2025
# gitlab: 614
# Rd, 28/11/2025, with_for_update added
#-----------------------------------------
from sqlalchemy.orm.attributes import flag_modified

from functions.additional_functions import *
from decimal import Decimal
from models import Bk_func, Bk_reser, Bk_veran, Guest, Bill, Akt_kont, Bk_raum, Queasy, Bk_rart

bkf_data, Bkf = create_model("Bkf", {"veran_nr":int, "veran_seite":int, "zweck":[string,6], "datum":date, "uhrzeit":string, "resstatus":int, "r_resstatus":[int,8], "c_resstatus":[string,8], "raeume":[string,6], "uhrzeiten":[string,6], "rpersonen":[int,8], "tischform":[string,6], "rpreis":[Decimal,8], "dekoration":[string,6], "begin_time":string, "ending_time":string, "begin_i":int, "ending_i":int, "bezeich":string})
fsl_data, Fsl = create_model_like(Bk_func, {"deposit":Decimal, "limit_date":date, "deposit_payment":[Decimal,9], "payment_date":[date,9], "total_paid":Decimal, "payment_userinit":[string,9], "betriebsnr2":int, "cutoff":date, "raum":string, "grund":[string,18], "in_sales":string, "in_conv":string})
glist_data, Glist = create_model("Glist", {"gastnr":int, "karteityp":int, "name":string, "telefon":string, "land":string, "plz":string, "wohnort":string, "adresse1":string, "adresse2":string, "adresse3":string, "namekontakt":string, "von_datum":date, "bis_datum":date, "von_zeit":string, "bis_zeit":string, "rstatus":int, "fax":string, "firmen_nr":int})

def main_fs_assign_page1bl(bkf_data:[Bkf], fsl_data:[Fsl], resnr:int, resline:int, bill_gastnr:int, 
                           en_gastnr:int, bkf_veran_nr:int, q3_list_veran_nr:int, q3_list_veran_seite:int, 
                           rsvsort:int, user_init:string, glist_data:[Glist]):

    prepare_cache ([Bk_veran, Guest, Bill, Akt_kont, Bk_raum, Bk_rart])

    total_depo = to_decimal("0.0")
    name_contact:string = ""
    flag1:bool = False
    flag2:bool = False
    flag3:bool = False
    bk_func = bk_reser = bk_veran = guest = bill = akt_kont = bk_raum = queasy = bk_rart = None

    bkfc = bkreser = fsl = bkf = glist = bk_reser1 = None

    Bkfc = create_buffer("Bkfc",Bk_func)
    Bkreser = create_buffer("Bkreser",Bk_reser)
    Bk_reser1 = create_buffer("Bk_reser1",Bk_reser)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal total_depo, name_contact, flag1, flag2, flag3, bk_func, bk_reser, bk_veran, guest, bill, akt_kont, bk_raum, queasy, bk_rart
        nonlocal resnr, resline, bill_gastnr, en_gastnr, bkf_veran_nr, q3_list_veran_nr, q3_list_veran_seite, rsvsort, user_init
        nonlocal bkfc, bkreser, bk_reser1


        nonlocal bkfc, bkreser, fsl, bkf, glist, bk_reser1

        return {"total_depo": total_depo, "glist": glist_data}

    def assign_changes():

        nonlocal total_depo, name_contact, flag1, flag2, flag3, bk_func, bk_reser, bk_veran, guest, bill, akt_kont, bk_raum, queasy, bk_rart
        nonlocal resnr, resline, bill_gastnr, en_gastnr, bkf_veran_nr, q3_list_veran_nr, q3_list_veran_seite, rsvsort, user_init
        nonlocal bkfc, bkreser, bk_reser1


        nonlocal bkfc, bkreser, fsl, bkf, glist, bk_reser1

        bk_f = None
        Bk_f =  create_buffer("Bk_f",Bk_func)
        total_depo =  to_decimal("0")
        pass

        bk_f_obj_list = {}
        for bk_f, bkreser in db_session.query(Bk_f, Bkreser).join(Bkreser,(Bkreser.veran_nr == q3_list_veran_nr) & (Bkreser.veran_resnr == q3_list_veran_seite) & (Bkreser.resstatus == rsvsort)).filter(
                 (Bk_f.veran_nr == q3_list_veran_nr)).order_by(Bk_f._recid).all():
            if bk_f_obj_list.get(bk_f._recid):
                continue
            else:
                bk_f_obj_list[bk_f._recid] = True


            total_depo =  to_decimal(total_depo) + to_decimal(bk_f.rpreis[0] + (bk_f.rpersonen[0]) * to_decimal(bk_f.rpreis[6]))
            bk_func.vkontrolliert = user_init
            bk_func.geschenk = to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "hh:mm:ss")
        pass

        for bk_rart in db_session.query(Bk_rart).filter(
                 (Bk_rart.veran_nr == q3_list_veran_nr)).order_by(Bk_rart._recid).all():
            total_depo =  to_decimal(total_depo) + to_decimal(bk_rart.preis)
        fsl.geschenk = bk_func.geschenk
        fsl.vkontrolliert = bk_func.vkontrolliert
        fsl.personen = bk_func.personen

        bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, bk_func.veran_nr)]})

        if bk_veran:
            bk_veran.segmentcode = fsl.segmentcode
            bk_veran.payment_userinit[8] = fsl.in_sales
            bk_veran.payment_userinit[8] = bk_veran.payment_userinit[8] + chr_unicode(2) + fsl.in_conv

        # bk_reser = get_cache (Bk_reser, {"veran_nr": [(eq, bk_veran.veran_nr)]})
        bk_reser = db_session.query(Bkreser).filter(
                 (Bkreser.veran_nr == bk_veran.veran_nr)).with_for_update().first()

        if bk_reser:
            bk_reser.limitdate = fsl.cutoff


    bk_func = get_cache (Bk_func, {"veran_nr": [(eq, resnr)],"veran_seite": [(eq, resline)]})
    flag3 = None != bk_func

    if bill_gastnr != 0:

        # bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, bkf_veran_nr)]})
        bk_veran = db_session.query(Bk_veran).filter(
                 (Bk_veran.veran_nr == bkf_veran_nr)).with_for_update().first()
        bk_veran.gastnrver = bill_gastnr
        pass

        if bk_veran.rechnr != 0:

            guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnrver)]})

            # bill = get_cache (Bill, {"rechnr": [(eq, bk_veran.rechnr)]})
            bill = db_session.query(Bill).filter(
                     (Bill.rechnr == bk_veran.rechnr)).with_for_update().first()
            bill.gastnr = bk_veran.gastnrver
            bill.name = guest.name + ", " + guest.vorname1 + guest.anredefirma
            pass

    if en_gastnr != 0:

        # bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, bkf_veran_nr)]})
        bk_veran = db_session.query(Bk_veran).filter(
                 (Bk_veran.veran_nr == bkf_veran_nr)).with_for_update().first()
        bk_veran.gastnr = en_gastnr
        pass

        guest = get_cache (Guest, {"gastnr": [(eq, bk_veran.gastnr)]})

        akt_kont = get_cache (Akt_kont, {"gastnr": [(eq, guest.gastnr)]})

        if akt_kont:
            name_contact = akt_kont.name + ", " + akt_kont.vorname + " " + akt_kont.anrede
        else:
            name_contact = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma

        glist = query(glist_data, filters=(lambda glist: glist.gastnr == bk_veran.gastnr), first=True)

        if not glist:
            glist_data.clear()
            glist = Glist()
            glist_data.append(glist)

            glist.gastnr = guest.gastnr
            glist.karteityp = guest.karteityp
            glist.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
            glist.adresse1 = guest.adresse1
            glist.adresse2 = guest.adresse2
            glist.adresse3 = guest.adresse3
            glist.telefon = guest.telefon
            glist.land = guest.land
            glist.plz = guest.plz
            glist.wohnort = guest.wohnort
            glist.namekontakt = name_contact
            glist.rstatus = bk_veran.resstatus
            glist.fax = guest.fax
            glist.firmen_nr = guest.firmen_nr

    fsl = query(fsl_data, first=True)

    for bkf in query(bkf_data):

        bkfc = db_session.query(Bkfc).filter(
                 (Bkfc.veran_nr == bkf.veran_nr) & (Bkfc.veran_seite == bkf.veran_seite)).with_for_update().first()

        bk_reser1 = db_session.query(Bk_reser1).filter(
                 (Bk_reser1.veran_nr == bkf.veran_nr) & (Bk_reser1.veran_resnr == bkf.veran_seite)).with_for_update().first()
        flag1 = None != bkfc
        flag2 = None != bk_reser1

        if flag1 and flag2:
            pass
            pass

            if bkfc.zweck[0] != bkf.zweck[0]:

                bk_veran = get_cache (Bk_veran, {"veran_nr": [(eq, bkf.veran_nr)]})
                bk_veran.anlass = bkf.zweck[0]
                pass

            if fsl.betriebsnr != 0:
                bkfc.betriebsnr = fsl.betriebsnr
            bkfc.v_kontaktperson[0] = fsl.v_kontaktperson[0]
            bkfc.v_telefon = fsl.v_telefon
            bkfc.v_telefax = fsl.v_telefax
            bkfc.bestellt__durch = fsl.bestellt__durch
            bkfc.veranstalteranschrift[0] = fsl.veranstalteranschrift[0]
            bkfc.veranstalteranschrift[1] = fsl.veranstalteranschrift[1]
            bkfc.veranstalteranschrift[2] = fsl.veranstalteranschrift[2]
            bkfc.veranstalteranschrift[3] = fsl.veranstalteranschrift[3]
            bkfc.veranstalteranschrift[4] = fsl.Veranstalteranschrift[4]
            bkfc.technik[0] = fsl.technik[0]
            bkfc.technik[1] = fsl.technik[1]
            bkfc.adurch = fsl.adurch
            bkfc.rechnungsanschrift[0] = fsl.rechnungsanschrift[0]
            bkfc.rechnungsanschrift[1] = fsl.rechnungsanschrift[1]
            bkfc.rechnungsanschrift[2] = fsl.rechnungsanschrift[2]
            bkfc.rechnungsanschrift[3] = fsl.rechnungsanschrift[3]
            bkfc.kontaktperson[0] = fsl.kontaktperson[0]
            bkfc.telefon = fsl.telefon
            bkfc.telefax = fsl.telefax
            bkfc.c_resstatus[0] = bkf.c_resstatus[0]
            bkfc.r_resstatus[0] = bkf.r_resstatus[0]
            bkfc.resstatus = bkf.resstatus
            bkfc.raeume[0] = bkf.raeume[0]
            bkfc.datum = bkf.datum
            bkfc.bis_datum = bkf.datum
            bkfc.zweck[0] = trim(bkf.zweck[0])
            bkfc.raumbezeichnung[7] = fsl.raumbezeichnung[7]
            bkfc.rpreis[0] = bkf.rpreis[0]
            bkfc.rpersonen[0] = bkf.rpersonen[0]
            bkfc.personen = bkf.rpersonen[0]
            bkfc.tischform[0] = bkf.tischform[0]
            bkfc.dekoration[0] = bkf.dekoration[0]
            bk_reser1.resstatus = bkfc.r_resstatus[0]
            bk_reser1.raum = bkfc.raeume[0]
            bk_reser1.datum = bkf.datum
            bk_reser1.bis_datum = bkf.datum
            bk_reser1.limitdate = fsl.cutoff

            if bkfc.uhrzeit != bkf.uhrzeit:
                bkfc.uhrzeit = to_string(bkf.begin_time, "99:99") + " - " + to_string(bkf.ending_time, "99:99")
                bkfc.uhrzeit = to_string(bkf.begin_time, "99:99") + " - " + to_string(bkf.ending_time, "99:99")
                bk_reser1.von_zeit = bkf.begin_time
                bk_reser1.von_i = bkf.begin_i
                bk_reser1.bis_zeit = bkf.ending_time
                bk_reser1.bis_i = bkf.ending_i
            fsl.rpersonen[0] = bkf.rpersonen[0]
            pass
            pass
        flag_modified(bkfc, "v_kontaktperson")
        flag_modified(bkfc, "veranstalteranschrift")
        flag_modified(bkfc, "technik")
        flag_modified(bkfc, "rechnungsanschrift")
        flag_modified(bkfc, "kontaktperson")
        flag_modified(bkfc, "c_resstatus")
        flag_modified(bkfc, "r_resstatus")
        flag_modified(bkfc, "raeume")
        flag_modified(bkfc, "rpreis")
        flag_modified(bkfc, "rpersonen")
        flag_modified(bkfc, "personen")
        flag_modified(bkfc, "tischform")
        flag_modified(bkfc, "zweck")
        flag_modified(bkfc, "adurch")
        flag_modified(bkfc, "raumbezeichnung")

        # bk_raum = get_cache (Bk_raum, {"raum": [(eq, bkf.raeume[0])],"bezeich": [(eq, bkf.bezeich)]})
        bk_raum = db_session.query(Bk_raum).filter(
                 (Bk_raum.raum == bkf.raeume[0]) &
                 (Bk_raum.bezeich == bkf.bezeich)).with_for_update().first()

        if bk_raum:
            pass
            bk_raum.bezeich = bkf.bezeich


            pass

            # queasy = get_cache (Queasy, {"key": [(eq, 210)],"number1": [(eq, bkf.veran_nr)],"number2": [(eq, bkf.veran_seite)]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 210) &
                     (Queasy.number1 == bkf.veran_nr) &
                     (Queasy.number2 == bkf.veran_seite)).with_for_update().first

            if queasy:
                db_session.delete(queasy)
                pass
        else:

            # queasy = get_cache (Queasy, {"key": [(eq, 210)],"number1": [(eq, bkf.veran_nr)],"number2": [(eq, bkf.veran_seite)]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 210) &
                     (Queasy.number1 == bkf.veran_nr) &
                     (Queasy.number2 == bkf.veran_seite)).with_for_update().first()

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 210
                queasy.number1 = bkf.veran_nr
                queasy.number2 = bkf.veran_seite
                queasy.char1 = bkf.bezeich


            else:
                pass
                queasy.key = 210
                queasy.number1 = bkf.veran_nr
                queasy.number2 = bkf.veran_seite
                queasy.char1 = bkf.bezeich


                pass
    assign_changes()

    return generate_output()