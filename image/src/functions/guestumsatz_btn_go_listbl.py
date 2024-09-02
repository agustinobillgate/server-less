from functions.additional_functions import *
import decimal
from models import Guest, Guestat, Guestbud

def guestumsatz_btn_go_listbl(from_date:str, cardtype:int, hide_zero:bool, disptype:int):
    glodging_turnover_list = []
    gfb_turnover_list = []
    gother_turnover_list = []
    guest = guestat = guestbud = None

    glodging_turnover = gfb_turnover = gother_turnover = to_list = None

    glodging_turnover_list, Glodging_turnover = create_model("Glodging_turnover", {"cust_name":str, "t_o":decimal, "budget_to":decimal, "percnt_to":decimal, "ytd":decimal, "budget_ytd":decimal, "percnt_ytd":decimal, "lodg_to":decimal, "budget_lodg_to":decimal, "percnt_lodg_to":decimal, "lodg_ytd":decimal, "budget_lodg_ytd":decimal, "percnt_lodg_ytd":decimal, "rmnite":decimal, "budget_rmnite":decimal, "percnt_rmnite":decimal, "rmnite_ytd":decimal, "budget_rmnite_ytd":decimal, "percnt_rmnite_ytd":decimal})
    gfb_turnover_list, Gfb_turnover = create_model("Gfb_turnover", {"cust_name":str, "t_o":decimal, "fb_to":decimal, "budget_fb_to":decimal, "percnt_fb_to":decimal, "fb_ytd":decimal, "budget_fb_ytd":decimal, "percnt_fb_ytd":decimal})
    gother_turnover_list, Gother_turnover = create_model("Gother_turnover", {"cust_name":str, "t_o":decimal, "other_to":decimal, "budget_other_to":decimal, "percnt_other_to":decimal, "other_ytd":decimal, "budget_other_ytd":decimal, "percnt_other_ytd":decimal})
    to_list_list, To_list = create_model("To_list", {"gastnr":int, "name":str, "flag":[bool, 12], "gesamt":decimal, "b_gesamt":decimal, "proz1":decimal, "ygesamt":decimal, "b_ygesamt":decimal, "proz2":decimal, "logis":decimal, "b_logis":decimal, "proz3":decimal, "ylogis":decimal, "b_ylogis":decimal, "proz4":decimal, "fb":decimal, "b_fb":decimal, "proz5":decimal, "yfb":decimal, "b_yfb":decimal, "proz6":decimal, "sonst":decimal, "b_sonst":decimal, "proz7":decimal, "ysonst":decimal, "b_ysonst":decimal, "proz8":decimal, "room":decimal, "b_room":decimal, "proz9":decimal, "yroom":decimal, "b_yroom":decimal, "proz10":decimal})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal glodging_turnover_list, gfb_turnover_list, gother_turnover_list, guest, guestat, guestbud


        nonlocal glodging_turnover, gfb_turnover, gother_turnover, to_list
        nonlocal glodging_turnover_list, gfb_turnover_list, gother_turnover_list, to_list_list
        return {"glodging-turnover": glodging_turnover_list, "gfb-turnover": gfb_turnover_list, "gother-turnover": gother_turnover_list}

    def create_umsatz():

        nonlocal glodging_turnover_list, gfb_turnover_list, gother_turnover_list, guest, guestat, guestbud


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

        guestat_obj_list = []
        for guestat, guest in db_session.query(Guestat, Guest).join(Guest,(Guest.gastnr == Guestat.gastnr) &  (Guest.karteityp == cardtype)).filter(
                (Guestat.jahr == yy) &  (Guestat.monat <= mm) &  (Guestat.betriebsnr == 0)).all():
            if guestat._recid in guestat_obj_list:
                continue
            else:
                guestat_obj_list.append(guestat._recid)

            guestbud = db_session.query(Guestbud).filter(
                    (Guestbud.gastnr == guestat.gastnr) &  (Guestbud.monat == guestat.monat) &  (Guestbud.jahr == guestat.jahr)).first()

            to_list = query(to_list_list, filters=(lambda to_list :to_list.gastnr == guest.gastnr), first=True)

            if not to_list:
                to_list = To_list()
                to_list_list.append(to_list)

                to_list.gastnr = guest.gastnr
                to_list.name = guest.name + ", " + guest.vorname1 + " " + guest.anrede1 + guest.anredefirma
            to_list.ygesamt = to_list.ygesamt + guestat.gesamtumsatz
            to_list.ylogis = to_list.ylogis + guestat.argtumsatz
            to_list.yfb = to_list.yfb + guestat.f_b_umsatz
            to_list.ysonst = to_list.ysonst + guestat.sonst_umsatz
            to_list.yroom = to_list.yroom + guestat.room_nights

            if guestat.monat == mm:
                to_list.gesamt = to_list.gesamt + guestat.gesamtumsatz
                to_list.logis = to_list.logis + guestat.argtumsatz
                to_list.fb = to_list.fb + guestat.f_b_umsatz
                to_list.sonst = to_list.sonst + guestat.sonst_umsatz
                to_list.room = to_list.room + guestat.room_nights

            if guestbud and to_list.flag[guestbud.monat - 1]:
                to_list.flag[guestbud.monat - 1] = False
                to_list.b_ygesamt = to_list.b_ygesamt + guestbud.gesamtumsatz
                to_list.b_ylogis = to_list.b_ylogis + guestbud.argtumsatz
                to_list.b_yfb = to_list.b_yfb + guestbud.f_b_umsatz
                to_list.b_ysonst = to_list.b_ysonst + guestbud.sonst_umsatz
                to_list.b_yroom = to_list.b_yroom + guestbud.room_nights

                if guestbud.monat == mm:
                    to_list.flag[guestbud.monat - 1] = False
                    to_list.b_gesamt = guestbud.gesamtumsatz
                    to_list.b_logis = guestbud.argtumsatz
                    to_list.b_fb = guestbud.f_b_umsatz
                    to_list.b_sonst = guestbud.sonst_umsatz
                    to_list.b_room = guestbud.room_nights

        for to_list in query(to_list_list):

            if to_list.b_gesamt != 0:
                to_list.proz1 = to_list.gesamt / to_list.b_gesamt * 100

            if to_list.b_ygesamt != 0:
                to_list.proz2 = to_list.ygesamt / to_list.b_ygesamt * 100

            if to_list.b_logis != 0:
                to_list.proz3 = to_list.logis / to_list.b_logis * 100

            if to_list.b_ylogis != 0:
                to_list.proz4 = to_list.ylogis / to_list.b_ylogis * 100

            if to_list.b_fb != 0:
                to_list.proz5 = to_list.fb / to_list.b_fb * 100

            if to_list.b_yfb != 0:
                to_list.proz6 = to_list.yfb / to_list.b_yfb * 100

            if to_list.b_sonst != 0:
                to_list.proz7 = to_list.sonst / to_list.b_sonst * 100

            if to_list.b_ysonst != 0:
                to_list.proz8 = to_list.ysonst / to_list.b_ysonst * 100

            if to_list.b_room != 0:
                to_list.proz9 = to_list.room / to_list.b_room * 100

            if to_list.b_yroom != 0:
                to_list.proz10 = to_list.yroom / to_list.b_yroom * 100

        if hide_zero :

            for to_list in query(to_list_list, filters=(lambda to_list :to_list.gesamt != 0)):

                if disptype == 1:
                    glodging_turnover = Glodging_turnover()
                    glodging_turnover_list.append(glodging_turnover)

                    glodging_turnover.cust_name = to_list.name
                    glodging_turnover.t_o = to_list.gesamt
                    glodging_turnover.budget_to = to_list.b_gesamt
                    glodging_turnover.percnt_to = to_list.proz1
                    glodging_turnover.ytd = to_list.ygesamt
                    glodging_turnover.budget_ytd = to_list.b_ygesamt
                    glodging_turnover.percnt_ytd = to_list.proz2
                    glodging_turnover.lodg_to = to_list.logis
                    glodging_turnover.budget_lodg_to = to_list.b_logis
                    glodging_turnover.percnt_lodg_to = to_list.proz3
                    glodging_turnover.lodg_ytd = to_list.ylogis
                    glodging_turnover.budget_lodg_ytd = to_list.b_ylogis
                    glodging_turnover.percnt_lodg_ytd = to_list.proz4
                    glodging_turnover.rmnite = to_list.room
                    glodging_turnover.budget_rmnite = to_list.b_room
                    glodging_turnover.percnt_rmnite = to_list.proz9
                    glodging_turnover.rmnite_ytd = to_list.yroom
                    glodging_turnover.budget_rmnite_ytd = to_list.b_yroom
                    glodging_turnover.percnt_rmnite_ytd = to_list.proz10

                elif disptype == 2:
                    gfb_turnover = Gfb_turnover()
                    gfb_turnover_list.append(gfb_turnover)

                    gfb_turnover.cust_name = to_list.name
                    gfb_turnover.t_o = to_list.gesamt
                    gfb_turnover.fb_to = to_list.fb
                    gfb_turnover.budget_fb_to = to_list.b_fb
                    gfb_turnover.percnt_fb_to = to_list.proz5
                    gfb_turnover.fb_ytd = to_list.yfb
                    gfb_turnover.budget_fb_ytd = to_list.b_fb
                    gfb_turnover.percnt_fb_ytd = to_list.proz6

                elif disptype == 3:
                    gother_turnover = Gother_turnover()
                    gother_turnover_list.append(gother_turnover)

                    gother_turnover.cust_name = to_list.name
                    gother_turnover.t_o = to_list.gesamt
                    gother_turnover.other_to = to_list.sonst
                    gother_turnover.budget_other_to = to_list.b_sonst
                    gother_turnover.percnt_other_to = to_list.proz7
                    gother_turnover.other_ytd = to_list.ysonst
                    gother_turnover.budget_other_ytd = to_list.b_sonst
                    gother_turnover.percnt_other_ytd = to_list.proz8


        else:

            for to_list in query(to_list_list):

                if disptype == 1:
                    glodging_turnover = Glodging_turnover()
                    glodging_turnover_list.append(glodging_turnover)

                    glodging_turnover.cust_name = to_list.name
                    glodging_turnover.t_o = to_list.gesamt
                    glodging_turnover.budget_to = to_list.b_gesamt
                    glodging_turnover.percnt_to = to_list.proz1
                    glodging_turnover.ytd = to_list.ygesamt
                    glodging_turnover.budget_ytd = to_list.b_ygesamt
                    glodging_turnover.percnt_ytd = to_list.proz2
                    glodging_turnover.lodg_to = to_list.logis
                    glodging_turnover.budget_lodg_to = to_list.b_logis
                    glodging_turnover.percnt_lodg_to = to_list.proz3
                    glodging_turnover.lodg_ytd = to_list.ylogis
                    glodging_turnover.budget_lodg_ytd = to_list.b_ylogis
                    glodging_turnover.percnt_lodg_ytd = to_list.proz4
                    glodging_turnover.rmnite = to_list.room
                    glodging_turnover.budget_rmnite = to_list.b_room
                    glodging_turnover.percnt_rmnite = to_list.proz9
                    glodging_turnover.rmnite_ytd = to_list.yroom
                    glodging_turnover.budget_rmnite_ytd = to_list.b_yroom
                    glodging_turnover.percnt_rmnite_ytd = to_list.proz10

                elif disptype == 2:
                    gfb_turnover = Gfb_turnover()
                    gfb_turnover_list.append(gfb_turnover)

                    gfb_turnover.cust_name = to_list.name
                    gfb_turnover.t_o = to_list.gesamt
                    gfb_turnover.fb_to = to_list.fb
                    gfb_turnover.budget_fb_to = to_list.b_fb
                    gfb_turnover.percnt_fb_to = to_list.proz5
                    gfb_turnover.fb_ytd = to_list.yfb
                    gfb_turnover.budget_fb_ytd = to_list.b_fb
                    gfb_turnover.percnt_fb_ytd = to_list.proz6

                elif disptype == 3:
                    gother_turnover = Gother_turnover()
                    gother_turnover_list.append(gother_turnover)

                    gother_turnover.cust_name = to_list.name
                    gother_turnover.t_o = to_list.gesamt
                    gother_turnover.other_to = to_list.sonst
                    gother_turnover.budget_other_to = to_list.b_sonst
                    gother_turnover.percnt_other_to = to_list.proz7
                    gother_turnover.other_ytd = to_list.ysonst
                    gother_turnover.budget_other_ytd = to_list.b_sonst
                    gother_turnover.percnt_other_ytd = to_list.proz8

    create_umsatz()

    return generate_output()