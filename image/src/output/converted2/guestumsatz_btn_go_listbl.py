#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from models import Guest, Guestat, Guestbud

def guestumsatz_btn_go_listbl(from_date:string, cardtype:int, hide_zero:bool, disptype:int):

    prepare_cache ([Guest, Guestat, Guestbud])

    glodging_turnover_list = []
    gfb_turnover_list = []
    gother_turnover_list = []
    guest = guestat = guestbud = None

    glodging_turnover = gfb_turnover = gother_turnover = to_list = None

    glodging_turnover_list, Glodging_turnover = create_model("Glodging_turnover", {"cust_name":string, "t_o":Decimal, "budget_to":Decimal, "percnt_to":Decimal, "ytd":Decimal, "budget_ytd":Decimal, "percnt_ytd":Decimal, "lodg_to":Decimal, "budget_lodg_to":Decimal, "percnt_lodg_to":Decimal, "lodg_ytd":Decimal, "budget_lodg_ytd":Decimal, "percnt_lodg_ytd":Decimal, "rmnite":Decimal, "budget_rmnite":Decimal, "percnt_rmnite":Decimal, "rmnite_ytd":Decimal, "budget_rmnite_ytd":Decimal, "percnt_rmnite_ytd":Decimal})
    gfb_turnover_list, Gfb_turnover = create_model("Gfb_turnover", {"cust_name":string, "t_o":Decimal, "fb_to":Decimal, "budget_fb_to":Decimal, "percnt_fb_to":Decimal, "fb_ytd":Decimal, "budget_fb_ytd":Decimal, "percnt_fb_ytd":Decimal})
    gother_turnover_list, Gother_turnover = create_model("Gother_turnover", {"cust_name":string, "t_o":Decimal, "other_to":Decimal, "budget_other_to":Decimal, "percnt_other_to":Decimal, "other_ytd":Decimal, "budget_other_ytd":Decimal, "percnt_other_ytd":Decimal})
    to_list_list, To_list = create_model("To_list", {"gastnr":int, "name":string, "flag":[bool,12], "gesamt":Decimal, "b_gesamt":Decimal, "proz1":Decimal, "ygesamt":Decimal, "b_ygesamt":Decimal, "proz2":Decimal, "logis":Decimal, "b_logis":Decimal, "proz3":Decimal, "ylogis":Decimal, "b_ylogis":Decimal, "proz4":Decimal, "fb":Decimal, "b_fb":Decimal, "proz5":Decimal, "yfb":Decimal, "b_yfb":Decimal, "proz6":Decimal, "sonst":Decimal, "b_sonst":Decimal, "proz7":Decimal, "ysonst":Decimal, "b_ysonst":Decimal, "proz8":Decimal, "room":Decimal, "b_room":Decimal, "proz9":Decimal, "yroom":Decimal, "b_yroom":Decimal, "proz10":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal glodging_turnover_list, gfb_turnover_list, gother_turnover_list, guest, guestat, guestbud
        nonlocal from_date, cardtype, hide_zero, disptype


        nonlocal glodging_turnover, gfb_turnover, gother_turnover, to_list
        nonlocal glodging_turnover_list, gfb_turnover_list, gother_turnover_list, to_list_list

        return {"glodging-turnover": glodging_turnover_list, "gfb-turnover": gfb_turnover_list, "gother-turnover": gother_turnover_list}

    def create_umsatz():

        nonlocal glodging_turnover_list, gfb_turnover_list, gother_turnover_list, guest, guestat, guestbud
        nonlocal from_date, cardtype, hide_zero, disptype


        nonlocal glodging_turnover, gfb_turnover, gother_turnover, to_list
        nonlocal glodging_turnover_list, gfb_turnover_list, gother_turnover_list, to_list_list

        mm:int = 0
        yy:int = 0
        glodging_turnover_list.clear()
        gfb_turnover_list.clear()
        gother_turnover_list.clear()
        to_list_list.clear()
        mm = to_int(substring(from_date, 0, 2))
        yy = to_int(substring(from_date, 2, 4))

        guestat_obj_list = {}
        guestat = Guestat()
        guest = Guest()
        for guestat.gastnr, guestat.monat, guestat.jahr, guestat.gesamtumsatz, guestat.argtumsatz, guestat.f_b_umsatz, guestat.sonst_umsatz, guestat.room_nights, guestat._recid, guest.gastnr, guest.name, guest.vorname1, guest.anrede1, guest.anredefirma, guest._recid in db_session.query(Guestat.gastnr, Guestat.monat, Guestat.jahr, Guestat.gesamtumsatz, Guestat.argtumsatz, Guestat.f_b_umsatz, Guestat.sonst_umsatz, Guestat.room_nights, Guestat._recid, Guest.gastnr, Guest.name, Guest.vorname1, Guest.anrede1, Guest.anredefirma, Guest._recid).join(Guest,(Guest.gastnr == Guestat.gastnr) & (Guest.karteityp == cardtype)).filter(
                 (Guestat.jahr == yy) & (Guestat.monat <= mm) & (Guestat.betriebsnr == 0)).order_by(Guest.name).all():
            if guestat_obj_list.get(guestat._recid):
                continue
            else:
                guestat_obj_list[guestat._recid] = True

            guestbud = get_cache (Guestbud, {"gastnr": [(eq, guestat.gastnr)],"monat": [(eq, guestat.monat)],"jahr": [(eq, guestat.jahr)]})

            to_list = query(to_list_list, filters=(lambda to_list: to_list.gastnr == guest.gastnr), first=True)

            if not to_list:
                to_list = To_list()
                to_list_list.append(to_list)

                to_list.gastnr = guest.gastnr
                to_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
            to_list.ygesamt =  to_decimal(to_list.ygesamt) + to_decimal(guestat.gesamtumsatz)
            to_list.ylogis =  to_decimal(to_list.ylogis) + to_decimal(guestat.argtumsatz)
            to_list.yfb =  to_decimal(to_list.yfb) + to_decimal(guestat.f_b_umsatz)
            to_list.ysonst =  to_decimal(to_list.ysonst) + to_decimal(guestat.sonst_umsatz)
            to_list.yroom =  to_decimal(to_list.yroom) + to_decimal(guestat.room_nights)

            if guestat.monat == mm:
                to_list.gesamt =  to_decimal(to_list.gesamt) + to_decimal(guestat.gesamtumsatz)
                to_list.logis =  to_decimal(to_list.logis) + to_decimal(guestat.argtumsatz)
                to_list.fb =  to_decimal(to_list.fb) + to_decimal(guestat.f_b_umsatz)
                to_list.sonst =  to_decimal(to_list.sonst) + to_decimal(guestat.sonst_umsatz)
                to_list.room =  to_decimal(to_list.room) + to_decimal(guestat.room_nights)

            if guestbud and to_list.flag[guestbud.monat - 1]:
                to_list.flag[guestbud.monat - 1] = False
                to_list.b_ygesamt =  to_decimal(to_list.b_ygesamt) + to_decimal(guestbud.gesamtumsatz)
                to_list.b_ylogis =  to_decimal(to_list.b_ylogis) + to_decimal(guestbud.argtumsatz)
                to_list.b_yfb =  to_decimal(to_list.b_yfb) + to_decimal(guestbud.f_b_umsatz)
                to_list.b_ysonst =  to_decimal(to_list.b_ysonst) + to_decimal(guestbud.sonst_umsatz)
                to_list.b_yroom =  to_decimal(to_list.b_yroom) + to_decimal(guestbud.room_nights)

                if guestbud.monat == mm:
                    to_list.flag[guestbud.monat - 1] = False
                    to_list.b_gesamt =  to_decimal(guestbud.gesamtumsatz)
                    to_list.b_logis =  to_decimal(guestbud.argtumsatz)
                    to_list.b_fb =  to_decimal(guestbud.f_b_umsatz)
                    to_list.b_sonst =  to_decimal(guestbud.sonst_umsatz)
                    to_list.b_room =  to_decimal(guestbud.room_nights)

        for to_list in query(to_list_list):

            if to_list.b_gesamt != 0:
                to_list.proz1 =  to_decimal(to_list.gesamt) / to_decimal(to_list.b_gesamt) * to_decimal("100")

            if to_list.b_ygesamt != 0:
                to_list.proz2 =  to_decimal(to_list.ygesamt) / to_decimal(to_list.b_ygesamt) * to_decimal("100")

            if to_list.b_logis != 0:
                to_list.proz3 =  to_decimal(to_list.logis) / to_decimal(to_list.b_logis) * to_decimal("100")

            if to_list.b_ylogis != 0:
                to_list.proz4 =  to_decimal(to_list.ylogis) / to_decimal(to_list.b_ylogis) * to_decimal("100")

            if to_list.b_fb != 0:
                to_list.proz5 =  to_decimal(to_list.fb) / to_decimal(to_list.b_fb) * to_decimal("100")

            if to_list.b_yfb != 0:
                to_list.proz6 =  to_decimal(to_list.yfb) / to_decimal(to_list.b_yfb) * to_decimal("100")

            if to_list.b_sonst != 0:
                to_list.proz7 =  to_decimal(to_list.sonst) / to_decimal(to_list.b_sonst) * to_decimal("100")

            if to_list.b_ysonst != 0:
                to_list.proz8 =  to_decimal(to_list.ysonst) / to_decimal(to_list.b_ysonst) * to_decimal("100")

            if to_list.b_room != 0:
                to_list.proz9 =  to_decimal(to_list.room) / to_decimal(to_list.b_room) * to_decimal("100")

            if to_list.b_yroom != 0:
                to_list.proz10 =  to_decimal(to_list.yroom) / to_decimal(to_list.b_yroom) * to_decimal("100")

        if hide_zero :

            for to_list in query(to_list_list, filters=(lambda to_list: to_list.gesamt != 0)):

                if disptype == 1:
                    glodging_turnover = Glodging_turnover()
                    glodging_turnover_list.append(glodging_turnover)

                    glodging_turnover.cust_name = to_list.name
                    glodging_turnover.t_o =  to_decimal(to_list.gesamt)
                    glodging_turnover.budget_to =  to_decimal(to_list.b_gesamt)
                    glodging_turnover.percnt_to =  to_decimal(to_list.proz1)
                    glodging_turnover.ytd =  to_decimal(to_list.ygesamt)
                    glodging_turnover.budget_ytd =  to_decimal(to_list.b_ygesamt)
                    glodging_turnover.percnt_ytd =  to_decimal(to_list.proz2)
                    glodging_turnover.lodg_to =  to_decimal(to_list.logis)
                    glodging_turnover.budget_lodg_to =  to_decimal(to_list.b_logis)
                    glodging_turnover.percnt_lodg_to =  to_decimal(to_list.proz3)
                    glodging_turnover.lodg_ytd =  to_decimal(to_list.ylogis)
                    glodging_turnover.budget_lodg_ytd =  to_decimal(to_list.b_ylogis)
                    glodging_turnover.percnt_lodg_ytd =  to_decimal(to_list.proz4)
                    glodging_turnover.rmnite =  to_decimal(to_list.room)
                    glodging_turnover.budget_rmnite =  to_decimal(to_list.b_room)
                    glodging_turnover.percnt_rmnite =  to_decimal(to_list.proz9)
                    glodging_turnover.rmnite_ytd =  to_decimal(to_list.yroom)
                    glodging_turnover.budget_rmnite_ytd =  to_decimal(to_list.b_yroom)
                    glodging_turnover.percnt_rmnite_ytd =  to_decimal(to_list.proz10)

                elif disptype == 2:
                    gfb_turnover = Gfb_turnover()
                    gfb_turnover_list.append(gfb_turnover)

                    gfb_turnover.cust_name = to_list.name
                    gfb_turnover.t_o =  to_decimal(to_list.gesamt)
                    gfb_turnover.fb_to =  to_decimal(to_list.fb)
                    gfb_turnover.budget_fb_to =  to_decimal(to_list.b_fb)
                    gfb_turnover.percnt_fb_to =  to_decimal(to_list.proz5)
                    gfb_turnover.fb_ytd =  to_decimal(to_list.yfb)
                    gfb_turnover.budget_fb_ytd =  to_decimal(to_list.b_fb)
                    gfb_turnover.percnt_fb_ytd =  to_decimal(to_list.proz6)

                elif disptype == 3:
                    gother_turnover = Gother_turnover()
                    gother_turnover_list.append(gother_turnover)

                    gother_turnover.cust_name = to_list.name
                    gother_turnover.t_o =  to_decimal(to_list.gesamt)
                    gother_turnover.other_to =  to_decimal(to_list.sonst)
                    gother_turnover.budget_other_to =  to_decimal(to_list.b_sonst)
                    gother_turnover.percnt_other_to =  to_decimal(to_list.proz7)
                    gother_turnover.other_ytd =  to_decimal(to_list.ysonst)
                    gother_turnover.budget_other_ytd =  to_decimal(to_list.b_sonst)
                    gother_turnover.percnt_other_ytd =  to_decimal(to_list.proz8)


        else:

            for to_list in query(to_list_list):

                if disptype == 1:
                    glodging_turnover = Glodging_turnover()
                    glodging_turnover_list.append(glodging_turnover)

                    glodging_turnover.cust_name = to_list.name
                    glodging_turnover.t_o =  to_decimal(to_list.gesamt)
                    glodging_turnover.budget_to =  to_decimal(to_list.b_gesamt)
                    glodging_turnover.percnt_to =  to_decimal(to_list.proz1)
                    glodging_turnover.ytd =  to_decimal(to_list.ygesamt)
                    glodging_turnover.budget_ytd =  to_decimal(to_list.b_ygesamt)
                    glodging_turnover.percnt_ytd =  to_decimal(to_list.proz2)
                    glodging_turnover.lodg_to =  to_decimal(to_list.logis)
                    glodging_turnover.budget_lodg_to =  to_decimal(to_list.b_logis)
                    glodging_turnover.percnt_lodg_to =  to_decimal(to_list.proz3)
                    glodging_turnover.lodg_ytd =  to_decimal(to_list.ylogis)
                    glodging_turnover.budget_lodg_ytd =  to_decimal(to_list.b_ylogis)
                    glodging_turnover.percnt_lodg_ytd =  to_decimal(to_list.proz4)
                    glodging_turnover.rmnite =  to_decimal(to_list.room)
                    glodging_turnover.budget_rmnite =  to_decimal(to_list.b_room)
                    glodging_turnover.percnt_rmnite =  to_decimal(to_list.proz9)
                    glodging_turnover.rmnite_ytd =  to_decimal(to_list.yroom)
                    glodging_turnover.budget_rmnite_ytd =  to_decimal(to_list.b_yroom)
                    glodging_turnover.percnt_rmnite_ytd =  to_decimal(to_list.proz10)

                elif disptype == 2:
                    gfb_turnover = Gfb_turnover()
                    gfb_turnover_list.append(gfb_turnover)

                    gfb_turnover.cust_name = to_list.name
                    gfb_turnover.t_o =  to_decimal(to_list.gesamt)
                    gfb_turnover.fb_to =  to_decimal(to_list.fb)
                    gfb_turnover.budget_fb_to =  to_decimal(to_list.b_fb)
                    gfb_turnover.percnt_fb_to =  to_decimal(to_list.proz5)
                    gfb_turnover.fb_ytd =  to_decimal(to_list.yfb)
                    gfb_turnover.budget_fb_ytd =  to_decimal(to_list.b_fb)
                    gfb_turnover.percnt_fb_ytd =  to_decimal(to_list.proz6)

                elif disptype == 3:
                    gother_turnover = Gother_turnover()
                    gother_turnover_list.append(gother_turnover)

                    gother_turnover.cust_name = to_list.name
                    gother_turnover.t_o =  to_decimal(to_list.gesamt)
                    gother_turnover.other_to =  to_decimal(to_list.sonst)
                    gother_turnover.budget_other_to =  to_decimal(to_list.b_sonst)
                    gother_turnover.percnt_other_to =  to_decimal(to_list.proz7)
                    gother_turnover.other_ytd =  to_decimal(to_list.ysonst)
                    gother_turnover.budget_other_ytd =  to_decimal(to_list.b_sonst)
                    gother_turnover.percnt_other_ytd =  to_decimal(to_list.proz8)


    create_umsatz()

    return generate_output()