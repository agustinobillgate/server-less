from functions.additional_functions import *
import decimal
from datetime import date
from models import Htparam, Res_line, Guest, Reservation, nation, Arrangement, Guestseg, Argt_line, Mealcoup, Queasy

def bfast_kcard_parsingroomdatabl(inproomnumber:str, inpmealtime:str):
    outstr = ""
    p_87:date = None
    gastnr:int = 0
    guestname:str = ""
    argt_bez:str = ""
    resnr:int = 0
    cidate:date = None
    codate:date = None
    num_of_day:int = 0
    i:int = 0
    tmpstr:str = ""
    tmpint:int = 0
    vip_nr:List[int] = create_empty_list(10,0)
    totadult:int = 0
    totcompli:int = 0
    totchild:int = 0
    totconsumed:int = 0
    vipflag:str = ""
    nation:str = ""
    rsv_comment:str = ""
    bill_instruct:str = ""
    artgrp_abf:int = 0
    artgrp_lunch:int = 0
    artgrp_dinner:int = 0
    artgrp_lundin:int = 0
    htparam = res_line = guest = reservation = nation = arrangement = guestseg = argt_line = mealcoup = queasy = None

    b_res_line = None

    B_res_line = create_buffer("B_res_line",Res_line)

    db_session = local_storage.db_session

    def generate_output():
        nonlocal outstr, p_87, gastnr, guestname, argt_bez, resnr, cidate, codate, num_of_day, i, tmpstr, tmpint, vip_nr, totadult, totcompli, totchild, totconsumed, vipflag, nation, rsv_comment, bill_instruct, artgrp_abf, artgrp_lunch, artgrp_dinner, artgrp_lundin, htparam, res_line, guest, reservation, nation, arrangement, guestseg, argt_line, mealcoup, queasy
        nonlocal inproomnumber, inpmealtime
        nonlocal b_res_line


        nonlocal b_res_line
        return {"outstr": outstr}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 125)).first()

    if htparam:
        artgrp_abf = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 227)).first()

    if htparam:
        artgrp_lunch = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 228)).first()

    if htparam:
        artgrp_dinner = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 229)).first()

    if htparam:
        artgrp_lundin = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 87)).first()

    if htparam:
        p_87 = htparam.fdate

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 700)).first()
    vip_nr[0] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 701)).first()
    vip_nr[1] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 702)).first()
    vip_nr[2] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 703)).first()
    vip_nr[3] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 704)).first()
    vip_nr[4] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 705)).first()
    vip_nr[5] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 706)).first()
    vip_nr[6] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 707)).first()
    vip_nr[7] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 708)).first()
    vip_nr[8] = htparam.finteger

    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 712)).first()
    vip_nr[9] = htparam.finteger

    res_line = db_session.query(Res_line).filter(
             (Res_line.zinr == inproomnumber) & (Res_line.resstatus == 6) & (Res_line.p_87 >= Res_line.ankunft) & (Res_line.p_87 <= Res_line.abreise)).first()

    if res_line:

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == res_line.gastnrmember)).first()

        reservation = db_session.query(Reservation).filter(
                 (Reservation.resnr == res_line.resnr)).first()

        if not reservation:
            outstr = "Main Reservation data not found"

            return generate_output()

        if not guest:

            guest = db_session.query(Guest).filter(
                     (Guest.gastnr == res_line.gastnr)).first()

        nation = db_session.query(nation).filter(
                 (nation.kurzbez == guest.nation1)).first()

        if nation:
            tmpstr = nation.bezeich
        else:
            tmpstr = ""

        arrangement = db_session.query(Arrangement).filter(
                 (Arrangement.arrangement == res_line.arrangement)).first()

        if arrangement and guest:
            resnr = res_line.resnr
            gastnr = guest.gastnr
            guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
            cidate = res_line.ankunft
            codate = res_line.abreise
            argt_bez = " " + arrangement.arrangement + " : " + arrangement.argt_bez
            rsv_comment = reservation.bemerk + chr(10) + res_line.bemerk
            nation = entry(0, tmpstr, ";")
            guestname = guestname + " [" + nation + "]"

            for guestseg in db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == res_line.gastnrmember)).order_by(Guestseg._recid).all():
                for i in range(1,len(vip_nr)  + 1) :

                    if guestseg.segmentcode == vip_nr[i - 1]:
                        vipflag = "VIP " + to_string(i)
                        i = 100
                        break

                if i == 100:
                    break

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).all():

                if argt_line.argt_artnr == artgrp_abf and inpmealtime.lower()  == ("Breakfast").lower() :

                    if argt_line.fakt_modus == 3 and (p_87 - res_line.ankunft == 1):
                        totadult = res_line.erwachs
                        totcompli = res_line.gratis

                    elif argt_line.fakt_modus == 6 and (p_87 - res_line.ankunft <= argt_line.intervall):
                        totadult = res_line.erwachs
                        totcompli = res_line.gratis

                    elif argt_line.fakt_modus != 3 and argt_line.fakt_modus != 6:
                        totadult = res_line.erwachs
                        totcompli = res_line.gratis
                    for i in range(1,num_entries(res_line.zimmer_wunsch, ";")  + 1) :

                        if re.match(r".*ChAge.*",entry(i - 1, res_line.zimmer_wunsch, ";"), re.IGNORECASE):
                            tmpstr = substring(entry(i - 1, res_line.zimmer_wunsch, ";") , 5)
                    for i in range(1,res_line.kind1 + 1) :

                        if i > num_entries(tmpstr, ","):
                            break

                        if to_int(entry(i - 1, tmpstr, ",")) > 12:
                            tmpint = tmpint + 1
                    totadult = totadult + tmpint
                    totchild = res_line.kind1 - tmpint

                elif argt_line.argt_artnr == artgrp_lunch and inpmealtime.lower()  == ("Lunch").lower() :
                    pass

                elif argt_line.argt_artnr == artgrp_dinner and inpmealtime.lower()  == ("Dinner").lower() :
                    pass
    else:
        outstr = "No InHouse guest in selected room"

        return generate_output()
    num_of_day = p_87 - res_line.ankunft

    if num_of_day > 32:
        num_of_day = num_of_day - 32

    if num_of_day == 0:
        outstr = "If guest checked-in today, a breakfast voucher will be available on the next day"

        return generate_output()

    if totadult + totchild + totcompli > 0 and res_line:

        for mealcoup in db_session.query(Mealcoup).filter(
                 (Mealcoup.resnr == res_line.resnr) & (Mealcoup.zinr == res_line.zinr) & (Mealcoup.name == inpmealtime)).order_by(Mealcoup._recid).all():
            totconsumed = mealcoup.verbrauch[num_of_day - 1]

    for b_res_line in db_session.query(B_res_line).filter(
             (B_res_line.resnr == res_line.resnr) & (B_res_line.zinr == res_line.zinr) & (B_res_line.resstatus > 6) & (B_res_line.kontakt_nr != 0)).order_by(B_res_line._recid).all():

        guest = db_session.query(Guest).filter(
                 (Guest.gastnr == b_res_line.gastnrmember)).first()

        if guest:
            tmpstr = ""

            nation = db_session.query(nation).filter(
                     (nation.kurzbez == guest.nation1)).first()

            if nation:
                tmpstr = nation.bezeich
            guestname = guestname + chr(10) + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + " [" + entry(0, tmpstr, ";") + "]"

    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code))).first()

    if queasy:
        bill_instruct = queasy.char1
    outstr = "success" + chr(2) + to_string(resnr) + chr(2) + to_string(gastnr) + chr(2) + guestname + chr(2) + argt_bez + chr(2) + to_string(cidate, "99/99/9999") + chr(2) + to_string(codate, "99/99/9999") + chr(2) + to_string(totadult) + chr(2) + to_string(totcompli) + chr(2) + to_string(totchild) + chr(2) + to_string(totconsumed) + chr(2) + vipflag + chr(2) + nation + chr(2) + rsv_comment + chr(2) + bill_instruct

    return generate_output()