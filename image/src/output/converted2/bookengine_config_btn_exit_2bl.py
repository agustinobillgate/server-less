#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from functions.update_repeatflag_bl import update_repeatflag_bl
from models import Queasy, Bediener, Res_history

def bookengine_config_btn_exit_2bl(bookengid:int, autostart:bool, period:int, delay:int, hotelcode:string, username:string, password:string, liveflag:bool, defcurr:string, pushrateflag:bool, pullbookflag:bool, pushavailflag:bool, workpath:string, progavail:string, user_init:string, pushratebypax:bool, uppercasename:bool, delayrate:int, delaypull:int, delayavail:int, pushall:bool, re_calculate:bool, restriction:bool, allotment:bool, pax:int, bedsetup:bool, pushbookflag:bool, delaypushbook:int, vcwsagent:string, vcwsagent2:string, vcwsagent3:string, vcwsagent4:string, vcwsagent5:string, vcwebhost:string, vcwebport:string, email:string, dyna_code:string):

    prepare_cache ([Queasy, Bediener, Res_history])

    i:int = 0
    str:string = ""
    oldstr:string = ""
    ct:string = ""
    oldct:string = ""
    progavail1:string = ""
    queasy = bediener = res_history = None

    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, str, oldstr, ct, oldct, progavail1, queasy, bediener, res_history
        nonlocal bookengid, autostart, period, delay, hotelcode, username, password, liveflag, defcurr, pushrateflag, pullbookflag, pushavailflag, workpath, progavail, user_init, pushratebypax, uppercasename, delayrate, delaypull, delayavail, pushall, re_calculate, restriction, allotment, pax, bedsetup, pushbookflag, delaypushbook, vcwsagent, vcwsagent2, vcwsagent3, vcwsagent4, vcwsagent5, vcwebhost, vcwebport, email, dyna_code

        return {}

    progavail1 = progavail + "=" +\
            dyna_code + "=" +\
            to_string(pushratebypax) + "=" +\
            to_string(uppercasename) + "=" +\
            to_string(delayrate) + "=" +\
            to_string(delaypull) + "=" +\
            to_string(delayavail) + "=" +\
            to_string(pushall) + "=" +\
            to_string(re_calculate) + "=" +\
            to_string(restriction) + "=" +\
            to_string(allotment) + "=" +\
            to_string(pax) + "=" +\
            to_string(bedsetup) + "=" +\
            to_string(pushbookflag) + "=" +\
            to_string(delaypushbook) + "=" +\
            vcwsagent + "=" +\
            vcwsagent2 + "=" +\
            vcwsagent3 + "=" +\
            vcwsagent4 + "=" +\
            vcwebhost + "=" +\
            vcwebport + "=" +\
            email + "=" +\
            vcwsagent5


    ct = "$autostart$" + to_string(autostart) + ";" + "$period$" + to_string(period) + ";" + "$delay$" + to_string(delay) + ";" + "$liveflag$" + to_string(liveflag) + ";" + "$defcurr$" + to_string(defcurr) + ";" + "$workpath$" + to_string(workpath) + ";" + "$progname$" + to_string(progavail1) + ";" + "$htlcode$" + to_string(hotelcode) + ";" + "$username$" + to_string(username) + ";" + "$password$" + to_string(password) + ";" + "$pushrate$" + to_string(pushrateflag) + ";" + "$pullbook$" + to_string(pullbookflag) + ";" + "$pushavail$" + to_string(pushavailflag)

    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, bookengid)]})

    if queasy:

        if queasy.char1.lower()  != (ct).lower() :
            get_output(update_repeatflag_bl())
        oldct = queasy.char1
        pass
        queasy.char1 = ct
        pass
        for i in range(1,num_entries(ct, ";")  + 1) :
            str = entry(i - 1, ct, ";")
            oldstr = entry(i - 1, oldct, ";")

            if oldstr.lower()  != (str).lower() :

                bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Change Config from: " + oldstr + ", to: " + str
                    res_history.action = "Booking Engine Interface"


                    pass
                    pass
    else:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 160
        queasy.number1 = bookengid
        queasy.char1 = ct

        bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Set Config, Booking Engine ID: " + to_string(bookengid) + ", Config: " + ct
            res_history.action = "Booking Engine Interface"


            pass
            pass

    return generate_output()