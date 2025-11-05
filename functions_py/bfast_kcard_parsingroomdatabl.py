#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Guest, Reservation, Nation, Arrangement, Guestseg, Argt_line, Mealcoup, Queasy

def bfast_kcard_parsingroomdatabl(inproomnumber:string, inpmealtime:string):

    prepare_cache ([Htparam, Res_line, Guest, Reservation, Nation, Arrangement, Guestseg, Argt_line, Mealcoup, Queasy])

    outstr = ""
    p_87:date = None
    gastnr:int = 0
    guestname:string = ""
    argt_bez:string = ""
    resnr:int = 0
    cidate:date = None
    codate:date = None
    num_of_day:int = 0
    i:int = 0
    tmpstr:string = ""
    tmpint:int = 0
    vip_nr:List[int] = create_empty_list(10,0)
    totadult:int = 0
    totcompli:int = 0
    totchild:int = 0
    totconsumed:int = 0
    vipflag:string = ""
    nation_guest:string = ""
    rsv_comment:string = ""
    bill_instruct:string = ""
    artgrp_abf:int = 0
    artgrp_lunch:int = 0
    artgrp_dinner:int = 0
    artgrp_lundin:int = 0
    htparam = res_line = guest = reservation = nation = arrangement = guestseg = argt_line = mealcoup = queasy = None

    b_res_line = None

    B_res_line = create_buffer("B_res_line",Res_line)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal outstr, p_87, gastnr, guestname, argt_bez, resnr, cidate, codate, num_of_day, i, tmpstr, tmpint, vip_nr, totadult, totcompli, totchild, totconsumed, vipflag, nation_guest, rsv_comment, bill_instruct, artgrp_abf, artgrp_lunch, artgrp_dinner, artgrp_lundin, htparam, res_line, guest, reservation, nation, arrangement, guestseg, argt_line, mealcoup, queasy
        nonlocal inproomnumber, inpmealtime
        nonlocal b_res_line


        nonlocal b_res_line

        return {"outstr": outstr}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 125)]})

    if htparam:
        artgrp_abf = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 227)]})

    if htparam:
        artgrp_lunch = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 228)]})

    if htparam:
        artgrp_dinner = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 229)]})

    if htparam:
        artgrp_lundin = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})

    if htparam:
        p_87 = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 700)]})
    vip_nr[0] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 701)]})
    vip_nr[1] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 702)]})
    vip_nr[2] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 703)]})
    vip_nr[3] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 704)]})
    vip_nr[4] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 705)]})
    vip_nr[5] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 706)]})
    vip_nr[6] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 707)]})
    vip_nr[7] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 708)]})
    vip_nr[8] = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 712)]})
    vip_nr[9] = htparam.finteger

    res_line = get_cache (Res_line, {"zinr": [(eq, inproomnumber)],"resstatus": [(eq, 6)],"ankunft": [(le, p_87)],"abreise": [(ge, p_87)]})

    if res_line:

        guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnrmember)]})

        reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

        if not reservation:
            outstr = "Main Reservation data not found"

            return generate_output()

        if not guest:

            guest = get_cache (Guest, {"gastnr": [(eq, res_line.gastnr)]})

        nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

        if nation:
            tmpstr = nation.bezeich
        else:
            tmpstr = ""

        arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})

        if arrangement and guest:
            resnr = res_line.resnr
            gastnr = guest.gastnr
            guestname = guest.name + ", " + guest.vorname1 + " " + guest.anrede1
            cidate = res_line.ankunft
            codate = res_line.abreise
            argt_bez = " " + arrangement.arrangement + " : " + arrangement.argt_bez
            rsv_comment = reservation.bemerk + chr_unicode(10) + res_line.bemerk
            nation_guest = entry(0, tmpstr, ";")
            guestname = guestname + " [" + nation_guest + "]"

            for guestseg in db_session.query(Guestseg).filter(
                     (Guestseg.gastnr == res_line.gastnrmember)).order_by(Guestseg._recid).yield_per(100):
                for i in range(1,length(vip_nr)  + 1) :

                    if guestseg.segmentcode == vip_nr[i - 1]:
                        vipflag = "VIP " + to_string(i)
                        i = 100
                        break

                if i == 100:
                    break

            for argt_line in db_session.query(Argt_line).filter(
                     (Argt_line.argtnr == arrangement.argtnr)).order_by(Argt_line._recid).yield_per(100):

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

                        if matches(entry(i - 1, res_line.zimmer_wunsch, ";"),r"*ChAge*"):
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
    num_of_day = (p_87 - res_line.ankunft).days

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

        guest = get_cache (Guest, {"gastnr": [(eq, b_res_line.gastnrmember)]})

        if guest:
            tmpstr = ""

            nation = get_cache (Nation, {"kurzbez": [(eq, guest.nation1)]})

            if nation:
                tmpstr = nation.bezeich
            guestname = guestname + chr_unicode(10) + guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + " [" + entry(0, tmpstr, ";") + "]"

    # queasy = get_cache (Queasy, {"key": [(eq, 9)],"number1": [(eq, to_int(res_line.code.strip()))]})
    queasy = db_session.query(Queasy).filter(
             (Queasy.key == 9) & (Queasy.number1 == to_int(res_line.code.strip()))).first()

    if queasy:
        bill_instruct = queasy.char1
    outstr = "success" + chr_unicode(2) + to_string(resnr) + chr_unicode(2) + to_string(gastnr) + chr_unicode(2) + guestname + chr_unicode(2) + argt_bez + chr_unicode(2) + to_string(cidate, "99/99/9999") + chr_unicode(2) + to_string(codate, "99/99/9999") + chr_unicode(2) + to_string(totadult) + chr_unicode(2) + to_string(totcompli) + chr_unicode(2) + to_string(totchild) + chr_unicode(2) + to_string(totconsumed) + chr_unicode(2) + vipflag + chr_unicode(2) + nation_guest + chr_unicode(2) + rsv_comment + chr_unicode(2) + bill_instruct

    return generate_output()