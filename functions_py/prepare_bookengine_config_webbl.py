#using conversion tools version: 1.0.0.117
#-----------------------------------------
# Rd 31/7/2025
# gitlab: 726
# 
#-----------------------------------------
from functions.additional_functions import *
from decimal import Decimal
from models import Queasy, Waehrung

def prepare_bookengine_config_webbl(bookengid:int):

    prepare_cache ([Queasy, Waehrung])

    bookeng_name = ""
    t_list_data = []
    currency_list_data = []
    i:int = 0
    str:string = ""
    temp_str:string = ""
    queasy = waehrung = None

    currency_list = t_list = None

    currency_list_data, Currency_list = create_model("Currency_list", {"waehrungsnr":int, "bezeich":string, "wabkurz":string})
    t_list_data, T_list = create_model("T_list", {"autostart":bool, "period":int, "delay":int, "hotelcode":string, "username":string, "password":string, "liveflag":bool, "defcurr":string, "pushrateflag":bool, "pullbookflag":bool, "pushavailflag":bool, "workpath":string, "progavail":string, "progavail1":string, "pushratebypax":bool, "uppercasename":bool, "delayrate":int, "delaypull":int, "delayavail":int, "pushall":bool, "re_calculate":bool, "restriction":bool, "allotment":bool, "pax":int, "bedsetup":bool, "pushbookflag":bool, "delaypushbook":int, "vcwsagent":string, "vcwsagent1":string, "vcwsagent2":string, "vcwsagent3":string, "vcwsagent4":string, "vcwsagent5":string, "vcwebhost":string, "vcwebport":string, "email":string, "dyna_code":string, "incltentative":bool})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal bookeng_name, t_list_data, currency_list_data, i, str, temp_str, queasy, waehrung
        nonlocal bookengid


        nonlocal currency_list, t_list
        nonlocal currency_list_data, t_list_data

        return {"bookeng_name": bookeng_name, "t-list": t_list_data, "currency-list": currency_list_data}

    def fill_list():

        nonlocal bookeng_name, t_list_data, currency_list_data, i, str, temp_str, queasy, waehrung
        nonlocal bookengid


        nonlocal currency_list, t_list
        nonlocal currency_list_data, t_list_data

        if num_entries(temp_str, "=") > 1:
            t_list.progavail = entry(0, temp_str, "=")

            if num_entries(temp_str, "=") >= 3:
                t_list.pushratebypax = logical(entry(2, temp_str, "="))
            else:
                t_list.pushratebypax = False

            if num_entries(temp_str, "=") >= 4:
                t_list.uppercasename = logical(entry(3, temp_str, "="))
            else:
                t_list.uppercasename = False

            if num_entries(temp_str, "=") >= 5:
                t_list.delayrate = to_int(entry(4, temp_str, "="))
                t_list.delaypull = to_int(entry(5, temp_str, "="))
                t_list.delayavail = to_int(entry(6, temp_str, "="))


            else:
                t_list.delayrate = 300
                t_list.delaypull = 60
                t_list.delayavail = 60

            if num_entries(temp_str, "=") >= 8:
                t_list.pushall = logical(entry(7, temp_str, "="))
                t_list.re_calculate = logical(entry(8, temp_str, "="))


            else:
                t_list.pushall = False
                t_list.re_calculate = False

            if num_entries(temp_str, "=") >= 10:
                t_list.restriction = logical(entry(9, temp_str, "="))
                t_list.allotment = logical(entry(10, temp_str, "="))
                t_list.pax = to_int(entry(11, temp_str, "="))
                t_list.bedsetup = logical(entry(12, temp_str, "="))

            if num_entries(temp_str, "=") >= 14:
                t_list.pushbookflag = logical(entry(13, temp_str, "="))
                t_list.delaypushbook = to_int(entry(14, temp_str, "="))

            if num_entries(temp_str, "=") >= 16:
                t_list.vcwsagent = entry(15, temp_str, "=")
                t_list.vcwsagent2 = entry(16, temp_str, "=")
                t_list.vcwsagent3 = entry(17, temp_str, "=")
                t_list.vcwsagent4 = entry(18, temp_str, "=")
                t_list.vcwebhost = entry(19, temp_str, "=")
                t_list.vcwebport = entry(20, temp_str, "=")

            if num_entries(temp_str, "=") >= 22:
                t_list.email = entry(21, temp_str, "=")

            if num_entries(temp_str, "=") >= 23:
                t_list.vcwsagent5 = entry(22, temp_str, "=")

            if num_entries(temp_str, "=") >= 24:
                t_list.incltentative = logical(entry(23, temp_str, "="))
        else:
            t_list.progavail = temp_str
            t_list.dyna_code = ""
            t_list.pushratebypax = False
            t_list.uppercasename = False
            t_list.delayrate = 300
            t_list.delaypull = 60
            t_list.delayavail = 60
            t_list.pushall = True
            t_list.re_calculate = False
            t_list.delaypushbook = 60

    queasy = get_cache (Queasy, {"key": [(eq, 159)],"number1": [(eq, bookengid)]})

    if queasy:
        bookeng_name = queasy.char1
    else:
        return generate_output()

    queasy = get_cache (Queasy, {"key": [(eq, 160)],"number1": [(eq, bookengid)]})

    if queasy:
        t_list = T_list()
        t_list_data.append(t_list)

        for i in range(1,num_entries(queasy.char1, ";")  + 1) :
            str = entry(i - 1, queasy.char1, ";")

            if substring(str, 0, 11) == ("$autostart$").lower() :
                t_list.autostart = logical(substring(str, 11))

            elif substring(str, 0, 8) == ("$period$").lower() :
                t_list.period = to_int(substring(str, 8))

            elif substring(str, 0, 7) == ("$delay$").lower() :
                t_list.delay = to_int(substring(str, 7))

            elif substring(str, 0, 10) == ("$liveflag$").lower() :
                t_list.liveflag = logical(substring(str, 10))

            elif substring(str, 0, 9) == ("$defcurr$").lower() :
                t_list.defcurr = substring(str, 9)

            elif substring(str, 0, 10) == ("$workpath$").lower() :
                t_list.workpath = substring(str, 10)

            elif substring(str, 0, 10) == ("$progname$").lower() :
                temp_str = substring(str, 10)

            elif substring(str, 0, 9) == ("$htlcode$").lower() :
                t_list.hotelcode = substring(str, 9)

            elif substring(str, 0, 10) == ("$username$").lower() :
                t_list.username = substring(str, 10)

            elif substring(str, 0, 10) == ("$password$").lower() :
                t_list.password = substring(str, 10)

            elif substring(str, 0, 10) == ("$pushrate$").lower() :
                t_list.pushrateflag = logical(substring(str, 10))

            elif substring(str, 0, 10) == ("$pullbook$").lower() :
                t_list.pullbookflag = logical(substring(str, 10))

            elif substring(str, 0, 11) == ("$pushavail$").lower() :
                t_list.pushavailflag = logical(substring(str, 11))

    for waehrung in db_session.query(Waehrung).filter(
             (Waehrung.betriebsnr == 0)).order_by(Waehrung._recid).all():
        currency_list = Currency_list()
        currency_list_data.append(currency_list)

        currency_list.waehrungsnr = waehrung.waehrungsnr
        currency_list.bezeich = waehrung.bezeich
        currency_list.wabkurz = waehrung.wabkurz


    fill_list()

    return generate_output()