#using conversion tools version: 1.0.0.117
#------------------------------------------------
# Rd 18/7/25
# Rulita, 26/08/25
# Issue Fixing variable fdate change to tmp_fdate
# Issue Fixing variable tdate change to tmp_tdate
#------------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Htparam, Bediener, Salesbud, Salestat, Genstat, Guest, H_bill, H_artikel, Artikel, H_bill_line
def safe_divide(numerator, denominator):
    numerator, denominator = to_decimal(numerator), to_decimal(denominator)
    return (numerator / denominator * to_decimal("100")) if denominator != 0 else to_decimal("0")

def sales_perform_btn_go_webbl(from_date:string, to_date:string, usr_init:string, show_breakdown:bool):

    prepare_cache ([Htparam, Bediener, Salesbud, Salestat, Genstat, Guest, Artikel, H_bill_line])

    its_ok = True
    slist_data = []
    m1:int = 0
    m2:int = 0
    y1:int = 0
    y2:int = 0
    yy:int = 0
    monat:int = 0
    jahr:int = 0
    usr_grp:int = 0
    user_total_lodg:Decimal = to_decimal("0.0")
    user_total_lbudget:Decimal = to_decimal("0.0")
    user_total_lproz:Decimal = to_decimal("0.0")
    user_total_fbrev:Decimal = to_decimal("0.0")
    user_total_fbbudget:Decimal = to_decimal("0.0")
    user_total_fbproz:Decimal = to_decimal("0.0")
    user_total_otrev:Decimal = to_decimal("0.0")
    user_total_otbudget:Decimal = to_decimal("0.0")
    user_total_otproz:Decimal = to_decimal("0.0")
    user_total_rmnight:Decimal = to_decimal("0.0")
    user_total_rbudget:Decimal = to_decimal("0.0")
    user_total_rmproz:Decimal = to_decimal("0.0")
    htparam = bediener = salesbud = salestat = genstat = guest = h_bill = h_artikel = artikel = h_bill_line = None

    slist = sbuff = buff_slist = None

    slist_data, Slist = create_model("Slist", {"bezeich":string, "yr":int, "mnth":int, "userinit":string, "lodg":Decimal, "lbudget":Decimal, "lproz":Decimal, "fbrev":Decimal, "fbbudget":Decimal, "fbproz":Decimal, "otrev":Decimal, "otbudget":Decimal, "otproz":Decimal, "rmnight":int, "rbudget":int, "rmproz":Decimal, "ytd_lodg":Decimal, "ytd_lbudget":Decimal, "ytd_lproz":Decimal, "ytd_fbrev":Decimal, "ytd_fbbudget":Decimal, "ytd_fbproz":Decimal, "ytd_rmnight":int, "ytd_rbudget":int, "ytd_rmproz":Decimal, "ytd_otrev":Decimal, "ytd_otbudget":Decimal, "ytd_otproz":Decimal, "is_data":bool})

    set_cache(Salesbud, None, [["bediener_nr", "monat", "jahr"]], True, [], ["bediener_nr", "monat", "jahr"])
    set_cache(Salestat, None, [["bediener_nr", "monat", "jahr"]], True, [], ["bediener_nr", "monat", "jahr"])
    set_cache(Htparam, None, [["paramnr"]], True, [], ["paramnr"])
    set_cache(Bediener, None, [["userinit"]], True, [], ["userinit"])

    db_session = local_storage.db_session

    def generate_output():
        nonlocal its_ok, slist_data, m1, m2, y1, y2, yy, monat, jahr, usr_grp, user_total_lodg, user_total_lbudget, user_total_lproz, user_total_fbrev, user_total_fbbudget, user_total_fbproz, user_total_otrev, user_total_otbudget, user_total_otproz, user_total_rmnight, user_total_rbudget, user_total_rmproz, htparam, bediener, salesbud, salestat, genstat, guest, h_bill, h_artikel, artikel, h_bill_line
        nonlocal from_date, to_date, usr_init, show_breakdown


        nonlocal slist, sbuff, buff_slist
        nonlocal slist_data

        return {"its_ok": its_ok, "slist": slist_data}

    def add_start_zero(input_int:int, number_of_char:int):

        nonlocal its_ok, slist_data, m1, m2, y1, y2, yy, monat, jahr, usr_grp, user_total_lodg, user_total_lbudget, user_total_lproz, user_total_fbrev, user_total_fbbudget, user_total_fbproz, user_total_otrev, user_total_otbudget, user_total_otproz, user_total_rmnight, user_total_rbudget, user_total_rmproz, htparam, bediener, salesbud, salestat, genstat, guest, h_bill, h_artikel, artikel, h_bill_line
        nonlocal from_date, to_date, usr_init, show_breakdown


        nonlocal slist, sbuff, buff_slist
        nonlocal slist_data

        char_tmp:string = ""
        needed:int = 0
        char_tmp = to_string(input_int)
        needed = number_of_char - length(char_tmp)

        if needed < 0:
            needed = 0
        char_tmp = fill("0", needed) + char_tmp
        return char_tmp


    def check_budget():

        nonlocal its_ok, slist_data, usr_grp, user_total_lodg, user_total_lbudget, user_total_lproz, user_total_fbrev, user_total_fbbudget, user_total_fbproz, user_total_otrev, user_total_otbudget, user_total_otproz, user_total_rmnight, user_total_rbudget, user_total_rmproz, htparam, bediener, salesbud, salestat, genstat, guest, h_bill, h_artikel, artikel, h_bill_line
        nonlocal from_date, to_date, usr_init, show_breakdown


        nonlocal slist, sbuff, buff_slist
        nonlocal slist_data

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

            salesbud = get_cache (Salesbud, {"bediener_nr": [(eq, bediener.nr)],"monat": [(eq, monat)],"jahr": [(eq, jahr)]})

            if not salesbud:
                salesbud = Salesbud()
                db_session.add(salesbud)

                salesbud.bediener_nr = bediener.nr
                salesbud.monat = monat
                salesbud.jahr = jahr


                pass

                return

            salestat = get_cache (Salestat, {"bediener_nr": [(eq, bediener.nr)],"monat": [(eq, monat)],"jahr": [(eq, jahr)]})

            if not salestat:
                salestat = Salestat()
                db_session.add(salestat)

                salestat.bediener_nr = bediener.nr
                salestat.monat = monat
                salestat.jahr = jahr


                pass

                return


    def create_list():

        nonlocal its_ok, slist_data, m1, m2, y1, y2, yy, monat, jahr, usr_grp, user_total_lodg, user_total_lbudget, user_total_lproz, user_total_fbrev, user_total_fbbudget, user_total_fbproz, user_total_otrev, user_total_otbudget, user_total_otproz, user_total_rmnight, user_total_rbudget, user_total_rmproz, htparam, bediener, salesbud, salestat, genstat, guest, h_bill, h_artikel, artikel, h_bill_line
        nonlocal from_date, to_date, usr_init, show_breakdown


        nonlocal slist, sbuff, buff_slist
        nonlocal slist_data

        # Rulita chg fdate to tmp_fdate
        # Rulita chg tdate to tmp_tdate
        do_it:bool = False
        tmp_fdate:date = None   
        fdate_1styear:date = None
        tmp_tdate:date = None
        loopi:date = None
        stat_buff = None
        bud_buff = None
        bgenstat = None
        Stat_buff =  create_buffer("Stat_buff",Salestat)
        Bud_buff =  create_buffer("Bud_buff",Salesbud)
        Bgenstat =  create_buffer("Bgenstat",Genstat)
        
        
        tmp_fdate = date_mdy(to_int(substring(from_date, 0, 2)) , 1, to_int(substring(from_date, 2, 4)))

        if to_int(substring(to_date, 0, 2)) == 12:
            tmp_tdate = date_mdy(1, 1, to_int(substring(to_date, 2, 4)) + timedelta(days=1) - 1)
        else:
            # tdate = date_mdy(to_int(substring(to_date, 0, 2)) + timedelta(days=1, 1, to_int(substring(to_date, 2, 4))) - 1)
            month = to_int(substring(to_date, 0, 2))
            day = to_int(substring(to_date, 2, 2))
            year = to_int(substring(to_date, 4, 4))

            # Create a date object, add one day, then subtract one day (effectively no change—fix if that's not intended)
            temp_date = date(year, month, day) + timedelta(days=1) - timedelta(days=1)

            # Assign final date using date_mdy
            tmp_tdate = date_mdy(temp_date.month, temp_date.day, temp_date.year)

        for loopi in date_range(tmp_fdate,tmp_tdate) :

            if show_breakdown:

                slist = query(slist_data, filters=(lambda slist: slist.mnth == get_month(loopi) and slist.yr == get_year(loopi) and slist.userinit == bediener.userinit), first=True)

                if not slist:
                    slist = Slist()
                    slist_data.append(slist)

                    slist.userinit = bediener.userinit
                    slist.yr = get_year(loopi)
                    slist.mnth = get_month(loopi)
                    slist.bezeich = add_start_zero (get_month(loopi) , 2) + "/" + add_start_zero (get_year(loopi) , 4)
                    slist.is_data = True


            else:

                slist = query(slist_data, filters=(lambda slist: slist.mnth == get_month(loopi) and slist.yr == get_year(loopi)), first=True)

                if not slist:
                    slist = Slist()
                    slist_data.append(slist)

                    slist.userinit = bediener.userinit
                    slist.yr = get_year(loopi)
                    slist.mnth = get_month(loopi)
                    slist.bezeich = add_start_zero (get_month(loopi) , 2) + "/" + add_start_zero (get_year(loopi) , 4)
                    slist.is_data = True


        fdate_1styear = date_mdy(1, 1, to_int(substring(from_date, 2, 4)))

        genstat_obj_list = {}
        genstat = Genstat()
        guest = Guest()
        for genstat.resstatus, genstat.datum, genstat.logis, genstat.zipreis, genstat.gratis, genstat.erwachs, genstat.kind1, genstat.kind2, genstat._recid, guest.phonetik3, guest._recid in db_session.query(Genstat.resstatus, Genstat.datum, Genstat.logis, Genstat.zipreis, Genstat.gratis, Genstat.erwachs, Genstat.kind1, Genstat.kind2, Genstat._recid, Guest.phonetik3, Guest._recid).join(Guest,(Guest.gastnr == Genstat.gastnr)).filter(
                 (Genstat.datum >= fdate_1styear) & (Genstat.datum <= tmp_tdate) & (Genstat.zinr != "") & (Genstat.res_logic[inc_value(1)])).order_by(Genstat.datum, Guest.name, Guest.gastnr).all():
            if genstat_obj_list.get(genstat._recid):
                continue
            else:
                genstat_obj_list[genstat._recid] = True


            do_it = True

            if genstat.zipreis == 0:

                if (genstat.gratis > 0):
                    do_it = False

                if (genstat.erwachs + genstat.kind1 + genstat.kind2 + genstat.gratis == 0) and genstat.resstatus != 13:
                    do_it = False

            if do_it:

                if guest.phonetik3 == trim(bediener.userinit):

                    if show_breakdown:

                        slist = query(slist_data, filters=(lambda slist: slist.mnth == get_month(genstat.datum) and slist.yr == get_year(genstat.datum) and slist.userinit == bediener.userinit), first=True)

                        if slist:

                            if genstat.resstatus != 13:
                                slist.lodg =  to_decimal(slist.lodg) + to_decimal(genstat.logis)
                                slist.rmnight = slist.rmnight + 1
                                user_total_lodg =  to_decimal(user_total_lodg) + to_decimal(genstat.logis)
                                user_total_rmnight =  to_decimal(user_total_rmnight) + to_decimal("1")


                    else:

                        slist = query(slist_data, filters=(lambda slist: slist.mnth == get_month(genstat.datum) and slist.yr == get_year(genstat.datum)), first=True)

                        if slist:

                            if genstat.resstatus != 13:
                                slist.lodg =  to_decimal(slist.lodg) + to_decimal(genstat.logis)
                                slist.rmnight = slist.rmnight + 1
                                user_total_lodg =  to_decimal(user_total_lodg) + to_decimal(genstat.logis)
                                user_total_rmnight =  to_decimal(user_total_rmnight) + to_decimal("1")

        salestat_obj_list = {}
        salestat = Salestat()
        salesbud = Salesbud()
        for salestat.monat, salestat.jahr, salestat.sonst_umsatz, salestat.f_b_umsatz, salestat.bediener_nr, salestat._recid, salesbud.sonst_umsatz, salesbud.f_b_umsatz, salesbud.room_nights, salesbud.argtumsatz, salesbud.bediener_nr, salesbud.monat, salesbud.jahr, salesbud._recid in db_session.query(Salestat.monat, Salestat.jahr, Salestat.sonst_umsatz, Salestat.f_b_umsatz, Salestat.bediener_nr, Salestat._recid, Salesbud.sonst_umsatz, Salesbud.f_b_umsatz, Salesbud.room_nights, Salesbud.argtumsatz, Salesbud.bediener_nr, Salesbud.monat, Salesbud.jahr, Salesbud._recid).join(Salesbud,(Salesbud.bediener_nr == Salestat.bediener_nr) & (Salesbud.monat == Salestat.monat) & (Salesbud.jahr == Salestat.jahr)).filter(
                 (Salestat.bediener_nr == bediener.nr) & (((Salestat.jahr > get_year(fdate_1styear)) & (Salestat.monat >= 1)) | ((Salestat.jahr == get_year(fdate_1styear)) & (Salestat.monat >= get_month(fdate_1styear)))) & (((Salestat.jahr < to_int(substring(to_date, 2, 4))) & (Salestat.monat >= 1)) | ((Salestat.jahr == to_int(substring(to_date, 2, 4))) & (Salestat.monat <= to_int(substring(to_date, 0, 2)))))).order_by(Salestat.jahr, Salestat.monat).all():
            if salestat_obj_list.get(salestat._recid):
                continue
            else:
                salestat_obj_list[salestat._recid] = True

            if show_breakdown:

                slist = query(slist_data, filters=(lambda slist:(slist.mnth == salestat.monat) and (slist.yr == salestat.jahr) and slist.userinit == bediener.userinit), first=True)

                if slist:
                    slist.otrev =  to_decimal(slist.otrev) + to_decimal(salestat.sonst_umsatz)
                    slist.otbudget =  to_decimal(slist.otbudget) + to_decimal(salesbud.sonst_umsatz)
                    slist.fbrev =  to_decimal(slist.fbrev) + to_decimal(salestat.f_b_umsatz)
                    slist.fbbudget =  to_decimal(slist.fbbudget) + to_decimal(salesbud.f_b_umsatz)
                    slist.rbudget = slist.rbudget + salesbud.room_nights
                    slist.lbudget =  to_decimal(slist.lbudget) + to_decimal(salesbud.argtumsatz)
                    user_total_otrev =  to_decimal(user_total_otrev) + to_decimal(salestat.sonst_umsatz)
                    user_total_otbudget =  to_decimal(user_total_otbudget) + to_decimal(salesbud.sonst_umsatz)
                    user_total_fbrev =  to_decimal(user_total_fbrev) + to_decimal(salestat.f_b_umsatz)
                    user_total_fbbudget =  to_decimal(user_total_fbbudget) + to_decimal(salesbud.f_b_umsatz)
                    user_total_lbudget =  to_decimal(user_total_lbudget) + to_decimal(salesbud.room_nights)
                    user_total_rbudget =  to_decimal(user_total_rbudget) + to_decimal(salesbud.argtumsatz)


            else:

                slist = query(slist_data, filters=(lambda slist:(slist.mnth == salestat.monat) and (slist.yr == salestat.jahr)), first=True)

                if slist:
                    slist.otrev =  to_decimal(slist.otrev) + to_decimal(salestat.sonst_umsatz)
                    slist.otbudget =  to_decimal(slist.otbudget) + to_decimal(salesbud.sonst_umsatz)
                    slist.fbrev =  to_decimal(slist.fbrev) + to_decimal(salestat.f_b_umsatz)
                    slist.fbbudget =  to_decimal(slist.fbbudget) + to_decimal(salesbud.f_b_umsatz)
                    slist.rbudget = slist.rbudget + salesbud.room_nights
                    slist.lbudget =  to_decimal(slist.lbudget) + to_decimal(salesbud.argtumsatz)
                    user_total_otrev =  to_decimal(user_total_otrev) + to_decimal(salestat.sonst_umsatz)
                    user_total_otbudget =  to_decimal(user_total_otbudget) + to_decimal(salesbud.sonst_umsatz)
                    user_total_fbrev =  to_decimal(user_total_fbrev) + to_decimal(salestat.f_b_umsatz)
                    user_total_fbbudget =  to_decimal(user_total_fbbudget) + to_decimal(salesbud.f_b_umsatz)
                    user_total_lbudget =  to_decimal(user_total_lbudget) + to_decimal(salesbud.room_nights)
                    user_total_rbudget =  to_decimal(user_total_rbudget) + to_decimal(salesbud.argtumsatz)


    def count_ytd():

        nonlocal its_ok, slist_data, m1, m2, y1, y2, yy, monat, jahr, usr_grp, user_total_lodg, user_total_lbudget, user_total_lproz, user_total_fbrev, user_total_fbbudget, user_total_fbproz, user_total_otrev, user_total_otbudget, user_total_otproz, user_total_rmnight, user_total_rbudget, user_total_rmproz, htparam, bediener, salesbud, salestat, genstat, guest, h_bill, h_artikel, artikel, h_bill_line
        nonlocal from_date, to_date, usr_init, show_breakdown


        nonlocal slist, sbuff, buff_slist
        nonlocal slist_data

        year_tmp:int = 0
        user_tmp:string = ""
        ytd_lodging:Decimal = to_decimal("0.0")
        ytd_rmnight:Decimal = to_decimal("0.0")
        ytd_fnb:Decimal = to_decimal("0.0")
        ytd_other:Decimal = to_decimal("0.0")
        ytd_bud_lodg:Decimal = to_decimal("0.0")
        ytd_bud_rmnight:Decimal = to_decimal("0.0")
        ytd_bud_fnb:Decimal = to_decimal("0.0")
        ytd_bud_ot:Decimal = to_decimal("0.0")
        usr_tot_ytd_lodging:Decimal = to_decimal("0.0")
        usr_tot_ytd_rmnight:Decimal = to_decimal("0.0")
        usr_tot_ytd_fnb:Decimal = to_decimal("0.0")
        usr_tot_ytd_other:Decimal = to_decimal("0.0")
        usr_tot_ytd_bud_lodg:Decimal = to_decimal("0.0")
        usr_tot_ytd_bud_rmnight:Decimal = to_decimal("0.0")
        usr_tot_ytd_bud_fnb:Decimal = to_decimal("0.0")
        usr_tot_ytd_bud_ot:Decimal = to_decimal("0.0")
        Sbuff = Slist
        sbuff_data = slist_data

        for slist in query(slist_data, filters=(lambda slist: slist.yr >= 0), sort_by=[("userinit",False),("yr",False),("mnth",False)]):

            if user_tmp != slist.userinit:

                sbuff = query(sbuff_data, filters=(lambda sbuff: sbuff.userinit.lower()  == (user_tmp).lower()  and sbuff.bezeich.lower()  == ("T O T A L").lower()), first=True)

                if sbuff:
                    sbuff.ytd_lodg =  to_decimal(usr_tot_ytd_lodging)
                    sbuff.ytd_rmnight = usr_tot_ytd_rmnight
                    sbuff.ytd_otrev =  to_decimal(usr_tot_ytd_other)
                    sbuff.ytd_fbrev =  to_decimal(usr_tot_ytd_fnb)
                    sbuff.ytd_lbudget =  to_decimal(usr_tot_ytd_bud_lodg)
                    sbuff.ytd_rbudget = usr_tot_ytd_bud_rmnight
                    sbuff.ytd_otbudget =  to_decimal(usr_tot_ytd_bud_ot)
                    sbuff.ytd_fbbudget =  to_decimal(usr_tot_ytd_bud_fnb)

                    # Rd 18/7/25
                    # sbuff.ytd_lproz =  to_decimal(sbuff.ytd_lodg) / to_decimal(sbuff.ytd_lbudget) * to_decimal("100")
                    # sbuff.ytd_rmproz =  to_decimal(sbuff.ytd_rmnight) / to_decimal(sbuff.ytd_rbudget) * to_decimal("100")
                    # sbuff.ytd_otproz =  to_decimal(sbuff.ytd_otrev) / to_decimal(sbuff.ytd_otbudget) * to_decimal("100")
                    # sbuff.ytd_fbproz =  to_decimal(sbuff.ytd_fbrev) / to_decimal(sbuff.ytd_fbbudget) * to_decimal("100")
                    sbuff.ytd_lproz = (
                        to_decimal(sbuff.ytd_lodg) / to_decimal(sbuff.ytd_lbudget) * to_decimal("100")
                        if to_decimal(sbuff.ytd_lbudget) != 0
                        else to_decimal("0")
                    )

                    sbuff.ytd_rmproz = (
                        to_decimal(sbuff.ytd_rmnight) / to_decimal(sbuff.ytd_rbudget) * to_decimal("100")
                        if to_decimal(sbuff.ytd_rbudget) != 0
                        else to_decimal("0")
                    )

                    sbuff.ytd_otproz = (
                        to_decimal(sbuff.ytd_otrev) / to_decimal(sbuff.ytd_otbudget) * to_decimal("100")
                        if to_decimal(sbuff.ytd_otbudget) != 0
                        else to_decimal("0")
                    )

                    sbuff.ytd_fbproz = (
                        to_decimal(sbuff.ytd_fbrev) / to_decimal(sbuff.ytd_fbbudget) * to_decimal("100")
                        if to_decimal(sbuff.ytd_fbbudget) != 0
                        else to_decimal("0")
                    )


                    if sbuff.ytd_lproz == None:
                        sbuff.ytd_lproz =  to_decimal(0.00)

                    if sbuff.ytd_rmproz == None:
                        sbuff.ytd_rmproz =  to_decimal(0.00)

                    if sbuff.ytd_otproz == None:
                        sbuff.ytd_otproz =  to_decimal(0.00)

                    if sbuff.ytd_fbproz == None:
                        sbuff.ytd_fbproz =  to_decimal(0.00)
                usr_tot_ytd_lodging =  to_decimal("0")
                usr_tot_ytd_rmnight =  to_decimal("0")
                usr_tot_ytd_fnb =  to_decimal("0")
                usr_tot_ytd_other =  to_decimal("0")
                usr_tot_ytd_bud_lodg =  to_decimal("0")
                usr_tot_ytd_bud_rmnight =  to_decimal("0")
                usr_tot_ytd_bud_fnb =  to_decimal("0")
                usr_tot_ytd_bud_ot =  to_decimal("0")

            if user_tmp != slist.userinit or year_tmp != slist.yr:
                ytd_lodging =  to_decimal("0")
                ytd_rmnight =  to_decimal("0")
                ytd_fnb =  to_decimal("0")
                ytd_other =  to_decimal("0")
                ytd_bud_lodg =  to_decimal("0")
                ytd_bud_rmnight =  to_decimal("0")
                ytd_bud_fnb =  to_decimal("0")
                ytd_bud_ot =  to_decimal("0")


                user_tmp = slist.userinit
                year_tmp = slist.yr
            
            # Rd 18/7/25
            # slist.lproz =  to_decimal(slist.lodg) / to_decimal(slist.lbudget) * to_decimal("100")
            slist.lproz = (
                to_decimal(slist.lodg) / to_decimal(slist.lbudget) * to_decimal("100")
                if to_decimal(slist.lbudget) != 0
                else to_decimal("0")
            )
            # slist.rmproz =  to_decimal(slist.rmnight) / to_decimal(slist.rbudget) * to_decimal("100")
            slist.rmproz = (
                to_decimal(slist.rmnight) / to_decimal(slist.rbudget) * to_decimal("100")
                if to_decimal(slist.rbudget) != 0
                else to_decimal("0")
            )
            # slist.otproz =  to_decimal(slist.otrev) / to_decimal(slist.otbudget) * to_decimal("100")
            slist.otproz = (
                to_decimal(slist.otrev) / to_decimal(slist.otbudget) * to_decimal("100")
                if to_decimal(slist.otbudget) != 0
                else to_decimal("0")
            )
            # slist.fbproz =  to_decimal(slist.fbrev) / to_decimal(slist.fbbudget) * to_decimal("100")
            slist.fbproz = (
                to_decimal(slist.fbrev) / to_decimal(slist.fbbudget) * to_decimal("100")
                if to_decimal(slist.fbbudget) != 0
                else to_decimal("0")
            )

            if slist.lproz == None:
                slist.lproz =  to_decimal(0.00)

            if slist.rmproz == None:
                slist.rmproz =  to_decimal(0.00)

            if slist.otproz == None:
                slist.otproz =  to_decimal(0.00)

            if slist.fbproz == None:
                slist.fbproz =  to_decimal(0.00)
            ytd_lodging =  to_decimal(ytd_lodging) + to_decimal(slist.lodg)
            ytd_rmnight =  to_decimal(ytd_rmnight) + to_decimal(slist.rmnight)
            ytd_fnb =  to_decimal(ytd_fnb) + to_decimal(slist.fbrev)
            ytd_other =  to_decimal(ytd_other) + to_decimal(slist.otrev)
            ytd_bud_lodg =  to_decimal(ytd_bud_lodg) + to_decimal(slist.lbudget)
            ytd_bud_rmnight =  to_decimal(ytd_bud_rmnight) + to_decimal(slist.rbudget)
            ytd_bud_fnb =  to_decimal(ytd_bud_fnb) + to_decimal(slist.fbbudget)
            ytd_bud_ot =  to_decimal(ytd_bud_ot) + to_decimal(slist.otbudget)
            slist.ytd_lodg =  to_decimal(ytd_lodging)
            slist.ytd_rmnight = ytd_rmnight
            slist.ytd_otrev =  to_decimal(ytd_other)
            slist.ytd_fbrev =  to_decimal(ytd_fnb)
            slist.ytd_lbudget =  to_decimal(ytd_bud_lodg)
            slist.ytd_rbudget = ytd_bud_rmnight
            slist.ytd_otbudget =  to_decimal(ytd_bud_ot)
            slist.ytd_fbbudget =  to_decimal(ytd_bud_fnb)

            # Rd 18/7/25
            # slist.ytd_lproz =  to_decimal(slist.ytd_lodg) / to_decimal(slist.ytd_lbudget) * to_decimal("100")
            # slist.ytd_rmproz =  to_decimal(slist.ytd_rmnight) / to_decimal(slist.ytd_rbudget) * to_decimal("100")
            # slist.ytd_otproz =  to_decimal(slist.ytd_otrev) / to_decimal(slist.ytd_otbudget) * to_decimal("100")
            # slist.ytd_fbproz =  to_decimal(slist.ytd_fbrev) / to_decimal(slist.ytd_fbbudget) * to_decimal("100")
            slist.ytd_lproz = (
                to_decimal(slist.ytd_lodg) / to_decimal(slist.ytd_lbudget) * to_decimal("100")
                if to_decimal(slist.ytd_lbudget) != 0
                else to_decimal("0")
            )

            slist.ytd_rmproz = (
                to_decimal(slist.ytd_rmnight) / to_decimal(slist.ytd_rbudget) * to_decimal("100")
                if to_decimal(slist.ytd_rbudget) != 0
                else to_decimal("0")
            )

            slist.ytd_otproz = (
                to_decimal(slist.ytd_otrev) / to_decimal(slist.ytd_otbudget) * to_decimal("100")
                if to_decimal(slist.ytd_otbudget) != 0
                else to_decimal("0")
            )

            slist.ytd_fbproz = (
                to_decimal(slist.ytd_fbrev) / to_decimal(slist.ytd_fbbudget) * to_decimal("100")
                if to_decimal(slist.ytd_fbbudget) != 0
                else to_decimal("0")
            )


            if slist.lodg == 0:
                slist.ytd_lodg =  to_decimal("0")

            if slist.rmnight == 0:
                slist.ytd_rmnight = 0

            if slist.fbrev == 0:
                slist.ytd_fbrev =  to_decimal("0")

            if slist.otrev == 0:
                slist.ytd_otrev =  to_decimal("0")
            usr_tot_ytd_lodging =  to_decimal(usr_tot_ytd_lodging) + to_decimal(slist.ytd_lodg)
            usr_tot_ytd_rmnight =  to_decimal(usr_tot_ytd_rmnight) + to_decimal(slist.ytd_rmnight)
            usr_tot_ytd_other =  to_decimal(usr_tot_ytd_other) + to_decimal(slist.ytd_otrev)
            usr_tot_ytd_fnb =  to_decimal(usr_tot_ytd_fnb) + to_decimal(slist.ytd_fbrev)
            usr_tot_ytd_bud_lodg =  to_decimal(usr_tot_ytd_bud_lodg) + to_decimal(slist.ytd_lbudget)
            usr_tot_ytd_bud_rmnight =  to_decimal(usr_tot_ytd_bud_rmnight) + to_decimal(slist.ytd_rbudget)
            usr_tot_ytd_bud_ot =  to_decimal(usr_tot_ytd_bud_ot) + to_decimal(slist.ytd_otbudget)
            usr_tot_ytd_bud_fnb =  to_decimal(usr_tot_ytd_bud_fnb) + to_decimal(slist.ytd_fbbudget)

            if slist.ytd_lproz == None:
                slist.ytd_lproz =  to_decimal(0.00)

            if slist.ytd_rmproz == None:
                slist.ytd_rmproz =  to_decimal(0.00)

            if slist.ytd_otproz == None:
                slist.ytd_otproz =  to_decimal(0.00)

            if slist.ytd_fbproz == None:
                slist.ytd_fbproz =  to_decimal(0.00)


    def count_total():

        nonlocal its_ok, slist_data, m1, m2, y1, y2, yy, monat, jahr, usr_grp, user_total_lodg, user_total_lbudget, user_total_lproz, user_total_fbrev, user_total_fbbudget, user_total_fbproz, user_total_otrev, user_total_otbudget, user_total_otproz, user_total_rmnight, user_total_rbudget, user_total_rmproz, htparam, bediener, salesbud, salestat, genstat, guest, h_bill, h_artikel, artikel, h_bill_line
        nonlocal from_date, to_date, usr_init, show_breakdown


        nonlocal slist, sbuff, buff_slist
        nonlocal slist_data


        Buff_slist = Slist
        buff_slist_data = slist_data
        slist = Slist()
        slist_data.append(slist)

        slist.mnth = -1
        slist.yr = -1
        slist.is_data = True

        if show_breakdown:
            slist.bezeich = "GRAND TOTAL"
        else:
            slist.bezeich = "T O T A L"

        for buff_slist in query(buff_slist_data, filters=(lambda buff_slist: buff_slist.yr >= 0 and buff_slist.mnth >= 0)):
            slist.lodg =  to_decimal(slist.lodg) + to_decimal(buff_slist.lodg)
            slist.lbudget =  to_decimal(slist.lbudget) + to_decimal(buff_slist.lbudget)
            slist.fbrev =  to_decimal(slist.fbrev) + to_decimal(buff_slist.fbrev)
            slist.fbbudget =  to_decimal(slist.fbbudget) + to_decimal(buff_slist.fbbudget)
            slist.otrev =  to_decimal(slist.otrev) + to_decimal(buff_slist.otrev)
            slist.otbudget =  to_decimal(slist.otbudget) + to_decimal(buff_slist.otbudget)
            slist.rmnight = slist.rmnight + buff_slist.rmnight
            slist.rbudget = slist.rbudget + buff_slist.rbudget
            slist.ytd_lodg =  to_decimal(slist.ytd_lodg) + to_decimal(buff_slist.ytd_lodg)
            slist.ytd_lbudget =  to_decimal(slist.ytd_lbudget) + to_decimal(buff_slist.ytd_lbudget)
            slist.ytd_fbrev =  to_decimal(slist.ytd_fbrev) + to_decimal(buff_slist.ytd_fbrev)
            slist.ytd_fbbudget =  to_decimal(slist.ytd_fbbudget) + to_decimal(buff_slist.ytd_fbbudget)
            slist.ytd_rmnight = slist.ytd_rmnight + buff_slist.ytd_rmnight
            slist.ytd_rbudget = slist.ytd_rbudget + buff_slist.ytd_rbudget
            slist.ytd_otrev =  to_decimal(slist.ytd_otrev) + to_decimal(buff_slist.ytd_otrev)
            slist.ytd_otbudget =  to_decimal(slist.ytd_otbudget) + to_decimal(buff_slist.ytd_otbudget)


        # slist.lproz =  to_decimal(slist.lodg) / to_decimal(slist.lbudget) * to_decimal("100")
        # slist.rmproz =  to_decimal(slist.rmnight) / to_decimal(slist.rbudget) * to_decimal("100")
        # slist.fbproz =  to_decimal(slist.fbrev) / to_decimal(slist.fbbudget) * to_decimal("100")
        # slist.otproz =  to_decimal(slist.otrev) / to_decimal(slist.otbudget) * to_decimal("100")
        # slist.ytd_lproz =  to_decimal(slist.ytd_lodg) / to_decimal(slist.ytd_lbudget) * to_decimal("100")
        # slist.ytd_rmproz =  to_decimal(slist.ytd_rmnight) / to_decimal(slist.ytd_rbudget) * to_decimal("100")
        # slist.ytd_fbproz =  to_decimal(slist.ytd_fbrev) / to_decimal(slist.ytd_fbbudget) * to_decimal("100")
        # slist.ytd_otproz =  to_decimal(slist.ytd_otrev) / to_decimal(slist.ytd_otbudget) * to_decimal("100")


        slist.lproz = safe_divide(slist.lodg, slist.lbudget)
        slist.rmproz = safe_divide(slist.rmnight, slist.rbudget)
        slist.fbproz = safe_divide(slist.fbrev, slist.fbbudget)
        slist.otproz = safe_divide(slist.otrev, slist.otbudget)
        slist.ytd_lproz = safe_divide(slist.ytd_lodg, slist.ytd_lbudget)
        slist.ytd_rmproz = safe_divide(slist.ytd_rmnight, slist.ytd_rbudget)
        slist.ytd_fbproz = safe_divide(slist.ytd_fbrev, slist.ytd_fbbudget)
        slist.ytd_otproz = safe_divide(slist.ytd_otrev, slist.ytd_otbudget)

        if slist.lproz == None:
            slist.lproz =  to_decimal(0.00)

        if slist.rmproz == None:
            slist.rmproz =  to_decimal(0.00)

        if slist.otproz == None:
            slist.otproz =  to_decimal(0.00)

        if slist.fbproz == None:
            slist.fbproz =  to_decimal(0.00)

        if slist.ytd_lproz == None:
            slist.ytd_lproz =  to_decimal(0.00)

        if slist.ytd_rmproz == None:
            slist.ytd_rmproz =  to_decimal(0.00)

        if slist.ytd_otproz == None:
            slist.ytd_otproz =  to_decimal(0.00)

        if slist.ytd_fbproz == None:
            slist.ytd_fbproz =  to_decimal(0.00)


    def include_outlet_fnb():

        nonlocal its_ok, slist_data, m1, m2, y1, y2, yy, monat, jahr, usr_grp, user_total_lodg, user_total_lbudget, user_total_lproz, user_total_fbrev, user_total_fbbudget, user_total_fbproz, user_total_otrev, user_total_otbudget, user_total_otproz, user_total_rmnight, user_total_rbudget, user_total_rmproz, htparam, bediener, salesbud, salestat, genstat, guest, h_bill, h_artikel, artikel, h_bill_line
        nonlocal usr_init, show_breakdown


        nonlocal slist, sbuff, buff_slist
        nonlocal slist_data

        from_date:date = None
        to_date:date = None
        temp_date:date = None
        count_loop:int = 0

        if show_breakdown:

            for slist in query(slist_data, filters=(lambda slist: slist.userinit == bediener.userinit and slist.yr >= 0), sort_by=[("yr",False),("mnth",False)]):
                from_date = date_mdy(slist.mnth, 1, slist.yr)

                if slist.mnth == 12:
                    to_date = date_mdy(1, 1, slist.yr + timedelta(days=1)) - timedelta(days=1)
                else:
                    to_date = date_mdy(slist.mnth + 1, 1, slist.yr) - timedelta(days=1)

                h_bill_line_obj_list = {}
                for h_bill_line, h_bill, guest, h_artikel, artikel in db_session.query(H_bill_line, H_bill, Guest, H_artikel, Artikel).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) & (H_bill.departement == H_bill_line.departement) & (H_bill.flag == 1)).join(Guest,(Guest.gastnr == H_bill.resnr) & (Guest.phonetik3 == trim(bediener.userinit))).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.artart == 0)).filter(
                         (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.artnr != 0)).order_by(H_bill_line.bill_datum).all():
                    if h_bill_line_obj_list.get(h_bill_line._recid):
                        continue
                    else:
                        h_bill_line_obj_list[h_bill_line._recid] = True

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6:
                        slist.fbrev =  to_decimal(slist.fbrev) + to_decimal(h_bill_line.betrag)
                        user_total_fbrev =  to_decimal(user_total_fbrev) + to_decimal(h_bill_line.betrag)

                    elif artikel.umsatzart == 4:
                        slist.otrev =  to_decimal(slist.otrev) + to_decimal(h_bill_line.betrag)
                        user_total_otrev =  to_decimal(user_total_otrev) + to_decimal(h_bill_line.betrag)
        else:

            for slist in query(slist_data, filters=(lambda slist: slist.yr >= 0), sort_by=[("yr",False),("mnth",False)]):
                from_date = date_mdy(slist.mnth, 1, slist.yr)

                if slist.mnth == 12:
                    to_date = date_mdy(1, 1, slist.yr + timedelta(days=1)) - timedelta(days=1)
                else:
                    to_date = date_mdy(slist.mnth + 1, 1, slist.yr) - timedelta(days=1)

                h_bill_line_obj_list = {}
                for h_bill_line, h_bill, guest, h_artikel, artikel in db_session.query(H_bill_line, H_bill, Guest, H_artikel, Artikel).join(H_bill,(H_bill.rechnr == H_bill_line.rechnr) & (H_bill.departement == H_bill_line.departement) & (H_bill.flag == 1)).join(Guest,(Guest.gastnr == H_bill.resnr) & (Guest.phonetik3 == trim(bediener.userinit))).join(H_artikel,(H_artikel.artnr == H_bill_line.artnr) & (H_artikel.departement == H_bill_line.departement)).join(Artikel,(Artikel.artnr == H_artikel.artnrfront) & (Artikel.departement == H_artikel.departement) & (Artikel.artart == 0)).filter(
                         (H_bill_line.bill_datum >= from_date) & (H_bill_line.bill_datum <= to_date) & (H_bill_line.artnr != 0)).order_by(H_bill_line.bill_datum).all():
                    if h_bill_line_obj_list.get(h_bill_line._recid):
                        continue
                    else:
                        h_bill_line_obj_list[h_bill_line._recid] = True

                    if artikel.umsatzart == 3 or artikel.umsatzart == 5 or artikel.umsatzart == 6:
                        slist.fbrev =  to_decimal(slist.fbrev) + to_decimal(h_bill_line.betrag)
                        user_total_fbrev =  to_decimal(user_total_fbrev) + to_decimal(h_bill_line.betrag)

                    elif artikel.umsatzart == 4:
                        slist.otrev =  to_decimal(slist.otrev) + to_decimal(h_bill_line.betrag)
                        user_total_otrev =  to_decimal(user_total_otrev) + to_decimal(h_bill_line.betrag)

    m1 = to_int(substring(from_date, 0, 2))
    y1 = to_int(substring(from_date, 2, 4))
    y2 = to_int(substring(to_date, 2, 4))
    m2 = to_int(substring(to_date, 0, 2))

    if usr_init.lower()  == ("ALL").lower()  or usr_init.lower()  == None:

        htparam = get_cache (Htparam, {"paramnr": [(eq, 547)]})

        if htparam:
            usr_grp = htparam.finteger

        for bediener in db_session.query(Bediener).filter(
                 (Bediener.user_group == usr_grp)).order_by(Bediener._recid).all():
            check_budget()

            if its_ok:
                user_total_lodg =  to_decimal("0")
                user_total_lbudget =  to_decimal("0")
                user_total_fbrev =  to_decimal("0")
                user_total_fbbudget =  to_decimal("0")
                user_total_otrev =  to_decimal("0")
                user_total_otbudget =  to_decimal("0")
                user_total_rmnight =  to_decimal("0")
                user_total_rbudget =  to_decimal("0")

                if show_breakdown:
                    slist = Slist()
                    slist_data.append(slist)

                    slist.userinit = bediener.userinit
                    slist.bezeich = bediener.userinit + " - " + bediener.username
                    slist.yr = -2
                    slist.mnth = -2
                    slist.is_data = False


                create_list()
                include_outlet_fnb()

                if show_breakdown:
                    slist = Slist()
                    slist_data.append(slist)

                    slist.userinit = bediener.userinit
                    slist.bezeich = "T O T A L"
                    slist.yr = -2
                    slist.mnth = -2
                    slist.lodg =  to_decimal(user_total_lodg)
                    slist.lbudget =  to_decimal(user_total_lbudget)
                    slist.fbrev =  to_decimal(user_total_fbrev)
                    slist.fbbudget =  to_decimal(user_total_fbbudget)
                    slist.otrev =  to_decimal(user_total_otrev)
                    slist.otbudget =  to_decimal(user_total_otbudget)
                    slist.rmnight = user_total_rmnight
                    slist.rbudget = user_total_rbudget
                    slist.is_data = True


                    slist = Slist()
                    slist_data.append(slist)

                    slist.yr = -2
                    slist.mnth = -2
                    slist.is_data = False


        count_ytd()
        count_total()
    else:

        bediener = get_cache (Bediener, {"userinit": [(eq, usr_init)]})
        check_budget()

        if its_ok:
            create_list()
            include_outlet_fnb()
            count_ytd()
        count_total()

    return generate_output()