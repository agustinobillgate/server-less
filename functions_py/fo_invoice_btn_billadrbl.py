#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 05/11/2025
# to_int(res_line.code))]}) -> to_int(res_line.code.strip()))}).first() 
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import Bill, Guest, Bediener, Res_line, Res_history, Reservation, Queasy, Waehrung

def fo_invoice_btn_billadrbl(gastpay:int, bil_recid:int, user_init:string):

    prepare_cache ([Bill, Guest, Bediener, Res_line, Res_history, Reservation, Queasy, Waehrung])

    art_no = 0
    resname = ""
    rescomment = ""
    r_gastnrpay = 0
    bill_gastnr = 0
    bill_name = ""
    g_address:string = ""
    g_wonhort:string = ""
    g_plz:string = ""
    g_land:string = ""
    curr_gastnr:int = 0
    bill = guest = bediener = res_line = res_history = reservation = queasy = waehrung = None

    bbuff = gbuff = None

    Bbuff = create_buffer("Bbuff",Bill)
    Gbuff = create_buffer("Gbuff",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_no, resname, rescomment, r_gastnrpay, bill_gastnr, bill_name, g_address, g_wonhort, g_plz, g_land, curr_gastnr, bill, guest, bediener, res_line, res_history, reservation, queasy, waehrung
        nonlocal gastpay, bil_recid, user_init
        nonlocal bbuff, gbuff


        nonlocal bbuff, gbuff

        return {"art_no": art_no, "resname": resname, "rescomment": rescomment, "r_gastnrpay": r_gastnrpay, "bill_gastnr": bill_gastnr, "bill_name": bill_name}

    def fill_rescomment(fill_co:bool):

        nonlocal art_no, resname, rescomment, r_gastnrpay, bill_gastnr, bill_name, g_address, g_wonhort, g_plz, g_land, curr_gastnr, bill, guest, bediener, res_line, res_history, reservation, queasy, waehrung
        nonlocal gastpay, bil_recid, user_init
        nonlocal bbuff, gbuff


        nonlocal bbuff, gbuff

        guestmember = None
        usr = None
        resbuff = None
        rbuff = None
        Guestmember =  create_buffer("Guestmember",Guest)
        Usr =  create_buffer("Usr",Bediener)
        Resbuff =  create_buffer("Resbuff",Res_line)
        Rbuff =  create_buffer("Rbuff",Res_line)

        reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})

        if res_line:

            guestmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        if bill.reslinnr > 0:

            resbuff = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.parent_nr)]})
        rescomment = ""

        if fill_co:

            usr = get_cache (Bediener, {"userinit": [(eq, bill.vesrcod)]})

            if usr:
                rescomment = rescomment + "C/O by: " + usr.username + chr_unicode(10)

        if resbuff and trim(entry(0, resbuff.memozinr, ";")) != "":

            rbuff = get_cache (Res_line, {"zinr": [(eq, trim(entry(0, resbuff.memozinr, ";")))],"resstatus": [(eq, 6)]})

            if rbuff:
                rescomment = rescomment + "Transf " + resbuff.zinr + " -> " + entry(0, resbuff.memozinr, ";") + " " + rbuff.name + chr_unicode(10)
            else:
                rescomment = rescomment + "Transf " + resbuff.zinr + " -> " + entry(0, resbuff.memozinr, ";") + chr_unicode(10)

        if resbuff and resbuff.code != "":

            # queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code.strip()))]})
            queasy = db_session.query(Queasy).filter(
                     (Queasy.key == 9) & (Queasy.number1 == to_int(resbuff.code.strip()))).first()

            if queasy:
                rescomment = rescomment + queasy.char1 + chr_unicode(10)

        if res_line and res_line.bemerk != "":
            rescomment = rescomment + res_line.bemerk

        if reservation and reservation.bemerk != "":
            rescomment = rescomment + reservation.bemerk + chr_unicode(10)

        if guestmember and guestmember.bemerk != "":
            rescomment = rescomment + guestmember.bemerk + chr_unicode(10)

        if res_line:

            waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

        if resbuff:
            rescomment = rescomment + "Arr " + to_string(resbuff.ankunft) + " Dep " + to_string(resbuff.abreise) + " A " + to_string(resbuff.erwachs) + " Ch " + to_string(resbuff.kind1) + " Ch " + to_string(resbuff.kind2) + " Com " + to_string(resbuff.gratis) + chr_unicode(10) + "Argt " + resbuff.arrangement

        if waehrung:
            rescomment = rescomment + ">>Currency " + waehrung.wabkurz + chr_unicode(10)
        else:
            rescomment = rescomment + chr_unicode(10)

    bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

    bbuff = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    guest = get_cache (Guest, {"gastnr": [(eq, gastpay)]})

    if bbuff:

        bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})
        g_address = guest.adresse1
        g_wonhort = guest.wohnort
        g_plz = guest.plz
        g_land = guest.land

        if g_address == None:
            g_address = ""

        if g_wonhort == None:
            g_wonhort = ""

        if g_plz == None:
            g_plz = ""

        if g_land == None:
            g_land = ""
        curr_gastnr = bill.gastnr
        art_no = guest.zahlungsart
        bill.gastnr = guest.gastnr
        bill.name = guest.name
        bill_gastnr = bill.gastnr
        bill_name = bill.name
        r_gastnrpay = guest.gastnr
        resname = guest.name + ", " + guest.vorname1 + guest.anredefirma +\
                " " + guest.anrede1 +\
                chr_unicode(10) + g_address +\
                chr_unicode(10) + g_wonhort + " " + g_plz +\
                chr_unicode(10) + g_land

        if bill.resnr > 0 and bill.reslinnr > 0:

            res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

            if res_line:
                res_line.gastnrpay = guest.gastnr
                pass
        fill_rescomment(False)

        if curr_gastnr != gastpay:

            gbuff = get_cache (Guest, {"gastnr": [(eq, curr_gastnr)]})
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.betriebsnr = bediener.nr
            res_history.resnr = bill.resnr
            res_history.reslinnr = bill.reslinnr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.action = "Bill Receiver Changed"
            res_history.aenderung = gbuff.name + chr_unicode(10) + chr_unicode(10) +\
                    "*** Changed to:" + chr_unicode(10) + chr_unicode(10) +\
                    guest.name + chr_unicode(10) + chr_unicode(10) +\
                    "*** Bill No: " + to_string(bill.rechnr)


            pass
            pass
    else:

        return generate_output()

    return generate_output()