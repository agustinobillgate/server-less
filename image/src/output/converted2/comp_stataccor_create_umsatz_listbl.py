#using conversion tools version: 1.0.0.111

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from models import Zinrstat, Akt_code

def comp_stataccor_create_umsatz_listbl(pvilanguage:int, to_date:date, show_ytd:bool):

    prepare_cache ([Zinrstat, Akt_code])

    cl_list_list = []
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
    lvcarea:string = "comp-stataccor"
    zinrstat = akt_code = None

    cl_list = t_zinrstat = None

    cl_list_list, Cl_list = create_model("Cl_list", {"hno":int, "htlname":string, "occ_rm":int, "occ_rm_c":int, "saleable":int, "rmrev":Decimal, "avrgrate":Decimal, "yield_":Decimal, "nat_mark":Decimal, "mark_share":Decimal, "revpar":Decimal, "rgi":Decimal, "mpi":Decimal, "ari":Decimal, "occ_proz":Decimal, "occ_proz_c":Decimal, "occ_rm1":int, "occ_rm_c1":int, "saleable1":int, "rmrev1":Decimal, "avrgrate1":Decimal, "yield1":Decimal, "nat_mark1":Decimal, "mark_share1":Decimal, "revpar1":Decimal, "rgi1":Decimal, "mpi1":Decimal, "ari1":Decimal, "occ_proz1":Decimal, "occ_proz_c1":Decimal, "occ_rm2":int, "occ_rm_c2":int, "saleable2":int, "rmrev2":Decimal, "avrgrate2":Decimal, "yield2":Decimal, "nat_mark2":Decimal, "mark_share2":Decimal, "revpar2":Decimal, "rgi2":Decimal, "mpi2":Decimal, "ari2":Decimal, "occ_proz2":Decimal, "occ_proz_c2":Decimal, "occ_rm3":int, "occ_rm_c3":int, "saleable3":int, "rmrev3":Decimal, "avrgrate3":Decimal, "yield3":Decimal, "nat_mark3":Decimal, "mark_share3":Decimal, "revpar3":Decimal, "rgi3":Decimal, "mpi3":Decimal, "ari3":Decimal, "occ_proz3":Decimal, "occ_proz_c3":Decimal, "occ_rm4":int, "occ_rm_c4":int, "saleable4":int, "rmrev4":Decimal, "avrgrate4":Decimal, "yield4":Decimal, "nat_mark4":Decimal, "mark_share4":Decimal, "revpar4":Decimal, "rgi4":Decimal, "mpi4":Decimal, "ari4":Decimal, "occ_proz4":Decimal, "occ_proz_c4":Decimal, "index_nr":int})

    T_zinrstat = create_buffer("T_zinrstat",Zinrstat)


    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_list, tsale, tsale1, tocc_rm, tocc_rm1, tocc_rm_c, tocc_rm_c1, tot_hotel, tocc_rm2, tocc_rm3, tocc_rm4, tocc_rm_c2, tocc_rm_c3, tocc_rm_c4, tsale2, tsale3, tsale4, trmrev, trmrev1, trmrev2, trmrev3, trmrev4, tavr, tavr1, tavr2, tavr3, tavr4, tocc_proz, tocc_proz1, tocc_proz2, tocc_proz3, tocc_proz4, tocc_proz_c, tocc_proz_c1, tocc_proz_c2, tocc_proz_c3, tocc_proz_c4, trevpar, trevpar1, trevpar2, trevpar3, trevpar4, trgi, trgi1, trgi2, trgi3, trgi4, tmpi, tmpi1, tmpi2, tmpi3, tmpi4, tari, tari1, tari2, tari3, tari4, from_date, last_fdate, last_tdate, lvcarea, zinrstat, akt_code
        nonlocal pvilanguage, to_date, show_ytd
        nonlocal t_zinrstat


        nonlocal cl_list, t_zinrstat
        nonlocal cl_list_list

        return {"cl-list": cl_list_list}

    def get_totalhtl():

        nonlocal cl_list_list, tsale, tsale1, tocc_rm, tocc_rm1, tocc_rm_c, tocc_rm_c1, tot_hotel, tocc_rm2, tocc_rm3, tocc_rm4, tocc_rm_c2, tocc_rm_c3, tocc_rm_c4, tsale2, tsale3, tsale4, trmrev, trmrev1, trmrev2, trmrev3, trmrev4, tavr, tavr1, tavr2, tavr3, tavr4, tocc_proz, tocc_proz1, tocc_proz2, tocc_proz3, tocc_proz4, tocc_proz_c, tocc_proz_c1, tocc_proz_c2, tocc_proz_c3, tocc_proz_c4, trevpar, trevpar1, trevpar2, trevpar3, trevpar4, trgi, trgi1, trgi2, trgi3, trgi4, tmpi, tmpi1, tmpi2, tmpi3, tmpi4, tari, tari1, tari2, tari3, tari4, from_date, last_fdate, last_tdate, lvcarea, zinrstat, akt_code
        nonlocal pvilanguage, to_date, show_ytd
        nonlocal t_zinrstat


        nonlocal cl_list, t_zinrstat
        nonlocal cl_list_list


        tot_hotel = 0

        for akt_code in db_session.query(Akt_code).filter(
                 (Akt_code.aktiongrup == 4)).order_by(Akt_code._recid).all():
            tot_hotel = tot_hotel + 1


    def create_umsatz():

        nonlocal cl_list_list, tsale, tsale1, tocc_rm, tocc_rm1, tocc_rm_c, tocc_rm_c1, tot_hotel, tocc_rm2, tocc_rm3, tocc_rm4, tocc_rm_c2, tocc_rm_c3, tocc_rm_c4, tsale2, tsale3, tsale4, trmrev, trmrev1, trmrev2, trmrev3, trmrev4, tavr, tavr1, tavr2, tavr3, tavr4, tocc_proz, tocc_proz1, tocc_proz2, tocc_proz3, tocc_proz4, tocc_proz_c, tocc_proz_c1, tocc_proz_c2, tocc_proz_c3, tocc_proz_c4, trevpar, trevpar1, trevpar2, trevpar3, trevpar4, trgi, trgi1, trgi2, trgi3, trgi4, tmpi, tmpi1, tmpi2, tmpi3, tmpi4, tari, tari1, tari2, tari3, tari4, from_date, last_fdate, last_tdate, lvcarea, zinrstat, akt_code
        nonlocal pvilanguage, to_date, show_ytd
        nonlocal t_zinrstat


        nonlocal cl_list, t_zinrstat
        nonlocal cl_list_list

        str1:string = ""
        str2:string = ""
        str3:string = ""
        str4:string = ""
        err:string = ""
        get_totalhtl()
        cl_list_list.clear()
        tocc_rm = 0
        tocc_rm1 = 0
        tocc_rm2 = 0
        tsale = 0
        tsale1 = 0
        tsale2 = 0
        trmrev =  to_decimal("0")
        trmrev1 =  to_decimal("0")
        trmrev2 =  to_decimal("0")
        tocc_proz =  to_decimal("0")
        tocc_proz1 =  to_decimal("0")
        tocc_proz2 =  to_decimal("0")
        trevpar =  to_decimal("0")
        trevpar1 =  to_decimal("0")
        trevpar2 =  to_decimal("0")
        trgi =  to_decimal("0")
        trgi1 =  to_decimal("0")
        trgi2 =  to_decimal("0")
        tmpi =  to_decimal("0")
        tmpi1 =  to_decimal("0")
        tmpi2 =  to_decimal("0")
        tari =  to_decimal("0")
        tari1 =  to_decimal("0")
        tari2 =  to_decimal("0")


        from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

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
                cl_list.occ_rm = cl_list.occ_rm + zinrstat.personen
                cl_list.occ_rm_c = cl_list.occ_rm_c + (zinrstat.personen + to_int(zinrstat.argtumsatz))
                cl_list.saleable = cl_list.saleable + zinrstat.zimmeranz
                cl_list.rmrev =  to_decimal(cl_list.rmrev) + to_decimal(zinrstat.logisumsatz)

            if get_month(zinrstat.datum) == get_month(to_date) and get_year(zinrstat.datum) == get_year(to_date):
                cl_list.occ_rm1 = cl_list.occ_rm1 + zinrstat.personen
                cl_list.occ_rm_c1 = cl_list.occ_rm_c1 + (zinrstat.personen + to_int(zinrstat.argtumsatz))
                cl_list.saleable1 = cl_list.saleable1 + zinrstat.zimmeranz
                cl_list.rmrev1 =  to_decimal(cl_list.rmrev1) + to_decimal(zinrstat.logisumsatz)

            if cl_list.saleable != 0:
                cl_list.occ_proz =  to_decimal(cl_list.occ_rm) / to_decimal(cl_list.saleable) * to_decimal("100")
                cl_list.occ_proz_c =  to_decimal(cl_list.occ_rm_c) / to_decimal(cl_list.saleable) * to_decimal("100")

            if cl_list.saleable1 != 0:
                cl_list.occ_proz1 =  to_decimal(cl_list.occ_rm1) / to_decimal(cl_list.saleable1) * to_decimal("100")
                cl_list.occ_proz_c1 =  to_decimal(cl_list.occ_rm_c1) / to_decimal(cl_list.saleable1) * to_decimal("100")

            if cl_list.occ_rm != 0:
                cl_list.avrgrate =  to_decimal(cl_list.rmrev) / to_decimal(cl_list.occ_rm)

            if cl_list.occ_rm1 != 0:
                cl_list.avrgrate1 =  to_decimal(cl_list.rmrev1) / to_decimal(cl_list.occ_rm1)

            if cl_list.saleable != 0:
                cl_list.yield_ =  to_decimal(cl_list.rmrev) / to_decimal(cl_list.saleable)

            if cl_list.saleable1 != 0:
                cl_list.yield1 =  to_decimal(cl_list.rmrev1) / to_decimal(cl_list.saleable1)

        for cl_list in query(cl_list_list):
            tocc_rm = tocc_rm + cl_list.occ_rm
            tocc_rm_c = tocc_rm_c + cl_list.occ_rm_c
            tocc_rm1 = tocc_rm1 + cl_list.occ_rm1
            tocc_rm_c1 = tocc_rm_c1 + cl_list.occ_rm_c1
            tsale = tsale + cl_list.saleable
            tsale1 = tsale1 + cl_list.saleable1
            trmrev1 =  to_decimal(trmrev1) + to_decimal(cl_list.rmrev1)
            trmrev =  to_decimal(trmrev) + to_decimal(cl_list.rmrev)


        tavr =  to_decimal(trmrev) / to_decimal(tocc_rm)
        tavr1 =  to_decimal(trmrev1) / to_decimal(tocc_rm1)
        tocc_proz = ( to_decimal(tocc_rm) / to_decimal(tsale)) * to_decimal("100")
        tocc_proz_c = ( to_decimal(tocc_rm_c) / to_decimal(tsale)) * to_decimal("100")
        tocc_proz1 = ( to_decimal(tocc_rm1) / to_decimal(tsale1)) * to_decimal("100")
        tocc_proz_c1 = ( to_decimal(tocc_rm_c1) / to_decimal(tsale1)) * to_decimal("100")
        trevpar =  to_decimal(trmrev) / to_decimal(tsale)
        trevpar1 =  to_decimal(trmrev1) / to_decimal(tsale1)

        if tocc_rm == None:
            tocc_rm = 0.00

        if tocc_rm_c == None:
            tocc_rm_c = 0.00

        if tocc_rm1 == None:
            tocc_rm1 = 0.00

        if tocc_rm_c1 == None:
            tocc_rm_c1 = 0.00

        if tsale == None:
            tsale = 0.00

        if tsale1 == None:
            tsale1 = 0.00

        if trmrev == None:
            trmrev =  to_decimal(0.00)

        if trmrev1 == None:
            trmrev1 =  to_decimal(0.00)

        if tavr == None:
            tavr =  to_decimal(0.00)

        if tavr1 == None:
            tavr1 =  to_decimal(0.00)

        if tocc_proz == None:
            tocc_proz =  to_decimal(0.00)

        if tocc_proz_c == None:
            tocc_proz_c =  to_decimal(0.00)

        if tocc_proz1 == None:
            tocc_proz1 =  to_decimal(0.00)

        if tocc_proz_c1 == None:
            tocc_proz_c1 =  to_decimal(0.00)

        if trevpar == None:
            trevpar =  to_decimal(0.00)

        if trevpar1 == None:
            trevpar1 =  to_decimal(0.00)

        for cl_list in query(cl_list_list):

            if cl_list.saleable != 0:
                cl_list.mpi =  to_decimal(cl_list.occ_proz) / to_decimal(tocc_proz)

            if cl_list.saleable != 0 and cl_list.rmrev != 0:
                cl_list.rgi =  to_decimal(cl_list.yield_) / to_decimal(trevpar)
            cl_list.ari =  to_decimal(cl_list.avrgrate) / to_decimal(tavr)

            if cl_list.saleable1 != 0:
                cl_list.mpi1 =  to_decimal(cl_list.occ_proz1) / to_decimal(tocc_proz1)

            if cl_list.saleable1 != 0 and cl_list.rmrev1 != 0:
                cl_list.rgi1 =  to_decimal(cl_list.yield1) / to_decimal(trevpar1)
            cl_list.ari1 =  to_decimal(cl_list.avrgrate1) / to_decimal(tavr1)

            if cl_list.ari == None:
                cl_list.ari =  to_decimal(0.00)

            if cl_list.ari1 == None:
                cl_list.ari1 =  to_decimal(0.00)

            if cl_list.mpi == None:
                cl_list.mpi =  to_decimal(0.00)

            if cl_list.mpi1 == None:
                cl_list.mpi1 =  to_decimal(0.00)

            if cl_list.rgi == None:
                cl_list.rgi =  to_decimal(0.00)

            if cl_list.rgi1 == None:
                cl_list.rgi1 =  to_decimal(0.00)
            trgi =  to_decimal(trevpar) / to_decimal(trevpar)
            trgi1 =  to_decimal(trevpar1) / to_decimal(trevpar1)
            tmpi =  to_decimal(tocc_proz) / to_decimal(tocc_proz)
            tmpi1 =  to_decimal(tocc_proz1) / to_decimal(tocc_proz1)
            tari =  to_decimal(tavr) / to_decimal(tavr)
            tari1 =  to_decimal(tavr1) / to_decimal(tavr1)

            if trgi == None:
                trgi =  to_decimal(0.00)

            if trgi1 == None:
                trgi1 =  to_decimal(0.00)

            if tmpi == None:
                tmpi =  to_decimal(0.00)

            if tmpi1 == None:
                tmpi1 =  to_decimal(0.00)

            if tari == None:
                tari =  to_decimal(0.00)

            if tari1 == None:
                tari1 =  to_decimal(0.00)
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.htlname = to_string("T O T A L", "x(24) ")
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
        cl_list.index_nr = 1
        cl_list.hno = 99999


    if not show_ytd:
        create_umsatz()

    return generate_output()