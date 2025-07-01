#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zinrstat, Akt_code

def comp_statisticbl(pvilanguage:int, from_date:date, to_date:date, all_occ:bool, check_ftd:bool):

    prepare_cache ([Zinrstat, Akt_code])

    tocc_rm:Decimal = to_decimal("0.0")
    tocc_rm1:Decimal = to_decimal("0.0")
    tocc_rm2:Decimal = to_decimal("0.0")
    tsale:Decimal = to_decimal("0.0")
    tsale1:Decimal = to_decimal("0.0")
    tsale2:Decimal = to_decimal("0.0")
    tocc_proz:Decimal = to_decimal("0.0")
    tocc_proz1:Decimal = to_decimal("0.0")
    tocc_proz2:Decimal = to_decimal("0.0")
    hotel1:Decimal = to_decimal("0.0")
    hotel2:Decimal = to_decimal("0.0")
    hotel3:Decimal = to_decimal("0.0")
    hotela:Decimal = to_decimal("0.0")
    hotelb:Decimal = to_decimal("0.0")
    hotelc:Decimal = to_decimal("0.0")
    output_list_list = []
    trmrev:Decimal = to_decimal("0.0")
    trmrev1:Decimal = to_decimal("0.0")
    trmrev2:Decimal = to_decimal("0.0")
    f_date:date = None
    t_date:date = None
    lvcarea:string = "comp-statistic"
    zinrstat = akt_code = None

    cl_list = output_list = None

    cl_list_list, Cl_list = create_model("Cl_list", {"hno":int, "htlname":string, "occ_rm":Decimal, "saleable":Decimal, "rmrev":Decimal, "avrgrate":Decimal, "yield_":Decimal, "nat_mark":Decimal, "mark_share":Decimal, "occ_rm1":Decimal, "saleable1":Decimal, "rmrev1":Decimal, "avrgrate1":Decimal, "yield1":Decimal, "nat_mark1":Decimal, "mark_share1":Decimal, "occ_rm2":Decimal, "saleable2":Decimal, "rmrev2":Decimal, "avrgrate2":Decimal, "yield2":Decimal, "nat_mark2":Decimal, "mark_share2":Decimal, "hotel1":Decimal, "hotel2":Decimal, "hotel3":Decimal, "occ_proz":Decimal, "occ_proz1":Decimal, "occ_proz2":Decimal})
    output_list_list, Output_list = create_model("Output_list", {"hno":int, "htlname":string, "occ_rm":string, "saleable":string, "rmrev":string, "avrgrate":string, "nat_mark":string, "mark_share":string, "yield_":string, "occ_rm1":string, "saleable1":string, "rmrev1":string, "avrgrate1":string, "nat_mark1":string, "mark_share1":string, "yield1":string, "occ_rm2":string, "saleable2":string, "rmrev2":string, "avrgrate2":string, "nat_mark2":string, "mark_share2":string, "yield2":string, "hotel1":string, "hotel2":string, "hotel3":string, "occ_proz":string, "occ_proz1":string, "occ_proz2":string})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal tocc_rm, tocc_rm1, tocc_rm2, tsale, tsale1, tsale2, tocc_proz, tocc_proz1, tocc_proz2, hotel1, hotel2, hotel3, hotela, hotelb, hotelc, output_list_list, trmrev, trmrev1, trmrev2, f_date, t_date, lvcarea, zinrstat, akt_code
        nonlocal pvilanguage, from_date, to_date, all_occ, check_ftd


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list

        return {"output-list": output_list_list}

    def to_date1():

        nonlocal tocc_rm, tocc_rm1, tocc_rm2, tsale, tsale1, tsale2, tocc_proz, tocc_proz1, tocc_proz2, hotel1, hotel2, hotel3, hotela, hotelb, hotelc, output_list_list, trmrev, trmrev1, trmrev2, f_date, t_date, lvcarea, zinrstat, akt_code
        nonlocal pvilanguage, from_date, to_date, all_occ, check_ftd


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list


        cl_list_list.clear()
        output_list_list.clear()
        tocc_rm =  to_decimal("0")
        tocc_rm1 =  to_decimal("0")
        tocc_rm2 =  to_decimal("0")
        tsale =  to_decimal("0")
        tsale1 =  to_decimal("0")
        tsale2 =  to_decimal("0")
        trmrev =  to_decimal("0")
        trmrev1 =  to_decimal("0")
        trmrev2 =  to_decimal("0")
        tocc_proz =  to_decimal("0")
        tocc_proz1 =  to_decimal("0")
        tocc_proz2 =  to_decimal("0")

        for zinrstat in db_session.query(Zinrstat).filter(
                 (Zinrstat.datum >= from_date) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == ("Competitor").lower())).order_by(Zinrstat._recid).all():

            akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, 4)],"aktionscode": [(eq, zinrstat.betriebsnr)]})

            cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.hno == zinrstat.betriebsnr), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.hno = zinrstat.betriebsnr

                if akt_code:
                    cl_list.htlname = akt_code.bezeich

            if zinrstat.datum == to_date:
                cl_list.occ_rm =  to_decimal(cl_list.occ_rm) + to_decimal(zinrstat.personen)
                cl_list.saleable =  to_decimal(cl_list.saleable) + to_decimal(zinrstat.zimmeranz)
                cl_list.rmrev =  to_decimal(cl_list.rmrev) + to_decimal(zinrstat.logisumsatz)
                cl_list.hotel1 = ( to_decimal(cl_list.occ_rm) / to_decimal(cl_list.saleable)) * to_decimal("100")

                if all_occ:
                    cl_list.occ_rm =  to_decimal(cl_list.occ_rm) + to_decimal(to_int(zinrstat.argtumsatz))

                if cl_list.saleable != 0:
                    cl_list.occ_proz =  to_decimal(cl_list.occ_rm) / to_decimal(cl_list.saleable) * to_decimal("100")

            if get_month(zinrstat.datum) == get_month(to_date) and get_year(zinrstat.datum) == get_year(to_date):
                cl_list.occ_rm1 =  to_decimal(cl_list.occ_rm1) + to_decimal(zinrstat.personen)
                cl_list.saleable1 =  to_decimal(cl_list.saleable1) + to_decimal(zinrstat.zimmeranz)
                cl_list.rmrev1 =  to_decimal(cl_list.rmrev1) + to_decimal(zinrstat.logisumsatz)
                cl_list.hotel2 = ( to_decimal(cl_list.occ_rm1) / to_decimal(cl_list.saleable1)) * to_decimal("100")

                if all_occ:
                    cl_list.occ_rm1 =  to_decimal(cl_list.occ_rm1) + to_decimal(to_int(zinrstat.argtumsatz))

                if cl_list.saleable1 != 0:
                    cl_list.occ_proz1 =  to_decimal(cl_list.occ_rm1) / to_decimal(cl_list.saleable1) * to_decimal("100")
            cl_list.occ_rm2 =  to_decimal(cl_list.occ_rm2) + to_decimal(zinrstat.personen)
            cl_list.saleable2 =  to_decimal(cl_list.saleable2) + to_decimal(zinrstat.zimmeranz)
            cl_list.rmrev2 =  to_decimal(cl_list.rmrev2) + to_decimal(zinrstat.logisumsatz)


            cl_list.hotel3 = ( to_decimal(cl_list.occ_rm2) / to_decimal(cl_list.saleable2)) * to_decimal("100")

            if all_occ:
                cl_list.occ_rm2 =  to_decimal(cl_list.occ_rm2) + to_decimal(to_int(zinrstat.argtumsatz))

            if cl_list.saleable2 != 0:
                cl_list.occ_proz2 =  to_decimal(cl_list.occ_rm2) / to_decimal(cl_list.saleable2) * to_decimal("100")

        for cl_list in query(cl_list_list, sort_by=[("hno",False)]):
            tocc_rm =  to_decimal(tocc_rm) + to_decimal(cl_list.occ_rm)
            tocc_rm1 =  to_decimal(tocc_rm1) + to_decimal(cl_list.occ_rm1)
            tocc_rm2 =  to_decimal(tocc_rm2) + to_decimal(cl_list.occ_rm2)
            tsale =  to_decimal(tsale) + to_decimal(cl_list.saleable)
            tsale1 =  to_decimal(tsale1) + to_decimal(cl_list.saleable1)
            tsale2 =  to_decimal(tsale2) + to_decimal(cl_list.saleable2)
            trmrev1 =  to_decimal(trmrev1) + to_decimal(cl_list.rmrev1)
            trmrev2 =  to_decimal(trmrev2) + to_decimal(cl_list.rmrev2)
            trmrev =  to_decimal(trmrev) + to_decimal(cl_list.rmrev)
            hotel1 =  to_decimal(hotel1) + to_decimal(cl_list.hotel1)
            hotel2 =  to_decimal(hotel2) + to_decimal(cl_list.hotel2)
            hotel3 =  to_decimal(hotel3) + to_decimal(cl_list.hotel3)
            tocc_proz =  to_decimal(tocc_proz) + to_decimal(cl_list.occ_proz)
            tocc_proz1 =  to_decimal(tocc_proz1) + to_decimal(cl_list.occ_proz1)
            tocc_proz2 =  to_decimal(tocc_proz2) + to_decimal(cl_list.occ_proz2)

        for cl_list in query(cl_list_list, sort_by=[("hno",True)]):

            if cl_list.occ_rm != 0:
                cl_list.avrgrate =  to_decimal(cl_list.rmrev) / to_decimal(cl_list.occ_rm)

            if cl_list.occ_rm1 != 0:
                cl_list.avrgrate1 =  to_decimal(cl_list.rmrev1) / to_decimal(cl_list.occ_rm1)

            if cl_list.occ_rm2 != 0:
                cl_list.avrgrate2 =  to_decimal(cl_list.rmrev2) / to_decimal(cl_list.occ_rm2)

            if cl_list.saleable != 0:
                cl_list.yield_ =  to_decimal(cl_list.rmrev) / to_decimal(cl_list.saleable)

            if cl_list.saleable1 != 0:
                cl_list.yield1 =  to_decimal(cl_list.rmrev1) / to_decimal(cl_list.saleable1)

            if cl_list.saleable2 != 0:
                cl_list.yield2 =  to_decimal(cl_list.rmrev2) / to_decimal(cl_list.saleable2)

            if cl_list.hotel3 != 0:
                cl_list.hotel3 = ( to_decimal(cl_list.occ_rm2) / to_decimal(cl_list.saleable2)) * to_decimal("100")

            if tsale != 0:
                cl_list.nat_mark =  to_decimal(cl_list.saleable) / to_decimal(tsale) * to_decimal("100")

            if tsale1 != 0:
                cl_list.nat_mark1 =  to_decimal(cl_list.saleable1) / to_decimal(tsale1) * to_decimal("100")

            if tsale2 != 0:
                cl_list.nat_mark2 =  to_decimal(cl_list.saleable2) / to_decimal(tsale2) * to_decimal("100")

            if tocc_rm != 0:
                cl_list.mark_share =  to_decimal(cl_list.occ_rm) / to_decimal(tocc_rm) * to_decimal("100")

            if tocc_rm1 != 0:
                cl_list.mark_share1 =  to_decimal(cl_list.occ_rm1) / to_decimal(tocc_rm1) * to_decimal("100")

            if tocc_rm2 != 0:
                cl_list.mark_share2 =  to_decimal(cl_list.occ_rm2) / to_decimal(tocc_rm2) * to_decimal("100")
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
            output_list.yield_ = to_string(cl_list.yield_, "->>,>>>,>>>,>>9.99")
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

        if tsale != None and tsale != 0:
            hotela = ( to_decimal(tocc_rm) / to_decimal(tsale)) * to_decimal("100")

        if tsale1 != None and tsale1 != 0:
            hotelb = ( to_decimal(tocc_rm1) / to_decimal(tsale1)) * to_decimal("100")

        if tsale2 != None and tsale2 != 0:
            hotelc = ( to_decimal(tocc_rm2) / to_decimal(tsale2)) * to_decimal("100")


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
            output_list.hotel1 = " 0.00"

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
        nonlocal pvilanguage, from_date, to_date, all_occ, check_ftd


        nonlocal cl_list, output_list
        nonlocal cl_list_list, output_list_list


        cl_list_list.clear()
        output_list_list.clear()
        tocc_rm =  to_decimal("0")
        tocc_rm1 =  to_decimal("0")
        tocc_rm2 =  to_decimal("0")
        tsale =  to_decimal("0")
        tsale1 =  to_decimal("0")
        tsale2 =  to_decimal("0")
        trmrev =  to_decimal("0")
        trmrev1 =  to_decimal("0")
        trmrev2 =  to_decimal("0")

        for zinrstat in db_session.query(Zinrstat).filter(
                 (Zinrstat.datum >= f_date) & (Zinrstat.datum <= t_date) & (Zinrstat.zinr == ("Competitor").lower())).order_by(Zinrstat._recid).all():

            akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, 4)],"aktionscode": [(eq, zinrstat.betriebsnr)]})

            cl_list = query(cl_list_list, filters=(lambda cl_list: cl_list.hno == zinrstat.betriebsnr), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.hno = zinrstat.betriebsnr

                if akt_code:
                    cl_list.htlname = akt_code.bezeich

            if zinrstat.datum == t_date:
                cl_list.occ_rm =  to_decimal(cl_list.occ_rm) + to_decimal(zinrstat.personen)
                cl_list.saleable =  to_decimal(cl_list.saleable) + to_decimal(zinrstat.zimmeranz)
                cl_list.rmrev =  to_decimal(cl_list.rmrev) + to_decimal(zinrstat.logisumsatz)
                cl_list.hotel1 = ( to_decimal(cl_list.occ_rm) / to_decimal(cl_list.saleable)) * to_decimal("100")

                if all_occ:
                    cl_list.occ_rm =  to_decimal(cl_list.occ_rm) + to_decimal(to_int(zinrstat.argtumsatz))

                if cl_list.saleable != 0:
                    cl_list.occ_proz =  to_decimal(cl_list.occ_rm) / to_decimal(cl_list.saleable) * to_decimal("100")

            if zinrstat.datum >= from_date and zinrstat.datum <= to_date:
                cl_list.occ_rm1 =  to_decimal(cl_list.occ_rm1) + to_decimal(zinrstat.personen)
                cl_list.saleable1 =  to_decimal(cl_list.saleable1) + to_decimal(zinrstat.zimmeranz)
                cl_list.rmrev1 =  to_decimal(cl_list.rmrev1) + to_decimal(zinrstat.logisumsatz)
                cl_list.hotel2 = ( to_decimal(cl_list.occ_rm1) / to_decimal(cl_list.saleable1)) * to_decimal("100")

                if all_occ:
                    cl_list.occ_rm1 =  to_decimal(cl_list.occ_rm1) + to_decimal(to_int(zinrstat.argtumsatz))

                if cl_list.saleable1 != 0:
                    cl_list.occ_proz1 =  to_decimal(cl_list.occ_rm1) / to_decimal(cl_list.saleable1) * to_decimal("100")
            cl_list.occ_rm2 =  to_decimal(cl_list.occ_rm2) + to_decimal(zinrstat.personen)
            cl_list.saleable2 =  to_decimal(cl_list.saleable2) + to_decimal(zinrstat.zimmeranz)
            cl_list.rmrev2 =  to_decimal(cl_list.rmrev2) + to_decimal(zinrstat.logisumsatz)


            cl_list.hotel3 = ( to_decimal(cl_list.occ_rm2) / to_decimal(cl_list.saleable2)) * to_decimal("100")

            if all_occ:
                cl_list.occ_rm2 =  to_decimal(cl_list.occ_rm2) + to_decimal(to_int(zinrstat.argtumsatz))

            if cl_list.saleable2 != 0:
                cl_list.occ_proz2 =  to_decimal(cl_list.occ_rm2) / to_decimal(cl_list.saleable2) * to_decimal("100")

        for cl_list in query(cl_list_list, sort_by=[("hno",True)]):
            tocc_rm =  to_decimal(tocc_rm) + to_decimal(cl_list.occ_rm)
            tocc_rm1 =  to_decimal(tocc_rm1) + to_decimal(cl_list.occ_rm1)
            tocc_rm2 =  to_decimal(tocc_rm2) + to_decimal(cl_list.occ_rm2)
            tsale =  to_decimal(tsale) + to_decimal(cl_list.saleable)
            tsale1 =  to_decimal(tsale1) + to_decimal(cl_list.saleable1)
            tsale2 =  to_decimal(tsale2) + to_decimal(cl_list.saleable2)
            trmrev1 =  to_decimal(trmrev1) + to_decimal(cl_list.rmrev1)
            trmrev2 =  to_decimal(trmrev2) + to_decimal(cl_list.rmrev2)
            trmrev =  to_decimal(trmrev) + to_decimal(cl_list.rmrev)
            hotel1 =  to_decimal(hotel1) + to_decimal(cl_list.hotel1)
            hotel2 =  to_decimal(hotel2) + to_decimal(cl_list.hotel2)
            hotel3 =  to_decimal(hotel3) + to_decimal(cl_list.hotel3)
            tocc_proz =  to_decimal(tocc_proz) + to_decimal(cl_list.occ_proz)
            tocc_proz1 =  to_decimal(tocc_proz1) + to_decimal(cl_list.occ_proz1)
            tocc_proz2 =  to_decimal(tocc_proz2) + to_decimal(cl_list.occ_proz2)

        for cl_list in query(cl_list_list, sort_by=[("hno",True)]):

            if cl_list.occ_rm != 0:
                cl_list.avrgrate =  to_decimal(cl_list.rmrev) / to_decimal(cl_list.occ_rm)

            if cl_list.occ_rm1 != 0:
                cl_list.avrgrate1 =  to_decimal(cl_list.rmrev1) / to_decimal(cl_list.occ_rm1)

            if cl_list.occ_rm2 != 0:
                cl_list.avrgrate2 =  to_decimal(cl_list.rmrev2) / to_decimal(cl_list.occ_rm2)

            if cl_list.saleable != 0:
                cl_list.yield_ =  to_decimal(cl_list.rmrev) / to_decimal(cl_list.saleable)

            if cl_list.saleable1 != 0:
                cl_list.yield1 =  to_decimal(cl_list.rmrev1) / to_decimal(cl_list.saleable1)

            if cl_list.saleable2 != 0:
                cl_list.yield2 =  to_decimal(cl_list.rmrev2) / to_decimal(cl_list.saleable2)

            if cl_list.hotel3 != 0:
                cl_list.hotel3 = ( to_decimal(cl_list.occ_rm2) / to_decimal(cl_list.saleable2)) * to_decimal("100")

            if tsale != 0:
                cl_list.nat_mark =  to_decimal(cl_list.saleable) / to_decimal(tsale) * to_decimal("100")

            if tsale1 != 0:
                cl_list.nat_mark1 =  to_decimal(cl_list.saleable1) / to_decimal(tsale1) * to_decimal("100")

            if tsale2 != 0:
                cl_list.nat_mark2 =  to_decimal(cl_list.saleable2) / to_decimal(tsale2) * to_decimal("100")

            if tocc_rm != 0:
                cl_list.mark_share =  to_decimal(cl_list.occ_rm) / to_decimal(tocc_rm) * to_decimal("100")

            if tocc_rm1 != 0:
                cl_list.mark_share1 =  to_decimal(cl_list.occ_rm1) / to_decimal(tocc_rm1) * to_decimal("100")

            if tocc_rm2 != 0:
                cl_list.mark_share2 =  to_decimal(cl_list.occ_rm2) / to_decimal(tocc_rm2) * to_decimal("100")
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
            output_list.yield_ = to_string(cl_list.yield_, "->>,>>>,>>>,>>9.99")
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

        if tsale != None and tsale != 0:
            hotela = ( to_decimal(tocc_rm) / to_decimal(tsale)) * to_decimal("100")

        if tsale1 != None and tsale1 != 0:
            hotelb = ( to_decimal(tocc_rm1) / to_decimal(tsale1)) * to_decimal("100")

        if tsale2 != None and tsale2 != 0:
            hotelc = ( to_decimal(tocc_rm2) / to_decimal(tsale2)) * to_decimal("100")


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
            output_list.hotel1 = " 0.00"

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
        to_date1()
    else:
        f_date = date_mdy(1, 1, get_year(to_date))
        t_date = to_date
        to_date2()

    return generate_output()