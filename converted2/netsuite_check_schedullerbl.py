#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Queasy

if_list_data, If_list = create_model("If_list", {"perideno":int, "send_date":date, "fr_date":date, "to_date":date, "sendflag":bool, "resendflag":bool})

def netsuite_check_schedullerbl(casetype:int, month_val:int, if_list_data:[If_list]):

    prepare_cache ([Htparam, Queasy])

    cur_time:string = ""
    time_send:string = "14:00"
    daylist:string = "Sunday,Monday,Tuesday,Wednesday,Thursday,Friday,Saturday"
    dayrun:string = "Tuesday"
    dayrunfrom:string = "Monday"
    dayrunto:string = "Sunday"
    daynum:int = 0
    daynumrun:int = 0
    dayname:string = ""
    daynamerun:string = ""
    get_period:int = 0
    loop_i:int = 0
    loop_run:int = 0
    lastdate:date = None
    lastday:int = 0
    rundate:date = None
    caldate:date = None
    get_senddate:date = None
    get_sendday:int = 0
    fdate:date = None
    tdate:date = None
    datum:date = None
    htparam = queasy = None

    period = if_list = None

    period_data, Period = create_model("Period", {"perideno":int, "send_date":date, "from_date":date, "to_date":date})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cur_time, time_send, daylist, dayrun, dayrunfrom, dayrunto, daynum, daynumrun, dayname, daynamerun, get_period, loop_i, loop_run, lastdate, lastday, rundate, caldate, get_senddate, get_sendday, fdate, tdate, datum, htparam, queasy
        nonlocal casetype, month_val


        nonlocal period, if_list
        nonlocal period_data

        return {"if-list": if_list_data}


    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    datum = htparam.fdate

    if casetype == 1:
        lastdate = date_mdy(get_month(datum) + timedelta(days=1, 1, get_year(datum)))
        lastdate = lastdate - timedelta(days=1)
        lastday = get_day(lastdate)
        daynum = get_weekday(datum)
        dayname = entry(daynum - 1, daylist)
        for loop_i in range(1,lastday + 1) :
            caldate = date_mdy(get_month(datum) , loop_i, get_year(datum))
            daynum = get_weekday(caldate)
            dayname = entry(daynum - 1, daylist)

            if dayname.lower()  == (dayrun).lower() :
                get_senddate = caldate
                get_sendday = get_day(caldate)

                if get_sendday <= 10:
                    fdate = date_mdy(get_month(caldate) , 1, get_year(caldate))
                    for loop_run in range(1,get_sendday + 1) :
                        rundate = date_mdy(get_month(fdate) , loop_run, get_year(fdate))
                        daynumrun = get_weekday(rundate)
                        daynamerun = entry(daynumrun - 1, daylist)

                        if daynamerun.lower()  == (dayrunto).lower() :
                            tdate = date_mdy(get_month(fdate) , loop_run, get_year(fdate))
                else:
                    for loop_run in range(1,get_sendday + 1) :
                        rundate = date_mdy(get_month(caldate) , loop_run, get_year(caldate))
                        daynumrun = get_weekday(rundate)
                        daynamerun = entry(daynumrun - 1, daylist)

                        if daynamerun.lower()  == (dayrunfrom).lower() :
                            fdate = date_mdy(get_month(rundate) , loop_run, get_year(rundate)) - timedelta(days=7)

                        if daynamerun.lower()  == (dayrunto).lower() :
                            tdate = date_mdy(get_month(rundate) , loop_run, get_year(rundate))

                if tdate == None:
                    pass
                else:
                    period = Period()
                    period_data.append(period)

                    get_period = get_period + 1
                    period.perideno = get_period
                    period.send_date = get_senddate
                    period.from_date = fdate
                    period.to_date = tdate

        for period in query(period_data, sort_by=[("perideno",True)]):
            get_period = period.perideno + 1
            tdate = period.to_date
            break

        if tdate != lastdate:
            period = Period()
            period_data.append(period)

            period.perideno = get_period
            period.send_date = lastdate
            period.from_date = lastdate - ((lastdate - tdate) - 1)
            period.to_date = lastdate

        for period in query(period_data):

            queasy = get_cache (Queasy, {"key": [(eq, 259)],"betriebsnr": [(eq, get_month(period.send_date))],"number1": [(eq, period.perideno)]})

            if not queasy:
                queasy = Queasy()
                db_session.add(queasy)

                queasy.key = 259
                queasy.betriebsnr = get_month(period.send_date)
                queasy.number1 = period.perideno
                queasy.date1 = period.send_date
                queasy.date2 = period.from_date
                queasy.date3 = period.to_date
                queasy.logi1 = False
                queasy.logi2 = False

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 259) & (Queasy.betriebsnr == get_month(datum))).order_by(Queasy._recid).all():
            if_list = If_list()
            if_list_data.append(if_list)

            if_list.perideno = queasy.number1
            if_list.send_date = queasy.date1
            if_list.fr_date = queasy.date2
            if_list.to_date = queasy.date3
            if_list.sendflag = queasy.logi1
            if_list.resendflag = queasy.logi2

    elif casetype == 2:

        for if_list in query(if_list_data):

            queasy = get_cache (Queasy, {"key": [(eq, 259)],"betriebsnr": [(eq, get_month(if_list.send_date))],"number1": [(eq, if_list.perideno)]})

            if queasy:
                queasy.logi1 = True


                queasy.logi2 = True

    elif casetype == 3:

        for queasy in db_session.query(Queasy).filter(
                 (Queasy.key == 259) & (Queasy.betriebsnr == month_val) & (get_year(Queasy.date1) == get_year(get_current_date()))).order_by(Queasy._recid).all():
            if_list = If_list()
            if_list_data.append(if_list)

            if_list.perideno = queasy.number1
            if_list.send_date = queasy.date1
            if_list.fr_date = queasy.date2
            if_list.to_date = queasy.date3
            if_list.sendflag = queasy.logi1
            if_list.resendflag = queasy.logi2

    return generate_output()