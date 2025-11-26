#using conversion tools version: 1.0.0.119
#------------------------------------------
# Rd, 26/11/2025, with_for_update
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Reslin_queasy, Res_line, Fixleist

def read_reslin_queasybl(case_type:int, rkey:string, inpchar:string, resno:int, reslinno:int, inpnum1:int, inpnum2:int, inpnum3:int, datum1:date, datum2:date):

    prepare_cache ([Res_line, Fixleist])

    t_reslin_queasy_data = []
    curr_datum:date = None
    fixleist_flag:bool = False
    fixleist_tot:Decimal = to_decimal("0.0")
    roomrate_tot:Decimal = to_decimal("0.0")
    grand_tot:Decimal = to_decimal("0.0")
    delta:int = 0
    start_date:date = None
    tmpint:int = 0
    tmpdate:date = None
    reslin_queasy = res_line = fixleist = None

    t_reslin_queasy = None

    t_reslin_queasy_data, T_reslin_queasy = create_model_like(Reslin_queasy)

    db_session = local_storage.db_session
    rkey = rkey.strip()
    inpchar = inpchar.strip()

    def generate_output():
        nonlocal t_reslin_queasy_data, curr_datum, fixleist_flag, fixleist_tot, roomrate_tot, grand_tot, delta, start_date, tmpint, tmpdate, reslin_queasy, res_line, fixleist
        nonlocal case_type, rkey, inpchar, resno, reslinno, inpnum1, inpnum2, inpnum3, datum1, datum2


        nonlocal t_reslin_queasy
        nonlocal t_reslin_queasy_data

        return {"t-reslin-queasy": t_reslin_queasy_data}

    def create_fixcost():

        nonlocal t_reslin_queasy_data, curr_datum, fixleist_flag, fixleist_tot, roomrate_tot, grand_tot, delta, start_date, tmpint, tmpdate, reslin_queasy, res_line, fixleist
        nonlocal case_type, rkey, inpchar, resno, reslinno, inpnum1, inpnum2, inpnum3, datum1, datum2


        nonlocal t_reslin_queasy
        nonlocal t_reslin_queasy_data

        t_reslin_queasy = query(t_reslin_queasy_data, filters=(lambda t_reslin_queasy: t_reslin_queasy.key.lower()  == ("FIXLEIST").lower()  and t_reslin_queasy.number1 == fixleist.artnr and t_reslin_queasy.number3 == fixleist.departement and t_reslin_queasy.deci1 == fixleist.betrag and t_reslin_queasy.date2 == curr_datum - timedelta(days=1)), first=True)

        if not t_reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            t_reslin_queasy.key = "FIXLEIST"
            t_reslin_queasy.resnr = resno
            t_reslin_queasy.reslinnr = reslinno
            t_reslin_queasy.char2 = fixleist.bezeich
            t_reslin_queasy.number1 = fixleist.artnr
            t_reslin_queasy.number2 = fixleist.number
            t_reslin_queasy.number3 = fixleist.departement
            t_reslin_queasy.date1 = curr_datum
            t_reslin_queasy.date2 = curr_datum
            t_reslin_queasy.deci1 =  to_decimal(fixleist.betrag)
            t_reslin_queasy.deci2 =  to_decimal("1")
            t_reslin_queasy.deci3 = ( to_decimal(t_reslin_queasy.number2) * to_decimal(t_reslin_queasy.deci1) )
            t_reslin_queasy.betriebsnr = fixleist.betriebsnr


        else:
            pass
            t_reslin_queasy.deci2 =  to_decimal(t_reslin_queasy.deci2) + to_decimal("1")
            t_reslin_queasy.date2 = curr_datum
            t_reslin_queasy.deci3 =  to_decimal(t_reslin_queasy.deci3) + to_decimal((t_reslin_queasy.number2) * to_decimal(t_reslin_queasy.deci1))
        fixleist_tot =  to_decimal(fixleist_tot) + to_decimal((t_reslin_queasy.number2) * to_decimal(t_reslin_queasy.deci1))
        pass
        pass


    if case_type == 1:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 2:

        if inpchar == "" and inpnum2 == 0:

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == (rkey).lower()) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno)).order_by(Reslin_queasy._recid).all():
                t_reslin_queasy = T_reslin_queasy()
                t_reslin_queasy_data.append(t_reslin_queasy)

                buffer_copy(reslin_queasy, t_reslin_queasy)

        else:

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == (rkey).lower()) & (Reslin_queasy.char1 == inpchar) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy.number2 == inpnum2)).order_by(Reslin_queasy._recid).all():
                t_reslin_queasy = T_reslin_queasy()
                t_reslin_queasy_data.append(t_reslin_queasy)

                buffer_copy(reslin_queasy, t_reslin_queasy)

    elif case_type == 3:
        for curr_datum in date_range(datum1,datum2) :

            reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"date1": [(le, curr_datum)],"date2": [(ge, curr_datum)]})

            if reslin_queasy:

                t_reslin_queasy = query(t_reslin_queasy_data, first=True)

                if not t_reslin_queasy:
                    t_reslin_queasy = T_reslin_queasy()
                    t_reslin_queasy_data.append(t_reslin_queasy)

                buffer_copy(reslin_queasy, t_reslin_queasy)
            else:
                t_reslin_queasy_data.remove(t_reslin_queasy)

                return generate_output()
    elif case_type == 4:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"char1": [(eq, inpchar)],"reslinnr": [(eq, reslinno)],"number1": [(eq, inpnum1)],"number2": [(eq, inpnum2)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 5:

        for reslin_queasy in db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == (rkey).lower()) & (Reslin_queasy.char1 == inpchar) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy.number1 == inpnum1) & (Reslin_queasy.number2 == inpnum2)).order_by(Reslin_queasy.resnr, Reslin_queasy.number3, Reslin_queasy.date1).all():
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 6:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"char1": [(eq, inpchar)],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"number1": [(eq, inpnum1)],"number2": [(eq, inpnum2)],"number3": [(eq, inpnum3)],"date1": [(le, datum1)],"date2": [(ge, datum1)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 7:

        for reslin_queasy in db_session.query(Reslin_queasy).order_by(Reslin_queasy._recid).all():
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 8:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"betriebsnr": [(eq, 0)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 9:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)],"date1": [(le, datum1)],"date2": [(ge, datum1)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 10:

        reslin_queasy = get_cache (Reslin_queasy, {"key": [(eq, rkey)],"char1": [(eq, inpchar)],"number1": [(eq, inpnum1)],"number2": [(eq, inpnum2)],"reslinnr": [(eq, reslinno)],"deci1": [(ne, 0)]})

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
    elif case_type == 11:

        reslin_queasy = db_session.query(Reslin_queasy).filter(
                 (Reslin_queasy.key == (rkey).lower()) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy.betriebsnr == inpnum1) & ((Reslin_queasy.logi1) | (Reslin_queasy.logi2) | (Reslin_queasy.logi3))).first()

        if reslin_queasy:
            t_reslin_queasy = T_reslin_queasy()
            t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)
            
    elif case_type == 12:

        if inpchar == "" and inpnum2 == 0:

            res_line = get_cache (Res_line, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

            if res_line:
                roomrate_tot =  to_decimal("0")
                for curr_datum in date_range(res_line.ankunft,res_line.abreise - 1) :

                    for reslin_queasy in db_session.query(Reslin_queasy).filter(
                             (Reslin_queasy.key == (rkey).lower()) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy.date1 <= curr_datum) & (Reslin_queasy.date2 >= curr_datum)).order_by(Reslin_queasy._recid).all():

                        t_reslin_queasy = query(t_reslin_queasy_data, filters=(lambda t_reslin_queasy: t_reslin_queasy.key == reslin_queasy.key and t_reslin_queasy.date2 == curr_datum - timedelta(days=1) and t_reslin_queasy.deci1 == reslin_queasy.deci1), first=True)

                        if not t_reslin_queasy:
                            t_reslin_queasy = T_reslin_queasy()
                            t_reslin_queasy_data.append(t_reslin_queasy)

                            buffer_copy(reslin_queasy, t_reslin_queasy,except_fields=["reslin_queasy.char1","reslin_queasy.date1","reslin_queasy.date2","reslin_queasy.number2"])
                            t_reslin_queasy.date1 = curr_datum
                            t_reslin_queasy.date2 = curr_datum
                            t_reslin_queasy.deci2 =  to_decimal("1")
                            t_reslin_queasy.deci3 =  to_decimal(t_reslin_queasy.deci1)
                        else:
                            pass
                            t_reslin_queasy.date2 = curr_datum
                            t_reslin_queasy.deci2 =  to_decimal(t_reslin_queasy.deci2) + to_decimal("1")
                            t_reslin_queasy.deci3 =  to_decimal(t_reslin_queasy.deci3) + to_decimal(t_reslin_queasy.deci1)
                        roomrate_tot =  to_decimal(roomrate_tot) + to_decimal(t_reslin_queasy.deci1)
                        pass
                        pass

                    t_reslin_queasy = query(t_reslin_queasy_data, filters=(lambda t_reslin_queasy: t_reslin_queasy.key.lower()  == ("arrangement").lower()  and t_reslin_queasy.resnr == resno and t_reslin_queasy.reslinnr == reslinno), first=True)

                    if not t_reslin_queasy:
                        t_reslin_queasy = T_reslin_queasy()
                        t_reslin_queasy_data.append(t_reslin_queasy)

                        t_reslin_queasy.key = "arrangement"
                        t_reslin_queasy.resnr = resno
                        t_reslin_queasy.reslinnr = reslinno
                        t_reslin_queasy.date1 = res_line.ankunft
                        t_reslin_queasy.date2 = res_line.abreise
                        t_reslin_queasy.char2 = "ROOM CHARGE"
                        t_reslin_queasy.deci1 =  to_decimal(res_line.zipreis)
                        t_reslin_queasy.deci2 =  to_decimal(t_reslin_queasy.date2) - to_decimal(t_reslin_queasy.date1)
                        t_reslin_queasy.deci3 =  to_decimal(t_reslin_queasy.deci1) * to_decimal(t_reslin_queasy.deci2)
                        roomrate_tot =  to_decimal(t_reslin_queasy.deci3)

                    fixleist = get_cache (Fixleist, {"resnr": [(eq, resno)],"reslinnr": [(eq, reslinno)]})

                    if fixleist:

                        t_reslin_queasy = query(t_reslin_queasy_data, filters=(lambda t_reslin_queasy: t_reslin_queasy.key.lower()  == ("FIXLEIST").lower()  and t_reslin_queasy.char1.lower()  == ("FIX COST").lower()), first=True)

                        if not t_reslin_queasy:
                            t_reslin_queasy = T_reslin_queasy()
                            t_reslin_queasy_data.append(t_reslin_queasy)

                            t_reslin_queasy.key = "FIXLEIST"
                            t_reslin_queasy.resnr = resno
                            t_reslin_queasy.reslinnr = reslinno
                            t_reslin_queasy.char1 = "FIX COST"

                        for fixleist in db_session.query(Fixleist).filter(
                                 (Fixleist.resnr == resno) & (Fixleist.reslinnr == reslinno)).order_by(Fixleist.departement, Fixleist.artnr).all():

                            if fixleist.sequenz == 1:
                                create_fixcost()

                            elif fixleist.sequenz == 2 or fixleist.sequenz == 3:

                                if res_line.ankunft == curr_datum:
                                    create_fixcost()

                            elif fixleist.sequenz == 4 and get_day(curr_datum) == 1:
                                create_fixcost()

                            elif fixleist.sequenz == 5 and get_day(curr_datum + 1) == 1:
                                create_fixcost()

                            elif fixleist.sequenz == 6:

                                if fixleist.lfakt == None:
                                    delta = 0
                                else:
                                    delta = (fixleist.lfakt - res_line.ankunft).days

                                    if delta < 0:
                                        delta = 0
                                start_date = res_line.ankunft + timedelta(days=delta)
                                tmpint = (res_line.abreise - start_date).days

                                if tmpint < fixleist.dekade:
                                    start_date = res_line.ankunft
                                tmpint = fixleist.dekade - 1
                                tmpdate = start_date + timedelta(days=tmpint)

                                if curr_datum <= tmpdate and curr_datum >= start_date:
                                    create_fixcost()

                if roomrate_tot != 0:
                    t_reslin_queasy = T_reslin_queasy()
                    t_reslin_queasy_data.append(t_reslin_queasy)

                    t_reslin_queasy.key = "arrangement"
                    t_reslin_queasy.char1 = "SUB T O T A L"
                    t_reslin_queasy.deci3 =  to_decimal(roomrate_tot)
                    t_reslin_queasy.betriebsnr = 99999

                if fixleist_tot != 0:
                    t_reslin_queasy = T_reslin_queasy()
                    t_reslin_queasy_data.append(t_reslin_queasy)

                    t_reslin_queasy.key = "FIXLEIST"
                    t_reslin_queasy.char1 = "SUB T O T A L"
                    t_reslin_queasy.deci3 =  to_decimal(fixleist_tot)
                    t_reslin_queasy.betriebsnr = 99999
                    t_reslin_queasy = T_reslin_queasy()
                    t_reslin_queasy_data.append(t_reslin_queasy)

                    t_reslin_queasy.key = "TOTAL"
                    t_reslin_queasy.char1 = "SUB T O T A L"
                    t_reslin_queasy.deci3 =  to_decimal(roomrate_tot) + to_decimal(fixleist_tot)
                    t_reslin_queasy.betriebsnr = 99999
                t_reslin_queasy.char1 = "T O T A L *"

                if res_line.zimmeranz > 1:
                    t_reslin_queasy = T_reslin_queasy()
                    t_reslin_queasy_data.append(t_reslin_queasy)

                    t_reslin_queasy.key = "TOTAL"
                    t_reslin_queasy.char1 = "TOTAL CHARGED"
                    t_reslin_queasy.char2 = "Room QTY x (T O T A L*)"
                    t_reslin_queasy.deci1 = ( to_decimal(roomrate_tot) + to_decimal(fixleist_tot) )
                    t_reslin_queasy.number2 = res_line.zimmeranz
                    t_reslin_queasy.deci3 =  to_decimal(t_reslin_queasy.deci1) * to_decimal(t_reslin_queasy.number2)
                    t_reslin_queasy.betriebsnr = 99999


        else:

            for reslin_queasy in db_session.query(Reslin_queasy).filter(
                     (Reslin_queasy.key == (rkey).lower()) & (Reslin_queasy.char1 == inpchar) & (Reslin_queasy.resnr == resno) & (Reslin_queasy.reslinnr == reslinno) & (Reslin_queasy.number2 == inpnum2)).order_by(Reslin_queasy._recid).all():
                t_reslin_queasy = T_reslin_queasy()
                t_reslin_queasy_data.append(t_reslin_queasy)

            buffer_copy(reslin_queasy, t_reslin_queasy)

    return generate_output()