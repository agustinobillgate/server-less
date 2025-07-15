#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from functions.ratecode_seek import ratecode_seek
from models import Reservation, Res_line, Htparam, Queasy, Guest, Arrangement, Guest_pr, Reslin_queasy, Ratecode

def reservation_btn_delbl(pvilanguage:int, curr_select:string, resno:int, reslinno:int):

    prepare_cache ([Reservation, Res_line, Htparam, Guest, Guest_pr, Ratecode])

    msg_str = ""
    delete_str = ""
    error_flag = True
    pswd_str = ""
    max_comp = 0
    com_rm = 0
    queasy_flag = False
    deposit:bool = False
    may_delete:bool = True
    lvcarea:string = "reservation"
    reservation = res_line = htparam = queasy = guest = arrangement = guest_pr = reslin_queasy = ratecode = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, delete_str, error_flag, pswd_str, max_comp, com_rm, queasy_flag, deposit, may_delete, lvcarea, reservation, res_line, htparam, queasy, guest, arrangement, guest_pr, reslin_queasy, ratecode
        nonlocal pvilanguage, curr_select, resno, reslinno

        return {"msg_str": msg_str, "delete_str": delete_str, "error_flag": error_flag, "pswd_str": pswd_str, "max_comp": max_comp, "com_rm": com_rm, "queasy_flag": queasy_flag}

    def delete_resline():

        nonlocal msg_str, delete_str, error_flag, pswd_str, max_comp, com_rm, queasy_flag, deposit, may_delete, lvcarea, reservation, res_line, htparam, queasy, guest, arrangement, guest_pr, reslin_queasy, ratecode
        nonlocal pvilanguage, curr_select, resno, reslinno

        if (res_line.active_flag == 1 or res_line.resstatus == 6 or res_line.resstatus == 13) and res_line.l_zuordnung[2] == 0:
            msg_str = translateExtended ("Deleting of Inhouse-Guests is not possible.", lvcarea, "")

            return

        htparam = get_cache (Htparam, {"paramnr": [(eq, 437)]})

        if htparam.flogical == False and res_line.betrieb_gast > 0 and res_line.l_zuordnung[2] == 0:
            msg_str = translateExtended ("KeyCard has been generated. Cancellation no longer possible.", lvcarea, "")

            return
        check_deposit()

        if may_delete == False and res_line.l_zuordnung[2] == 0:
            msg_str = translateExtended ("ATTENTION: deposit Payment exists for this reservartion.", lvcarea, "")

            return

        if res_line.resstatus != 11 and res_line.resstatus != 13:
            error_flag = check_compliment(res_line.resnr, res_line.reslinnr, res_line.gastnr, res_line.ankunft, res_line.reserve_int, res_line.zikatnr, res_line.arrangement, 0, res_line.zipreis)

            if error_flag:

                return

        queasy = get_cache (Queasy, {"key": [(eq, 32)],"char3": [(ne, "")]})

        if reservation:
            delete_str = reservation.vesrdepot2
        error_flag = False
        queasy_flag = None != queasy
        msg_str = "&Q" +\
                translateExtended ("Do you really want to DELETE the reservation:", lvcarea, "") +\
                chr_unicode(10) +\
                res_line.name + " - " + res_line.zinr +\
                chr_unicode(10) +\
                translateExtended ("Arrival :", lvcarea, "") + " " +\
                to_string(res_line.ankunft) + " " +\
                translateExtended ("Departure:", lvcarea, "") + " " +\
                to_string(res_line.abreise) + " ?"


    def delete_mainres():

        nonlocal msg_str, delete_str, error_flag, pswd_str, max_comp, com_rm, queasy_flag, deposit, may_delete, lvcarea, reservation, res_line, htparam, queasy, guest, arrangement, guest_pr, reslin_queasy, ratecode
        nonlocal pvilanguage, curr_select, resno, reslinno

        if not reservation:

            return

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == reservation.resnr) & ((Res_line.resstatus == 6) | (Res_line.resstatus == 13))).first()

        if res_line:
            msg_str = translateExtended ("Deleting not possible, In-House guest exists.", lvcarea, "")

            return

        res_line = db_session.query(Res_line).filter(
                 (Res_line.resnr == reservation.resnr) & (Res_line.active_flag == 0) & (Res_line.betrieb_gast > 0)).first()

        if res_line:
            msg_str = translateExtended ("KeyCard has been generated for", lvcarea, "") + " " + res_line.name + " - " + translateExtended ("RmNo", lvcarea, "") + " " + res_line.zinr + chr_unicode(10) + translateExtended ("Deleting for all members no longer possible.", lvcarea, "")

            return
        check_deposit()

        if deposit:
            msg_str = translateExtended ("ATTENTION: deposit Payment exists for this reservartion.", lvcarea, "")

            return

        guest = get_cache (Guest, {"gastnr": [(eq, reservation.gastnr)]})

        if guest:
            msg_str = "&Q" + translateExtended ("Do you really want to DELETE the main reservation of", lvcarea, "") + chr_unicode(10) + guest.name + ", " + guest.vorname1 + guest.anredefirma + " " + guest.anrede1 + chr_unicode(10) + translateExtended ("including it's all reservation members ?", lvcarea, "")
        else:
            msg_str = "&Q" + translateExtended ("Do you really want to DELETE the main reservation of", lvcarea, "") + chr_unicode(10) + "" + ", " + "" + "" + " " + "" + chr_unicode(10) + translateExtended ("including it's all reservation members ?", lvcarea, "")

        queasy = get_cache (Queasy, {"key": [(eq, 32)],"char3": [(ne, "")]})
        error_flag = False
        queasy_flag = None != queasy
        delete_str = reservation.vesrdepot2


    def check_deposit():

        nonlocal msg_str, delete_str, error_flag, pswd_str, max_comp, com_rm, queasy_flag, deposit, may_delete, lvcarea, reservation, res_line, htparam, queasy, guest, arrangement, guest_pr, reslin_queasy, ratecode
        nonlocal pvilanguage, curr_select, resno, reslinno

        anzahl:int = 0
        reservation1 = None
        resline1 = None
        Reservation1 =  create_buffer("Reservation1",Reservation)
        Resline1 =  create_buffer("Resline1",Res_line)

        reservation1 = get_cache (Reservation, {"resnr": [(eq, resno)]})

        if (reservation1.depositbez + reservation1.depositbez2) != 0:
            deposit = True

        if deposit and reservation1.bestat_datum == None:

            resline1 = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(eq, 1)]})

            if resline1:

                return

            resline1 = get_cache (Res_line, {"resnr": [(eq, resno)],"active_flag": [(eq, 2)],"resstatus": [(eq, 8)]})

            if resline1:

                return

            for resline1 in db_session.query(Resline1).filter(
                     (Resline1.resnr == resno) & (Resline1.active_flag == 0)).order_by(Resline1._recid).all():
                anzahl = anzahl + 1

        if anzahl == 1:
            may_delete = False


    def check_compliment(resnr:int, reslinnr:int, gastnr:int, datum:date, marknr:int, zikatnr:int, argt:string, qty:int, rate:Decimal):

        nonlocal msg_str, delete_str, error_flag, pswd_str, max_comp, com_rm, queasy_flag, deposit, may_delete, lvcarea, reservation, res_line, htparam, queasy, guest, arrangement, guest_pr, reslin_queasy, ratecode
        nonlocal pvilanguage, curr_select, resno, reslinno

        still_error = False
        s_recid:int = 0
        book_room:int = 0
        comp_room:int = 0
        max_room:int = 0
        pay_rm:int = 0
        curr_rm:int = 0
        passwd_ok:bool = False
        new_contrate:bool = False
        ct:string = ""
        contcode:string = ""
        resline = None

        def generate_inner_output():
            return (still_error)

        Resline =  create_buffer("Resline",Res_line)

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, argt)]})

        if not arrangement:

            return generate_inner_output()

        guest_pr = get_cache (Guest_pr, {"gastnr": [(eq, gastnr)]})

        if not guest_pr:

            return generate_inner_output()
        contcode = guest_pr.code

        res_line = get_cache (Res_line, {"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)]})
        ct = res_line.zimmer_wunsch

        if matches(ct,r"*$CODE$*"):
            ct = substring(ct, get_index(ct, "$CODE$") + 6 - 1)
            contcode = substring(ct, 0, get_index(ct, ";") - 1)

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, "arrangement")],"resnr": [(eq, resnr)],"reslinnr": [(eq, reslinnr)],"date1": [(le, datum)],"date2": [(ge, datum)]})

        if reslin_queasy:

            return generate_inner_output()

        if rate == 0:
            com_rm = qty
        else:
            pay_rm = qty

        for resline in db_session.query(Resline).filter(
                 (Resline.resnr == resnr) & (Resline.active_flag <= 1) & (Resline.resstatus <= 6) & (Resline.reslinnr != reslinnr)).order_by(Resline._recid).all():

            if resline.zipreis == 0:
                com_rm = com_rm + resline.zimmeranz
            else:
                pay_rm = pay_rm + resline.zimmeranz

        if com_rm == 0:

            return generate_inner_output()

        htparam = get_cache (Htparam, {"paramnr": [(eq, 550)]})

        if htparam.feldtyp == 4:
            new_contrate = htparam.flogical
        s_recid = get_output(ratecode_seek(resnr, reslinnr, contcode, datum))

        if s_recid == 0:

            return generate_inner_output()

        ratecode = get_cache (Ratecode, {"_recid": [(eq, s_recid)]})

        if num_entries(ratecode.char1[3], ";") < 3:

            return generate_inner_output()
        book_room = to_int(entry(0, ratecode.char1[3], ";"))
        comp_room = to_int(entry(1, ratecode.char1[3], ";"))
        max_room = to_int(entry(2, ratecode.char1[3], ";"))


        curr_rm = pay_rm

        if curr_rm > max_room:
            curr_rm = max_room
        max_comp = round(curr_rm / book_room - 0.5, 0) * comp_room

        if max_comp < 0:
            max_comp = 0

        if com_rm <= max_comp:

            return generate_inner_output()
        msg_str = translateExtended ("Wrong total number of compliment rooms:", lvcarea, "") + chr_unicode(10) + chr_unicode(10) + translateExtended ("Max allowed =", lvcarea, "") + " " + to_string(max_comp) + chr_unicode(10) + translateExtended ("Actual compliment rooms =", lvcarea, "") + " " + to_string(com_rm)

        htparam = get_cache (Htparam, {"paramnr": [(eq, 141)]})

        if htparam.fchar == "":
            still_error = True
        else:
            still_error = False
            pswd_str = htparam.fchar

        return generate_inner_output()

    reservation = get_cache (Reservation, {"resnr": [(eq, resno)]})

    res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

    if not res_line:

        return generate_output()

    if curr_select.lower()  == ("res-line").lower() :
        delete_resline()
    else:
        delete_mainres()

    return generate_output()