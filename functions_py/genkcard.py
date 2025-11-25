#using conversion tools version: 1.0.0.119

#------------------------------------------
# SKIP SKIP
# Rd, 24/11/2025, Update last counter dengan next_counter_for_update
#------------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Res_line, Zimmer, Counters, Queasy
from functions.next_counter_for_update import next_counter_for_update

def genkcard(ipccommand:int, iocroomno:string, room2:string, room3:string, iodfrom:date, iodto:date, ioitimefrom:int, ioitimeto:int, iocparms:string):

    prepare_cache ([Htparam, Res_line, Zimmer, Counters, Queasy])

    lvires = 0
    variable = None
    ci_date:date = None
    lvcport:string = ""
    lvcdatea:string = ""
    lvcdateb:string = ""
    lvchotelid:string = ""
    lviwtime:int = 4
    lvcrw:string = ""
    lvccard:string = ""
    lvcguest:string = ""
    lvcroom:string = ""
    lvm1:bytes = None
    lvm2:bytes = None
    lviidx:int = 0
    lviresnr:int = 0
    lviresnlinr:int = 1
    lvlexec:bool = True
    lvcerror:string = ""
    lvicntr:int = 0
    htparam = res_line = zimmer = counters = queasy = None

    db_session = local_storage.db_session
    last_count = 0
    error_lock:string = ""
    iocroomno = iocroomno.strip()
    room2 = room2.strip()
    room3 = room3.strip()
    iocparms = iocparms.strip()


    def generate_output():
        nonlocal lvires, variable, ci_date, lvcport, lvcdatea, lvcdateb, lvchotelid, lviwtime, lvcrw, lvccard, lvcguest, lvcroom, lvm1, lvm2, lviidx, lviresnr, lviresnlinr, lvlexec, lvcerror, lvicntr, htparam, res_line, zimmer, counters, queasy
        nonlocal ipccommand, iocroomno, room2, room3, iodfrom, iodto, ioitimefrom, ioitimeto, iocparms

        return {"iocroomno": iocroomno, "room2": room2, "room3": room3, "iodfrom": iodfrom, "iodto": iodto, "ioitimefrom": ioitimefrom, "ioitimeto": ioitimeto, "iocparms": iocparms, "lvires": lvires}

    def writecard():

        nonlocal lvires, variable, ci_date, lvcport, lvcdatea, lvcdateb, lvchotelid, lviwtime, lvcrw, lvccard, lvcguest, lvcroom, lvm1, lvm2, lviidx, lviresnr, lviresnlinr, lvlexec, lvcerror, lvicntr, htparam, res_line, zimmer, counters, queasy
        nonlocal ipccommand, iocroomno, room2, room3, iodfrom, iodto, ioitimefrom, ioitimeto, iocparms

        i:int = 0
        t1_info:string = "VHP-"
        gname:string = "-,"
        ct:string = ""
        st:string = ""
        floor:string = ""
        building:string = ""

        if lviresnr > 0:

            res_line = get_cache (Res_line, {"resnr": [(eq, lviresnr)],"reslinnr": [(eq, lviresnlinr)]})

            if res_line:
                gname = replace_str(trim(res_line.name) , " ", "_")
                gname = replace_str(gname, ",", "")
                gname = gname + ","


            else:
                gname = "-,"

        zimmer = get_cache (Zimmer, {"zinr": [(eq, lvcroom)]})

        if zimmer:
            floor = to_string(zimmer.etage)
            building = to_string(zimmer.code)

        if room2 != "":
            st = ";R2" + room2

        if room3 != "":
            st = st + ";R3" + room3
        ct = "XW" + ";PN" + "1" + ";RN" + lvcroom + st + ";NA" + gname + ";KC" + lvcport + ";TY" + lvccard + ";ct" + to_string(ioitimefrom) + ";OT" + to_string(ioitimeto) + ";CD" + to_string(get_month(iodfrom) , "99") + "/" + to_string(get_day(iodfrom) , "99") + "/" + to_string(get_year(iodfrom) , "9999") + ";OD" + to_string(get_month(iodto) , "99") + "/" + to_string(get_day(iodto) , "99") + "/" + to_string(get_year(iodto) , "9999") + ";ID" + user_init + ";T1" + t1_info + ";T2" + "-" + ";T3" + "-" + ";FL" + floor + ";BD" + building

        counters = get_cache (Counters, {"counter_no": [(eq, 30)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 30
            counters.counter_bez = "Counter for KeyCard Sequence"


        # counters.counter = counters.counter + 1
        # last_count, error_lock = get_output(next_counter_for_update(30))

        # if counters.counter > 9999:
        #     counters.counter = 1
        counters = db_session.query(Counters).filter(Counters.counter_no == 30).with_for_update().first()
        counters.counter = counters.counter + 1
        if counters.counter > 9999:
            counters.counter = 1
        db_session.commit()
        

        pass
        lvicntr = counters.counter


        iocparms = iocparms + ",Sequence=" + to_string(lvicntr)
        ct = ct + ";SQ" + to_string(counters.counter) + ";" + "&&" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS") + ";"
        queasy = Queasy()
        db_session.add(queasy)

        queasy.betriebsnr = 1
        queasy.key = 30
        queasy.date1 = get_current_date()
        queasy.logi1 = True
        queasy.char1 = "keycard"
        queasy.number1 = lvicntr
        queasy.number2 = lviresnr
        queasy.number3 = lviresnlinr
        queasy.char2 = lvcport
        queasy.char3 = ct


        pass
        pass
        pass


    def readcard():

        nonlocal lvires, variable, ci_date, lvcport, lvcdatea, lvcdateb, lvchotelid, lviwtime, lvcrw, lvccard, lvcguest, lvcroom, lvm1, lvm2, lviidx, lviresnr, lviresnlinr, lvlexec, lvcerror, lvicntr, htparam, res_line, zimmer, counters, queasy
        nonlocal ipccommand, iocroomno, room2, room3, iodfrom, iodto, ioitimefrom, ioitimeto, iocparms

        ct:string = ""
        ct = "XR" + ";KC" + lvcport

        counters = get_cache (Counters, {"counter_no": [(eq, 30)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 30
            counters.counter_bez = "Counter for KeyCard Sequence"


        # counters.counter = counters.counter + 1

        # if counters.counter > 99999999:
        #     counters.counter = 1

        counters = db_session.query(Counters).filter(Counters.counter_no == 30).with_for_update().first()
        counters.counter = counters.counter + 1
        if counters.counter > 99999999:
            counters.counter = 1
        db_session.commit()

        pass
        lvicntr = counters.counter


        iocparms = iocparms + ",Sequence=" + to_string(lvicntr)
        ct = ct + ";SQ" + to_string(counters.counter) + ";" + "&&" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS") + ";"
        queasy = Queasy()
        db_session.add(queasy)

        queasy.betriebsnr = 1
        queasy.key = 30
        queasy.date1 = get_current_date()
        queasy.logi1 = True
        queasy.char1 = "keycard"
        queasy.number1 = lvicntr
        queasy.number2 = lviresnr
        queasy.number3 = lviresnlinr
        queasy.char2 = lvcport
        queasy.char3 = ct


        pass
        pass
        pass


    def erasecard():

        nonlocal lvires, variable, ci_date, lvcport, lvcdatea, lvcdateb, lvchotelid, lviwtime, lvcrw, lvccard, lvcguest, lvcroom, lvm1, lvm2, lviidx, lviresnr, lviresnlinr, lvlexec, lvcerror, lvicntr, htparam, res_line, zimmer, counters, queasy
        nonlocal ipccommand, iocroomno, room2, room3, iodfrom, iodto, ioitimefrom, ioitimeto, iocparms

        ct:string = ""
        ct = "XE" + ";KC" + lvcport + ";RN" + lvcroom

        counters = get_cache (Counters, {"counter_no": [(eq, 30)]})

        if not counters:
            counters = Counters()
            db_session.add(counters)

            counters.counter_no = 30
            counters.counter_bez = "Counter for KeyCard Sequence"


        # counters.counter = counters.counter + 1

        # if counters.counter > 99999999:
        #     counters.counter = 1
        counters = db_session.query(Counters).filter(Counters.counter_no == 30).with_for_update().first()
        counters.counter = counters.counter + 1
        if counters.counter > 99999999:
            counters.counter = 1
        db_session.commit()

        pass
        lvicntr = counters.counter


        iocparms = iocparms + ",Sequence=" + to_string(lvicntr)
        ct = ct + ";SQ" + to_string(lvicntr) + ";" + "&&" + to_string(get_current_date()) + "-" + to_string(get_current_time_in_seconds(), "HH:MM:SS") + ";"
        queasy = Queasy()
        db_session.add(queasy)

        queasy.betriebsnr = 1
        queasy.key = 30
        queasy.date1 = get_current_date()
        queasy.logi1 = True
        queasy.char1 = "keycard"
        queasy.number1 = lvicntr
        queasy.number2 = lviresnr
        queasy.number3 = lviresnlinr
        queasy.char2 = lvcport
        queasy.char3 = ct


        pass
        pass
        pass

    htparam = get_cache (Htparam, {"paramnr": [(eq, 922)]})

    if not htparam:

        return generate_output()
    lvchotelid = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 923)]})

    if not htparam:

        return generate_output()
    lviwtime = to_int(htparam.fchar)

    htparam = get_cache (Htparam, {"paramnr": [(eq, 87)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 924)]})

    if not htparam:

        return generate_output()
    lvlexec = not (htparam.fchar BEGINS "N")
    for lviidx in range(1,num_entries(iocparms)  + 1) :

        if entry(0, entry(lviidx - 1, iocparms) , "=") == "resnr":
            lviresnr = to_int(entry(1, entry(lviidx - 1, iocparms) , "="))


        elif entry(0, entry(lviidx - 1, iocparms) , "=") == "reslinnr":
            lviresnlinr = to_int(entry(1, entry(lviidx - 1, iocparms) , "="))


        elif entry(0, entry(lviidx - 1, iocparms) , "=") == "cardtype":
            lvccard = to_string(-1 + to_int(entry(1, entry(lviidx - 1, iocparms) , "=")))
        elif entry(0, entry(lviidx - 1, iocparms) , "=") == "coder":
            lvcport = entry(1, entry(lviidx - 1, iocparms) , "=")

    if lvcport == "":
        for lviidx in range(1,num_entries(SESSION:PARAMETER, ";")  + 1) :

            if trim(entry(lviidx - 1, SESSION:PARAMETER, ";")) BEGINS "coder":
                lvcport = entry(1, entry(lviidx - 1, SESSION:PARAMETER, ";") , "=")


    lvcroom = iocroomno

    if ipccommand == 1:
        writecard()

    elif ipccommand == 2:
        readcard()

    elif ipccommand == 3:
        erasecard()

    return generate_output()