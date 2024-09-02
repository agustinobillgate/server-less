from functions.additional_functions import *
import decimal
from functions.update_repeatflag_bl import update_repeatflag_bl
from sqlalchemy import func
from models import Queasy, Bediener, Res_history

def bookengine_config_btn_exit_2bl(bookengid:int, autostart:bool, period:int, delay:int, hotelcode:str, username:str, password:str, liveflag:bool, defcurr:str, pushrateflag:bool, pullbookflag:bool, pushavailflag:bool, workpath:str, progavail:str, user_init:str, pushratebypax:bool, uppercasename:bool, delayrate:int, delaypull:int, delayavail:int, pushall:bool, re_calculate:bool, restriction:bool, allotment:bool, pax:int, bedsetup:bool, pushbookflag:bool, delaypushbook:int, vcwsagent:str, vcwsagent2:str, vcwsagent3:str, vcwsagent4:str, vcwsagent5:str, vcwebhost:str, vcwebport:str, email:str, dyna_code:str):
    i:int = 0
    str:str = ""
    oldstr:str = ""
    ct:str = ""
    oldct:str = ""
    progavail1:str = ""
    queasy = bediener = res_history = None


    db_session = local_storage.db_session

    def generate_output():
        nonlocal i, str, oldstr, ct, oldct, progavail1, queasy, bediener, res_history


        return {}

    progavail1 = progavail + " == " +\
            dyna_code + " == " +\
            to_string(pushratebypax) + " == " +\
            to_string(uppercasename) + " == " +\
            to_string(delayrate) + " == " +\
            to_string(delaypull) + " == " +\
            to_string(delayavail) + " == " +\
            to_string(pushall) + " == " +\
            to_string(re_calculate) + " == " +\
            to_string(restriction) + " == " +\
            to_string(allotment) + " == " +\
            to_string(pax) + " == " +\
            to_string(bedsetup) + " == " +\
            to_string(pushbookflag) + " == " +\
            to_string(delaypushbook) + " == " +\
            vcwsagent + " == " +\
            vcwsagent2 + " == " +\
            vcwsagent3 + " == " +\
            vcwsagent4 + " == " +\
            vcwebhost + " == " +\
            vcwebport + " == " +\
            email + " == " +\
            vcwsagent5


    ct = "$autostart$" + to_string(autostart) + ";" + "$period$" + to_string(period) + ";" + "$delay$" + to_string(delay) + ";" + "$liveflag$" + to_string(liveflag) + ";" + "$defcurr$" + to_string(defcurr) + ";" + "$workpath$" + to_string(workpath) + ";" + "$progname$" + to_string(progavail1) + ";" + "$htlcode$" + to_string(hotelcode) + ";" + "$username$" + to_string(username) + ";" + "$password$" + to_string(password) + ";" + "$pushrate$" + to_string(pushrateflag) + ";" + "$pullbook$" + to_string(pullbookflag) + ";" + "$pushavail$" + to_string(pushavailflag)

    queasy = db_session.query(Queasy).filter(
            (Queasy.KEY == 160) &  (Queasy.number1 == bookengid)).first()

    if queasy:

        if queasy.char1.lower()  != (ct).lower() :
            get_output(update_repeatflag_bl())
        oldct = queasy.char1

        queasy = db_session.query(Queasy).first()
        queasy.char1 = ct

        queasy = db_session.query(Queasy).first()
        for i in range(1,num_entries(ct, ";")  + 1) :
            str = entry(i - 1, ct, ";")
            oldstr = entry(i - 1, oldct, ";")

            if oldstr.lower()  != (str).lower() :

                bediener = db_session.query(Bediener).filter(
                        (func.lower(Bediener.userinit) == (user_init).lower())).first()

                if bediener:
                    res_history = Res_history()
                    db_session.add(res_history)

                    res_history.nr = bediener.nr
                    res_history.datum = get_current_date()
                    res_history.zeit = get_current_time_in_seconds()
                    res_history.aenderung = "Change Config from: " + oldstr + ", to: " + str
                    res_history.action = "Booking Engine Interface"

                    res_history = db_session.query(Res_history).first()

    else:
        queasy = Queasy()
        db_session.add(queasy)

        queasy.key = 160
        queasy.number1 = bookengid
        queasy.char1 = ct

        bediener = db_session.query(Bediener).filter(
                (func.lower(Bediener.userinit) == (user_init).lower())).first()

        if bediener:
            res_history = Res_history()
            db_session.add(res_history)

            res_history.nr = bediener.nr
            res_history.datum = get_current_date()
            res_history.zeit = get_current_time_in_seconds()
            res_history.aenderung = "Set Config, Booking Engine ID: " + to_string(bookengid) + ", Config: " + ct
            res_history.action = "Booking Engine Interface"

            res_history = db_session.query(Res_history).first()


    return generate_output()