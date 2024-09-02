from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zinrstat, Akt_code

def comp_statisticbl(pvilanguage:int, from_date:date, to_date:date, all_occ:bool, check_ftd:bool):
    tocc_rm:decimal = 0
    tocc_rm1:decimal = 0
    tocc_rm2:decimal = 0
    tsale:decimal = 0
    tsale1:decimal = 0
    tsale2:decimal = 0
    tocc_proz:decimal = 0
    tocc_proz1:decimal = 0
    tocc_proz2:decimal = 0
    hotel1:decimal = 0
    hotel2:decimal = 0
    hotel3:decimal = 0
    hotela:decimal = 0
    hotelb:decimal = 0
    hotelc:decimal = 0
    output_list_list = []
    trmrev:decimal = 0
    trmrev1:decimal = 0
    trmrev2:decimal = 0
    f_date:date = None
    t_date:date = None
    lvcarea:str = "comp_statistic"
    zinrstat = akt_code = None

    cl_list = output_list = None

    cl_list_list, Cl_list = create_model("Cl_list", {"hno":int, "htlname":str, "occ_rm":decimal, "saleable":decimal, "rmrev":decimal, "avrgrate":decimal, "yield_":decimal, "nat_mark":decimal, "mark_share":decimal, "occ_rm1":decimal, "saleable1":decimal, "rmrev1":decimal, "avrgrate1":decimal, "yield1":decimal, "nat_mark1":decimal, "mark_share1":decimal, "occ_rm2":decimal, "saleable2":decimal, "rmrev2":decimal, "avrgrate2":decimal, "yield2":decimal, "nat_mark2":decimal, "mark_share2":decimal, "hotel1":decimal, "hotel2":decimal, "hotel3":decimal, "occ_proz":decimal, "occ_proz1":decimal, "occ_proz2":decimal})
    output_list_list, Output_list = create_model("Output_list", {"hno":int, "htlname":str, "occ_rm":str, "saleable":str, "rmrev":str, "avrgrate":str, "nat_mark":str, "mark_share":str, "yield_":str, "occ_rm1":str, "saleable1":str, "rmrev1":str, "avrgrate1":str, "nat_mark1":str, "mark_share1":str, "yield1":str, "occ_rm2":str, "saleable2":str, "rmrev2":str, "avrgrate2":str, "nat_mark2":str, "mark_share2":str, "yield2":str, "hotel1":str, "hotel2":str, "hotel3":str, "occ_proz":str, "occ_proz1":str, "occ_proz2":str})


    db_session = local_storage.db_session

    def generate_output():
        nonlocal tocc_rm, tocc_rm1, tocc_rm2, tsale, tsale1, tsale2, tocc_proz, tocc_proz1, tocc_proz2, hotel1, hotel2, hotel3, hotela, hotelb, hotelc, output_list_list, trmrev, trmrev1, trmrev2, f_date, t_date, lvcarea, zinrstat, akt_code


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list
        return {"output-list": output_list_list}

    def to_date():

        nonlocal tocc_rm, tocc_rm1, tocc_rm2, tsale, tsale1, tsale2, tocc_proz, tocc_proz1, tocc_proz2, hotel1, hotel2, hotel3, hotela, hotelb, hotelc, output_list_list, trmrev, trmrev1, trmrev2, f_date, t_date, lvcarea, zinrstat, akt_code


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list


        cl_list_list.clear()
        output_list_list.clear()
        tocc_rm = 0
        tocc_rm1 = 0
        tocc_rm2 = 0
        tsale = 0
        tsale1 = 0
        tsale2 = 0
        trmrev = 0
        trmrev1 = 0
        trmrev2 = 0
        tocc_proz = 0
        tocc_proz1 = 0
        tocc_proz2 = 0

        for zinrstat in db_session.query(Zinrstat).filter(
                (Zinrstat.datum >= from_date) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == "Competitor")).all():

            akt_code = db_session.query(Akt_code).filter(
                    (Akt_code.aktiongrup == 4) &  (Akt_code.aktionscode == zinrstat.betriebsnr)).first()

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.hno == zinrstat.betriebsnr), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.hno = zinrstat.betriebsnr

                if akt_code:
                    cl_list.htlname = akt_code.bezeich

            if zinrstat.datum == to_date:
                cl_list.occ_rm = cl_list.occ_rm + zinrstat.personen
                cl_list.saleable = cl_list.saleable + zinrstat.zimmeranz
                cl_list.rmrev = cl_list.rmrev + zinrstat.logisumsatz
                cl_list.hotel1 = (cl_list.occ_rm / cl_list.saleable) * 100

                if all_occ:
                    cl_list.occ_rm = cl_list.occ_rm + to_int(zinrstat.argtumsatz)

                if cl_list.saleable != 0:
                    cl_list.occ_proz = cl_list.occ_rm / cl_list.saleable * 100

            if get_month(zinrstat.datum) == get_month(to_date) and get_year(zinrstat.datum) == get_year(to_date):
                cl_list.occ_rm1 = cl_list.occ_rm1 + zinrstat.personen
                cl_list.saleable1 = cl_list.saleable1 + zinrstat.zimmeranz
                cl_list.rmrev1 = cl_list.rmrev1 + zinrstat.logisumsatz
                cl_list.hotel2 = (cl_list.occ_rm1 / cl_list.saleable1) * 100

                if all_occ:
                    cl_list.occ_rm1 = cl_list.occ_rm1 + to_int(zinrstat.argtumsatz)

                if cl_list.saleable1 != 0:
                    cl_list.occ_proz1 = cl_list.occ_rm1 / cl_list.saleable1 * 100
            cl_list.occ_rm2 = cl_list.occ_rm2 + zinrstat.personen
            cl_list.saleable2 = cl_list.saleable2 + zinrstat.zimmeranz
            cl_list.rmrev2 = cl_list.rmrev2 + zinrstat.logisumsatz


            cl_list.hotel3 = (cl_list.occ_rm2 / cl_list.saleable2) * 100

            if all_occ:
                cl_list.occ_rm2 = cl_list.occ_rm2 + to_int(zinrstat.argtumsatz)

            if cl_list.saleable2 != 0:
                cl_list.occ_proz2 = cl_list.occ_rm2 / cl_list.saleable2 * 100

        for cl_list in query(cl_list_list):
            tocc_rm = tocc_rm + cl_list.occ_rm
            tocc_rm1 = tocc_rm1 + cl_list.occ_rm1
            tocc_rm2 = tocc_rm2 + cl_list.occ_rm2
            tsale = tsale + cl_list.saleable
            tsale1 = tsale1 + cl_list.saleable1
            tsale2 = tsale2 + cl_list.saleable2
            trmrev1 = trmrev1 + cl_list.rmrev1
            trmrev2 = trmrev2 + cl_list.rmrev2
            trmrev = trmrev + cl_list.rmrev
            hotel1 = hotel1 + cl_list.hotel1
            hotel2 = hotel2 + cl_list.hotel2
            hotel3 = hotel3 + cl_list.hotel3
            tocc_proz = tocc_proz + cl_list.occ_proz
            tocc_proz1 = tocc_proz1 + cl_list.occ_proz1
            tocc_proz2 = tocc_proz2 + cl_list.occ_proz2

        for cl_list in query(cl_list_list):

            if cl_list.occ_rm != 0:
                cl_list.avrgrate = cl_list.rmrev / cl_list.occ_rm

            if cl_list.occ_rm1 != 0:
                cl_list.avrgrate1 = cl_list.rmrev1 / cl_list.occ_rm1

            if cl_list.occ_rm2 != 0:
                cl_list.avrgrate2 = cl_list.rmrev2 / cl_list.occ_rm2

            if cl_list.saleable != 0:
                cl_list.yield_ = cl_list.rmrev / cl_list.saleable

            if cl_list.saleable1 != 0:
                cl_list.yield1 = cl_list.rmrev1 / cl_list.saleable1

            if cl_list.saleable2 != 0:
                cl_list.yield2 = cl_list.rmrev2 / cl_list.saleable2

            if cl_list.hotel3 != 0:
                cl_list.hotel3 = (cl_list.occ_rm2 / cl_list.saleable2) * 100

            if tsale != 0:
                cl_list.nat_mark = cl_list.saleable / tsale * 100

            if tsale1 != 0:
                cl_list.nat_mark1 = cl_list.saleable1 / tsale1 * 100

            if tsale2 != 0:
                cl_list.nat_mark2 = cl_list.saleable2 / tsale2 * 100

            if tocc_rm != 0:
                cl_list.mark_share = cl_list.occ_rm / tocc_rm * 100

            if tocc_rm1 != 0:
                cl_list.mark_share1 = cl_list.occ_rm1 / tocc_rm1 * 100

            if tocc_rm2 != 0:
                cl_list.mark_share2 = cl_list.occ_rm2 / tocc_rm2 * 100
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.hno = cl_list.hno
            output_list.htlname = cl_list.htlname
            output_list.occ_rm = to_string(cl_list.occ_rm, ">>>,>>9")
            output_list.saleable = to_string(cl_list.saleable, ">>>,>>9")
            output_list.rmrev = to_string(cl_list.rmrev, "->>,>>>,>>>,>>9.99")
            output_list.occ_rm1 = to_string(cl_list.occ_rm1, ">>>,>>9")
            output_list.saleable1 = to_string(cl_list.saleable1, ">>>,>>9")
            output_list.rmrev1 = to_string(cl_list.rmrev1, "->>,>>>,>>>,>>9.99")
            output_list.occ_rm2 = to_string(cl_list.occ_rm2, ">>>,>>9")
            output_list.saleable2 = to_string(cl_list.saleable2, ">>>,>>9")
            output_list.rmrev2 = to_string(cl_list.rmrev2, "->>>,>>>,>>>,>>9.99")
            output_list.avrgrate = to_string(cl_list.avrgrate, "->>,>>>,>>>,>>9.99")
            output_list.avrgrate1 = to_string(cl_list.avrgrate1, "->>,>>>,>>>,>>9.99")
            output_list.avrgrate2 = to_string(cl_list.avrgrate2, "->>,>>>,>>>,>>9.99")
            output_list.yield_ = to_string(cl_list.yield, "->>,>>>,>>>,>>9.99")
            output_list.yield1 = to_string(cl_list.yield1, "->>,>>>,>>>,>>9.99")
            output_list.yield2 = to_string(cl_list.yield2, "->>,>>>,>>>,>>9.99")
            output_list.nat_mark = to_string(cl_list.nat_mark, ">>9.99")
            output_list.nat_mark1 = to_string(cl_list.nat_mark1, ">>9.99")
            output_list.nat_mark2 = to_string(cl_list.nat_mark2, ">>9.99")
            output_list.mark_share = to_string(cl_list.mark_share, ">>9.99")
            output_list.mark_share1 = to_string(cl_list.mark_share1, ">>9.99")
            output_list.mark_share2 = to_string(cl_list.mark_share2, ">>9.99")
            output_list.hotel1 = to_string(cl_list.hotel1, ">>>,>>9.99")
            output_list.hotel2 = to_string(cl_list.hotel2, ">>>,>>9.99")
            output_list.hotel3 = to_string(cl_list.hotel3, ">>>,>>9.99")
            output_list.occ_proz = to_string(cl_list.occ_proz, ">>9.99")
            output_list.occ_proz1 = to_string(cl_list.occ_proz1, ">>9.99")
            output_list.occ_proz2 = to_string(cl_list.occ_proz2, ">>9.99")


        hotela = (tocc_rm / tsale) * 100
        hotelb = (tocc_rm1 / tsale1) * 100
        hotelc = (tocc_rm2 / tsale2) * 100


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.hno = 999999
        output_list.htlname = translateExtended ("T o t a l", lvcarea, "")
        output_list.occ_rm = to_string(tocc_rm, ">>>,>>9")
        output_list.occ_rm1 = to_string(tocc_rm1, ">>>,>>9")
        output_list.occ_rm2 = to_string(tocc_rm2, ">>>,>>9")
        output_list.saleable = to_string(tsale, ">>>,>>9")
        output_list.saleable1 = to_string(tsale1, ">>>,>>9")
        output_list.saleable2 = to_string(tsale2, ">>>,>>9")
        output_list.rmrev = to_string(trmrev, "->>,>>>,>>>,>>9.99")
        output_list.rmrev1 = to_string(trmrev1, "->>,>>>,>>>,>>9.99")
        output_list.rmrev2 = to_string(trmrev2, "->>>,>>>,>>>,>>9.99")
        output_list.nat_mark = "100.00"
        output_list.nat_mark1 = "100.00"
        output_list.nat_mark2 = "100.00"
        output_list.mark_share = "100.00"
        output_list.mark_share1 = "100.00"
        output_list.mark_share2 = "100.00"
        output_list.hotel1 = to_string(hotela, ">>>,>>9.99")
        output_list.hotel2 = to_string(hotelb, ">>>,>>9.99")
        output_list.hotel3 = to_string(hotelc, ">>>,>>9.99")

        if output_list.hotel1 == None:
            output_list.hotel1 = "  0.00"

        elif output_list.hotel2 == None:
            output_list.hotel2 = " 0.00"

        elif output_list.hotel3 == None:
            output_list.hotel3 = " 0.00"

        if tocc_rm != 0:
            output_list.avrgrate = to_string(trmrev / tocc_rm, "->>,>>>,>>>,>>9.99")
        else:
            output_list.avrgrate = to_string(0, "->>,>>>,>>>,>>9.99")

        if tocc_rm1 != 0:
            output_list.avrgrate1 = to_string(trmrev1 / tocc_rm1, "->>,>>>,>>>,>>9.99")
        else:
            output_list.avrgrate1 = to_string(0, "->>,>>>,>>>,>>9.99")

        if tocc_rm2 != 0:
            output_list.avrgrate2 = to_string(trmrev2 / tocc_rm2, "->>,>>>,>>>,>>9.99")
        else:
            output_list.avrgrate2 = to_string(0, "->>,>>>,>>>,>>9.99")

        if tsale != 0:
            output_list.yield_ = to_string(trmrev / tsale, "->>,>>>,>>>,>>9.99")
        else:
            output_list.yield_ = to_string(0, "->>,>>>,>>>,>>9.99")

        if tsale1 != 0:
            output_list.yield1 = to_string(trmrev1 / tsale1, "->>,>>>,>>>,>>9.99")
        else:
            output_list.yield1 = to_string(0, "->>,>>>,>>>,>>9.99")

        if tsale2 != 0:
            output_list.yield2 = to_string(trmrev2 / tsale2, "->>,>>>,>>>,>>9.99")
        else:
            output_list.yield2 = to_string(0, "->>,>>>,>>>,>>9.99")

        if tocc_proz != 0:
            output_list.occ_proz = to_string(tocc_rm / tsale * 100, ">>9.99")
        else:
            output_list.occ_proz = to_string(0, ">>9.99")

        if tocc_proz1 != 0:
            output_list.occ_proz1 = to_string(tocc_rm1 / tsale1 * 100, ">>9.99")
        else:
            output_list.occ_proz1 = to_string(0, ">>9.99")

        if tocc_proz2 != 0:
            output_list.occ_proz2 = to_string(tocc_rm2 / tsale2 * 100, ">>9.99")
        else:
            output_list.occ_proz2 = to_string(0, ">>9.99")

    def to_date2():

        nonlocal tocc_rm, tocc_rm1, tocc_rm2, tsale, tsale1, tsale2, tocc_proz, tocc_proz1, tocc_proz2, hotel1, hotel2, hotel3, hotela, hotelb, hotelc, output_list_list, trmrev, trmrev1, trmrev2, f_date, t_date, lvcarea, zinrstat, akt_code


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list


        cl_list_list.clear()
        output_list_list.clear()
        tocc_rm = 0
        tocc_rm1 = 0
        tocc_rm2 = 0
        tsale = 0
        tsale1 = 0
        tsale2 = 0
        trmrev = 0
        trmrev1 = 0
        trmrev2 = 0

        for zinrstat in db_session.query(Zinrstat).filter(
                (Zinrstat.datum >= f_date) &  (Zinrstat.datum <= to_date) &  (func.lower(Zinrstat.zinr) == "Competitor")).all():

            akt_code = db_session.query(Akt_code).filter(
                    (Akt_code.aktiongrup == 4) &  (Akt_code.aktionscode == zinrstat.betriebsnr)).first()

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.hno == zinrstat.betriebsnr), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.hno = zinrstat.betriebsnr

                if akt_code:
                    cl_list.htlname = akt_code.bezeich

            if zinrstat.datum == f_date:
                cl_list.occ_rm = cl_list.occ_rm + zinrstat.personen
                cl_list.saleable = cl_list.saleable + zinrstat.zimmeranz
                cl_list.rmrev = cl_list.rmrev + zinrstat.logisumsatz
                cl_list.hotel1 = (cl_list.occ_rm / cl_list.saleable) * 100

                if all_occ:
                    cl_list.occ_rm = cl_list.occ_rm + to_int(zinrstat.argtumsatz)

                if cl_list.saleable != 0:
                    cl_list.occ_proz = cl_list.occ_rm / cl_list.saleable * 100

            if get_month(zinrstat.datum) == get_month(to_date) and get_year(zinrstat.datum) == get_year(to_date):
                cl_list.occ_rm1 = cl_list.occ_rm1 + zinrstat.personen
                cl_list.saleable1 = cl_list.saleable1 + zinrstat.zimmeranz
                cl_list.rmrev1 = cl_list.rmrev1 + zinrstat.logisumsatz
                cl_list.hotel2 = (cl_list.occ_rm1 / cl_list.saleable1) * 100

                if all_occ:
                    cl_list.occ_rm1 = cl_list.occ_rm1 + to_int(zinrstat.argtumsatz)

                if cl_list.saleable1 != 0:
                    cl_list.occ_proz1 = cl_list.occ_rm1 / cl_list.saleable1 * 100
            cl_list.occ_rm2 = cl_list.occ_rm2 + zinrstat.personen
            cl_list.saleable2 = cl_list.saleable2 + zinrstat.zimmeranz
            cl_list.rmrev2 = cl_list.rmrev2 + zinrstat.logisumsatz


            cl_list.hotel3 = (cl_list.occ_rm2 / cl_list.saleable2) * 100

            if all_occ:
                cl_list.occ_rm2 = cl_list.occ_rm2 + to_int(zinrstat.argtumsatz)

            if cl_list.saleable2 != 0:
                cl_list.occ_proz2 = cl_list.occ_rm2 / cl_list.saleable2 * 100

        for cl_list in query(cl_list_list):
            tocc_rm = tocc_rm + cl_list.occ_rm
            tocc_rm1 = tocc_rm1 + cl_list.occ_rm1
            tocc_rm2 = tocc_rm2 + cl_list.occ_rm2
            tsale = tsale + cl_list.saleable
            tsale1 = tsale1 + cl_list.saleable1
            tsale2 = tsale2 + cl_list.saleable2
            trmrev1 = trmrev1 + cl_list.rmrev1
            trmrev2 = trmrev2 + cl_list.rmrev2
            trmrev = trmrev + cl_list.rmrev
            hotel1 = hotel1 + cl_list.hotel1
            hotel2 = hotel2 + cl_list.hotel2
            hotel3 = hotel3 + cl_list.hotel3
            tocc_proz = tocc_proz + cl_list.occ_proz
            tocc_proz1 = tocc_proz1 + cl_list.occ_proz1
            tocc_proz2 = tocc_proz2 + cl_list.occ_proz2

        for cl_list in query(cl_list_list):

            if cl_list.occ_rm != 0:
                cl_list.avrgrate = cl_list.rmrev / cl_list.occ_rm

            if cl_list.occ_rm1 != 0:
                cl_list.avrgrate1 = cl_list.rmrev1 / cl_list.occ_rm1

            if cl_list.occ_rm2 != 0:
                cl_list.avrgrate2 = cl_list.rmrev2 / cl_list.occ_rm2

            if cl_list.saleable != 0:
                cl_list.yield_ = cl_list.rmrev / cl_list.saleable

            if cl_list.saleable1 != 0:
                cl_list.yield1 = cl_list.rmrev1 / cl_list.saleable1

            if cl_list.saleable2 != 0:
                cl_list.yield2 = cl_list.rmrev2 / cl_list.saleable2

            if cl_list.hotel3 != 0:
                cl_list.hotel3 = (cl_list.occ_rm2 / cl_list.saleable2) * 100

            if tsale != 0:
                cl_list.nat_mark = cl_list.saleable / tsale * 100

            if tsale1 != 0:
                cl_list.nat_mark1 = cl_list.saleable1 / tsale1 * 100

            if tsale2 != 0:
                cl_list.nat_mark2 = cl_list.saleable2 / tsale2 * 100

            if tocc_rm != 0:
                cl_list.mark_share = cl_list.occ_rm / tocc_rm * 100

            if tocc_rm1 != 0:
                cl_list.mark_share1 = cl_list.occ_rm1 / tocc_rm1 * 100

            if tocc_rm2 != 0:
                cl_list.mark_share2 = cl_list.occ_rm2 / tocc_rm2 * 100
            output_list = Output_list()
            output_list_list.append(output_list)

            output_list.hno = cl_list.hno
            output_list.htlname = cl_list.htlname
            output_list.occ_rm = to_string(cl_list.occ_rm, ">>>,>>9")
            output_list.saleable = to_string(cl_list.saleable, ">>>,>>9")
            output_list.rmrev = to_string(cl_list.rmrev, "->>,>>>,>>>,>>9.99")
            output_list.occ_rm1 = to_string(cl_list.occ_rm1, ">>>,>>9")
            output_list.saleable1 = to_string(cl_list.saleable1, ">>>,>>9")
            output_list.rmrev1 = to_string(cl_list.rmrev1, "->>,>>>,>>>,>>9.99")
            output_list.occ_rm2 = to_string(cl_list.occ_rm2, ">>>,>>9")
            output_list.saleable2 = to_string(cl_list.saleable2, ">>>,>>9")
            output_list.rmrev2 = to_string(cl_list.rmrev2, "->>>,>>>,>>>,>>9.99")
            output_list.avrgrate = to_string(cl_list.avrgrate, "->>,>>>,>>>,>>9.99")
            output_list.avrgrate1 = to_string(cl_list.avrgrate1, "->>,>>>,>>>,>>9.99")
            output_list.avrgrate2 = to_string(cl_list.avrgrate2, "->>,>>>,>>>,>>9.99")
            output_list.yield_ = to_string(cl_list.yield, "->>,>>>,>>>,>>9.99")
            output_list.yield1 = to_string(cl_list.yield1, "->>,>>>,>>>,>>9.99")
            output_list.yield2 = to_string(cl_list.yield2, "->>,>>>,>>>,>>9.99")
            output_list.nat_mark = to_string(cl_list.nat_mark, ">>9.99")
            output_list.nat_mark1 = to_string(cl_list.nat_mark1, ">>9.99")
            output_list.nat_mark2 = to_string(cl_list.nat_mark2, ">>9.99")
            output_list.mark_share = to_string(cl_list.mark_share, ">>9.99")
            output_list.mark_share1 = to_string(cl_list.mark_share1, ">>9.99")
            output_list.mark_share2 = to_string(cl_list.mark_share2, ">>9.99")
            output_list.hotel1 = to_string(cl_list.hotel1, ">>>,>>9.99")
            output_list.hotel2 = to_string(cl_list.hotel2, ">>>,>>9.99")
            output_list.hotel3 = to_string(cl_list.hotel3, ">>>,>>9.99")
            output_list.occ_proz = to_string(cl_list.occ_proz, ">>9.99")
            output_list.occ_proz1 = to_string(cl_list.occ_proz1, ">>9.99")
            output_list.occ_proz2 = to_string(cl_list.occ_proz2, ">>9.99")


        hotela = (tocc_rm / tsale) * 100
        hotelb = (tocc_rm1 / tsale1) * 100
        hotelc = (tocc_rm2 / tsale2) * 100


        output_list = Output_list()
        output_list_list.append(output_list)

        output_list.hno = 999999
        output_list.htlname = translateExtended ("T o t a l", lvcarea, "")
        output_list.occ_rm = to_string(tocc_rm, ">>>,>>9")
        output_list.occ_rm1 = to_string(tocc_rm1, ">>>,>>9")
        output_list.occ_rm2 = to_string(tocc_rm2, ">>>,>>9")
        output_list.saleable = to_string(tsale, ">>>,>>9")
        output_list.saleable1 = to_string(tsale1, ">>>,>>9")
        output_list.saleable2 = to_string(tsale2, ">>>,>>9")
        output_list.rmrev = to_string(trmrev, "->>,>>>,>>>,>>9.99")
        output_list.rmrev1 = to_string(trmrev1, "->>,>>>,>>>,>>9.99")
        output_list.rmrev2 = to_string(trmrev2, "->>>,>>>,>>>,>>9.99")
        output_list.nat_mark = "100.00"
        output_list.nat_mark1 = "100.00"
        output_list.nat_mark2 = "100.00"
        output_list.mark_share = "100.00"
        output_list.mark_share1 = "100.00"
        output_list.mark_share2 = "100.00"
        output_list.hotel1 = to_string(hotela, ">>>,>>9.99")
        output_list.hotel2 = to_string(hotelb, ">>>,>>9.99")
        output_list.hotel3 = to_string(hotelc, ">>>,>>9.99")

        if output_list.hotel1 == None:
            output_list.hotel1 = "  0.00"

        elif output_list.hotel2 == None:
            output_list.hotel2 = " 0.00"

        elif output_list.hotel3 == None:
            output_list.hotel3 = " 0.00"

        if tocc_rm != 0:
            output_list.avrgrate = to_string(trmrev / tocc_rm, "->>,>>>,>>>,>>9.99")
        else:
            output_list.avrgrate = to_string(0, "->>,>>>,>>>,>>9.99")

        if tocc_rm1 != 0:
            output_list.avrgrate1 = to_string(trmrev1 / tocc_rm1, "->>,>>>,>>>,>>9.99")
        else:
            output_list.avrgrate1 = to_string(0, "->>,>>>,>>>,>>9.99")

        if tocc_rm2 != 0:
            output_list.avrgrate2 = to_string(trmrev2 / tocc_rm2, "->>,>>>,>>>,>>9.99")
        else:
            output_list.avrgrate2 = to_string(0, "->>,>>>,>>>,>>9.99")

        if tsale != 0:
            output_list.yield_ = to_string(trmrev / tsale, "->>,>>>,>>>,>>9.99")
        else:
            output_list.yield_ = to_string(0, "->>,>>>,>>>,>>9.99")

        if tsale1 != 0:
            output_list.yield1 = to_string(trmrev1 / tsale1, "->>,>>>,>>>,>>9.99")
        else:
            output_list.yield1 = to_string(0, "->>,>>>,>>>,>>9.99")

        if tsale2 != 0:
            output_list.yield2 = to_string(trmrev2 / tsale2, "->>,>>>,>>>,>>9.99")
        else:
            output_list.yield2 = to_string(0, "->>,>>>,>>>,>>9.99")

        if tocc_proz != 0:
            output_list.occ_proz = to_string((tocc_rm / tsale) * 100, ">>9.99")
        else:
            output_list.occ_proz = to_string(0, ">>9.99")

        if tocc_proz1 != 0:
            output_list.occ_proz1 = to_string((tocc_rm1 / tsale1) * 100, ">>9.99")
        else:
            output_list.occ_proz1 = to_string(0, ">>9.99")

        if tocc_proz2 != 0:
            output_list.occ_proz2 = to_string((tocc_rm2 / tsale2) * 100, ">>9.99")
        else:
            output_list.occ_proz2 = to_string(0, ">>9.99")


    if not check_ftd:
        from_date = date_mdy(1, 1, get_year(to_date))
        to_date()
    else:
        f_date = from_date
        t_date = to_date
        to_date2()

    return generate_output()