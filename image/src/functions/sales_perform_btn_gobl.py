from functions.additional_functions import *
import decimal
from sqlalchemy import func
from datetime import date
from models import Bediener, Salesbud, Salestat, Genstat, Guest

def sales_perform_btn_gobl(from_date:str, to_date:str, usr_init:str):
    its_ok = False
    slist_list = []
    m1:int = 0
    m2:int = 0
    y1:int = 0
    y2:int = 0
    yy:int = 0
    monat:int = 0
    jahr:int = 0
    bediener = salesbud = salestat = genstat = guest = None

    slist = stat_buff = bud_buff = bgenstat = None

    slist_list, Slist = create_model("Slist", {"yr":int, "mnth":int, "lodg":decimal, "lbudget":decimal, "lproz":decimal, "fbrev":decimal, "fbbudget":decimal, "fbproz":decimal, "otrev":decimal, "otbudget":decimal, "otproz":decimal, "rmnight":int, "rbudget":int, "rmproz":decimal, "ytd_lodg":decimal, "ytd_lbudget":decimal, "ytd_lproz":decimal, "ytd_fbrev":decimal, "ytd_fbbudget":decimal, "ytd_fbproz":decimal, "ytd_rmnight":int, "ytd_rbudget":int, "ytd_rmproz":decimal, "ytd_otrev":decimal, "ytd_otbudget":decimal, "ytd_otproz":decimal})

    Stat_buff = Salestat
    Bud_buff = Salesbud
    Bgenstat = Genstat

    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, slist_list, m1, m2, y1, y2, yy, monat, jahr, bediener, salesbud, salestat, genstat, guest
        nonlocal stat_buff, bud_buff, bgenstat


        nonlocal slist, stat_buff, bud_buff, bgenstat
        nonlocal slist_list
        return {"its_ok": its_ok, "slist": slist_list}

    def check_budget():

        nonlocal its_ok, slist_list, m1, m2, y1, y2, yy, monat, jahr, bediener, salesbud, salestat, genstat, guest
        nonlocal stat_buff, bud_buff, bgenstat


        nonlocal slist, stat_buff, bud_buff, bgenstat
        nonlocal slist_list

        m1:int = 0
        m2:int = 0
        y1:int = 0
        y2:int = 0
        yy:int = 0
        monat:int = 0
        jahr:int = 0
        m1 = to_int(substring(from_date, 0, 2))
        y1 = to_int(substring(from_date, 2, 4))
        y2 = to_int(substring(to_date, 2, 4))
        m2 = to_int(substring(to_date, 0, 2)) + y2 - y1
        jahr = y1
        for monat in range(m1,m2 + 1) :

            if monat > 12:
                monat = 1
                jahr = jahr + 1

            salesbud = db_session.query(Salesbud).filter(
                    (Salesbud.bediener_nr == bediener.nr) &  (Salesbud.monat == monat) &  (Salesbud.jahr == jahr)).first()

            if not salesbud:
                salesbud = Salesbud()
                db_session.add(salesbud)

                salesbud.bediener_nr = bediener.nr
                salesbud.monat = monat
                salesbud.jahr = jahr

                salesbud = db_session.query(Salesbud).first()

                return

            salestat = db_session.query(Salestat).filter(
                    (Salestat.bediener_nr == bediener.nr) &  (Salestat.monat == monat) &  (Salestat.jahr == jahr)).first()

            if not salestat:
                salestat = Salestat()
                db_session.add(salestat)

                salestat.bediener_nr = bediener.nr
                salestat.monat = monat
                salestat.jahr = jahr

                salesbud = db_session.query(Salesbud).first()

                return

    def create_list():

        nonlocal its_ok, slist_list, m1, m2, y1, y2, yy, monat, jahr, bediener, salesbud, salestat, genstat, guest
        nonlocal stat_buff, bud_buff, bgenstat


        nonlocal slist, stat_buff, bud_buff, bgenstat
        nonlocal slist_list

        mm_room:int = 0
        c_room:int = 0
        do_it:bool = False
        fdate:date = None
        mm:int = 0
        yy:int = 0
        loopi:date = None
        frdate:date = None
        tdate:date = None
        mdate:int = 0
        ytd_lodging:decimal = 0
        ytd_rmnight:decimal = 0
        mtd_lodging:decimal = 0
        mtd_rmnight:decimal = 0
        Stat_buff = Salestat
        Bud_buff = Salesbud
        Bgenstat = Genstat
        slist_list.clear()

        if to_int(substring(to_date, 0, 2)) == 1 or to_int(substring(to_date, 0, 2)) == 3 or to_int(substring(to_date, 0, 2)) == 5 or to_int(substring(to_date, 0, 2)) == 7 or to_int(substring(to_date, 0, 2)) == 8 or to_int(substring(to_date, 0, 2)) == 10 or to_int(substring(to_date, 0, 2)) == 12:
            mdate = 31

        elif to_int(substring(to_date, 0, 2)) == 4 or to_int(substring(to_date, 0, 2)) == 6 or to_int(substring(to_date, 0, 2)) == 9 or to_int(substring(to_date, 0, 2)) == 11:
            mdate = 30


        else:

            if (to_int(substring(to_date, 0, 2)) % 4) == 0:
                mdate = 29


            else:
                mdate = 28


        frdate = date_mdy(to_int(substring(from_date, 0, 2)) , 1, to_int(substring(from_date, 2, 4)))
        tdate = date_mdy(to_int(substring(to_date, 0, 2)) , mdate, to_int(substring(to_date, 2, 4)))


        for loopi in range(frdate,tdate + 1) :

            slist = query(slist_list, filters=(lambda slist :slist.mnth == get_month(loopi) and slist.yr == get_year(loopi)), first=True)

            if not slist:
                slist = Slist()
                slist_list.append(slist)

                slist.yr = get_year(loopi)
                slist.mnth = get_month(loopi)


        fdate = date_mdy(1, 1, to_int(substring(from_date, 2, 4)))

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                (Genstat.datum >= fdate) &  (Genstat.datum <= tdate) &  (Genstat.zinr != "") &  (Genstat.res_logic[1])).all():
            if genstat._recid in genstat_obj_list:
                continue
            else:
                genstat_obj_list.append(genstat._recid)


            do_it = True

            if genstat.zipreis == 0:

                if (genstat.gratis > 0):
                    do_it = False

                if (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13:
                    do_it = False

            if do_it and usr_init != None:

                if guest.phonetik3 == trim(usr_init):
                    ytd_lodging = ytd_lodging + genstat.logis
                    ytd_rmnight = ytd_rmnight + 1

                    slist = query(slist_list, filters=(lambda slist :slist.mnth == get_month(genstat.datum) and slist.yr == get_year(genstat.datum)), first=True)

                    if slist:

                        if genstat.resstatus != 13:
                            mtd_lodging = mtd_lodging + genstat.logis
                            mtd_rmnight = mtd_rmnight + 1
                            slist.lodg = mtd_lodging
                            slist.rmnight = mtd_rmnight
                            slist.ytd_lodg = ytd_lodging
                            slist.ytd_rmnight = ytd_rmnight

        salestat_obj_list = []
        for salestat, salesbud in db_session.query(Salestat, Salesbud).join(Salesbud,(Salesbud.bediener_nr == Salestat.bediener_nr) &  (Salesbud.monat == Salestat.monat) &  (Salesbud.jahr == Salestat.jahr)).filter(
                (Salestat.bediener_nr == bediener.nr) &  (((Salestat.jahr > to_int(substring(from_date, 2, 4))) &  (Salestat.monat >= 1)) |  ((Salestat.jahr == to_int(substring(from_date, 2, 4))) &  (Salestat.monat >= to_int(substring(from_date, 0, 2))))) &  (((Salestat.jahr < to_int(substring(to_date, 2, 4))) &  (Salestat.monat >= 1)) |  ((Salestat.jahr == to_int(substring(to_date, 2, 4))) &  (Salestat.monat <= to_int(substring(to_date, 0, 2)))))).all():
            if salestat._recid in salestat_obj_list:
                continue
            else:
                salestat_obj_list.append(salestat._recid)

            slist = query(slist_list, filters=(lambda slist :(slist.mnth == salestat.monat) and slist.Yr == salestat.jahr), first=True)

            if slist:
                slist.lbudget = salesbud.argtumsatz
                slist.otrev = salestat.sonst_umsatz
                slist.otbudget = salesbud.sonst_umsatz
                slist.otproz = salestat.sonst_umsatz / salesbud.sonst_umsatz * 100
                slist.fbrev = salestat.f_b_umsatz
                slist.fbbudget = salesbud.f_b_umsatz
                slist.fbproz = salestat.f_b_umsatz / salesbud.f_b_umsatz * 100
                slist.rbudget = salesbud.room_nights

                stat_buff_obj_list = []
                for stat_buff, bud_buff in db_session.query(Stat_buff, Bud_buff).join(Bud_buff,(Bud_buff.bediener_nr == Stat_buff.bediener_nr) &  (Bud_buff.monat == Stat_buff.monat) &  (Bud_buff.jahr == Stat_buff.jahr)).filter(
                        (Stat_buff.bediener_nr == bediener.nr) &  (Stat_buff.jahr == salestat.jahr) &  (Stat_buff.monat <= salestat.monat)).all():
                    if stat_buff._recid in stat_buff_obj_list:
                        continue
                    else:
                        stat_buff_obj_list.append(stat_buff._recid)


                    slist.ytd_lbudget = slist.ytd_lbudget + bud_buff.argtumsatz
                    slist.ytd_otrev = slist.ytd_otrev + stat_buff.sonst_umsatz
                    slist.ytd_otbudget = slist.ytd_otbudget + bud_buff.sonst_umsatz
                    slist.ytd_fbrev = slist.ytd_fbrev + stat_buff.f_b_umsatz
                    slist.ytd_fbbudget = slist.ytd_fbbudget + bud_buff.f_b_umsatz
                    slist.ytd_rbudget = slist.ytd_rbudget + bud_buff.room_nights


                slist.ytd_fbproz = slist.ytd_fbrev / slist.ytd_fbbudget * 100
                slist.ytd_otproz = slist.ytd_otrev / slist.ytd_otbudget * 100

                if slist.otproz == None:
                    slist.otproz = 0.00

                if slist.fbproz == None:
                    slist.fbproz = 0.00

                if slist.ytd_fbproz == None:
                    slist.ytd_fbproz = 0.00

                if slist.ytd_otproz == None:
                    slist.ytd_otproz = 0.00

        for slist in query(slist_list):
            slist.lproz = slist.lodg / mtd_lodging * 100
            slist.rmproz = slist.rmnight / mtd_rmnight * 100
            slist.ytd_lproz = slist.ytd_lodg / slist.ytd_lbudget * 100
            slist.ytd_rmproz = slist.ytd_rmnight / slist.ytd_rbudget * 100

            if slist.lproz == None:
                slist.lproz = 0.00

            if slist.rmproz == None:
                slist.rmproz = 0.00

            if slist.ytd_lproz == None:
                slist.ytd_lproz = 0.00

            if slist.ytd_rmproz == None:
                slist.ytd_rmproz = 0.00


    m1 = to_int(substring(from_date, 0, 2))
    y1 = to_int(substring(from_date, 2, 4))
    y2 = to_int(substring(to_date, 2, 4))
    m2 = to_int(substring(to_date, 0, 2))

    bediener = db_session.query(Bediener).filter(
            (func.lower(Bediener.userinit) == (usr_init).lower())).first()
    check_budget()

    if its_ok:
        create_list()

    return generate_output()