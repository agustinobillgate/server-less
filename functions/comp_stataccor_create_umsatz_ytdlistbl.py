#using conversion tools version: 1.0.0.117

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zinrstat, Akt_code

def comp_stataccor_create_umsatz_ytdlistbl(pvilanguage:int, to_date:date, show_ytd:bool):

    prepare_cache ([Zinrstat, Akt_code])

    cl_list_data = []
    tsale:int = 0
    tsale1:int = 0
    tocc_rm:int = 0
    tocc_rm1:int = 0
    tocc_rm_c:int = 0
    tocc_rm_c1:int = 0
    tot_hotel:int = 0
    tocc_rm2:int = 0
    tocc_rm3:int = 0
    tocc_rm4:int = 0
    tocc_rm_c2:int = 0
    tocc_rm_c3:int = 0
    tocc_rm_c4:int = 0
    tsale2:int = 0
    tsale3:int = 0
    tsale4:int = 0
    trmrev:Decimal = to_decimal("0.0")
    trmrev1:Decimal = to_decimal("0.0")
    trmrev2:Decimal = to_decimal("0.0")
    trmrev3:Decimal = to_decimal("0.0")
    trmrev4:Decimal = to_decimal("0.0")
    tavr:Decimal = to_decimal("0.0")
    tavr1:Decimal = to_decimal("0.0")
    tavr2:Decimal = to_decimal("0.0")
    tavr3:Decimal = to_decimal("0.0")
    tavr4:Decimal = to_decimal("0.0")
    tocc_proz:Decimal = to_decimal("0.0")
    tocc_proz1:Decimal = to_decimal("0.0")
    tocc_proz2:Decimal = to_decimal("0.0")
    tocc_proz3:Decimal = to_decimal("0.0")
    tocc_proz4:Decimal = to_decimal("0.0")
    tocc_proz_c:Decimal = to_decimal("0.0")
    tocc_proz_c1:Decimal = to_decimal("0.0")
    tocc_proz_c2:Decimal = to_decimal("0.0")
    tocc_proz_c3:Decimal = to_decimal("0.0")
    tocc_proz_c4:Decimal = to_decimal("0.0")
    trevpar:Decimal = to_decimal("0.0")
    trevpar1:Decimal = to_decimal("0.0")
    trevpar2:Decimal = to_decimal("0.0")
    trevpar3:Decimal = to_decimal("0.0")
    trevpar4:Decimal = to_decimal("0.0")
    trgi:Decimal = to_decimal("0.0")
    trgi1:Decimal = to_decimal("0.0")
    trgi2:Decimal = to_decimal("0.0")
    trgi3:Decimal = to_decimal("0.0")
    trgi4:Decimal = to_decimal("0.0")
    tmpi:Decimal = to_decimal("0.0")
    tmpi1:Decimal = to_decimal("0.0")
    tmpi2:Decimal = to_decimal("0.0")
    tmpi3:Decimal = to_decimal("0.0")
    tmpi4:Decimal = to_decimal("0.0")
    tari:Decimal = to_decimal("0.0")
    tari1:Decimal = to_decimal("0.0")
    tari2:Decimal = to_decimal("0.0")
    tari3:Decimal = to_decimal("0.0")
    tari4:Decimal = to_decimal("0.0")
    from_date:date = None
    last_fdate:date = None
    last_tdate:date = None
    last_year:int = 0
    lvcarea:string = "comp-stataccor"
    zinrstat = akt_code = None

    cl_list = t_zinrstat = None

    cl_list_data, Cl_list = create_model("Cl_list", {"hno":int, "htlname":string, "occ_rm":int, "occ_rm_c":int, "saleable":int, "rmrev":Decimal, "avrgrate":Decimal, "yield_":Decimal, "nat_mark":Decimal, "mark_share":Decimal, "revpar":Decimal, "rgi":Decimal, "mpi":Decimal, "ari":Decimal, "occ_proz":Decimal, "occ_proz_c":Decimal, "occ_rm1":int, "occ_rm_c1":int, "saleable1":int, "rmrev1":Decimal, "avrgrate1":Decimal, "yield1":Decimal, "nat_mark1":Decimal, "mark_share1":Decimal, "revpar1":Decimal, "rgi1":Decimal, "mpi1":Decimal, "ari1":Decimal, "occ_proz1":Decimal, "occ_proz_c1":Decimal, "occ_rm2":int, "occ_rm_c2":int, "saleable2":int, "rmrev2":Decimal, "avrgrate2":Decimal, "yield2":Decimal, "nat_mark2":Decimal, "mark_share2":Decimal, "revpar2":Decimal, "rgi2":Decimal, "mpi2":Decimal, "ari2":Decimal, "occ_proz2":Decimal, "occ_proz_c2":Decimal, "occ_rm3":int, "occ_rm_c3":int, "saleable3":int, "rmrev3":Decimal, "avrgrate3":Decimal, "yield3":Decimal, "nat_mark3":Decimal, "mark_share3":Decimal, "revpar3":Decimal, "rgi3":Decimal, "mpi3":Decimal, "ari3":Decimal, "occ_proz3":Decimal, "occ_proz_c3":Decimal, "occ_rm4":int, "occ_rm_c4":int, "saleable4":int, "rmrev4":Decimal, "avrgrate4":Decimal, "yield4":Decimal, "nat_mark4":Decimal, "mark_share4":Decimal, "revpar4":Decimal, "rgi4":Decimal, "mpi4":Decimal, "ari4":Decimal, "occ_proz4":Decimal, "occ_proz_c4":Decimal, "index_nr":int})

    T_zinrstat = create_buffer("T_zinrstat",Zinrstat)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_data, tsale, tsale1, tocc_rm, tocc_rm1, tocc_rm_c, tocc_rm_c1, tot_hotel, tocc_rm2, tocc_rm3, tocc_rm4, tocc_rm_c2, tocc_rm_c3, tocc_rm_c4, tsale2, tsale3, tsale4, trmrev, trmrev1, trmrev2, trmrev3, trmrev4, tavr, tavr1, tavr2, tavr3, tavr4, tocc_proz, tocc_proz1, tocc_proz2, tocc_proz3, tocc_proz4, tocc_proz_c, tocc_proz_c1, tocc_proz_c2, tocc_proz_c3, tocc_proz_c4, trevpar, trevpar1, trevpar2, trevpar3, trevpar4, trgi, trgi1, trgi2, trgi3, trgi4, tmpi, tmpi1, tmpi2, tmpi3, tmpi4, tari, tari1, tari2, tari3, tari4, from_date, last_fdate, last_tdate, last_year, lvcarea, zinrstat, akt_code
        nonlocal pvilanguage, to_date, show_ytd
        nonlocal t_zinrstat


        nonlocal cl_list, t_zinrstat
        nonlocal cl_list_data

        return {"cl-list": cl_list_data}

    def get_totalhtl():

        nonlocal cl_list_data, tsale, tsale1, tocc_rm, tocc_rm1, tocc_rm_c, tocc_rm_c1, tot_hotel, tocc_rm2, tocc_rm3, tocc_rm4, tocc_rm_c2, tocc_rm_c3, tocc_rm_c4, tsale2, tsale3, tsale4, trmrev, trmrev1, trmrev2, trmrev3, trmrev4, tavr, tavr1, tavr2, tavr3, tavr4, tocc_proz, tocc_proz1, tocc_proz2, tocc_proz3, tocc_proz4, tocc_proz_c, tocc_proz_c1, tocc_proz_c2, tocc_proz_c3, tocc_proz_c4, trevpar, trevpar1, trevpar2, trevpar3, trevpar4, trgi, trgi1, trgi2, trgi3, trgi4, tmpi, tmpi1, tmpi2, tmpi3, tmpi4, tari, tari1, tari2, tari3, tari4, from_date, last_fdate, last_tdate, last_year, lvcarea, zinrstat, akt_code
        nonlocal pvilanguage, to_date, show_ytd
        nonlocal t_zinrstat


        nonlocal cl_list, t_zinrstat
        nonlocal cl_list_data


        tot_hotel = 0

        for akt_code in db_session.query(Akt_code).filter(
                 (Akt_code.aktiongrup == 4)).order_by(Akt_code._recid).all():
            tot_hotel = tot_hotel + 1


    def create_umsatz1():

        nonlocal cl_list_data, tsale, tsale1, tocc_rm, tocc_rm1, tocc_rm_c, tocc_rm_c1, tot_hotel, tocc_rm2, tocc_rm3, tocc_rm4, tocc_rm_c2, tocc_rm_c3, tocc_rm_c4, tsale2, tsale3, tsale4, trmrev, trmrev1, trmrev2, trmrev3, trmrev4, tavr, tavr1, tavr2, tavr3, tavr4, tocc_proz, tocc_proz1, tocc_proz2, tocc_proz3, tocc_proz4, tocc_proz_c, tocc_proz_c1, tocc_proz_c2, tocc_proz_c3, tocc_proz_c4, trevpar, trevpar1, trevpar2, trevpar3, trevpar4, trgi, trgi1, trgi2, trgi3, trgi4, tmpi, tmpi1, tmpi2, tmpi3, tmpi4, tari, tari1, tari2, tari3, tari4, from_date, last_fdate, last_tdate, last_year, lvcarea, zinrstat, akt_code
        nonlocal pvilanguage, to_date, show_ytd
        nonlocal t_zinrstat


        nonlocal cl_list, t_zinrstat
        nonlocal cl_list_data

        str1:string = ""
        str2:string = ""
        str3:string = ""
        str4:string = ""
        dd:int = 0
        mm:int = 0
        get_totalhtl()
        cl_list_data.clear()
        tocc_rm = 0
        tocc_rm1 = 0
        tocc_rm2 = 0
        tocc_rm3 = 0
        tocc_rm4 = 0
        tocc_rm_c = 0
        tocc_rm_c1 = 0
        tocc_rm_c2 = 0
        tocc_rm_c3 = 0
        tocc_rm_c4 = 0
        tsale = 0
        tsale1 = 0
        tsale2 = 0
        tsale3 = 0
        tsale4 = 0
        trmrev =  to_decimal("0")
        trmrev1 =  to_decimal("0")
        trmrev2 =  to_decimal("0")
        trmrev3 =  to_decimal("0")
        trmrev4 =  to_decimal("0")
        tocc_proz =  to_decimal("0")
        tocc_proz1 =  to_decimal("0")
        tocc_proz2 =  to_decimal("0")
        tocc_proz3 =  to_decimal("0")
        tocc_proz4 =  to_decimal("0")
        trevpar =  to_decimal("0")
        tocc_proz_c =  to_decimal("0")
        tocc_proz_c1 =  to_decimal("0")
        tocc_proz_c2 =  to_decimal("0")
        tocc_proz_c3 =  to_decimal("0")
        tocc_proz_c4 =  to_decimal("0")
        trevpar1 =  to_decimal("0")
        trevpar2 =  to_decimal("0")
        trevpar3 =  to_decimal("0")
        trevpar4 =  to_decimal("0")
        trgi =  to_decimal("0")
        trgi1 =  to_decimal("0")
        trgi2 =  to_decimal("0")
        trgi3 =  to_decimal("0")
        trgi4 =  to_decimal("0")
        tmpi =  to_decimal("0")
        tmpi1 =  to_decimal("0")
        tmpi2 =  to_decimal("0")
        tmpi3 =  to_decimal("0")
        tmpi4 =  to_decimal("0")
        tari =  to_decimal("0")
        tari1 =  to_decimal("0")
        tari2 =  to_decimal("0")
        tari3 =  to_decimal("0")
        tari4 =  to_decimal("0")
        from_date = date_mdy(1, 1, get_year(to_date))
        last_year = get_year(to_date) - 1
        last_fdate = date_mdy(1, 1, last_year)
        dd = get_day(to_date)
        mm = get_month(to_date)

        if dd == 29 and mm == 2:
            last_tdate = date_mdy(get_month(to_date) , 28, last_year)
        else:
            last_tdate = date_mdy(get_month(to_date) , get_day(to_date) , last_year)

        for zinrstat in db_session.query(Zinrstat).filter(
                 (Zinrstat.datum >= from_date) & (Zinrstat.datum <= to_date) & (Zinrstat.zinr == ("Competitor").lower())).order_by(Zinrstat._recid).all():

            akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, 4)],"aktionscode": [(eq, zinrstat.betriebsnr)]})

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.hno == zinrstat.betriebsnr), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.hno = zinrstat.betriebsnr

                if akt_code:
                    cl_list.htlname = akt_code.bezeich

            if zinrstat.datum == to_date:
                cl_list.occ_rm = cl_list.occ_rm + zinrstat.personen
                cl_list.occ_rm_c = cl_list.occ_rm_c + (zinrstat.personen + to_int(zinrstat.argtumsatz))
                cl_list.saleable = cl_list.saleable + zinrstat.zimmeranz
                cl_list.rmrev =  to_decimal(cl_list.rmrev) + to_decimal(zinrstat.logisumsatz)

            if get_month(zinrstat.datum) == get_month(to_date) and get_year(zinrstat.datum) == get_year(to_date):
                cl_list.occ_rm1 = cl_list.occ_rm1 + zinrstat.personen
                cl_list.occ_rm_c1 = cl_list.occ_rm_c1 + (zinrstat.personen + to_int(zinrstat.argtumsatz))
                cl_list.saleable1 = cl_list.saleable1 + zinrstat.zimmeranz
                cl_list.rmrev1 =  to_decimal(cl_list.rmrev1) + to_decimal(zinrstat.logisumsatz)

            if zinrstat.datum >= from_date and zinrstat.datum <= to_date:
                cl_list.occ_rm2 = cl_list.occ_rm2 + zinrstat.personen
                cl_list.occ_rm_c2 = cl_list.occ_rm_c2 + (zinrstat.personen + to_int(zinrstat.argtumsatz))
                cl_list.saleable2 = cl_list.saleable2 + zinrstat.zimmeranz
                cl_list.rmrev2 =  to_decimal(cl_list.rmrev2) + to_decimal(zinrstat.logisumsatz)

            if cl_list.saleable != 0:
                cl_list.occ_proz =  to_decimal(cl_list.occ_rm) / to_decimal(cl_list.saleable) * to_decimal("100")
                cl_list.occ_proz_c =  to_decimal(cl_list.occ_rm_c) / to_decimal(cl_list.saleable) * to_decimal("100")

            if cl_list.saleable1 != 0:
                cl_list.occ_proz1 =  to_decimal(cl_list.occ_rm1) / to_decimal(cl_list.saleable1) * to_decimal("100")
                cl_list.occ_proz_c1 =  to_decimal(cl_list.occ_rm_c1) / to_decimal(cl_list.saleable1) * to_decimal("100")

            if cl_list.saleable2 != 0:
                cl_list.occ_proz2 =  to_decimal(cl_list.occ_rm2) / to_decimal(cl_list.saleable2) * to_decimal("100")
                cl_list.occ_proz_c2 =  to_decimal(cl_list.occ_rm_c2) / to_decimal(cl_list.saleable2) * to_decimal("100")

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

        for t_zinrstat in db_session.query(T_zinrstat).filter(
                 (T_zinrstat.datum >= last_fdate) & (T_zinrstat.datum <= last_tdate) & (T_zinrstat.zinr == ("Competitor").lower())).order_by(T_zinrstat._recid).all():

            akt_code = get_cache (Akt_code, {"aktiongrup": [(eq, 4)],"aktionscode": [(eq, t_zinrstat.betriebsnr)]})

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.hno == t_zinrstat.betriebsnr), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.hno = t_zinrstat.betriebsnr

                if akt_code:
                    cl_list.htlname = akt_code.bezeich

            if get_month(t_zinrstat.datum) == get_month(last_tdate) and get_year(t_zinrstat.datum) == get_year(last_fdate):
                cl_list.occ_rm3 = cl_list.occ_rm3 + t_zinrstat.personen
                cl_list.occ_rm_c3 = cl_list.occ_rm_c3 + (t_zinrstat.personen + to_int(t_zinrstat.argtumsatz))
                cl_list.saleable3 = cl_list.saleable3 + t_zinrstat.zimmeranz
                cl_list.rmrev3 =  to_decimal(cl_list.rmrev3) + to_decimal(t_zinrstat.logisumsatz)

            if t_zinrstat.datum >= last_fdate and t_zinrstat.datum <= last_tdate:
                cl_list.occ_rm4 = cl_list.occ_rm4 + t_zinrstat.personen
                cl_list.occ_rm_c4 = cl_list.occ_rm_c4 + (t_zinrstat.personen + to_int(t_zinrstat.argtumsatz))
                cl_list.saleable4 = cl_list.saleable4 + t_zinrstat.zimmeranz
                cl_list.rmrev4 =  to_decimal(cl_list.rmrev4) + to_decimal(t_zinrstat.logisumsatz)

            if cl_list.saleable3 != 0:
                cl_list.occ_proz3 =  to_decimal(cl_list.occ_rm3) / to_decimal(cl_list.saleable3) * to_decimal("100")
                cl_list.occ_proz_c3 =  to_decimal(cl_list.occ_rm_c3) / to_decimal(cl_list.saleable3) * to_decimal("100")

            if cl_list.saleable4 != 0:
                cl_list.occ_proz4 =  to_decimal(cl_list.occ_rm4) / to_decimal(cl_list.saleable4) * to_decimal("100")
                cl_list.occ_proz_c4 =  to_decimal(cl_list.occ_rm_c4) / to_decimal(cl_list.saleable4) * to_decimal("100")

            if cl_list.occ_rm3 != 0:
                cl_list.avrgrate3 =  to_decimal(cl_list.rmrev3) / to_decimal(cl_list.occ_rm3)

            if cl_list.occ_rm4 != 0:
                cl_list.avrgrate4 =  to_decimal(cl_list.rmrev4) / to_decimal(cl_list.occ_rm4)

            if cl_list.saleable3 != 0:
                cl_list.yield3 =  to_decimal(cl_list.rmrev3) / to_decimal(cl_list.saleable3)

            if cl_list.saleable4 != 0:
                cl_list.yield4 =  to_decimal(cl_list.rmrev4) / to_decimal(cl_list.saleable4)

        for cl_list in query(cl_list_data):
            tocc_rm = tocc_rm + cl_list.occ_rm
            tocc_rm1 = tocc_rm1 + cl_list.occ_rm1
            tocc_rm2 = tocc_rm2 + cl_list.occ_rm2
            tocc_rm3 = tocc_rm3 + cl_list.occ_rm3
            tocc_rm4 = tocc_rm4 + cl_list.occ_rm4
            tocc_rm_c = tocc_rm_c + cl_list.occ_rm_c
            tocc_rm_c1 = tocc_rm_c1 + cl_list.occ_rm_c1
            tocc_rm_c2 = tocc_rm_c2 + cl_list.occ_rm_c2
            tocc_rm_c3 = tocc_rm_c3 + cl_list.occ_rm_c3
            tocc_rm_c4 = tocc_rm_c4 + cl_list.occ_rm_c4
            tsale = tsale + cl_list.saleable
            tsale1 = tsale1 + cl_list.saleable1
            tsale2 = tsale2 + cl_list.saleable2
            tsale3 = tsale3 + cl_list.saleable3
            tsale4 = tsale4 + cl_list.saleable4
            trmrev1 =  to_decimal(trmrev1) + to_decimal(cl_list.rmrev1)
            trmrev =  to_decimal(trmrev) + to_decimal(cl_list.rmrev)
            trmrev2 =  to_decimal(trmrev2) + to_decimal(cl_list.rmrev2)
            trmrev3 =  to_decimal(trmrev3) + to_decimal(cl_list.rmrev3)
            trmrev4 =  to_decimal(trmrev4) + to_decimal(cl_list.rmrev4)

        if tocc_rm != 0:
            tavr =  to_decimal(trmrev) / to_decimal(tocc_rm)

        if tocc_rm1 != 0:
            tavr1 =  to_decimal(trmrev1) / to_decimal(tocc_rm1)

        if tocc_rm2 != 0:
            tavr2 =  to_decimal(trmrev2) / to_decimal(tocc_rm2)

        if tocc_rm3 != 0:
            tavr3 =  to_decimal(trmrev3) / to_decimal(tocc_rm3)

        if tocc_rm4 != 0:
            tavr4 =  to_decimal(trmrev4) / to_decimal(tocc_rm4)

        if tsale != 0:
            tocc_proz = ( to_decimal(tocc_rm) / to_decimal(tsale)) * to_decimal("100")
            tocc_proz_c = ( to_decimal(tocc_rm_c) / to_decimal(tsale)) * to_decimal("100")
            trevpar =  to_decimal(trmrev) / to_decimal(tsale)

        if tsale1 != 0:
            tocc_proz1 = ( to_decimal(tocc_rm1) / to_decimal(tsale1)) * to_decimal("100")
            tocc_proz_c1 = ( to_decimal(tocc_rm_c1) / to_decimal(tsale1)) * to_decimal("100")
            trevpar1 =  to_decimal(trmrev1) / to_decimal(tsale1)

        if tsale2 != 0:
            tocc_proz2 = ( to_decimal(tocc_rm2) / to_decimal(tsale2)) * to_decimal("100")
            tocc_proz_c2 = ( to_decimal(tocc_rm_c2) / to_decimal(tsale2)) * to_decimal("100")
            trevpar2 =  to_decimal(trmrev2) / to_decimal(tsale2)

        if tsale3 != 0:
            tocc_proz3 = ( to_decimal(tocc_rm3) / to_decimal(tsale3)) * to_decimal("100")
            tocc_proz_c3 = ( to_decimal(tocc_rm_c3) / to_decimal(tsale3)) * to_decimal("100")
            trevpar3 =  to_decimal(trmrev3) / to_decimal(tsale3)

        if tsale4 != 0:
            tocc_proz4 = ( to_decimal(tocc_rm4) / to_decimal(tsale4)) * to_decimal("100")
            tocc_proz_c4 = ( to_decimal(tocc_rm_c4) / to_decimal(tsale4)) * to_decimal("100")
            trevpar4 =  to_decimal(trmrev4) / to_decimal(tsale4)

        if tocc_rm == None:
            tocc_rm = 0.00

        if tocc_rm1 == None:
            tocc_rm1 = 0.00

        if tocc_rm2 == None:
            tocc_rm2 = 0.00

        if tocc_rm3 == None:
            tocc_rm3 = 0.00

        if tocc_rm4 == None:
            tocc_rm4 = 0.00

        if tocc_rm_c == None:
            tocc_rm_c = 0.00

        if tocc_rm_c1 == None:
            tocc_rm_c1 = 0.00

        if tocc_rm_c2 == None:
            tocc_rm_c2 = 0.00

        if tocc_rm_c3 == None:
            tocc_rm_c3 = 0.00

        if tocc_rm_c4 == None:
            tocc_rm_c4 = 0.00

        if tsale == None:
            tsale = 0.00

        if tsale1 == None:
            tsale1 = 0.00

        if tsale2 == None:
            tsale2 = 0.00

        if tsale3 == None:
            tsale3 = 0.00

        if tsale4 == None:
            tsale4 = 0.00

        if trmrev == None:
            trmrev =  to_decimal(0.00)

        if trmrev1 == None:
            trmrev1 =  to_decimal(0.00)

        if trmrev2 == None:
            trmrev2 =  to_decimal(0.00)

        if trmrev3 == None:
            trmrev3 =  to_decimal(0.00)

        if trmrev4 == None:
            trmrev4 =  to_decimal(0.00)

        if tavr == None:
            tavr =  to_decimal(0.00)

        if tavr1 == None:
            tavr1 =  to_decimal(0.00)

        if tavr2 == None:
            tavr2 =  to_decimal(0.00)

        if tavr3 == None:
            tavr3 =  to_decimal(0.00)

        if tavr4 == None:
            tavr4 =  to_decimal(0.00)

        if tocc_proz == None:
            tocc_proz =  to_decimal(0.00)

        if tocc_proz1 == None:
            tocc_proz1 =  to_decimal(0.00)

        if tocc_proz2 == None:
            tocc_proz2 =  to_decimal(0.00)

        if tocc_proz3 == None:
            tocc_proz3 =  to_decimal(0.00)

        if tocc_proz4 == None:
            tocc_proz4 =  to_decimal(0.00)

        if tocc_proz_c == None:
            tocc_proz_c =  to_decimal(0.00)

        if tocc_proz_c1 == None:
            tocc_proz_c1 =  to_decimal(0.00)

        if tocc_proz_c2 == None:
            tocc_proz_c2 =  to_decimal(0.00)

        if tocc_proz_c3 == None:
            tocc_proz_c3 =  to_decimal(0.00)

        if tocc_proz_c4 == None:
            tocc_proz_c4 =  to_decimal(0.00)

        if trevpar == None:
            trevpar =  to_decimal(0.00)

        if trevpar1 == None:
            trevpar1 =  to_decimal(0.00)

        if trevpar2 == None:
            trevpar2 =  to_decimal(0.00)

        if trevpar3 == None:
            trevpar3 =  to_decimal(0.00)

        if trevpar4 == None:
            trevpar4 =  to_decimal(0.00)

        for cl_list in query(cl_list_data):

            if cl_list.saleable != 0 and tocc_proz != 0:
                cl_list.mpi =  to_decimal(cl_list.occ_proz) / to_decimal(tocc_proz)

            if cl_list.saleable != 0 and cl_list.rmrev != 0 and trevpar != 0:
                cl_list.rgi =  to_decimal(cl_list.yield_) / to_decimal(trevpar)

            if tavr != 0:
                cl_list.ari =  to_decimal(cl_list.avrgrate) / to_decimal(tavr)

            if cl_list.saleable1 != 0 and tocc_proz1 != 0:
                cl_list.mpi1 =  to_decimal(cl_list.occ_proz1) / to_decimal(tocc_proz1)

            if cl_list.saleable1 != 0 and cl_list.rmrev1 != 0 and trevpar1 != 0:
                cl_list.rgi1 =  to_decimal(cl_list.yield1) / to_decimal(trevpar1)

            if tavr1 != 0:
                cl_list.ari1 =  to_decimal(cl_list.avrgrate1) / to_decimal(tavr1)

            if cl_list.saleable2 != 0 and tocc_proz2 != 0:
                cl_list.mpi2 =  to_decimal(cl_list.occ_proz2) / to_decimal(tocc_proz2)

            if cl_list.saleable2 != 0 and cl_list.rmrev2 != 0 and trevpar2 != 0:
                cl_list.rgi2 =  to_decimal(cl_list.yield2) / to_decimal(trevpar2)

            if tavr2 != 0:
                cl_list.ari2 =  to_decimal(cl_list.avrgrate2) / to_decimal(tavr2)

            if cl_list.saleable3 != 0 and tocc_proz3 != 0:
                cl_list.mpi3 =  to_decimal(cl_list.occ_proz3) / to_decimal(tocc_proz3)

            if cl_list.saleable3 != 0 and cl_list.rmrev3 != 0 and trevpar3 != 0:
                cl_list.rgi3 =  to_decimal(cl_list.yield3) / to_decimal(trevpar3)

            if tavr3 != 0:
                cl_list.ari3 =  to_decimal(cl_list.avrgrate3) / to_decimal(tavr3)

            if cl_list.saleable4 != 0 and tocc_proz4 != 0:
                cl_list.mpi4 =  to_decimal(cl_list.occ_proz4) / to_decimal(tocc_proz4)

            if cl_list.saleable4 != 0 and cl_list.rmrev4 != 0 and trevpar4 != 0:
                cl_list.rgi4 =  to_decimal(cl_list.yield4) / to_decimal(trevpar4)

            if tavr4 != 0:
                cl_list.ari4 =  to_decimal(cl_list.avrgrate4) / to_decimal(tavr4)

            if cl_list.ari == None:
                cl_list.ari =  to_decimal(0.00)

            if cl_list.ari1 == None:
                cl_list.ari1 =  to_decimal(0.00)

            if cl_list.ari2 == None:
                cl_list.ari2 =  to_decimal(0.00)

            if cl_list.ari3 == None:
                cl_list.ari3 =  to_decimal(0.00)

            if cl_list.ari4 == None:
                cl_list.ari4 =  to_decimal(0.00)

            if trevpar != 0:
                trgi =  to_decimal(trevpar) / to_decimal(trevpar)

            if trevpar1 != 0:
                trgi1 =  to_decimal(trevpar1) / to_decimal(trevpar1)

            if trevpar2 != 0:
                trgi2 =  to_decimal(trevpar2) / to_decimal(trevpar2)

            if trevpar3 != 0:
                trgi3 =  to_decimal(trevpar3) / to_decimal(trevpar3)

            if trevpar4 != 0:
                trgi4 =  to_decimal(trevpar4) / to_decimal(trevpar4)

            if tocc_proz != 0:
                tmpi =  to_decimal(tocc_proz) / to_decimal(tocc_proz)

            if tocc_proz1 != 0:
                tmpi1 =  to_decimal(tocc_proz1) / to_decimal(tocc_proz1)

            if tocc_proz2 != 0:
                tmpi2 =  to_decimal(tocc_proz2) / to_decimal(tocc_proz2)

            if tocc_proz3 != 0:
                tmpi3 =  to_decimal(tocc_proz3) / to_decimal(tocc_proz3)

            if tocc_proz4 != 0:
                tmpi4 =  to_decimal(tocc_proz4) / to_decimal(tocc_proz4)

            if tavr != 0:
                tari =  to_decimal(tavr) / to_decimal(tavr)

            if tavr1 != 0:
                tari1 =  to_decimal(tavr1) / to_decimal(tavr1)

            if tavr2 != 0:
                tari2 =  to_decimal(tavr2) / to_decimal(tavr2)

            if tavr3 != 0:
                tari3 =  to_decimal(tavr3) / to_decimal(tavr3)

            if tavr4 != 0:
                tari4 =  to_decimal(tavr4) / to_decimal(tavr4)

            if trgi == None:
                trgi =  to_decimal(0.00)

            if trgi1 == None:
                trgi1 =  to_decimal(0.00)

            if trgi2 == None:
                trgi2 =  to_decimal(0.00)

            if trgi3 == None:
                trgi3 =  to_decimal(0.00)

            if trgi4 == None:
                trgi4 =  to_decimal(0.00)

            if tmpi == None:
                tmpi =  to_decimal(0.00)

            if tmpi1 == None:
                tmpi1 =  to_decimal(0.00)

            if tmpi2 == None:
                tmpi2 =  to_decimal(0.00)

            if tmpi3 == None:
                tmpi3 =  to_decimal(0.00)

            if tmpi4 == None:
                tmpi4 =  to_decimal(0.00)

            if tari == None:
                tari =  to_decimal(0.00)

            if tari1 == None:
                tari1 =  to_decimal(0.00)

            if tari2 == None:
                tari2 =  to_decimal(0.00)

            if tari3 == None:
                tari3 =  to_decimal(0.00)

            if tari4 == None:
                tari4 =  to_decimal(0.00)
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.htlname = "T O T A L"
        cl_list.saleable = tsale
        cl_list.occ_rm = tocc_rm
        cl_list.occ_rm_c = tocc_rm_c
        cl_list.occ_proz =  to_decimal(tocc_proz)
        cl_list.occ_proz_c =  to_decimal(tocc_proz_c)
        cl_list.avrgrate =  to_decimal(tavr)
        cl_list.rmrev =  to_decimal(trmrev)
        cl_list.yield_ =  to_decimal(trevpar)
        cl_list.rgi =  to_decimal(trgi)
        cl_list.mpi =  to_decimal(tmpi)
        cl_list.ari =  to_decimal(tari)
        cl_list.saleable1 = tsale1
        cl_list.occ_rm1 = tocc_rm1
        cl_list.occ_rm_c1 = tocc_rm_c1
        cl_list.occ_proz1 =  to_decimal(tocc_proz1)
        cl_list.occ_proz_c1 =  to_decimal(tocc_proz_c1)
        cl_list.avrgrate1 =  to_decimal(tavr1)
        cl_list.rmrev1 =  to_decimal(trmrev1)
        cl_list.yield1 =  to_decimal(trevpar1)
        cl_list.rgi1 =  to_decimal(trgi1)
        cl_list.mpi1 =  to_decimal(tmpi1)
        cl_list.ari1 =  to_decimal(tari1)
        cl_list.saleable2 = tsale2
        cl_list.occ_rm2 = tocc_rm2
        cl_list.occ_rm_c2 = tocc_rm_c2
        cl_list.occ_proz2 =  to_decimal(tocc_proz2)
        cl_list.occ_proz_c2 =  to_decimal(tocc_proz_c2)
        cl_list.avrgrate2 =  to_decimal(tavr2)
        cl_list.rmrev2 =  to_decimal(trmrev2)
        cl_list.yield2 =  to_decimal(trevpar2)
        cl_list.rgi2 =  to_decimal(trgi2)
        cl_list.mpi2 =  to_decimal(tmpi2)
        cl_list.ari2 =  to_decimal(tari2)
        cl_list.saleable3 = tsale3
        cl_list.occ_rm3 = tocc_rm3
        cl_list.occ_rm_c3 = tocc_rm_c3
        cl_list.occ_proz3 =  to_decimal(tocc_proz3)
        cl_list.occ_proz_c3 =  to_decimal(tocc_proz_c3)
        cl_list.avrgrate3 =  to_decimal(tavr3)
        cl_list.rmrev3 =  to_decimal(trmrev3)
        cl_list.yield3 =  to_decimal(trevpar3)
        cl_list.rgi3 =  to_decimal(trgi3)
        cl_list.mpi3 =  to_decimal(tmpi3)
        cl_list.ari3 =  to_decimal(tari3)
        cl_list.saleable4 = tsale4
        cl_list.occ_rm4 = tocc_rm4
        cl_list.occ_rm_c4 = tocc_rm_c4
        cl_list.occ_proz4 =  to_decimal(tocc_proz4)
        cl_list.occ_proz_c4 =  to_decimal(tocc_proz_c4)
        cl_list.avrgrate4 =  to_decimal(tavr4)
        cl_list.rmrev4 =  to_decimal(trmrev4)
        cl_list.yield4 =  to_decimal(trevpar4)
        cl_list.rgi4 =  to_decimal(trgi4)
        cl_list.mpi4 =  to_decimal(tmpi4)
        cl_list.ari4 =  to_decimal(tari4)
        cl_list.index_nr = 1
        cl_list.hno = 99999


    if show_ytd:
        create_umsatz1()

    return generate_output()