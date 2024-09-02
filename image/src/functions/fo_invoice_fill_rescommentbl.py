from functions.additional_functions import *
import decimal
from models import Bediener, Res_line, Guest, Bill, Reservation, Queasy, Waehrung

def fo_invoice_fill_rescommentbl(bil_recid:int, fill_co:bool):
    rescomment = ""
    bediener = res_line = guest = bill = reservation = queasy = waehrung = None

    usr = resbuff = rbuff = guestmember = None

    Usr = Bediener
    Resbuff = Res_line
    Rbuff = Res_line
    Guestmember = Guest

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rescomment, bediener, res_line, guest, bill, reservation, queasy, waehrung
        nonlocal usr, resbuff, rbuff, guestmember


        nonlocal usr, resbuff, rbuff, guestmember
        return {"rescomment": rescomment}


    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()

    res_line = db_session.query(Res_line).filter(
            (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

    reservation = db_session.query(Reservation).filter(
            (Reservation.resnr == bill.resnr)).first()

    if res_line:

        guestmember = db_session.query(Guestmember).filter(
                (Guestmember.gastnr == res_line.gastnrmember)).first()

    resbuff = db_session.query(Resbuff).filter(
            (Resbuff.resnr == bill.resnr) &  (Resbuff.reslinnr == bill.parent_nr)).first()
    rescomment = ""

    if fill_co:

        usr = db_session.query(Usr).filter(
                (Usr.userinit == bill.vesrcod)).first()

        if usr:
            rescomment = rescomment + "C/O by: " + usr.username + chr (10)

    if resbuff and trim(entry(0, resbuff.memozinr, ";")) != "":

        rbuff = db_session.query(Rbuff).filter(
                (Rbuff.zinr == trim(entry(0, resbuff.memozinr, ";"))) &  (Rbuff.resstatus == 6)).first()

        if rbuff:
            rescomment = rescomment + "Transf " + resbuff.zinr + " -> " + entry(0, resbuff.memozinr, ";") + " " + rbuff.name + chr(10)
        else:
            rescomment = rescomment + "Transf " + resbuff.zinr + " -> " + entry(0, resbuff.memozinr, ";") + chr(10)

    if resbuff and resbuff.code != "":

        queasy = db_session.query(Queasy).filter(
                (Queasy.key == 9) &  (Queasy.number1 == to_int(res_line.code))).first()

        if queasy:
            rescomment = rescomment + queasy.char1 + chr (10)

    if bill.vesrdepot != "":
        rescomment = rescomment + bill.vesrdepot + chr(10)

    if res_line and res_line.bemerk != "":
        rescomment = rescomment + res_line.bemerk + chr (10)

    if reservation and reservation.bemerk != "":
        rescomment = rescomment + reservation.bemerk + chr (10)

    if guestmember and guestmember.bemerk != "":
        rescomment = rescomment + guestmember.bemerk + chr (10)

    waehrung = db_session.query(Waehrung).filter(
            (Waehrungsnr == res_line.betriebsnr)).first()

    if resbuff:
        rescomment = rescomment + "Arr " + to_string(resbuff.ankunft) + " Dep " + to_string(resbuff.abreise) + " A " + to_string(resbuff.erwachs) + " Ch " + to_string(resbuff.kind1) + " Ch " + to_string(resbuff.kind2) + " Com " + to_string(resbuff.gratis) + chr(10) + "Argt " + resbuff.arrangement

    if waehrung:
        rescomment = rescomment + ">>Currency " + waehrung.wabkurz + chr(10)
    else:
        rescomment = rescomment + chr(10)

    return generate_output()