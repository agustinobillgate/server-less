#using conversion tools version: 1.0.0.117

#------------------------------------------
# Rd, 12/11/2025
# tambah strip payload,
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Bediener, Res_history, Guest_pr

def bookengine_config_btn_exit_web_3bl(bookengid:int, autostart:bool, period:int, delay:int, hotelcode:string, username:string, password:string, liveflag:bool, defcurr:string, pushrateflag:bool, pullbookflag:bool, pushavailflag:bool, workpath:string, progavail:string, user_init:string, pushratebypax:bool, uppercasename:bool, delayrate:int, delaypull:int, delayavail:int, pushall:bool, re_calculate:bool, restriction:bool, allotment:bool, pax:int, bedsetup:bool, pushbookflag:bool, delaypushbook:int, vcwsagent:string, vcwsagent2:string, vcwsagent3:string, vcwsagent4:string, vcwsagent5:string, vcwebhost:string, vcwebport:string, email:string, dyna_code:string, incl_tentative:bool):

    prepare_cache ([Queasy, Bediener, Res_history])

    i:int = 0
    str:string = ""
    oldstr:string = ""
    ct:string = ""
    oldct:string = ""
    progavail1:string = ""
    be_name:string = ""
    queasy = bediener = res_history = None

    t_list = nameqsy = bqueasy = None

    t_list_data, T_list = create_model("T_list", {"autostart":bool, "period":int, "delay":int, "hotelcode":string, "username":string, "password":string, "liveflag":bool, "defcurr":string, "pushrateflag":bool, "pullbookflag":bool, "pushavailflag":bool, "workpath":string, "progavail":string, "prog_avail_update":string, "dyna_code":string, "pushratebypax":bool, "uppercasename":bool, "delayrate":int, "delaypull":int, "delayavail":int, "pushall":bool, "re_calculate":bool, "restriction":bool, "allotment":bool, "pax":int, "bedsetup":bool, "pushbookflag":bool, "delaypushbook":int, "vcwsagent":string, "vcwsagent2":string, "vcwsagent3":string, "vcwsagent4":string, "vcwebhost":string, "vcwebport":string, "email":string, "vcwsagent5":string, "incl_tentative":bool})
    t_push_list_data, T_push_list = create_model("T_push_list", {"rcodevhp":string, "rcodebe":string, "rmtypevhp":string, "rmtypebe":string, "argtvhp":string, "flag":int})
    
    Nameqsy = create_buffer("Nameqsy",Queasy)
    Bqueasy = create_buffer("Bqueasy",Queasy)


    db_session = local_storage.db_session

    # Rd, strip
    dyna_code = dyna_code.strip()
    email = email.strip()
    hotelcode = hotelcode.strip()
    username = username.strip()
    password = password.strip()
    vcwebhost = vcwebhost.strip()
    vcwebport = vcwebport.strip()
    vcwsagent = vcwsagent.strip()
    vcwsagent2 = vcwsagent2.strip()
    vcwsagent3 = vcwsagent3.strip()
    vcwsagent4 = vcwsagent4.strip()
    vcwsagent5 = vcwsagent5.strip()
    workpath = workpath.strip()


    def generate_output():
        nonlocal i, str, oldstr, ct, oldct, progavail1, be_name, queasy, bediener, res_history
        nonlocal bookengid, autostart, period, delay, hotelcode, username, password, liveflag, defcurr, pushrateflag, pullbookflag, pushavailflag, workpath, progavail, user_init, pushratebypax, uppercasename, delayrate, delaypull, delayavail, pushall, re_calculate, restriction, allotment, pax, bedsetup, pushbookflag, delaypushbook, vcwsagent, vcwsagent2, vcwsagent3, vcwsagent4, vcwsagent5, vcwebhost, vcwebport, email, dyna_code, incl_tentative
        nonlocal nameqsy, bqueasy
        nonlocal t_list, nameqsy, bqueasy
        nonlocal t_list_data
        print("Configuration Saved Successfully")
        return {}

    def assign_tlist_values():

        nonlocal i, str, oldstr, ct, oldct, progavail1, be_name, queasy, bediener, res_history
        nonlocal bookengid, autostart, period, delay, hotelcode, username, password, liveflag, defcurr, pushrateflag, pullbookflag, pushavailflag, workpath, progavail, user_init, pushratebypax, uppercasename, delayrate, delaypull, delayavail, pushall, re_calculate, restriction, allotment, pax, bedsetup, pushbookflag, delaypushbook, vcwsagent, vcwsagent2, vcwsagent3, vcwsagent4, vcwsagent5, vcwebhost, vcwebport, email, dyna_code, incl_tentative
        nonlocal nameqsy, bqueasy


        nonlocal t_list, nameqsy, bqueasy
        nonlocal t_list_data

        if num_entries(t_list.progavail, "=") > 1:
            t_list.prog_avail_update = entry(0, t_list.progavail, "=")
            t_list.dyna_code = entry(1, t_list.progavail, "=")

            if num_entries(t_list.progavail, "=") >= 3:
                t_list.pushratebypax = logical(entry(2, t_list.progavail, "="))
            else:
                t_list.pushratebypax = False

            if num_entries(t_list.progavail, "=") >= 4:
                t_list.uppercasename = logical(entry(3, t_list.progavail, "="))
            else:
                t_list.uppercasename = False

            if num_entries(t_list.progavail, "=") >= 5:
                t_list.delayrate = to_int(entry(4, t_list.progavail, "="))
                t_list.delaypull = to_int(entry(5, t_list.progavail, "="))
                t_list.delayavail = to_int(entry(6, t_list.progavail, "="))


            else:
                t_list.delayrate = 300
                t_list.delaypull = 60
                t_list.delayavail = 60

            if num_entries(t_list.progavail, "=") >= 8:
                t_list.pushall = logical(entry(7, t_list.progavail, "="))
                t_list.re_calculate = logical(entry(8, t_list.progavail, "="))


            else:
                t_list.pushall = False
                t_list.re_calculate = False

            if num_entries(t_list.progavail, "=") >= 10:
                t_list.restriction = logical(entry(9, t_list.progavail, "="))
                t_list.allotment = logical(entry(10, t_list.progavail, "="))
                t_list.pax = to_int(entry(11, t_list.progavail, "="))
                t_list.bedsetup = logical(entry(12, t_list.progavail, "="))

            if num_entries(t_list.progavail, "=") >= 14:
                t_list.pushbookflag = logical(entry(13, t_list.progavail, "="))
                t_list.delaypushbook = to_int(entry(14, t_list.progavail, "="))

            if num_entries(t_list.progavail, "=") >= 16:
                t_list.vcwsagent = entry(15, t_list.progavail, "=")
                t_list.vcwsagent2 = entry(16, t_list.progavail, "=")
                t_list.vcwsagent3 = entry(17, t_list.progavail, "=")
                t_list.vcwsagent4 = entry(18, t_list.progavail, "=")
                t_list.vcwebhost = entry(19, t_list.progavail, "=")
                t_list.vcwebport = entry(20, t_list.progavail, "=")

            if num_entries(t_list.progavail, "=") >= 22:
                t_list.email = entry(21, t_list.progavail, "=")

            if num_entries(t_list.progavail, "=") >= 23:
                t_list.vcwsagent5 = entry(22, t_list.progavail, "=")

            if num_entries(t_list.progavail, "=") >= 24:
                t_list.incl_tentative = logical(entry(23, t_list.progavail, "="))

    def create_logdetails():

        nonlocal i, str, oldstr, ct, oldct, progavail1, be_name, queasy, bediener, res_history
        nonlocal bookengid, autostart, period, delay, hotelcode, username, password, liveflag, defcurr, pushrateflag, pullbookflag, pushavailflag, workpath, progavail, user_init, pushratebypax, uppercasename, delayrate, delaypull, delayavail, pushall, re_calculate, restriction, allotment, pax, bedsetup, pushbookflag, delaypushbook, vcwsagent, vcwsagent2, vcwsagent3, vcwsagent4, vcwsagent5, vcwebhost, vcwebport, email, dyna_code, incl_tentative
        nonlocal nameqsy, bqueasy


        nonlocal t_list, nameqsy, bqueasy
        nonlocal t_list_data

        logmessage:string = ""
        logmessage = ""

        t_list = query(t_list_data, first=True)

        if t_list:

            if t_list.autostart != autostart:
                logmessage = logmessage + "autostart=" + to_string(t_list.autostart) + ">>" + to_string(autostart) + " "

            if t_list.period != period:
                logmessage = logmessage + "period=" + to_string(t_list.period) + ">>" + to_string(period) + " "

            if t_list.delay != delay:
                logmessage = logmessage + "delay=" + to_string(t_list.delay) + ">>" + to_string(delay) + " "

            if t_list.liveflag != liveflag:
                logmessage = logmessage + "liveflag=" + to_string(t_list.liveflag) + ">>" + to_string(liveflag) + " "

            if t_list.defcurr  != (defcurr) :
                logmessage = logmessage + "defcurr=" + t_list.defcurr + ">>" + defcurr + " "

            if t_list.workpath  != (workpath) :
                logmessage = logmessage + "workpath=" + t_list.workpath + ">>" + workpath + " "

            if t_list.hotelcode  != (hotelcode) :
                logmessage = logmessage + "htlcode=" + t_list.hotelcode + ">>" + hotelcode + " "

            if t_list.username  != (username) :
                logmessage = logmessage + "usrname=" + t_list.username + ">>" + username + " "

            if t_list.password  != (password) :
                logmessage = logmessage + "pswd=" + t_list.password + ">>" + password + " "

            if t_list.pushrateflag != pushrateflag:
                logmessage = logmessage + "pushrate=" + to_string(t_list.pushrateflag) + ">>" + to_string(pushrateflag) + " "

            if t_list.pullbookflag != pullbookflag:
                logmessage = logmessage + "pullbook=" + to_string(t_list.pullbookflag) + ">>" + to_string(pullbookflag) + " "

            if t_list.pushavailflag != pushavailflag:
                logmessage = logmessage + "pushavail=" + to_string(t_list.pushavailflag) + ">>" + to_string(pushavailflag) + " "

            if t_list.prog_avail_update != entry(0, progavail1, "="):
                logmessage = logmessage + "progname=" + t_list.prog_avail_update + ">>" + entry(0, progavail1, "=") + " "

            if t_list.dyna_code != entry(1, progavail1, "="):
                logmessage = logmessage + "dynacode=" + t_list.dyna_code + ">>" + entry(1, progavail1, "=") + " "

            if to_string(t_list.pushratebypax) != entry(2, progavail1, "="):
                logmessage = logmessage + "bypax=" + to_string(t_list.pushratebypax) + ">>" + entry(2, progavail1, "=") + " "

            if to_string(t_list.uppercasename) != entry(3, progavail1, "="):
                logmessage = logmessage + "uppercase=" + to_string(t_list.uppercasename) + ">>" + entry(3, progavail1, "=") + " "

            if to_string(t_list.delayrate) != entry(4, progavail1, "="):
                logmessage = logmessage + "delayrate=" + to_string(t_list.delayrate) + ">>" + entry(4, progavail1, "=") + " "

            if to_string(t_list.delaypull) != entry(5, progavail1, "="):
                logmessage = logmessage + "delaypull=" + to_string(t_list.delaypull) + ">>" + entry(5, progavail1, "=") + " "

            if to_string(t_list.delayavail) != entry(6, progavail1, "="):
                logmessage = logmessage + "delayavail=" + to_string(t_list.delayavail) + ">>" + entry(6, progavail1, "=") + " "

            if to_string(t_list.pushall) != entry(7, progavail1, "="):
                logmessage = logmessage + "pushall=" + to_string(t_list.pushall) + ">>" + entry(7, progavail1, "=") + " "

            if to_string(t_list.re_calculate) != entry(8, progavail1, "="):
                logmessage = logmessage + "recalc=" + to_string(t_list.re_calculate) + ">>" + entry(8, progavail1, "=") + " "

            if to_string(t_list.restriction) != entry(9, progavail1, "="):
                logmessage = logmessage + "restrict=" + to_string(t_list.restriction) + ">>" + entry(9, progavail1, "=") + " "

            if to_string(t_list.allotment) != entry(10, progavail1, "="):
                logmessage = logmessage + "allot=" + to_string(t_list.allotment) + ">>" + entry(10, progavail1, "=") + " "

            if to_string(t_list.pax) != entry(11, progavail1, "="):
                logmessage = logmessage + "pax=" + to_string(t_list.pax) + ">>" + entry(11, progavail1, "=") + " "

            if to_string(t_list.bedsetup) != entry(12, progavail1, "="):
                logmessage = logmessage + "bed=" + to_string(t_list.bedsetup) + ">>" + entry(12, progavail1, "=") + " "

            if to_string(t_list.pushbookflag) != entry(13, progavail1, "="):
                logmessage = logmessage + "pushbook=" + to_string(t_list.pushbookflag) + ">>" + entry(13, progavail1, "=") + " "

            if to_string(t_list.delaypushbook) != entry(14, progavail1, "="):
                logmessage = logmessage + "delaypushbook=" + to_string(t_list.delaypushbook) + ">>" + entry(14, progavail1, "=") + " "

            if t_list.vcwsagent != entry(15, progavail1, "="):
                logmessage = logmessage + "pullbookurl=" + t_list.vcwsagent + ">>" + entry(15, progavail1, "=") + " "

            if t_list.vcwsagent2 != entry(16, progavail1, "="):
                logmessage = logmessage + "pushavailurl=" + t_list.vcwsagent2 + ">>" + entry(16, progavail1, "=") + " "

            if t_list.vcwsagent3 != entry(17, progavail1, "="):
                logmessage = logmessage + "pushrateurl=" + t_list.vcwsagent3 + ">>" + entry(17, progavail1, "=") + " "

            if t_list.vcwsagent4 != entry(18, progavail1, "="):
                logmessage = logmessage + "notifurl=" + t_list.vcwsagent4 + ">>" + entry(18, progavail1, "=") + " "

            if t_list.vcwebhost != entry(19, progavail1, "="):
                logmessage = logmessage + "host=" + t_list.vcwebhost + ">>" + entry(19, progavail1, "=") + " "

            if t_list.vcwebport != entry(20, progavail1, "="):
                logmessage = logmessage + "port=" + t_list.vcwebport + ">>" + entry(20, progavail1, "=") + " "

            if t_list.email != entry(21, progavail1, "="):
                logmessage = logmessage + "email=" + t_list.email + ">>" + entry(21, progavail1, "=") + " "

            if t_list.vcwsagent5 != entry(22, progavail1, "="):
                logmessage = logmessage + "pushbookurl=" + t_list.vcwsagent5 + ">>" + entry(22, progavail1, "=") + " "

            if to_string(t_list.incl_tentative) != entry(23, progavail1, "="):
                pass

        if logmessage != "":

            bediener = get_cache (Bediener, {"userinit": [(eq, user_init)]})

            if bediener:
                res_history = Res_history()
                db_session.add(res_history)

                res_history.nr = bediener.nr
                res_history.datum = get_current_date()
                res_history.zeit = get_current_time_in_seconds()
                res_history.action = "Booking Engine Interface"


                res_history.aenderung = chr_unicode(40) + be_name + chr_unicode(41) + " " + logmessage
                pass

    progavail1 =    progavail + "=" +\
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
                    vcwsagent5 + "=" +\
                    to_string(incl_tentative)
    

    ct = "$autostart$" + to_string(autostart) + ";" + "$period$" + to_string(period) + ";" + "$delay$" + \
                        to_string(delay) + ";" + "$liveflag$" + to_string(liveflag) + ";" + "$defcurr$" + \
                        to_string(defcurr) + ";" + "$workpath$" + to_string(workpath) + ";" + "$progname$" + \
                        to_string(progavail1) + ";" + "$htlcode$" + to_string(hotelcode) + ";" + "$username$" + \
                        to_string(username) + ";" + "$password$" + to_string(password) + ";" + "$pushrate$" + \
                        to_string(pushrateflag) + ";" + "$pullbook$" + to_string(pullbookflag) + ";" + "$pushavail$" + \
                        to_string(pushavailflag)
    
    nameqsy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, bookengid)]})

    if nameqsy:
        be_name = nameqsy.char1 + "|Config"
    t_list_data.clear()

    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, bookengid)]})

    if queasy:
        t_list = T_list()
        t_list_data.append(t_list)

        for i in range(1,num_entries(queasy.char1, ";")  + 1) :
            str = entry(i - 1, queasy.char1, ";")

            if substring(str, 0, 11) == ("$autostart$") :
                t_list.autostart = logical(substring(str, 11))

            elif substring(str, 0, 8) == ("$period$") :
                t_list.period = to_int(substring(str, 8))

            elif substring(str, 0, 7) == ("$delay$") :
                t_list.delay = to_int(substring(str, 7))

            elif substring(str, 0, 10) == ("$liveflag$") :
                t_list.liveflag = logical(substring(str, 10))

            elif substring(str, 0, 9) == ("$defcurr$") :
                t_list.defcurr = substring(str, 9)

            elif substring(str, 0, 10) == ("$workpath$") :
                t_list.workpath = substring(str, 10)

            elif substring(str, 0, 10) == ("$progname$") :
                t_list.progavail = substring(str, 10)

            elif substring(str, 0, 9) == ("$htlcode$") :
                t_list.hotelcode = substring(str, 9)

            elif substring(str, 0, 10) == ("$username$") :
                t_list.username = substring(str, 10)

            elif substring(str, 0, 10) == ("$password$") :
                t_list.password = substring(str, 10)

            elif substring(str, 0, 10) == ("$pushrate$") :
                t_list.pushrateflag = logical(substring(str, 10))

            elif substring(str, 0, 10) == ("$pullbook$") :
                t_list.pullbookflag = logical(substring(str, 10))

            elif substring(str, 0, 11) == ("$pushavail$") :
                t_list.pushavailflag = logical(substring(str, 11))
        assign_tlist_values()

        if queasy.char1  != (ct) :
            create_logdetails()

            bqueasy = get_cache (Queasy, {"key": [(eq, 167)],"number1": [(eq, bookengid)]})

            if bqueasy:
                pass
                bqueasy.date1 = get_current_date()
                bqueasy.logi1 = True
                pass
                pass
            else:
                bqueasy = Queasy()
                db_session.add(bqueasy)

                bqueasy.key = 167
                bqueasy.date1 = get_current_date()
                bqueasy.number1 = bookengid
                bqueasy.logi1 = True


        pass
        queasy.char1 = ct
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
            res_history.action = "Booking Engine Interface"


            res_history.aenderung = chr_unicode(40) + be_name + chr_unicode(41) + " New Config Has Been Created"
            pass

    # debug t_list_data
    # for t in query(t_list_data):
    #     print(f"--> T_list record: autostart={t.autostart}, period={t.period}, delay={t.delay}, hotelcode={t.hotelcode}, username={t.username}, pushrateflag={t.pushrateflag}, pushavailflag={t.pushavailflag}, progavail={t.progavail}")   

    
    #-----------------------------------------------
    # Rd, 12/11/2025: insert to TPushList
    # tambahan CM, queasy:161
    # temp-table di add queasy 161
    gastnrbe:int = 0
    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, bookengid)]})

    if queasy:
        gastnrbe = queasy.number2
        queasy_obj_list = {}

    for queasy, guest_pr in db_session.query(Queasy, Guest_pr) \
            .join(Guest_pr,(Guest_pr.gastnr == gastnrbe) & 
                  (Guest_pr.code == entry(0, Queasy.char1, ";")))\
            .filter(
                    (Queasy.key == 161) & 
                    (Queasy.number1 == bookengid)
                    ).order_by(Queasy._recid).all():
        
        if queasy_obj_list.get(queasy._recid):
            continue
        else:
            queasy_obj_list[queasy._recid] = True

        if entry(1, queasy.char1, ";") =="":
            continue
        if entry(3, queasy.char1, ";") =="":
            continue
        
        t_push_list = T_push_list()
        t_push_list_data.append(t_push_list)

        t_push_list.rcodevhp = entry(0, queasy.char1, ";")
        t_push_list.rcodebe = entry(1, queasy.char1, ";")
        t_push_list.rmtypevhp = entry(2, queasy.char1, ";")
        t_push_list.rmtypebe = entry(3, queasy.char1, ";")
        t_push_list.argtvhp = entry(4, queasy.char1, ";")

    db_session.commit()
    return generate_output()