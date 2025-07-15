from functions.additional_functions import *
import decimal
from sqlalchemy import func
from datetime import date
from models import Bediener, Htparam, Salesbud, Salestat, Genstat, Guest

def sales_perform_btn_go_2bl(from_date:str, to_date:str, usr_init:str, disp_all:bool):
    its_ok = True
    slist_list = []
    m1:int = 0
    m2:int = 0
    y1:int = 0
    y2:int = 0
    yy:int = 0
    monat:int = 0
    jahr:int = 0
    usr_grp:int = 0
    bediener = htparam = salesbud = salestat = genstat = guest = None

    slist = tlist = None

    slist_list, Slist = create_model("Slist", {"yr":int, "mnth":int, "lodg":decimal, "lbudget":decimal, "lproz":decimal, "fbrev":decimal, "fbbudget":decimal, "fbproz":decimal, "otrev":decimal, "otbudget":decimal, "otproz":decimal, "rmnight":int, "rbudget":int, "rmproz":decimal, "ytd_lodg":decimal, "ytd_lbudget":decimal, "ytd_lproz":decimal, "ytd_fbrev":decimal, "ytd_fbbudget":decimal, "ytd_fbproz":decimal, "ytd_rmnight":int, "ytd_rbudget":int, "ytd_rmproz":decimal, "ytd_otrev":decimal, "ytd_otbudget":decimal, "ytd_otproz":decimal})
    tlist_list, Tlist = create_model_like(Slist, {"entry_count":int})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, slist_list, m1, m2, y1, y2, yy, monat, jahr, usr_grp, bediener, htparam, salesbud, salestat, genstat, guest
        nonlocal from_date, to_date, usr_init, disp_all


        nonlocal slist, tlist
        nonlocal slist_list, tlist_list
        return {"its_ok": its_ok, "slist": slist_list}

    def check_budget():

        nonlocal its_ok, slist_list, usr_grp, bediener, htparam, salesbud, salestat, genstat, guest
        nonlocal from_date, to_date, usr_init, disp_all


        nonlocal slist, tlist
        nonlocal slist_list, tlist_list

        m1:int = 0
        m2:int = 0
        y1:int = 0
        y2:int = 0
        yy:int = 0
        monat:int = 0
        jahr:int = 0
        y1 = to_int(substring(from_date, 2, 4))
        y2 = to_int(substring(to_date, 2, 4))
        m1 = to_int(substring(from_date, 0, 2))
        m2 = to_int(substring(to_date, 0, 2)) + (12 * (y2 - y1))
        jahr = y1
        for monat in range(m1,m2 + 1) :

            if monat > 12:
                monat = 1
                jahr = jahr + 1

            salesbud = db_session.query(Salesbud).filter(
                     (Salesbud.bediener_nr == bediener.nr) & (Salesbud.monat == monat) & (Salesbud.jahr == jahr)).first()

            if not salesbud:
                salesbud = Salesbud()
                db_session.add(salesbud)

                salesbud.bediener_nr = bediener.nr
                salesbud.monat = monat
                salesbud.jahr = jahr

                return

            salestat = db_session.query(Salestat).filter(
                     (Salestat.bediener_nr == bediener.nr) & (Salestat.monat == monat) & (Salestat.jahr == jahr)).first()

            if not salestat:
                salestat = Salestat()
                db_session.add(salestat)

                salestat.bediener_nr = bediener.nr
                salestat.monat = monat
                salestat.jahr = jahr

                return


    def create_list():

        nonlocal its_ok, slist_list, m1, m2, y1, y2, yy, monat, jahr, usr_grp, bediener, htparam, salesbud, salestat, genstat, guest
        nonlocal from_date, to_date, usr_init, disp_all


        nonlocal slist, tlist
        nonlocal slist_list, tlist_list

        do_it:bool = False
        fdate:date = None
        fdate_1styear:date = None
        tdate:date = None
        loopi:date = None
        ytd_lodging:decimal = to_decimal("0.0")
        ytd_rmnight:decimal = to_decimal("0.0")
        mtd_lodging:decimal = to_decimal("0.0")
        mtd_rmnight:decimal = to_decimal("0.0")
        stat_buff = None
        bud_buff = None
        bgenstat = None
        Stat_buff =  create_buffer("Stat_buff",Salestat)
        Bud_buff =  create_buffer("Bud_buff",Salesbud)
        Bgenstat =  create_buffer("Bgenstat",Genstat)
        slist_list.clear()
        htparam.fdate = date_mdy(to_int(substring(from_date, 0, 2)) , 1, to_int(substring(from_date, 2, 4)))

        if to_int(substring(to_date, 0, 2)) == 12:
            tdate = date_mdy(1, 1, to_int(substring(to_date, 2, 4)) + timedelta(days=1) - 1)
        else:
            tdate = date_mdy(to_int(substring(to_date, 0, 2)) + timedelta(days=1, 1, to_int(substring(to_date, 2, 4))) - 1)
        for loopi in date_range(fdate,tdate) :

            slist = query(slist_list, filters=(lambda slist: slist.mnth == get_month(loopi) and slist.yr == get_year(loopi)), first=True)

            if not slist:
                slist = Slist()
                slist_list.append(slist)

                slist.yr = get_year(loopi)
                slist.mnth = get_month(loopi)


        fdate_1styear = date_mdy(1, 1, to_int(substring(from_date, 2, 4)))

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (Genstat.datum >= fdate_1styear) & (Genstat.datum <= tdate) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1))]).order_by(Genstat.datum, Guest.name, Guest.gastnr).all():
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
                    ytd_lodging =  to_decimal(ytd_lodging) + to_decimal(genstat.logis)
                    ytd_rmnight =  to_decimal(ytd_rmnight) + to_decimal("1")

                    slist = query(slist_list, filters=(lambda slist: slist.mnth == get_month(genstat.datum) and slist.yr == get_year(genstat.datum)), first=True)

                    if slist:

                        if genstat.resstatus != 13:
                            slist.lodg =  to_decimal(slist.lodg) + to_decimal(genstat.logis)
                            slist.rmnight = slist.rmnight + 1
                            slist.ytd_lodg =  to_decimal(ytd_lodging)
                            slist.ytd_rmnight = ytd_rmnight

        salestat_obj_list = []
        for salestat, salesbud in db_session.query(Salestat, Salesbud).join(Salesbud,(Salesbud.bediener_nr == Salestat.bediener_nr) & (Salesbud.monat == Salestat.monat) & (Salesbud.jahr == Salestat.jahr)).filter(
                 (Salestat.bediener_nr == bediener.nr) & (((Salestat.jahr > to_int(substring(from_date, 2, 4))) & (Salestat.monat >= 1)) | ((Salestat.jahr == to_int(substring(from_date, 2, 4))) & (Salestat.monat >= to_int(substring(from_date, 0, 2))))) & (((Salestat.jahr < to_int(substring(to_date, 2, 4))) & (Salestat.monat >= 1)) | ((Salestat.jahr == to_int(substring(to_date, 2, 4))) & (Salestat.monat <= to_int(substring(to_date, 0, 2)))))).order_by(Salestat.jahr, Salestat.monat).all():
            if salestat._recid in salestat_obj_list:
                continue
            else:
                salestat_obj_list.append(salestat._recid)

            slist = query(slist_list, filters=(lambda slist:(slist.mnth == salestat.monat) and slist.Yr == salestat.jahr), first=True)

            if slist:
                slist.lbudget =  to_decimal(salesbud.argtumsatz)
                slist.otrev =  to_decimal(salestat.sonst_umsatz)
                slist.otbudget =  to_decimal(salesbud.sonst_umsatz)
                slist.otproz =  to_decimal(salestat.sonst_umsatz) / to_decimal(salesbud.sonst_umsatz) * to_decimal("100")
                slist.fbrev =  to_decimal(salestat.f_b_umsatz)
                slist.fbbudget =  to_decimal(salesbud.f_b_umsatz)
                slist.fbproz =  to_decimal(salestat.f_b_umsatz) / to_decimal(salesbud.f_b_umsatz) * to_decimal("100")
                slist.rbudget = salesbud.room_nights

                stat_buff_obj_list = []
                for stat_buff, bud_buff in db_session.query(Stat_buff, Bud_buff).join(Bud_buff,(Bud_buff.bediener_nr == Stat_buff.bediener_nr) & (Bud_buff.monat == Stat_buff.monat) & (Bud_buff.jahr == Stat_buff.jahr)).filter(
                         (Stat_buff.bediener_nr == bediener.nr) & (Stat_buff.jahr == salestat.jahr) & (Stat_buff.monat <= salestat.monat)).order_by(Stat_buff.jahr, Stat_buff.monat).all():
                    if stat_buff._recid in stat_buff_obj_list:
                        continue
                    else:
                        stat_buff_obj_list.append(stat_buff._recid)


                    slist.ytd_lbudget =  to_decimal(slist.ytd_lbudget) + to_decimal(bud_buff.argtumsatz)
                    slist.ytd_otrev =  to_decimal(slist.ytd_otrev) + to_decimal(stat_buff.sonst_umsatz)
                    slist.ytd_otbudget =  to_decimal(slist.ytd_otbudget) + to_decimal(bud_buff.sonst_umsatz)
                    slist.ytd_fbrev =  to_decimal(slist.ytd_fbrev) + to_decimal(stat_buff.f_b_umsatz)
                    slist.ytd_fbbudget =  to_decimal(slist.ytd_fbbudget) + to_decimal(bud_buff.f_b_umsatz)
                    slist.ytd_rbudget = slist.ytd_rbudget + bud_buff.room_nights


                slist.ytd_fbproz =  to_decimal(slist.ytd_fbrev) / to_decimal(slist.ytd_fbbudget) * to_decimal("100")
                slist.ytd_otproz =  to_decimal(slist.ytd_otrev) / to_decimal(slist.ytd_otbudget) * to_decimal("100")

                if slist.otproz == None:
                    slist.otproz =  to_decimal(0.00)

                if slist.fbproz == None:
                    slist.fbproz =  to_decimal(0.00)

                if slist.ytd_fbproz == None:
                    slist.ytd_fbproz =  to_decimal(0.00)

                if slist.ytd_otproz == None:
                    slist.ytd_otproz =  to_decimal(0.00)

        for slist in query(slist_list):
            slist.lproz =  to_decimal(slist.lodg) / to_decimal(mtd_lodging) * to_decimal("100")
            slist.rmproz =  to_decimal(slist.rmnight) / to_decimal(mtd_rmnight) * to_decimal("100")
            slist.ytd_lproz =  to_decimal(slist.ytd_lodg) / to_decimal(slist.ytd_lbudget) * to_decimal("100")
            slist.ytd_rmproz =  to_decimal(slist.ytd_rmnight) / to_decimal(slist.ytd_rbudget) * to_decimal("100")

            if slist.lproz == None:
                slist.lproz =  to_decimal(0.00)

            if slist.rmproz == None:
                slist.rmproz =  to_decimal(0.00)

            if slist.ytd_lproz == None:
                slist.ytd_lproz =  to_decimal(0.00)

            if slist.ytd_rmproz == None:
                slist.ytd_rmproz =  to_decimal(0.00)


    def create_list2():

        nonlocal its_ok, slist_list, m1, m2, y1, y2, yy, monat, jahr, usr_grp, bediener, htparam, salesbud, salestat, genstat, guest
        nonlocal from_date, to_date, usr_init, disp_all


        nonlocal slist, tlist
        nonlocal slist_list, tlist_list

        do_it:bool = False
        fdate:date = None
        fdate_1styear:date = None
        tdate:date = None
        loopi:date = None
        ytd_lodging:decimal = to_decimal("0.0")
        ytd_rmnight:decimal = to_decimal("0.0")
        mtd_lodging:decimal = to_decimal("0.0")
        mtd_rmnight:decimal = to_decimal("0.0")
        stat_buff = None
        bud_buff = None
        bgenstat = None
        Stat_buff =  create_buffer("Stat_buff",Salestat)
        Bud_buff =  create_buffer("Bud_buff",Salesbud)
        Bgenstat =  create_buffer("Bgenstat",Genstat)
        slist_list.clear()
        htparam.fdate = date_mdy(to_int(substring(from_date, 0, 2)) , 1, to_int(substring(from_date, 2, 4)))

        if to_int(substring(to_date, 0, 2)) == 12:
            tdate = date_mdy(1, 1, to_int(substring(to_date, 2, 4)) + timedelta(days=1) - 1)
        else:
            tdate = date_mdy(to_int(substring(to_date, 0, 2)) + timedelta(days=1, 1, to_int(substring(to_date, 2, 4))) - 1)
        for loopi in date_range(fdate,tdate) :

            slist = query(slist_list, filters=(lambda slist: slist.mnth == get_month(loopi) and slist.yr == get_year(loopi)), first=True)

            if not slist:
                slist = Slist()
                slist_list.append(slist)

                slist.yr = get_year(loopi)
                slist.mnth = get_month(loopi)


        fdate_1styear = date_mdy(1, 1, to_int(substring(from_date, 2, 4)))

        genstat_obj_list = []
        for genstat, guest in db_session.query(Genstat, Guest).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (Genstat.datum >= fdate_1styear) & (Genstat.datum <= tdate) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1))]).order_by(Genstat.datum, Guest.name, Guest.gastnr).all():
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

            if do_it and bediener.userinit != None:

                if guest.phonetik3 == trim(bediener.userinit):
                    ytd_lodging =  to_decimal(ytd_lodging) + to_decimal(genstat.logis)
                    ytd_rmnight =  to_decimal(ytd_rmnight) + to_decimal("1")

                    slist = query(slist_list, filters=(lambda slist: slist.mnth == get_month(genstat.datum) and slist.yr == get_year(genstat.datum)), first=True)

                    if slist:

                        if genstat.resstatus != 13:
                            slist.lodg =  to_decimal(slist.lodg) + to_decimal(genstat.logis)
                            slist.rmnight = slist.rmnight + 1
                            slist.ytd_lodg =  to_decimal(ytd_lodging)
                            slist.ytd_rmnight = ytd_rmnight

        salestat_obj_list = []
        for salestat, salesbud in db_session.query(Salestat, Salesbud).join(Salesbud,(Salesbud.bediener_nr == Salestat.bediener_nr) & (Salesbud.monat == Salestat.monat) & (Salesbud.jahr == Salestat.jahr)).filter(
                 (Salestat.bediener_nr == bediener.nr) & (((Salestat.jahr > to_int(substring(from_date, 2, 4))) & (Salestat.monat >= 1)) | ((Salestat.jahr == to_int(substring(from_date, 2, 4))) & (Salestat.monat >= to_int(substring(from_date, 0, 2))))) & (((Salestat.jahr < to_int(substring(to_date, 2, 4))) & (Salestat.monat >= 1)) | ((Salestat.jahr == to_int(substring(to_date, 2, 4))) & (Salestat.monat <= to_int(substring(to_date, 0, 2)))))).order_by(Salestat.jahr, Salestat.monat).all():
            if salestat._recid in salestat_obj_list:
                continue
            else:
                salestat_obj_list.append(salestat._recid)

            slist = query(slist_list, filters=(lambda slist:(slist.mnth == salestat.monat) and slist.Yr == salestat.jahr), first=True)

            if slist:
                slist.lbudget =  to_decimal(salesbud.argtumsatz)
                slist.otrev =  to_decimal(salestat.sonst_umsatz)
                slist.otbudget =  to_decimal(salesbud.sonst_umsatz)
                slist.otproz =  to_decimal(salestat.sonst_umsatz) / to_decimal(salesbud.sonst_umsatz) * to_decimal("100")
                slist.fbrev =  to_decimal(salestat.f_b_umsatz)
                slist.fbbudget =  to_decimal(salesbud.f_b_umsatz)
                slist.fbproz =  to_decimal(salestat.f_b_umsatz) / to_decimal(salesbud.f_b_umsatz) * to_decimal("100")
                slist.rbudget = salesbud.room_nights

                stat_buff_obj_list = []
                for stat_buff, bud_buff in db_session.query(Stat_buff, Bud_buff).join(Bud_buff,(Bud_buff.bediener_nr == Stat_buff.bediener_nr) & (Bud_buff.monat == Stat_buff.monat) & (Bud_buff.jahr == Stat_buff.jahr)).filter(
                         (Stat_buff.bediener_nr == bediener.nr) & (Stat_buff.jahr == salestat.jahr) & (Stat_buff.monat <= salestat.monat)).order_by(Stat_buff.jahr, Stat_buff.monat).all():
                    if stat_buff._recid in stat_buff_obj_list:
                        continue
                    else:
                        stat_buff_obj_list.append(stat_buff._recid)


                    slist.ytd_lbudget =  to_decimal(slist.ytd_lbudget) + to_decimal(bud_buff.argtumsatz)
                    slist.ytd_otrev =  to_decimal(slist.ytd_otrev) + to_decimal(stat_buff.sonst_umsatz)
                    slist.ytd_otbudget =  to_decimal(slist.ytd_otbudget) + to_decimal(bud_buff.sonst_umsatz)
                    slist.ytd_fbrev =  to_decimal(slist.ytd_fbrev) + to_decimal(stat_buff.f_b_umsatz)
                    slist.ytd_fbbudget =  to_decimal(slist.ytd_fbbudget) + to_decimal(bud_buff.f_b_umsatz)
                    slist.ytd_rbudget = slist.ytd_rbudget + bud_buff.room_nights


                slist.ytd_fbproz =  to_decimal(slist.ytd_fbrev) / to_decimal(slist.ytd_fbbudget) * to_decimal("100")
                slist.ytd_otproz =  to_decimal(slist.ytd_otrev) / to_decimal(slist.ytd_otbudget) * to_decimal("100")

                if slist.otproz == None:
                    slist.otproz =  to_decimal(0.00)

                if slist.fbproz == None:
                    slist.fbproz =  to_decimal(0.00)

                if slist.ytd_fbproz == None:
                    slist.ytd_fbproz =  to_decimal(0.00)

                if slist.ytd_otproz == None:
                    slist.ytd_otproz =  to_decimal(0.00)

        for slist in query(slist_list):
            slist.lproz =  to_decimal(slist.lodg) / to_decimal(mtd_lodging) * to_decimal("100")
            slist.rmproz =  to_decimal(slist.rmnight) / to_decimal(mtd_rmnight) * to_decimal("100")
            slist.ytd_lproz =  to_decimal(slist.ytd_lodg) / to_decimal(slist.ytd_lbudget) * to_decimal("100")
            slist.ytd_rmproz =  to_decimal(slist.ytd_rmnight) / to_decimal(slist.ytd_rbudget) * to_decimal("100")

            if slist.lproz == None:
                slist.lproz =  to_decimal(0.00)

            if slist.rmproz == None:
                slist.rmproz =  to_decimal(0.00)

            if slist.ytd_lproz == None:
                slist.ytd_lproz =  to_decimal(0.00)

            if slist.ytd_rmproz == None:
                slist.ytd_rmproz =  to_decimal(0.00)


    def add_total():

        nonlocal its_ok, slist_list, m1, m2, y1, y2, yy, monat, jahr, usr_grp, bediener, htparam, salesbud, salestat, genstat, guest
        nonlocal from_date, to_date, usr_init, disp_all


        nonlocal slist, tlist
        nonlocal slist_list, tlist_list

        for slist in query(slist_list):

            tlist = query(tlist_list, filters=(lambda tlist: tlist.yr == slist.yr and tlist.mnth == slist.mnth), first=True)
            tlist.entry_count = tlist.entry_count + 1
            tlist.lproz =  to_decimal(tlist.lproz) + to_decimal(slist.lproz)
            tlist.rmproz =  to_decimal(tlist.rmproz) + to_decimal(slist.rmproz)
            tlist.lbudget =  to_decimal(tlist.lbudget) + to_decimal(slist.lbudget)
            tlist.otrev =  to_decimal(tlist.otrev) + to_decimal(slist.otrev)
            tlist.otbudget =  to_decimal(tlist.otbudget) + to_decimal(slist.otbudge)
            tlist.fbrev =  to_decimal(tlist.fbrev) + to_decimal(slist.fbrev)
            tlist.fbbudget =  to_decimal(tlist.fbbudget) + to_decimal(slist.fbbudge)
            tlist.rbudget = tlist.rbudget + slist.rbudget
            tlist.lodg =  to_decimal(tlist.lodg) + to_decimal(slist.lodg)
            tlist.rmnight = tlist.rmnight + slist.rmnight
            tlist.ytd_lproz =  to_decimal(tlist.ytd_lproz) + to_decimal(slist.ytd_lproz)
            tlist.ytd_rmproz =  to_decimal(tlist.ytd_rmproz) + to_decimal(slist.ytd_rmproz)
            tlist.ytd_lbudget =  to_decimal(tlist.ytd_lbudget) + to_decimal(slist.ytd_lbudget)
            tlist.ytd_otrev =  to_decimal(tlist.ytd_otrev) + to_decimal(slist.ytd_otrev)
            tlist.ytd_otbudget =  to_decimal(tlist.ytd_otbudget) + to_decimal(slist.ytd_otbudget)
            tlist.ytd_fbrev =  to_decimal(tlist.ytd_fbrev) + to_decimal(slist.ytd_fbrev)
            tlist.ytd_fbbudget =  to_decimal(tlist.ytd_fbbudget) + to_decimal(slist.ytd_fbbudget)
            tlist.ytd_rbudget = tlist.ytd_rbudget + slist.ytd_rbudget
            tlist.ytd_rmnight = tlist.ytd_rmnight + slist.ytd_rmnight
            tlist.ytd_lodg =  to_decimal(tlist.ytd_lodg) + to_decimal(slist.ytd_lodg)


    def return_total():

        nonlocal its_ok, slist_list, m1, m2, y1, y2, yy, monat, jahr, usr_grp, bediener, htparam, salesbud, salestat, genstat, guest
        nonlocal from_date, to_date, usr_init, disp_all


        nonlocal slist, tlist
        nonlocal slist_list, tlist_list


        slist_list.clear()

        for tlist in query(tlist_list, sort_by=[("yr",False),("mnth",False)]):
            slist = Slist()
            slist_list.append(slist)

            slist.yr = tlist.yr
            slist.mnth = tlist.mnth
            slist.ytd_lbudget =  to_decimal(tlist.ytd_lbudget)
            slist.ytd_otrev =  to_decimal(tlist.ytd_otrev)
            slist.ytd_otbudget =  to_decimal(tlist.ytd_otbudget)
            slist.ytd_fbrev =  to_decimal(tlist.ytd_fbrev)
            slist.ytd_fbbudget =  to_decimal(tlist.ytd_fbbudget)
            slist.ytd_rbudget = tlist.ytd_rbudget
            slist.ytd_otproz =  to_decimal(tlist.ytd_otrev) / to_decimal(tlist.ytd_otbudget) * to_decimal("100")
            slist.ytd_fbproz =  to_decimal(tlist.ytd_fbrev) / to_decimal(tlist.ytd_fbbudget) * to_decimal("100")
            slist.lbudget =  to_decimal(tlist.lbudget)
            slist.otrev =  to_decimal(tlist.otrev)
            slist.otbudget =  to_decimal(tlist.otbudget)
            slist.fbrev =  to_decimal(tlist.fbrev)
            slist.fbbudget =  to_decimal(tlist.fbbudget)
            slist.rbudget = tlist.rbudget
            slist.otproz =  to_decimal(tlist.otrev) / to_decimal(tlist.otbudget) * to_decimal("100")
            slist.fbproz =  to_decimal(tlist.fbrev) / to_decimal(tlist.fbbudget) * to_decimal("100")
            slist.lodg =  to_decimal(tlist.lodg)
            slist.rmnight = tlist.rmnight
            slist.ytd_lodg =  to_decimal(tlist.ytd_lodg)
            slist.ytd_rmnight = tlist.ytd_rmnight
            slist.lproz =  to_decimal(tlist.lproz) / to_decimal(tlist.entry_count)
            slist.rmproz =  to_decimal(tlist.rmproz) / to_decimal(tlist.entry_count)
            slist.ytd_lproz =  to_decimal(tlist.ytd_lproz) / to_decimal(tlist.entry_count)
            slist.ytd_rmproz =  to_decimal(tlist.ytd_rmnight) / to_decimal(tlist.ytd_rbudget) * to_decimal("100")

            if slist.lproz == None:
                slist.lproz =  to_decimal(0.00)

            if slist.rmproz == None:
                slist.rmproz =  to_decimal(0.00)

            if slist.ytd_lproz == None:
                slist.ytd_lproz =  to_decimal(0.00)

            if slist.ytd_otproz == None:
                slist.ytd_otproz =  to_decimal(0.00)

            if slist.ytd_fbproz == None:
                slist.ytd_fbproz =  to_decimal(0.00)

            if slist.otproz == None:
                slist.otproz =  to_decimal(0.00)

            if slist.fbproz == None:
                slist.fbproz =  to_decimal(0.00)

            if slist.ytd_rmproz == None:
                slist.ytd_rmproz =  to_decimal(0.00)


    y1 = to_int(substring(from_date, 2, 4))
    y2 = to_int(substring(to_date, 2, 4))
    m1 = to_int(substring(from_date, 0, 2))
    m2 = to_int(substring(to_date, 0, 2))

    if disp_all == False:

        bediener = db_session.query(Bediener).filter(
                 (func.lower(Bediener.userinit) == (usr_init).lower())).first()
        check_budget()

        if its_ok:
            create_list()

    elif disp_all :

        htparam = db_session.query(Htparam).filter(
                 (Htparam.paramnr == 547)).first()
        usr_grp = htparam.finteger

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.user_group == usr_grp) & (Bediener.flag == 0)).order_by(Bediener._recid).all():
            check_budget()

            if its_ok:
                create_list2()

            if not tlist:

                for slist in query(slist_list):
                    tlist = Tlist()
                    tlist_list.append(tlist)

                    tlist.yr = slist.yr
                    tlist.mnth = slist.mnth

            add_total()
        return_total()

    return generate_output()