from functions.additional_functions import *
import decimal
from sqlalchemy import func
from models import Guest, Bediener, Bill, Res_line, Res_history, Reservation, Queasy, Waehrung

def fo_invoice_btn_billadrbl(gastpay:int, bil_recid:int, user_init:str):
    art_no = 0
    resname = ""
    rescomment = ""
    r_gastnrpay = 0
    bill_gastnr = 0
    bill_name = ""
    g_address:str = ""
    g_wonhort:str = ""
    g_plz:str = ""
    g_land:str = ""
    curr_gastnr:int = 0
    guest = bediener = bill = res_line = res_history = reservation = queasy = waehrung = None

    gbuff = guestmember = usr = resbuff = rbuff = None

    Gbuff = Guest
    Guestmember = Guest
    Usr = Bediener
    Resbuff = Res_line
    Rbuff = Res_line

    db_session = local_storage.db_session

    def generate_output():
        nonlocal art_no, resname, rescomment, r_gastnrpay, bill_gastnr, bill_name, g_address, g_wonhort, g_plz, g_land, curr_gastnr, guest, bediener, bill, res_line, res_history, reservation, queasy, waehrung
        nonlocal gbuff, guestmember, usr, resbuff, rbuff


        nonlocal gbuff, guestmember, usr, resbuff, rbuff
        return {"art_no": art_no, "resname": resname, "rescomment": rescomment, "r_gastnrpay": r_gastnrpay, "bill_gastnr": bill_gastnr, "bill_name": bill_name}

    def fill_rescomment(fill_co:bool):

        nonlocal art_no, resname, rescomment, r_gastnrpay, bill_gastnr, bill_name, g_address, g_wonhort, g_plz, g_land, curr_gastnr, guest, bediener, bill, res_line, res_history, reservation, queasy, waehrung
        nonlocal gbuff, guestmember, usr, resbuff, rbuff


        nonlocal gbuff, guestmember, usr, resbuff, rbuff


        Guestmember = Guest
        Usr = Bediener
        Resbuff = Res_line
        Rbuff = Res_line

        reservation = db_session.query(Reservation).filter(
                (Reservation.resnr == bill.resnr)).first()

        if res_line:

            guestmember = db_session.query(Guestmember).filter(
                    (Guestmember.gastnr == res_line.gastnrmember)).first()

        if bill.reslinnr > 0:

            resbuff = db_session.query(Resbuff).filter(
                    (Resbuff.resnr == bill.resnr) &  (Resbuff.reslinnr == bill.parent_nr)).first()
        rescomment = ""

        if fill_co:

            usr = db_session.query(Usr).filter(
                    (Usr.userinit == bill.vesrcod)).first()

            if usr:
                rescomment = rescomment + "C/O by: " + usr.username + chr(10)

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
                rescomment = rescomment + queasy.char1 + chr(10)

        if res_line and res_line.bemerk != "":
            rescomment = rescomment + res_line.bemerk

        if reservation and reservation.bemerk != "":
            rescomment = rescomment + reservation.bemerk + chr(10)

        if guestmember and guestmember.bemerk != "":
            rescomment = rescomment + guestmember.bemerk + chr(10)

        if res_line:

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrungsnr == res_line.betriebsnr)).first()

        if resbuff:
            rescomment = rescomment + "Arr " + to_string(resbuff.ankunft) + " Dep " + to_string(resbuff.abreise) + " A " + to_string(resbuff.erwachs) + " Ch " + to_string(resbuff.kind1) + " Ch " + to_string(resbuff.kind2) + " Com " + to_string(resbuff.gratis) + chr(10) + "Argt " + resbuff.arrangement

        if waehrung:
            rescomment = rescomment + ">>Currency " + waehrung.wabkurz + chr(10)
        else:
            rescomment = rescomment + chr(10)


    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (user_init).lower())).first()

    bill = db_session.query(Bill).filter(
            (Bill._recid == bil_recid)).first()

    guest = db_session.query(Guest).filter(
            (Guest.gastnr == gastpay)).first()
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
            chr (10) + g_address +\
            chr (10) + g_wonhort + " " + g_plz +\
            chr (10) + g_land

    if bill.resnr > 0 and bill.reslinnr > 0:

        res_line = db_session.query(Res_line).filter(
                (Res_line.resnr == bill.resnr) &  (Res_line.reslinnr == bill.reslinnr)).first()

        if res_line:
            res_line.gastnrpay = guest.gastnr

            res_line = db_session.query(Res_line).first()
    fill_rescomment(False)

    if curr_gastnr != gastpay:

        gbuff = db_session.query(Gbuff).filter(
                (Gbuff.gastnr == curr_gastnr)).first()
        res_history = Res_history()
        db_session.add(res_history)

        res_history.nr = bediener.nr
        res_history.betriebsnr = bediener.nr
        res_history.resnr = bill.resnr
        res_history.reslinnr = bill.reslinnr
        res_history.datum = get_current_date()
        res_history.zeit = get_current_time_in_seconds()
        res_history.action = "Bill Receiver Changed"
        res_history.aenderung = gbuff.name + chr(10) + chr(10) +\
                "*** Changed to:" + chr(10) + chr(10) +\
                guest.name + chr(10) + chr(10) +\
                "*** Bill No: " + to_string(bill.rechnr)

        res_history = db_session.query(Res_history).first()


    return generate_output()