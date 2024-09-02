from functions.additional_functions import *
import decimal
from models import Queasy, Waehrung

def prepare_bookengine_config_webbl(bookengid:int):
    bookeng_name = ""
    t_list_list = []
    currency_list_list = []
    i:int = 0
    str:str = ""
    queasy = waehrung = None

    currency_list = t_list = None

    currency_list_list, Currency_list = create_model("Currency_list", {"waehrungsnr":int, "bezeich":str, "wabkurz":str})
    t_list_list, T_list = create_model("T_list", {"autostart":bool, "period":int, "delay":int, "hotelcode":str, "username":str, "password":str, "liveflag":bool, "defcurr":str, "pushrateflag":bool, "pullbookflag":bool, "pushavailflag":bool, "workpath":str, "progavail":str, "progavail1":str, "pushratebypax":bool, "uppercasename":bool, "delayrate":int, "delaypull":int, "delayavail":int, "pushall":bool, "re_calculate":bool, "restriction":bool, "allotment":bool, "pax":int, "bedsetup":bool, "pushbookflag":bool, "delaypushbook":int, "vcwsagent":str, "vcwsagent1":str, "vcwsagent2":str, "vcwsagent3":str, "vcwsagent4":str, "vcwsagent5":str, "vcwebhost":str, "vcwebport":str, "email":str, "dyna_code":str, "incltentative":bool})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal bookeng_name, t_list_list, currency_list_list, i, str, queasy, waehrung


        nonlocal currency_list, t_list
        nonlocal currency_list_list, t_list_list
        return {"bookeng_name": bookeng_name, "t-list": t_list_list, "currency-list": currency_list_list}

    def fill_list():

        nonlocal bookeng_name, t_list_list, currency_list_list, i, str, queasy, waehrung


        nonlocal currency_list, t_list
        nonlocal currency_list_list, t_list_list

        if num_entries(t_list.progavail1, " == ") > 1:
            t_list.progavail = entry(0, t_list.progavail1, " == ")

            if num_entries(t_list.progavail1, " == ") >= 3:
                t_list.pushratebypax = logical(entry(2, t_list.progavail1, " == "))
            else:
                t_list.pushratebypax = False

            if num_entries(t_list.progavail1, " == ") >= 4:
                t_list.upperCaseName = logical(entry(3, t_list.progavail1, " == "))
            else:
                t_list.upperCaseName = False

            if num_entries(t_list.progavail1, " == ") >= 5:
                t_list.delayRate = to_int(entry(4, t_list.progavail1, " == "))
                t_list.delayPull = to_int(entry(5, t_list.progavail1, " == "))
                t_list.delayAvail = to_int(entry(6, t_list.progavail1, " == "))


            else:
                t_list.delayRate = 300
                t_list.delayPull = 60
                t_list.delayAvail = 60

            if num_entries(t_list.progavail1, " == ") >= 8:
                t_list.pushAll = logical(entry(7, t_list.progavail1, " == "))
                t_list.re_calculate = logical(entry(8, t_list.progavail1, " == "))


            else:
                t_list.pushAll = False
                t_list.re_calculate = False

            if num_entries(t_list.progavail1, " == ") >= 10:
                t_list.restriction = logical(entry(9, t_list.progavail1, " == "))
                t_list.allotment = logical(entry(10, t_list.progavail1, " == "))
                t_list.pax = to_int(entry(11, t_list.progavail1, " == "))
                t_list.bedsetup = logical(entry(12, t_list.progavail1, " == "))

            if num_entries(t_list.progavail1, " == ") >= 14:
                t_list.pushbookflag = logical(entry(13, t_list.progavail1, " == "))
                t_list.delaypushbook = to_int(entry(14, t_list.progavail1, " == "))

            if num_entries(t_list.progavail1, " == ") >= 16:
                t_list.vcWSAgent = entry(15, t_list.progavail1, " == ")
                t_list.vcWSAgent2 = entry(16, t_list.progavail1, " == ")
                t_list.vcWSAgent3 = entry(17, t_list.progavail1, " == ")
                t_list.vcWSAgent4 = entry(18, t_list.progavail1, " == ")
                t_list.vcWebHost = entry(19, t_list.progavail1, " == ")
                t_list.vcWebPort = entry(20, t_list.progavail1, " == ")

            if num_entries(t_list.progavail1, " == ") >= 22:
                t_list.email = entry(21, t_list.progavail1, " == ")

            if num_entries(t_list.progavail1, " == ") >= 23:
                t_list.vcWSAgent5 = entry(22, t_list.progavail1, " == ")

            if num_entries(t_list.progavail1, " == ") >= 24:
                t_list.inclTentative = logical(entry(23, t_list.progavail1, " == "))
        else:
            t_list.progavail = t_list.progavail1
            t_list.dyna_code = ""
            t_list.pushratebypax = False
            t_list.upperCaseName = False
            t_list.delayRate = 300
            t_list.delayPull = 60
            t_list.delayAvail = 60
            t_list.pushAll = True
            t_list.re_calculate = False
            t_list.delaypushbook = 60


    queasy = db_session.query(Queasy).filter(
            (Queasy.KEY == 159) &  (Queasy.number1 == bookengid)).first()

    if queasy:
        bookeng_name = queasy.char1

    queasy = db_session.query(Queasy).filter(
            (Queasy.KEY == 160) &  (Queasy.number1 == bookengid)).first()

    if queasy:
        t_list = T_list()
        t_list_list.append(t_list)

        for i in range(1,num_entries(queasy.char1, ";")  + 1) :
            str = entry(i - 1, queasy.char1, ";")

            if substring(str, 0, 11) == "$autostart$":
                t_list.autostart = logical(substring(str, 11))

            elif substring(str, 0, 8) == "$period$":
                t_list.period = to_int(substring(str, 8))

            elif substring(str, 0, 7) == "$delay$":
                t_list.delay = to_int(substring(str, 7))

            elif substring(str, 0, 10) == "$liveflag$":
                t_list.liveflag = logical(substring(str, 10))

            elif substring(str, 0, 9) == "$defcurr$":
                t_list.defcurr = substring(str, 9)

            elif substring(str, 0, 10) == "$workpath$":
                t_list.workpath = substring(str, 10)

            elif substring(str, 0, 10) == "$progname$":
                t_list.progavail1 = substring(str, 10)

            elif substring(str, 0, 9) == "$htlcode$":
                t_list.hotelcode = substring(str, 9)

            elif substring(str, 0, 10) == "$username$":
                t_list.username = substring(str, 10)

            elif substring(str, 0, 10) == "$password$":
                t_list.password = substring(str, 10)

            elif substring(str, 0, 10) == "$pushrate$":
                t_list.pushrateflag = logical(substring(str, 10))

            elif substring(str, 0, 10) == "$pullbook$":
                t_list.pullbookflag = logical(substring(str, 10))

            elif substring(str, 0, 11) == "$pushavail$":
                t_list.pushavailflag = logical(substring(str, 11))

    for waehrung in db_session.query(Waehrung).filter(
            (Waehrung.betriebsnr == 0)).all():
        currency_list = Currency_list()
        currency_list_list.append(currency_list)

        currency_list.waehrungsnr = waehrungsnr
        currency_list.bezeich = waehrung.bezeich
        currency_list.wabkurz = waehrung.wabkurz


    fill_list()

    return generate_output()