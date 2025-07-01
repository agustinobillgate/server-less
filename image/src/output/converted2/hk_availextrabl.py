#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Res_line, Fixleist, Arrangement, Reslin_queasy

def hk_availextrabl(pvilanguage:int, art_nr:int, fdate:date, tdate:date):

    prepare_cache ([Fixleist, Arrangement, Reslin_queasy])

    tmp_extra_list = []
    bdate:date = None
    edate:date = None
    eposdate:date = None
    lvcarea:string = "hk-availextra"
    res_line = fixleist = arrangement = reslin_queasy = None

    tmp_resline = tmp_extra = None

    tmp_resline_list, Tmp_resline = create_model_like(Res_line)
    tmp_extra_list, Tmp_extra = create_model("Tmp_extra", {"reihe":int, "typ_pos":string, "pos_from":string, "cdate":date, "room":string, "qty":int, "rsvno":int})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tmp_extra_list, bdate, edate, eposdate, lvcarea, res_line, fixleist, arrangement, reslin_queasy
        nonlocal pvilanguage, art_nr, fdate, tdate


        nonlocal tmp_resline, tmp_extra
        nonlocal tmp_resline_list, tmp_extra_list

        return {"tmp-extra": tmp_extra_list}

    def create_data():

        nonlocal tmp_extra_list, bdate, edate, eposdate, lvcarea, res_line, fixleist, arrangement, reslin_queasy
        nonlocal pvilanguage, art_nr, fdate, tdate


        nonlocal tmp_resline, tmp_extra
        nonlocal tmp_resline_list, tmp_extra_list

        do_it:bool = False
        argtnr:int = 0
        tmp_resline_list.clear()
        tmp_extra_list.clear()

        for res_line in db_session.query(Res_line).filter(
                 (not_ (Res_line.abreise < fdate)) & (not_ (Res_line.ankunft > tdate)) & (Res_line.resstatus != 9) & (Res_line.resstatus != 10) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line.resnr).all():
            tmp_resline = Tmp_resline()
            tmp_resline_list.append(tmp_resline)

            buffer_copy(res_line, tmp_resline)

        for tmp_resline in query(tmp_resline_list, sort_by=[("resnr",False)]):

            for fixleist in db_session.query(Fixleist).filter(
                     (Fixleist.resnr == tmp_resline.resnr) & (Fixleist.reslinnr == tmp_resline.reslinnr) & (Fixleist.artnr == art_nr) & (Fixleist.departement == 0)).order_by(Fixleist._recid).all():

                if tmp_resline.ankunft == tmp_resline.abreise:

                    if fixleist.sequenz == 1 or fixleist.sequenz == 2 or fixleist.sequenz == 6:
                        create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                    elif fixleist.sequenz == 4:

                        if get_day(tmp_resline.ankunft) == 1:
                            create_tmpextra("Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                    elif fixleist.sequenz == 5:

                        if get_day(tmp_resline.ankunft + 1) == 1:
                            create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)
                else:

                    if fixleist.sequenz == 1 or fixleist.sequenz == 2 or fixleist.sequenz == 4 or fixleist.sequenz == 5:

                        if tmp_resline.ankunft < fdate:
                            bdate = fdate
                        else:
                            bdate = tmp_resline.ankunft

                        if tmp_resline.abreise > tdate:
                            edate = tdate
                        else:
                            edate = tmp_resline.abreise

                    if fixleist.sequenz == 1:
                        while bdate <= edate :

                            if tmp_resline.abreise > bdate:
                                create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)

                            elif tmp_resline.abreise == bdate and tmp_resline.abreisezeit >= (18 * 3600):
                                create_tmpextra(1, "Dayuse", "1", bdate, tmp_resline.zinr + " " + translateExtended ("DayUse till", lvcarea, "") + " " + to_string(tmp_resline.abreisezeit, "HH:MM"), 0)
                            bdate = bdate + timedelta(days=1)

                    elif fixleist.sequenz == 2:
                        create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), tmp_resline.ankunft, tmp_resline.zinr, fixleist.number)

                    elif fixleist.sequenz == 4:
                        while bdate <= edate :

                            if get_day(bdate) == 1 and tmp_resline.abreise > bdate:
                                create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)

                            elif get_day(bdate) == 1 and tmp_resline.abreise == bdate and tmp_resline.abreisezeit >= (18 * 3600):
                                create_tmpextra(1, "Dayuse", "1", bdate, tmp_resline.zinr + " " + translateExtended ("DayUse till", lvcarea, "") + " " + to_string(tmp_resline.abreisezeit, "HH:MM"), 0)
                            bdate = bdate + timedelta(days=1)

                    elif fixleist.sequenz == 5:
                        while bdate <= edate :

                            if get_day(bdate + 1) == 1 and tmp_resline.abreise < bdate:
                                create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)

                            elif get_day(bdate + 1) == 1 and tmp_resline.abreise == bdate and tmp_resline.abreisezeit >= (18 * 3600):
                                create_tmpextra(1, "Dayuse", "1", bdate, tmp_resline.zinr + " " + translateExtended ("DayUse till", lvcarea, "") + " " + to_string(tmp_resline.abreisezeit, "HH:MM"), 0)
                            bdate = bdate + timedelta(days=1)

                    elif fixleist.sequenz == 6:
                        eposdate = (fixleist.lfakt + timedelta(days=fixleist.dekade - 1))

                        if fixleist.lfakt <= fdate:
                            bdate = fdate
                        else:
                            bdate = fixleist.lfakt

                        if eposdate > tdate:
                            edate = tdate

                        elif eposdate <= tdate:

                            if eposdate >= tmp_resline.abreise:
                                edate = tmp_resline.abreise
                            else:
                                edate = eposdate
                        while bdate <= edate :

                            if tmp_resline.abreise > bdate:
                                create_tmpextra(0, "Fix-cost line", to_string(fixleist.sequenz), bdate, tmp_resline.zinr, fixleist.number)

                            elif tmp_resline.abreise == bdate and tmp_resline.abreisezeit >= (18 * 3600):
                                create_tmpextra(1, "Dayuse", "1", bdate, tmp_resline.zinr + " " + translateExtended ("DayUse till", lvcarea, "") + " " + to_string(tmp_resline.abreisezeit, "HH:MM"), 0)
                            bdate = bdate + timedelta(days=1)

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, tmp_resline.arrangement)]})

            if arrangement:
                argtnr = arrangement.argtnr

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == ("fargt-line").lower()) & (Reslin_queasy.resnr == tmp_resline.resnr) & (Reslin_queasy.reslinnr == tmp_resline.reslinnr) & (Reslin_queasy.number1 == 0) & (Reslin_queasy.number3 == art_nr) & (Reslin_queasy.number2 == argtnr)).order_by(Reslin_queasy._recid).all():

                if reslin_queasy.date1 < fdate:
                    bdate = fdate
                else:
                    bdate = reslin_queasy.date1

                if reslin_queasy.date2 > tdate:
                    edate = tdate
                else:
                    edate = reslin_queasy.date2
                while bdate <= edate :

                    if tmp_resline.abreise > bdate:
                        create_tmpextra(0, "argt line", "0", bdate, tmp_resline.zinr, 1)

                    elif tmp_resline.abreise == bdate and tmp_resline.abreisezeit >= (18 * 3600):
                        create_tmpextra(1, "Dayuse", "1", bdate, tmp_resline.zinr + " " + translateExtended ("DayUse till", lvcarea, "") + " " + to_string(tmp_resline.abreisezeit, "HH:MM"), 0)
                    bdate = bdate + timedelta(days=1)


    def create_tmpextra(reihe:int, typ_pos:string, pos_from:string, cdate:date, room:string, qty:int):

        nonlocal tmp_extra_list, bdate, edate, eposdate, lvcarea, res_line, fixleist, arrangement, reslin_queasy
        nonlocal pvilanguage, art_nr, fdate, tdate


        nonlocal tmp_resline, tmp_extra
        nonlocal tmp_resline_list, tmp_extra_list


        tmp_extra = Tmp_extra()
        tmp_extra_list.append(tmp_extra)

        tmp_extra.typ_pos = typ_pos
        tmp_extra.pos_from = pos_from
        tmp_extra.cdate = cdate
        tmp_extra.room = room
        tmp_extra.qty = qty
        tmp_extra.reihe = reihe
        tmp_extra.rsvno = tmp_resline.resnr


    create_data()

    return generate_output()