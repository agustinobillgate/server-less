from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from functions.ratecode_seek import ratecode_seek
from functions.htpchar import htpchar
from models import Res_line, Arrangement, Guest_pr, Reslin_queasy, Htparam, Ratecode, Pricecod

def check_complimentbl(pvilanguage:int, resnr:int, reslinnr:int, gastnr:int, datum:date, marknr:int, zikatnr:int, argt:str, qty:int, rate:decimal):
    still_error = False
    comp_room = 0
    max_room = 0
    pswd_str = ""
    msg_str = ""
    s_recid:int = 0
    book_room:int = 0
    pay_rm:int = 0
    curr_rm:int = 0
    max_comp:int = 0
    com_rm:int = 0
    passwd_ok:bool = False
    new_contrate:bool = False
    ct:str = ""
    contcode:str = ""
    lvcarea:str = "check-compliment"
    res_line = arrangement = guest_pr = reslin_queasy = htparam = ratecode = pricecod = None

    resline = None

    Resline = create_buffer("Resline",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal still_error, comp_room, max_room, pswd_str, msg_str, s_recid, book_room, pay_rm, curr_rm, max_comp, com_rm, passwd_ok, new_contrate, ct, contcode, lvcarea, res_line, arrangement, guest_pr, reslin_queasy, htparam, ratecode, pricecod
        nonlocal pvilanguage, resnr, reslinnr, gastnr, datum, marknr, zikatnr, argt, qty, rate
        nonlocal resline


        nonlocal resline
        return {"still_error": still_error, "comp_room": comp_room, "max_room": max_room, "pswd_str": pswd_str, "msg_str": msg_str}


    arrangement = db_session.query(Arrangement).filter(
             (func.lower(Arrangement.arrangement) == (argt).lower())).first()

    if not arrangement:

        return generate_output()

    guest_pr = db_session.query(Guest_pr).filter(
             (Guest_pr.gastnr == gastnr)).first()

    if not guest_pr:

        return generate_output()
    contcode = guest_pr.code

    res_line = db_session.query(Res_line).filter(
             (Res_line.resnr == resnr) & (Res_line.reslinnr == reslinnr)).first()
    ct = res_line.zimmer_wunsch

    if re.match(r".*\$CODE\$.*",ct, re.IGNORECASE):
        ct = substring(ct, 0 + get_index(ct, "$CODE$") + 6)
        contcode = substring(ct, 0, 1 + get_index(ct, ";") - 1)

    reslin_queasy = db_session.query(Reslin_queasy).filter(
             (func.lower(Reslin_queasy.key) == ("arrangement").lower()) & (Reslin_queasy.resnr == resnr) & (Reslin_queasy.reslinnr == reslinnr) & (datum >= Reslin_queasy.date1) & (datum <= Reslin_queasy.date2)).first()

    if reslin_queasy:

        return generate_output()

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

        return generate_output()

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 550)).first()

    if htparam.feldtyp == 4:
        new_contrate = htparam.flogical

    if new_contrate:
        s_recid = get_output(ratecode_seek(resnr, reslinnr, contcode, datum))

        if s_recid == 0:

            return generate_output()

        ratecode = db_session.query(Ratecode).filter(
                 (Ratecode._recid == s_recid)).first()

        if not ratecode:

            return generate_output()

        if num_entries(ratecode.char1[3], ";") < 3:

            return generate_output()
        book_room = to_int(entry(0, ratecode.char1[3], ";"))
        comp_room = to_int(entry(1, ratecode.char1[3], ";"))
        max_room = to_int(entry(2, ratecode.char1[3], ";"))
    else:

        pricecod = db_session.query(Pricecod).filter(
                 (func.lower(Pricecod.code) == (contcode).lower()) & (Pricecod.marknr == marknr) & (Pricecod.argtnr == arrangement.argtnr) & (Pricecod.zikatnr == zikatnr) & (datum >= Pricecod.startperiode) & (datum <= Pricecod.endperiode)).first()

        if not pricecod:

            return generate_output()

        if num_entries(pricecod.bezeichnung, ";") < 3:

            return generate_output()
        book_room = to_int(entry(0, pricecod.bezeichnung, ";"))
        comp_room = to_int(entry(1, pricecod.bezeichnung, ";"))
        max_room = to_int(entry(2, pricecod.bezeichnung, ";"))
    curr_rm = pay_rm

    if curr_rm > max_room:
        curr_rm = max_room
    max_comp = round(curr_rm / book_room - 0.5, 0) * comp_room

    if max_comp < 0:
        max_comp = 0

    if com_rm <= max_comp:

        return generate_output()
    msg_str = translateExtended ("Wrong total number of compliment rooms:", lvcarea, "") + chr(10) + translateExtended ("Max allowed =", lvcarea, "") + " " + to_string(max_comp) + chr(10) + translateExtended ("Actual compliment rooms =", lvcarea, "") + " " + to_string(com_rm) + chr(2)
    pswd_str = get_output(htpchar(141))
    still_error = (pswd_str == "")

    return generate_output()