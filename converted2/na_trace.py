from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Htparam, Guest, Res_line, Reslin_queasy

def na_trace():
    ci_date:date = None
    loopi:int = 0
    doit:bool = False
    htparam = guest = res_line = reslin_queasy = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal ci_date, loopi, doit, htparam, guest, res_line, reslin_queasy

        return {}


    htparam = db_session.query(Htparam).filter(
             (Htparam.paramnr == 110)).first()

    if htparam:
        ci_date = htparam.fdate + timedelta(days=1)

    res_line_obj_list = []
    for res_line, guest in db_session.query(Res_line, Guest).join(Guest,(Guest.gastnr == Res_line.gastnr) & (Guest.karteityp == 2) & (Guest.steuernr != "")).filter(
             ((Res_line.ankunft == ci_date) | (Res_line.abreise == ci_date)) & (Res_line.resstatus != 11) & (Res_line.resstatus != 13) & (Res_line.resstatus != 99) & (Res_line.gastnr > 0) & (Res_line.l_zuordnung[inc_value(2)] == 0)).order_by(Res_line._recid).all():
        if res_line._recid in res_line_obj_list:
            continue
        else:
            res_line_obj_list.append(res_line._recid)


        doit = True

        if re.match(r".*e1-booking.*",guest.name, re.IGNORECASE):
            doit = False

        if doit:
            for loopi in range(0,2 + 1) :

                reslin_queasy = db_session.query(Reslin_queasy).filter(
                         (func.lower(Reslin_queasy.key) == ("flag").lower()) & (Reslin_queasy.resnr == res_line.resnr) & (Reslin_queasy.reslinnr == res_line.reslinnr) & (Reslin_queasy.betriebsnr == loopi)).first()

                if not reslin_queasy:
                    reslin_queasy = Reslin_queasy()
                    db_session.add(reslin_queasy)

                    reslin_queasy.key = "flag"
                    reslin_queasy.resnr = res_line.resnr
                    reslin_queasy.reslinnr = res_line.reslinnr
                    reslin_queasy.betriebsnr = loopi
                    reslin_queasy.date1 = ci_date
                    reslin_queasy.char1 = "Booking by OTA : " + to_string(guest.NAME, "x(70)")
                    reslin_queasy.char1 = reslin_queasy.char1 + chr(2) + "$$"
                    reslin_queasy.char1 = reslin_queasy.char1 +\
                            chr(2) + to_string(get_month(ci_date) , "99") +\
                            to_string(get_day(ci_date) , "99") +\
                            to_string(get_year(ci_date)) +\
                            chr(2) + "1"
                    reslin_queasy.number1 = 0
                    reslin_queasy.deci1 =  to_decimal("0")

                    if res_line.ankunft == ci_date:
                        reslin_queasy.char1 = reslin_queasy.char1 + chr(2) +\
                            to_string(to_int(YES))

                    elif res_line.abreise == ci_date:
                        reslin_queasy.logi1 = True


                    break
                else:

                    if reslin_queasy.date1 == None:
                        reslin_queasy.date1 = ci_date
                        reslin_queasy.char1 = "Booking by OTA : " + to_string(guest.NAME, "x(70)")
                        reslin_queasy.char1 = reslin_queasy.char1 + chr(2) + "$$"
                        reslin_queasy.char1 = reslin_queasy.char1 +\
                                chr(2) + to_string(get_month(ci_date) , "99") +\
                                to_string(get_day(ci_date) , "99") +\
                                to_string(get_year(ci_date)) +\
                                chr(2) + "1"
                        reslin_queasy.number1 = 0
                        reslin_queasy.deci1 =  to_decimal("0")

                        if res_line.ankunft == ci_date:
                            reslin_queasy.char1 = reslin_queasy.char1 + chr(2) +\
                                to_string(to_int(YES))

                        elif res_line.abreise == ci_date:
                            reslin_queasy.logi1 = True


                        break

                    elif reslin_queasy.date2 == None:
                        reslin_queasy.date2 = ci_date
                        reslin_queasy.char2 = "Booking by OTA : " + to_string(guest.NAME, "x(70)")
                        reslin_queasy.char2 = reslin_queasy.char2 + chr(2) + "$$"
                        reslin_queasy.char2 = reslin_queasy.char2 +\
                                chr(2) + to_string(get_month(ci_date) , "99") +\
                                to_string(get_day(ci_date) , "99") +\
                                to_string(get_year(ci_date)) +\
                                chr(2) + "1"
                        reslin_queasy.number2 = 0
                        reslin_queasy.deci2 =  to_decimal("0")

                        if res_line.ankunft == ci_date:
                            reslin_queasy.char2 = reslin_queasy.char2 + chr(2) +\
                                to_string(to_int(YES))

                        elif res_line.abreise == ci_date:
                            reslin_queasy.logi2 = True


                        break

                    elif reslin_queasy.date3 == None:
                        reslin_queasy.date3 = ci_date
                        reslin_queasy.char3 = "Booking by OTA : " + to_string(guest.NAME, "x(70)")
                        reslin_queasy.char3 = reslin_queasy.char3 + chr(2) + "$$"
                        reslin_queasy.char3 = reslin_queasy.char3 +\
                                chr(2) + to_string(get_month(ci_date) , "99") +\
                                to_string(get_day(ci_date) , "99") +\
                                to_string(get_year(ci_date)) +\
                                chr(2) + "1"
                        reslin_queasy.number3 = 0
                        reslin_queasy.deci3 =  to_decimal("0")

                        if res_line.ankunft == ci_date:
                            reslin_queasy.char3 = reslin_queasy.char3 + chr(2) +\
                                to_string(to_int(YES))

                        elif res_line.abreise == ci_date:
                            reslin_queasy.logi3 = True


                        break

    return generate_output()