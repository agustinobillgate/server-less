from functions.additional_functions import *
import decimal
from datetime import date
from sqlalchemy import func
from models import Zinrstat, Akt_code

def comp_stataccor_create_umsatz_listbl(pvilanguage:int, to_date:date, show_ytd:bool):
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
    trmrev:decimal = 0
    trmrev1:decimal = 0
    trmrev2:decimal = 0
    trmrev3:decimal = 0
    trmrev4:decimal = 0
    tavr:decimal = 0
    tavr1:decimal = 0
    tavr2:decimal = 0
    tavr3:decimal = 0
    tavr4:decimal = 0
    tocc_proz:decimal = 0
    tocc_proz1:decimal = 0
    tocc_proz2:decimal = 0
    tocc_proz3:decimal = 0
    tocc_proz4:decimal = 0
    tocc_proz_c:decimal = 0
    tocc_proz_c1:decimal = 0
    tocc_proz_c2:decimal = 0
    tocc_proz_c3:decimal = 0
    tocc_proz_c4:decimal = 0
    trevpar:decimal = 0
    trevpar1:decimal = 0
    trevpar2:decimal = 0
    trevpar3:decimal = 0
    trevpar4:decimal = 0
    trgi:decimal = 0
    trgi1:decimal = 0
    trgi2:decimal = 0
    trgi3:decimal = 0
    trgi4:decimal = 0
    tmpi:decimal = 0
    tmpi1:decimal = 0
    tmpi2:decimal = 0
    tmpi3:decimal = 0
    tmpi4:decimal = 0
    tari:decimal = 0
    tari1:decimal = 0
    tari2:decimal = 0
    tari3:decimal = 0
    tari4:decimal = 0
    from_date:date = None
    last_fdate:date = None
    last_tdate:date = None
    lvcarea:str = "comp_stataccor"
    zinrstat = akt_code = None

    cl_list = t_zinrstat = None

    cl_list_list, Cl_list = create_model("Cl_list", {"hno":int, "htlname":str, "occ_rm":int, "occ_rm_c":int, "saleable":int, "rmrev":decimal, "avrgrate":decimal, "yield_":decimal, "nat_mark":decimal, "mark_share":decimal, "revpar":decimal, "rgi":decimal, "mpi":decimal, "ari":decimal, "occ_proz":decimal, "occ_proz_c":decimal, "occ_rm1":int, "occ_rm_c1":int, "saleable1":int, "rmrev1":decimal, "avrgrate1":decimal, "yield1":decimal, "nat_mark1":decimal, "mark_share1":decimal, "revpar1":decimal, "rgi1":decimal, "mpi1":decimal, "ari1":decimal, "occ_proz1":decimal, "occ_proz_c1":decimal, "occ_rm2":int, "occ_rm_c2":int, "saleable2":int, "rmrev2":decimal, "avrgrate2":decimal, "yield2":decimal, "nat_mark2":decimal, "mark_share2":decimal, "revpar2":decimal, "rgi2":decimal, "mpi2":decimal, "ari2":decimal, "occ_proz2":decimal, "occ_proz_c2":decimal, "occ_rm3":int, "occ_rm_c3":int, "saleable3":int, "rmrev3":decimal, "avrgrate3":decimal, "yield3":decimal, "nat_mark3":decimal, "mark_share3":decimal, "revpar3":decimal, "rgi3":decimal, "mpi3":decimal, "ari3":decimal, "occ_proz3":decimal, "occ_proz_c3":decimal, "occ_rm4":int, "occ_rm_c4":int, "saleable4":int, "rmrev4":decimal, "avrgrate4":decimal, "yield4":decimal, "nat_mark4":decimal, "mark_share4":decimal, "revpar4":decimal, "rgi4":decimal, "mpi4":decimal, "ari4":decimal, "occ_proz4":decimal, "occ_proz_c4":decimal, "index_nr":int})

    T_zinrstat = Zinrstat

    db_session = local_storage.db_session

    def generate_output():
        nonlocal cl_list_list, tsale, tsale1, tocc_rm, tocc_rm1, tocc_rm_c, tocc_rm_c1, tot_hotel, tocc_rm2, tocc_rm3, tocc_rm4, tocc_rm_c2, tocc_rm_c3, tocc_rm_c4, tsale2, tsale3, tsale4, trmrev, trmrev1, trmrev2, trmrev3, trmrev4, tavr, tavr1, tavr2, tavr3, tavr4, tocc_proz, tocc_proz1, tocc_proz2, tocc_proz3, tocc_proz4, tocc_proz_c, tocc_proz_c1, tocc_proz_c2, tocc_proz_c3, tocc_proz_c4, trevpar, trevpar1, trevpar2, trevpar3, trevpar4, trgi, trgi1, trgi2, trgi3, trgi4, tmpi, tmpi1, tmpi2, tmpi3, tmpi4, tari, tari1, tari2, tari3, tari4, from_date, last_fdate, last_tdate, lvcarea, zinrstat, akt_code
        nonlocal t_zinrstat


        nonlocal cl_list, t_zinrstat
        nonlocal cl_list_list
        return {"cl-list": cl_list_list}

    def get_totalhtl():

        nonlocal cl_list_list, tsale, tsale1, tocc_rm, tocc_rm1, tocc_rm_c, tocc_rm_c1, tot_hotel, tocc_rm2, tocc_rm3, tocc_rm4, tocc_rm_c2, tocc_rm_c3, tocc_rm_c4, tsale2, tsale3, tsale4, trmrev, trmrev1, trmrev2, trmrev3, trmrev4, tavr, tavr1, tavr2, tavr3, tavr4, tocc_proz, tocc_proz1, tocc_proz2, tocc_proz3, tocc_proz4, tocc_proz_c, tocc_proz_c1, tocc_proz_c2, tocc_proz_c3, tocc_proz_c4, trevpar, trevpar1, trevpar2, trevpar3, trevpar4, trgi, trgi1, trgi2, trgi3, trgi4, tmpi, tmpi1, tmpi2, tmpi3, tmpi4, tari, tari1, tari2, tari3, tari4, from_date, last_fdate, last_tdate, lvcarea, zinrstat, akt_code
        nonlocal t_zinrstat


        nonlocal cl_list, t_zinrstat
        nonlocal cl_list_list


        tot_hotel = 0

        for akt_code in db_session.query(Akt_code).filter(
                (Akt_code.aktiongrup == 4)).all():
            tot_hotel = tot_hotel + 1

    def create_umsatz():

        nonlocal cl_list_list, tsale, tsale1, tocc_rm, tocc_rm1, tocc_rm_c, tocc_rm_c1, tot_hotel, tocc_rm2, tocc_rm3, tocc_rm4, tocc_rm_c2, tocc_rm_c3, tocc_rm_c4, tsale2, tsale3, tsale4, trmrev, trmrev1, trmrev2, trmrev3, trmrev4, tavr, tavr1, tavr2, tavr3, tavr4, tocc_proz, tocc_proz1, tocc_proz2, tocc_proz3, tocc_proz4, tocc_proz_c, tocc_proz_c1, tocc_proz_c2, tocc_proz_c3, tocc_proz_c4, trevpar, trevpar1, trevpar2, trevpar3, trevpar4, trgi, trgi1, trgi2, trgi3, trgi4, tmpi, tmpi1, tmpi2, tmpi3, tmpi4, tari, tari1, tari2, tari3, tari4, from_date, last_fdate, last_tdate, lvcarea, zinrstat, akt_code
        nonlocal t_zinrstat


        nonlocal cl_list, t_zinrstat
        nonlocal cl_list_list

        str1:str = ""
        str2:str = ""
        str3:str = ""
        str4:str = ""
        err:str = ""
        get_totalhtl()
        cl_list_list.clear()
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
        trevpar = 0
        trevpar1 = 0
        trevpar2 = 0
        trgi = 0
        trgi1 = 0
        trgi2 = 0
        tmpi = 0
        tmpi1 = 0
        tmpi2 = 0
        tari = 0
        tari1 = 0
        tari2 = 0


        from_date = date_mdy(get_month(to_date) , 1, get_year(to_date))

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
                cl_list.occ_rm_c = cl_list.occ_rm_c + (zinrstat.personen + to_int(zinrstat.argtumsatz))
                cl_list.saleable = cl_list.saleable + zinrstat.zimmeranz
                cl_list.rmrev = cl_list.rmrev + zinrstat.logisumsatz

            if get_month(zinrstat.datum) == get_month(to_date) and get_year(zinrstat.datum) == get_year(to_date):
                cl_list.occ_rm1 = cl_list.occ_rm1 + zinrstat.personen
                cl_list.occ_rm_c1 = cl_list.occ_rm_c1 + (zinrstat.personen + to_int(zinrstat.argtumsatz))
                cl_list.saleable1 = cl_list.saleable1 + zinrstat.zimmeranz
                cl_list.rmrev1 = cl_list.rmrev1 + zinrstat.logisumsatz

            if cl_list.saleable != 0:
                cl_list.occ_proz = cl_list.occ_rm / cl_list.saleable * 100
                cl_list.occ_proz_c = cl_list.occ_rm_c / cl_list.saleable * 100

            if cl_list.saleable1 != 0:
                cl_list.occ_proz1 = cl_list.occ_rm1 / cl_list.saleable1 * 100
                cl_list.occ_proz_c1 = cl_list.occ_rm_c1 / cl_list.saleable1 * 100

            if cl_list.occ_rm != 0:
                cl_list.avrgrate = cl_list.rmrev / cl_list.occ_rm

            if cl_list.occ_rm1 != 0:
                cl_list.avrgrate1 = cl_list.rmrev1 / cl_list.occ_rm1

            if cl_list.saleable != 0:
                cl_list.yield_ = cl_list.rmrev / cl_list.saleable

            if cl_list.saleable1 != 0:
                cl_list.yield1 = cl_list.rmrev1 / cl_list.saleable1

        for cl_list in query(cl_list_list):
            tocc_rm = tocc_rm + cl_list.occ_rm
            tocc_rm_c = tocc_rm_c + cl_list.occ_rm_c
            tocc_rm1 = tocc_rm1 + cl_list.occ_rm1
            tocc_rm_c1 = tocc_rm_c1 + cl_list.occ_rm_c1
            tsale = tsale + cl_list.saleable
            tsale1 = tsale1 + cl_list.saleable1
            trmrev1 = trmrev1 + cl_list.rmrev1
            trmrev = trmrev + cl_list.rmrev


        tavr = trmrev / tocc_rm
        tavr1 = trmrev1 / tocc_rm1
        tocc_proz = (tocc_rm / tsale) * 100
        tocc_proz_c = (tocc_rm_c / tsale) * 100
        tocc_proz1 = (tocc_rm1 / tsale1) * 100
        tocc_proz_c1 = (tocc_rm_c1 / tsale1) * 100
        trevpar = trmrev / tsale
        trevpar1 = trmrev1 / tsale1

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
            trmrev = 0.00

        if trmrev1 == None:
            trmrev1 = 0.00

        if tavr == None:
            tavr = 0.00

        if tavr1 == None:
            tavr1 = 0.00

        if tocc_proz == None:
            tocc_proz = 0.00

        if tocc_proz_c == None:
            tocc_proz_c = 0.00

        if tocc_proz1 == None:
            tocc_proz1 = 0.00

        if tocc_proz_c1 == None:
            tocc_proz_c1 = 0.00

        if trevpar == None:
            trevpar = 0.00

        if trevpar1 == None:
            trevpar1 = 0.00

        for cl_list in query(cl_list_list):

            if cl_list.saleable != 0:
                cl_list.mpi = cl_list.occ_proz / tocc_proz

            if cl_list.saleable != 0 and cl_list.rmrev != 0:
                cl_list.rgi = cl_list.yield_ / trevpar
            cl_list.ari = cl_list.avrgrate / tavr

            if cl_list.saleable1 != 0:
                cl_list.mpi1 = cl_list.occ_proz1 / tocc_proz1

            if cl_list.saleable1 != 0 and cl_list.rmrev1 != 0:
                cl_list.rgi1 = cl_list.yield1 / trevpar1
            cl_list.ari1 = cl_list.avrgrate1 / tavr1

            if cl_list.ari == None:
                cl_list.ari = 0.00

            if cl_list.ari1 == None:
                cl_list.ari1 = 0.00

            if cl_list.mpi == None:
                cl_list.mpi = 0.00

            if cl_list.mpi1 == None:
                cl_list.mpi1 = 0.00

            if cl_list.rgi == None:
                cl_list.rgi = 0.00

            if cl_list.rgi1 == None:
                cl_list.rgi1 = 0.00
            trgi = trevpar / trevpar
            trgi1 = trevpar1 / trevpar1
            tmpi = tocc_proz / tocc_proz
            tmpi1 = tocc_proz1 / tocc_proz1
            tari = tavr / tavr
            tari1 = tavr1 / tavr1

            if trgi == None:
                trgi = 0.00

            if trgi1 == None:
                trgi1 = 0.00

            if tmpi == None:
                tmpi = 0.00

            if tmpi1 == None:
                tmpi1 = 0.00

            if tari == None:
                tari = 0.00

            if tari1 == None:
                tari1 = 0.00
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.htlname = to_string("T O T A L", "x(24) ")
        cl_list.saleable = tsale
        cl_list.occ_rm = tocc_rm
        cl_list.occ_rm_c = tocc_rm_c
        cl_list.occ_proz = tocc_proz
        cl_list.occ_proz_c = tocc_proz_c
        cl_list.avrgrate = tavr
        cl_list.rmrev = trmrev
        cl_list.yield_ = trevpar
        cl_list.rgi = trgi
        cl_list.mpi = tmpi
        cl_list.ari = tari
        cl_list.saleable1 = tsale1
        cl_list.occ_rm1 = tocc_rm1
        cl_list.occ_rm_c1 = tocc_rm_c1
        cl_list.occ_proz1 = tocc_proz1
        cl_list.occ_proz_c1 = tocc_proz_c1
        cl_list.avrgrate1 = tavr1
        cl_list.rmrev1 = trmrev1
        cl_list.yield1 = trevpar1
        cl_list.rgi1 = trgi1
        cl_list.mpi1 = tmpi1
        cl_list.ari1 = tari1
        cl_list.index_nr = 1
        cl_list.hno = 99999

    if not show_ytd:
        create_umsatz()

    return generate_output()