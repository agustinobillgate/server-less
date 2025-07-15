#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from models import Bediener, Res_line, Guest, Bill, Reservation, Queasy, Waehrung

def fo_invoice_fill_rescommentbl(bil_recid:int, fill_co:bool):

    prepare_cache ([Bediener, Res_line, Guest, Bill, Reservation, Queasy, Waehrung])

    rescomment = ""
    bediener = res_line = guest = bill = reservation = queasy = waehrung = None

    usr = resbuff = rbuff = guestmember = None

    Usr = create_buffer("Usr",Bediener)
    Resbuff = create_buffer("Resbuff",Res_line)
    Rbuff = create_buffer("Rbuff",Res_line)
    Guestmember = create_buffer("Guestmember",Guest)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal rescomment, bediener, res_line, guest, bill, reservation, queasy, waehrung
        nonlocal bil_recid, fill_co
        nonlocal usr, resbuff, rbuff, guestmember


        nonlocal usr, resbuff, rbuff, guestmember

        return {"rescomment": rescomment}


    bill = get_cache (Bill, {"_recid": [(eq, bil_recid)]})

    if not bill:

        return generate_output()

    res_line = get_cache (Res_line, {"resnr": [(eq, bill.resnr)],"reslinnr": [(eq, bill.reslinnr)]})

    reservation = get_cache (Reservation, {"resnr": [(eq, bill.resnr)]})

    if res_line:

        guestmember = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

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

        queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code))]})

        if queasy:
            rescomment = rescomment + queasy.char1 + chr_unicode(10)

    if bill.vesrdepot != "":
        rescomment = rescomment + bill.vesrdepot + chr_unicode(10)

    if res_line and res_line.bemerk != "":
        rescomment = rescomment + res_line.bemerk + chr_unicode(10)

    if reservation and reservation.bemerk != "":
        rescomment = rescomment + reservation.bemerk + chr_unicode(10)

    if guestmember and guestmember.bemerk != "":
        rescomment = rescomment + guestmember.bemerk + chr_unicode(10)

    waehrung = get_cache (Waehrung, {"waehrungsnr": [(eq, res_line.betriebsnr)]})

    if resbuff:
        rescomment = rescomment + "Arr " + to_string(resbuff.ankunft) + " Dep " + to_string(resbuff.abreise) + " A " + to_string(resbuff.erwachs) + " Ch " + to_string(resbuff.kind1) + " Ch " + to_string(resbuff.kind2) + " Com " + to_string(resbuff.gratis) + chr_unicode(10) + "Argt " + resbuff.arrangement

    if waehrung:
        rescomment = rescomment + ">>Currency " + waehrung.wabkurz + chr_unicode(10)
    else:
        rescomment = rescomment + chr_unicode(10)

    return generate_output()