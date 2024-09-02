from functions.additional_functions import *
import decimal
from datetime import date
from models import Bediener, Htparam, Waehrung, Guestat1, Exrate, Guest

def rm_atproduct_create_umsatz1_webbl(ci_date:date, tdate:date, to_date:date, show_ftd:, curr_id_screenvalue:str, currency_type:int, cardtype:int, fdate:date):
    rm_atproduct_list = []
    sales_list_list = []
    bediener = htparam = waehrung = guestat1 = exrate = guest = None

    rm_atproduct = sales_list = to_list = bediener1 = None

    rm_atproduct_list, Rm_atproduct = create_model("Rm_atproduct", {"name":str, "room":str, "pax":str, "lodg":str, "proz":str, "rm_rate":str, "mtd_room":str, "mtd_pax":str, "mtd_lodg":str, "mtdproz":str, "mtd_rm_rate":str, "ytd_room":str, "ytd_pax":str, "ytd_lodg":str, "ytd_proz":str, "ytd_rm_rate":str})
    sales_list_list, Sales_list = create_model("Sales_list", {"sales_id":str, "sales_name":str})
    to_list_list, To_list = create_model("To_list", {"sales_id":str, "gastnr":int, "name":str, "room":int, "croom":int, "pax":int, "logis":decimal, "proz":decimal, "avrgrate":decimal, "m_room":int, "mc_room":int, "m_pax":int, "m_logis":decimal, "m_proz":decimal, "m_avrgrate":decimal, "y_room":int, "yc_room":int, "y_pax":int, "y_logis":decimal, "y_proz":decimal, "y_avrgrate":decimal})

    Bediener1 = Bediener

    db_session = local_storage.db_session

    def generate_output():
        nonlocal rm_atproduct_list, sales_list_list, bediener, htparam, waehrung, guestat1, exrate, guest
        nonlocal bediener1


        nonlocal rm_atproduct, sales_list, to_list, bediener1
        nonlocal rm_atproduct_list, sales_list_list, to_list_list
        return {"rm-atproduct": rm_atproduct_list, "sales-list": sales_list_list}

    def create_umsatz1():

        nonlocal rm_atproduct_list, sales_list_list, bediener, htparam, waehrung, guestat1, exrate, guest
        nonlocal bediener1


        nonlocal rm_atproduct, sales_list, to_list, bediener1
        nonlocal rm_atproduct_list, sales_list_list, to_list_list

        from_date:date = None
        datum:date = None
        curr_date:date = None
        date1:date = None
        date2:date = None
        sales_id:str = ""
        curr_sales:str = ""
        sales_name:str = ""
        mm:int = 0
        yy:int = 0
        s_pax:int = 0
        s_mpax:int = 0
        s_ypax:int = 0
        s_room:int = 0
        s_mroom:int = 0
        s_yroom:int = 0
        s_lodge:decimal = 0
        s_mlodge:decimal = 0
        s_ylodge:decimal = 0
        s_rate:decimal = 0
        s_mrate:decimal = 0
        s_yrate:decimal = 0
        do_it:bool = False
        room:int = 0
        croom:int = 0
        pax:int = 0
        logis:decimal = 0
        avrgrate:decimal = 0
        m_room:int = 0
        mc_room:int = 0
        m_pax:int = 0
        m_logis:decimal = 0
        m_avrgrate:decimal = 0
        y_room:int = 0
        yc_room:int = 0
        y_pax:int = 0
        y_logis:decimal = 0
        y_avrgrate:decimal = 0
        exchg_rate:decimal = 1
        ind:int = 0
        price_decimal:int = 0
        foreign_nr:int = 0
        Bediener1 = Bediener

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 491)).first()
        price_decimal = htparam.finteger

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 144)).first()

        if htparam.fchar != "":

            waehrung = db_session.query(Waehrung).filter(
                    (Waehrung.wabkurz == htparam.fchar)).first()

            if waehrung:
                foreign_nr = waehrungsnr
        room = 0
        croom = 0
        pax = 0
        logis = 0
        m_room = 0
        mc_room = 0
        m_pax = 0
        m_logis = 0
        y_room = 0
        yc_room = 0
        y_pax = 0
        y_logis = 0
        mm = get_month(to_date)
        yy = get_year(to_date)
        from_date = date_mdy(1, 1, yy)
        curr_date = None

        if show_ftd:
            to_date = tdate


        rm_atproduct_list.clear()
        to_list_list.clear()
        sales_id = ""

        if curr_id_screenvalue != None:
            sales_id = trim(entry(0, curr_id_screenvalue, "-"))

        if from_date < ci_date:
            date1 = from_date

            if to_date < ci_date:
                date2 = to_date
            else:
                date2 = ci_date - 1

            for guestat1 in db_session.query(Guestat1).filter(
                    (Guestat1.datum >= date1) &  (Guestat1.datum <= date2) &  (Guestat1.logis > 0)).all():
                exchg_rate = 1

                if curr_date != guestat1.datum and currency_type == 2:

                    if foreign_nr != 0:

                        exrate = db_session.query(Exrate).filter(
                                (Exrate.artnr == foreign_nr) &  (Exrate.datum == datum)).first()

                        if exrate:
                            exchg_rate = exrate.betrag

                guest = db_session.query(Guest).filter(
                        (Guest.gastnr == guestat1.gastnr)).first()

                if cardtype == 3:
                    do_it = True
                else:
                    do_it = (guest.karteityp == cardtype)

                if do_it and sales_id != "":
                    do_it = sales_id == guest.phonetik3

                if do_it:

                    to_list = query(to_list_list, filters=(lambda to_list :to_list.gastnr == guest.gastnr and to_list.sales_id == guest.phonetik3), first=True)

                    if not to_list:
                        to_list = To_list()
                        to_list_list.append(to_list)

                        to_list.sales_id = guest.phonetik3
                        to_list.gastnr = guest.gastnr
                        to_list.name = guest.name + ", " + guest.vorname1 + " " +\
                                guest.anrede1 + guest.anredefirma

                    if guestat1.datum == to_date:
                        to_list.room = to_list.room + guestat1.zimmeranz
                        to_list.croom = to_list.croom + guestat1.betriebsnr
                        to_list.pax = to_list.pax + guestat1.persanz
                        to_list.logis = to_list.logis + guestat1.logis / exchg_rate
                        room = room + guestat1.zimmeranz
                        croom = croom + guestat1.betriebsnr
                        pax = pax + guestat1.persanz
                        logis = logis + guestat1.logis / exchg_rate

                    if (not show_ftd and get_month(guestat1.datum) == mm and get_year(guestat1.datum) == yy) or (show_ftd and guestat1.datum >= fdate and guestat1.datum <= to_date):
                        to_list.m_room = to_list.m_room + guestat1.zimmeranz
                        to_list.mc_room = to_list.mc_room + guestat1.betriebsnr
                        to_list.m_pax = to_list.m_pax + guestat1.persanz
                        to_list.m_logis = to_list.m_logis + guestat1.logis / exchg_rate
                        m_room = m_room + guestat1.zimmeranz
                        mc_room = mc_room + guestat1.betriebsnr
                        m_pax = m_pax + guestat1.persanz
                        m_logis = m_logis + guestat1.logis / exchg_rate


                    to_list.y_room = to_list.y_room + guestat1.zimmeranz
                    to_list.yc_room = to_list.yc_room + guestat1.betriebsnr
                    to_list.y_pax = to_list.y_pax + guestat1.persanz
                    to_list.y_logis = to_list.y_logis + guestat1.logis / exchg_rate
                    y_room = y_room + guestat1.zimmeranz
                    yc_room = yc_room + guestat1.betriebsnr
                    y_pax = y_pax + guestat1.persanz
                    y_logis = y_logis + guestat1.logis / exchg_rate

        if to_date >= ci_date:

            if from_date >= ci_date:
                date1 = from_date
            else:
                date1 = ci_date
            date2 = to_date

        for to_list in query(to_list_list):

            if to_list.y_logis == 0 and to_list.y_room == 0:
                to_list_list.remove(to_list)
            else:

                if (to_list.room - to_list.croom) != 0:
                    to_list.avrgrate = to_list.logis / (to_list.room - to_list.croom)

                if (to_list.m_room - to_list.mc_room) != 0:
                    to_list.m_avrgrate = to_list.m_logis / (to_list.m_room - to_list.mc_room)

                if (to_list.y_room - to_list.yc_room) != 0:
                    to_list.y_avrgrate = to_list.y_logis / (to_list.y_room - to_list.yc_room)

                if logis != 0:
                    to_list.proz = to_list.logis / logis * 100

                if m_logis != 0:
                    to_list.m_proz = to_list.m_logis / m_logis * 100

                if y_logis != 0:
                    to_list.y_proz = to_list.y_logis / y_logis * 100
        curr_sales = "UNKNOWN"

        for to_list in query(to_list_list):

            sales_list = query(sales_list_list, filters=(lambda sales_list :sales_list.sales_id == to_list.sales_id), first=True)

            if not sales_list:

                bediener1 = db_session.query(Bediener1).filter(
                        (Bediener1.userinit == to_list.sales_id)).first()
                sales_list = Sales_list()
                sales_list_list.append(sales_list)

                sales_list.sales_id = to_list.sales_id

                if bediener1:
                    sales_list.sales_name = bediener1.username

            if sales_id == "" or (entry(0, curr_id_screenvalue, "-") == to_list.sales_id):

                if curr_sales.lower()  == "UNKNOWN":
                    s_pax = 0
                    s_mpax = 0
                    s_ypax = 0
                    s_room = 0
                    s_mroom = 0
                    s_yroom = 0
                    s_lodge = 0
                    s_mlodge = 0
                    s_ylodge = 0
                    s_rate = 0
                    s_mrate = 0
                    s_yrate = 0
                    curr_sales = to_list.sales_id

                    bediener1 = db_session.query(Bediener1).filter(
                            (Bediener1.userinit == to_list.sales_id)).first()
                    sales_name = to_string(curr_sales, "x(2)") + " - "

                    if bediener1:
                        sales_name = sales_name + bediener1.username
                    else:
                        sales_name = sales_name + "Undefined"
                    rm_atproduct = Rm_atproduct()
                    rm_atproduct_list.append(rm_atproduct)

                    rm_atproduct.name = to_string(sales_name, "x(24)")

                if curr_sales != to_list.sales_id:

                    if s_room != 0:
                        s_rate = s_lodge / s_room

                    if s_mroom != 0:
                        s_mrate = s_mlodge / s_mroom

                    if s_yroom != 0:
                        s_yrate = s_ylodge / s_yroom
                    rm_atproduct = Rm_atproduct()
                    rm_atproduct_list.append(rm_atproduct)


                    if price_decimal == 0 and currency_type == 1:
                        rm_atproduct.name = to_string(("Total Sales - " + curr_sales) , "x(24)")
                        rm_atproduct.room = to_string(s_room, ">>9")
                        rm_atproduct.pax = to_string(s_pax, ">>9")
                        rm_atproduct.lodg = to_string(s_lodge, ">>,>>>,>>>,>>9")
                        rm_atproduct.proz = to_string(0, ">>>>>>")
                        rm_atproduct.rm_rate = to_string(s_rate, ">>,>>>,>>>,>>9")
                        rm_atproduct.mtd_Room = to_string(s_mroom, ">>,>>9")
                        rm_atproduct.mtd_pax = to_string(s_mpax, ">>,>>9")
                        rm_atproduct.mtd_lodg = to_string(s_mlodge, ">>,>>>,>>>,>>9")
                        rm_atproduct.mtdproz = to_string(0, ">>>>>>")
                        rm_atproduct.mtd_rm_rate = to_string(s_mrate, ">>,>>>,>>>,>>9")
                        rm_atproduct.ytd_Room = to_string(s_yroom, ">>>,>>9")
                        rm_atproduct.ytd_pax = to_string(s_ypax, ">>>,>>9")
                        rm_atproduct.ytd_lodg = to_string(s_ylodge, ">>,>>>,>>>,>>9")
                        rm_atproduct.ytd_proz = to_string(0, ">>>>>>")
                        rm_atproduct.ytd_rm_rate = to_string(s_yrate, ">>,>>>,>>>,>>9")


                    else:
                        rm_atproduct.name = to_string(("Total Sales - " + curr_sales) , "x(24)")
                        rm_atproduct.room = to_string(s_room, ">>9")
                        rm_atproduct.pax = to_string(s_pax, ">>9")
                        rm_atproduct.lodg = to_string(s_lodge, ">>>,>>>,>>9.99")
                        rm_atproduct.proz = to_string(0, ">>>>>>")
                        rm_atproduct.rm_rate = to_string(s_rate, ">>>,>>>,>>9.99")
                        rm_atproduct.mtd_Room = to_string(s_mroom, ">>,>>9")
                        rm_atproduct.mtd_pax = to_string(s_mpax, ">>,>>9")
                        rm_atproduct.mtd_lodg = to_string(s_mlodge, ">,>>>,>>>,>>9.99")
                        rm_atproduct.mtdproz = to_string(0, ">>>>>>")
                        rm_atproduct.mtd_rm_rate = to_string(s_mrate, ">>>,>>>,>>9.99")
                        rm_atproduct.ytd_Room = to_string(s_yroom, ">>>,>>9")
                        rm_atproduct.ytd_pax = to_string(s_ypax, ">>>,>>9")
                        rm_atproduct.ytd_lodg = to_string(s_ylodge, ">>>,>>>,>>9.99")
                        rm_atproduct.ytd_proz = to_string(0, ">>>>>>")
                        rm_atproduct.ytd_rm_rate = to_string(s_yrate, ">>>,>>>,>>9.99")


                    rm_atproduct = Rm_atproduct()
                    rm_atproduct_list.append(rm_atproduct)

                    curr_sales = to_list.sales_id

                    bediener1 = db_session.query(Bediener1).filter(
                            (Bediener1.userinit == to_list.sales_id)).first()
                    sales_name = to_string(curr_sales, "x(2)") + " - "

                    if bediener1:
                        sales_name = sales_name + bediener1.username
                    else:
                        sales_name = sales_name + "Undefined"
                    rm_atproduct = Rm_atproduct()
                    rm_atproduct_list.append(rm_atproduct)

                    rm_atproduct.name = to_string(sales_name, "x(24)")
                    s_pax = 0
                    s_mpax = 0
                    s_ypax = 0
                    s_room = 0
                    s_mroom = 0
                    s_yroom = 0
                    s_lodge = 0
                    s_mlodge = 0
                    s_ylodge = 0
                    s_rate = 0
                    s_mrate = 0
                    s_yrate = 0
                s_pax = s_pax + to_list.pax
                s_mpax = s_mpax + to_list.m_pax
                s_ypax = s_ypax + to_list.y_pax
                s_room = s_room + to_list.room
                s_mroom = s_mroom + to_list.m_room
                s_yroom = s_yroom + to_list.y_room
                s_lodge = s_lodge + to_list.logis
                s_mlodge = s_mlodge + to_list.m_logis
                s_ylodge = s_ylodge + to_list.y_logis
                rm_atproduct = Rm_atproduct()
                rm_atproduct_list.append(rm_atproduct)


                if price_decimal == 0 and currency_type == 1:
                    rm_atproduct.name = to_string(to_list.name, "x(24)")
                    rm_atproduct.room = to_string(to_list.room, ">>9")
                    rm_atproduct.pax = to_string(to_list.pax, ">>9")
                    rm_atproduct.lodg = to_string(to_list.logis, ">>,>>>,>>>,>>9")
                    rm_atproduct.proz = to_string(to_list.proz, ">>9.99")
                    rm_atproduct.rm_rate = to_string(to_list.avrgrate, ">>,>>>,>>>,>>9")
                    rm_atproduct.mtd_Room = to_string(to_list.m_room, ">>,>>9")
                    rm_atproduct.mtd_pax = to_string(to_list.m_pax, ">>,>>9")
                    rm_atproduct.mtd_lodg = to_string(to_list.m_logis, ">>,>>>,>>>,>>9")
                    rm_atproduct.mtdproz = to_string(to_list.m_proz, ">>9.99")
                    rm_atproduct.mtd_rm_rate = to_string(to_list.m_avrgrate, ">>,>>>,>>>,>>9")
                    rm_atproduct.ytd_Room = to_string(to_list.y_room, ">>>,>>9")
                    rm_atproduct.ytd_pax = to_string(to_list.y_pax, ">>>,>>9")
                    rm_atproduct.ytd_lodg = to_string(to_list.y_logis, ">>,>>>,>>>,>>9")
                    rm_atproduct.ytd_proz = to_string(to_list.y_proz, ">>9.99")
                    rm_atproduct.ytd_rm_rate = to_string(to_list.y_avrgrate, ">>,>>>,>>>,>>9")


                else:
                    rm_atproduct.name = to_string(to_list.name, "x(24)")
                    rm_atproduct.room = to_string(to_list.room, ">>9")
                    rm_atproduct.pax = to_string(to_list.pax, ">>9")
                    rm_atproduct.lodg = to_string(to_list.logis, ">>>,>>>,>>9.99")
                    rm_atproduct.proz = to_string(to_list.proz, ">>9.99")
                    rm_atproduct.rm_rate = to_string(to_list.avrgrate, ">>>,>>>,>>9.99")
                    rm_atproduct.mtd_Room = to_string(to_list.m_room, ">>,>>9")
                    rm_atproduct.mtd_pax = to_string(to_list.m_pax, ">>,>>9")
                    rm_atproduct.mtd_lodg = to_string(to_list.m_logis, ">,>>>,>>>,>>9.99")
                    rm_atproduct.mtdproz = to_string(to_list.m_proz, ">>9.99")
                    rm_atproduct.mtd_rm_rate = to_string(to_list.m_avrgrate, ">>>,>>>,>>9.99")
                    rm_atproduct.ytd_Room = to_string(to_list.y_room, ">>>,>>9")
                    rm_atproduct.ytd_pax = to_string(to_list.y_pax, ">>>,>>9")
                    rm_atproduct.ytd_lodg = to_string(to_list.y_logis, ">>>,>>>,>>9.99")
                    rm_atproduct.ytd_proz = to_string(to_list.y_proz, ">>9.99")
                    rm_atproduct.ytd_rm_rate = to_string(to_list.y_avrgrate, ">>>,>>>,>>9.99")

        if s_room != 0:
            s_rate = s_lodge / s_room

        if s_mroom != 0:
            s_mrate = s_mlodge / s_mroom

        if s_yroom != 0:
            s_yrate = s_ylodge / s_yroom
        rm_atproduct = Rm_atproduct()
        rm_atproduct_list.append(rm_atproduct)


        if price_decimal == 0 and currency_type == 1:
            rm_atproduct.name = to_string(("Total Sales - " + curr_sales) , "x(24)")
            rm_atproduct.room = to_string(s_room, ">>9")
            rm_atproduct.pax = to_string(s_pax, ">>9")
            rm_atproduct.lodg = to_string(s_lodge, ">>,>>>,>>>,>>9")
            rm_atproduct.proz = to_string(0, ">>>>>>")
            rm_atproduct.rm_rate = to_string(s_rate, ">>,>>>,>>>,>>9")
            rm_atproduct.mtd_Room = to_string(s_mroom, ">>,>>9")
            rm_atproduct.mtd_pax = to_string(s_mpax, ">>,>>9")
            rm_atproduct.mtd_lodg = to_string(s_mlodge, ">>,>>>,>>>,>>9")
            rm_atproduct.mtdproz = to_string(0, ">>>>>>")
            rm_atproduct.mtd_rm_rate = to_string(s_mrate, ">>,>>>,>>>,>>9")
            rm_atproduct.ytd_Room = to_string(s_yroom, ">>>,>>9")
            rm_atproduct.ytd_pax = to_string(s_ypax, ">>>,>>9")
            rm_atproduct.ytd_lodg = to_string(s_ylodge, ">>,>>>,>>>,>>9")
            rm_atproduct.ytd_proz = to_string(0, ">>>>>>")
            rm_atproduct.ytd_rm_rate = to_string(s_yrate, ">>,>>>,>>>,>>9")


        else:
            rm_atproduct.name = to_string(("Total Sales - " + curr_sales) , "x(24)")
            rm_atproduct.room = to_string(s_room, ">>9")
            rm_atproduct.pax = to_string(s_pax, ">>9")
            rm_atproduct.lodg = to_string(s_lodge, ">>>,>>>,>>9.99")
            rm_atproduct.proz = to_string(0, ">>>>>>")
            rm_atproduct.rm_rate = to_string(s_rate, ">>>,>>>,>>9.99")
            rm_atproduct.mtd_Room = to_string(s_mroom, ">>,>>9")
            rm_atproduct.mtd_pax = to_string(s_mpax, ">>,>>9")
            rm_atproduct.mtd_lodg = to_string(s_mlodge, ">,>>>,>>>,>>9.99")
            rm_atproduct.mtdproz = to_string(0, ">>>>>>")
            rm_atproduct.mtd_rm_rate = to_string(s_mrate, ">>>,>>>,>>9.99")
            rm_atproduct.ytd_Room = to_string(s_yroom, ">>>,>>9")
            rm_atproduct.ytd_pax = to_string(s_ypax, ">>>,>>9")
            rm_atproduct.ytd_lodg = to_string(s_ylodge, ">>>,>>>,>>9.99")
            rm_atproduct.ytd_proz = to_string(0, ">>>>>>")
            rm_atproduct.ytd_rm_rate = to_string(s_yrate, ">>>,>>>,>>9.99")


        avrgrate = 0

        if (room - croom) != 0:
            avrgrate = logis / (room - croom)
        m_avrgrate = 0

        if (m_room - mc_room) != 0:
            m_avrgrate = m_logis / (m_room - mc_room)
        y_avrgrate = 0

        if (y_room - yc_room) != 0:
            y_avrgrate = y_logis / (y_room - yc_room)
        rm_atproduct = Rm_atproduct()
        rm_atproduct_list.append(rm_atproduct)

        rm_atproduct = Rm_atproduct()
        rm_atproduct_list.append(rm_atproduct)


        if price_decimal == 0 and currency_type == 1:
            rm_atproduct.name = to_string("Grand Total Sales", "x(24)")
            rm_atproduct.room = to_string(room, ">>9")
            rm_atproduct.pax = to_string(pax, ">>9")
            rm_atproduct.lodg = to_string(logis, ">>,>>>,>>>,>>9")
            rm_atproduct.proz = to_string(100, ">>9.99")
            rm_atproduct.rm_rate = to_string(avrgrate, ">>,>>>,>>>,>>9")
            rm_atproduct.mtd_Room = to_string(m_room, ">>,>>9")
            rm_atproduct.mtd_pax = to_string(m_pax, ">>,>>9")
            rm_atproduct.mtd_lodg = to_string(m_logis, ">>,>>>,>>>,>>9")
            rm_atproduct.mtdproz = to_string(100, ">>9.99")
            rm_atproduct.mtd_rm_rate = to_string(m_avrgrate, ">>,>>>,>>>,>>9")
            rm_atproduct.ytd_Room = to_string(y_room, ">>>,>>9")
            rm_atproduct.ytd_pax = to_string(y_pax, ">>>,>>9")
            rm_atproduct.ytd_lodg = to_string(y_logis, ">>,>>>,>>>,>>9")
            rm_atproduct.ytd_proz = to_string(100, ">>9.99")
            rm_atproduct.ytd_rm_rate = to_string(y_avrgrate, ">>,>>>,>>>,>>9")


        else:
            rm_atproduct.name = to_string("T o t a l", "x(24)")
            rm_atproduct.room = to_string(room, ">>9")
            rm_atproduct.pax = to_string(pax, ">>9")
            rm_atproduct.lodg = to_string(logis, ">>>,>>>,>>9.99")
            rm_atproduct.proz = to_string(100, ">>9.99")
            rm_atproduct.rm_rate = to_string(avrgrate, ">>>,>>>,>>9.99")
            rm_atproduct.mtd_Room = to_string(m_room, ">>,>>9")
            rm_atproduct.mtd_pax = to_string(m_pax, ">>,>>9")
            rm_atproduct.mtd_lodg = to_string(m_logis, ">,>>>,>>>,>>9.99")
            rm_atproduct.mtdproz = to_string(100, ">>9.99")
            rm_atproduct.mtd_rm_rate = to_string(m_avrgrate, ">>>,>>>,>>9.99")
            rm_atproduct.ytd_Room = to_string(y_room, ">>>,>>9")
            rm_atproduct.ytd_pax = to_string(y_pax, ">>>,>>9")
            rm_atproduct.ytd_lodg = to_string(y_logis, ">>>,>>>,>>9.99")
            rm_atproduct.ytd_proz = to_string(100, ">>9.99")
            rm_atproduct.ytd_rm_rate = to_string(y_avrgrate, ">>>,>>>,>>9.99")


    create_umsatz1()

    return generate_output()