#using conversion tools version: 1.0.0.117
#------------------------------------------
# Rd, 11/9/2025
# baris TOTAL tidak ada.
# for loop query diganti manual
# for test in query(test_data, filters=(lambda test: not matches(test.xx,r""))):
#------------------------------------------

from functions.additional_functions import *
from decimal import Decimal
from datetime import date
from sqlalchemy import func
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.argt_betrag import argt_betrag
from models import Htparam, Waehrung, Zimmer, Artikel, Res_line, Reservation, Arrangement, Argt_line

def prepare_rm_atdrecapbl(pvilanguage:int):

    prepare_cache ([Htparam, Waehrung, Zimmer, Artikel, Res_line, Arrangement, Argt_line])

    msg_str = ""
    ci_date = None
    price_decimal = 0
    long_digit = False
    foreign_rate = False
    curr_local = ""
    curr_foreign = ""
    exchg_rate = to_decimal("0.0")
    flag_t = False
    t_occ = 0
    t_hu = 0
    t_ooo = 0
    t_com = 0
    t_vac = 0
    t_sum = 0
    t_inact = 0
    t_rev = to_decimal("0.0")
    t_nrev = to_decimal("0.0")
    t_pax = 0
    t_cpax = 0
    cl_list_data = []
    fact:Decimal = to_decimal("0.0")
    frate:Decimal = to_decimal("0.0")
    ex_rate:Decimal = to_decimal("0.0")
    lvcarea:string = "rm-ATdrecap"
    htparam = waehrung = zimmer = artikel = res_line = reservation = arrangement = argt_line = None

    test = cl_list = None

    test_data, Test = create_model("Test", {"xx":string, "yy":string})
    cl_list_data, Cl_list = create_model("Cl_list", {"flag":int, "loc":string, "etage":string, "inact":int, "occ":int, "hu":int, "ooo":int, "com":int, "vac":int, "sum":int, "pax":int, "cpax":int, "rev":Decimal, "nrev":Decimal})

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, ci_date, price_decimal, long_digit, foreign_rate, curr_local, curr_foreign, exchg_rate, flag_t, t_occ, t_hu, t_ooo, t_com, t_vac, t_sum, t_inact, t_rev, t_nrev, t_pax, t_cpax, cl_list_data, fact, frate, ex_rate, lvcarea, htparam, waehrung, zimmer, artikel, res_line, reservation, arrangement, argt_line
        nonlocal pvilanguage


        nonlocal test, cl_list
        nonlocal test_data, cl_list_data

        return {"msg_str": msg_str, "ci_date": ci_date, "price_decimal": price_decimal, "long_digit": long_digit, "foreign_rate": foreign_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "exchg_rate": exchg_rate, "flag_t": flag_t, "t_occ": t_occ, "t_hu": t_hu, "t_ooo": t_ooo, "t_com": t_com, "t_vac": t_vac, "t_sum": t_sum, "t_inact": t_inact, "t_rev": t_rev, "t_nrev": t_nrev, "t_pax": t_pax, "t_cpax": t_cpax, "cl-list": cl_list_data}

    def create_list():

        nonlocal msg_str, ci_date, price_decimal, long_digit, foreign_rate, curr_local, curr_foreign, exchg_rate, flag_t, t_occ, t_hu, t_ooo, t_com, t_vac, t_sum, t_inact, t_rev, t_nrev, t_pax, t_cpax, cl_list_data, frate, ex_rate, lvcarea, htparam, waehrung, zimmer, artikel, res_line, reservation, arrangement, argt_line
        nonlocal pvilanguage


        nonlocal test, cl_list
        nonlocal test_data, cl_list_data

        temp_loc:string = ""
        temp_et:string = ""
        status_vat:bool = False
        serv:Decimal = to_decimal("0.0")
        vat:Decimal = to_decimal("0.0")
        vat2:Decimal = to_decimal("0.0")
        fact:Decimal = to_decimal("0.0")
        serv_vat:bool = False
        argt_betrag_out:Decimal = to_decimal("0.0")
        lodging:Decimal = to_decimal("0.0")
        i:int = 0
        n:int = 0
        tmp_value:Decimal = to_decimal("0.0")
        tmp_value2:Decimal = to_decimal("0.0")
        tmp_value3:Decimal = to_decimal("0.0")
        bzimmer = None
        Bzimmer =  create_buffer("Bzimmer",Zimmer)

        bzimmer = db_session.query(Bzimmer).filter(
                 (not_(matches(Bzimmer.code,"")))).first()

        if bzimmer:
            flag_t = True

        for zimmer in db_session.query(Zimmer).order_by(Zimmer.code).all():

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.etage == to_string(zimmer.etage) and cl_list.loc == zimmer.code), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.loc = zimmer.code
                cl_list.etage = to_string(zimmer.etage)

            if zimmer.zistatus <= 2:
                cl_list.vac = cl_list.vac + 1

            elif zimmer.zistatus == 6:
                cl_list.ooo = cl_list.ooo + 1

            if not zimmer.sleeping:
                cl_list.inact = cl_list.inact + 1

        htparam = get_cache (Htparam, {"paramnr": [(eq, 479)]})
        serv_vat = htparam.flogical

        htparam = get_cache (Htparam, {"paramnr": [(eq, 127)]})
        status_vat = htparam.flogical

        artikel = get_cache (Artikel, {"artnr": [(eq, 99)],"departement": [(eq, 0)]})

        if artikel and status_vat :
            serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, ci_date))
            vat =  to_decimal(vat) + to_decimal(vat2)

        res_line_obj_list = {}
        res_line = Res_line()
        zimmer = Zimmer()
        for res_line.resnr, res_line.arrangement, res_line.erwachs, res_line.gratis, res_line.zinr, res_line.zipreis, res_line._recid, res_line.kind1, res_line.betriebsnr, res_line.reserve_dec, zimmer.etage, zimmer.code, zimmer.zistatus, zimmer._recid in db_session.query(Res_line.resnr, Res_line.arrangement, Res_line.erwachs, Res_line.gratis, Res_line.zinr, Res_line.zipreis, Res_line._recid, Res_line.kind1, Res_line.betriebsnr, Res_line.reserve_dec, Zimmer.etage, Zimmer.code, Zimmer.zistatus, Zimmer._recid).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                 ((Res_line.active_flag == 1) & (Res_line.resstatus != 12)) & (((Res_line.abreise > ci_date)) | ((Res_line.ankunft == Res_line.abreise)))).order_by(Res_line.zinr, Res_line.resnr).all():
            if res_line_obj_list.get(res_line._recid):
                continue
            else:
                res_line_obj_list[res_line._recid] = True

            reservation = get_cache (Reservation, {"resnr": [(eq, res_line.resnr)]})

            arrangement = get_cache (Arrangement, {"arrangement": [(eq, res_line.arrangement)]})
            frate =  to_decimal("1")

            if res_line.betriebsnr != 1:
                frate =  to_decimal(exchg_rate)

            elif res_line.adrflag:
                frate =  to_decimal("1")

            elif res_line.reserve_dec != 0:
                frate =  to_decimal(res_line.reserve_dec)

            cl_list = query(cl_list_data, filters=(lambda cl_list: cl_list.etage == to_string(zimmer.etage) and cl_list.loc == zimmer.code), first=True)

            if res_line.gratis > 0 or (res_line.zipreis == 0 and res_line.erwachs > 0):

                if zimmer.sleeping:
                    cl_list.com = cl_list.com + 1
                else:
                    cl_list.hu = cl_list.hu + 1
                cl_list.cpax = cl_list.cpax + res_line.gratis + res_line.erwachs

                if res_line.zipreis == 0 and res_line.erwachs > 0:
                    msg_str = msg_str + chr_unicode(2) + "&W" + translateExtended ("RmNo ", lvcarea, "") + res_line.zinr + ": Rate = 0 and Adult = " + to_string(res_line.erwachs) + " found."

            if res_line.zipreis > 0:
                lodging =  to_decimal(res_line.zipreis)

                for argt_line in db_session.query(Argt_line).filter(
                         (Argt_line.argtnr == arrangement.argtnr) & not_ (Argt_line.kind2)).order_by(Argt_line._recid).all():

                    artikel = get_cache (Artikel, {"artnr": [(eq, argt_line.argt_artnr)],"departement": [(eq, argt_line.departement)]})
                    argt_betrag_out, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                    lodging =  to_decimal(lodging) - to_decimal(argt_betrag_out)
                tmp_value =  to_decimal(lodging) * to_decimal(frate)
                lodging =  to_decimal(round (tmp_value , price_decimal))

                if foreign_rate and price_decimal == 0:

                    htparam = get_cache (Htparam, {"paramnr": [(eq, 145)]})

                    if htparam.finteger != 0:
                        n = 1
                        for i in range(1,htparam.finteger + 1) :
                            n = n * 10
                        lodging = to_decimal(round(lodging / n , 0) * n)
                cl_list.occ = cl_list.occ + 1
                cl_list.pax = cl_list.pax + res_line.erwachs + res_line.kind1
                cl_list.rev =  to_decimal(cl_list.rev) + to_decimal(lodging)
        gr_tot()

        for cl_list in query(cl_list_data, filters=(lambda cl_list: not matches(cl_list.loc,r"Gr. TOTAL")), sort_by=[("loc",True)]):

            test = query(test_data, filters=(lambda test: test.xx == cl_list.loc), first=True)

            if not test:
                test = Test()
                test_data.append(test)

                test.xx = cl_list.loc
                test.yy = ""

        for cl_list in query(cl_list_data, filters=(lambda cl_list: not matches(cl_list.etage,r"G. TOTAL")), sort_by=[("etage",True)]):

            test = query(test_data, filters=(lambda test: test.yy == cl_list.etage), first=True)

            if not test:
                test = Test()
                test_data.append(test)

                test.yy = cl_list.etage
                test.xx = ""

        for test in query(test_data, filters=(lambda test: matches(test.xx,r"") and not matches(test.yy,r"G.TOTAL"))):
            t_occ = 0
            t_hu = 0
            t_ooo = 0
            t_com = 0
            t_vac = 0
            t_sum = 0
            t_inact = 0
            t_rev =  to_decimal("0")
            t_nrev =  to_decimal("0")
            t_pax = 0
            t_cpax = 0

            for cl_list in query(cl_list_data, filters=(lambda cl_list: cl_list.etage == test.yy)):

                if fact != 0 and fact != None:
                    tmp_value2 =  to_decimal(cl_list.rev) / to_decimal(fact)
                else:
                    tmp_value2 =  to_decimal("0")
                temp_et = cl_list.etage
                temp_loc = cl_list.loc
                cl_list.sum = cl_list.occ + cl_list.hu + cl_list.ooo + cl_list.com + cl_list.vac
                cl_list.nrev =  to_decimal(round (tmp_value2 , price_decimal))
                t_occ = t_occ + cl_list.occ
                t_hu = t_hu + cl_list.hu
                t_ooo = t_ooo + cl_list.ooo
                t_com = t_com + cl_list.com
                t_vac = t_vac + cl_list.vac
                t_sum = t_sum + cl_list.sum
                t_inact = t_inact + cl_list.inact
                t_rev =  to_decimal(t_rev) + to_decimal(cl_list.rev)
                t_nrev =  to_decimal(t_nrev) + to_decimal(cl_list.nrev)
                t_pax = t_pax + cl_list.pax
                t_cpax = t_cpax + cl_list.cpax

            # Rd, 11/9/2025
            # for loop query diganti manual
            # if not matches(temp_et,r""):
            if temp_et != r"":
                cl_list = Cl_list()
                cl_list_data.append(cl_list)

                cl_list.flag = 1

                cl_list.etage = temp_et + "-TOTAL"
                cl_list.loc = ""

                cl_list.occ = t_occ
                cl_list.hu = t_hu
                cl_list.ooo = t_ooo
                cl_list.com = t_com
                cl_list.vac = t_vac
                cl_list.sum = t_sum
                cl_list.inact = t_inact
                cl_list.rev =  to_decimal(t_rev)
                cl_list.nrev =  to_decimal(t_nrev)
                cl_list.pax = t_pax
                cl_list.cpax = t_cpax
            t_occ = 0
            t_hu = 0
            t_ooo = 0
            t_com = 0
            t_vac = 0
            t_sum = 0
            t_inact = 0
            t_rev =  to_decimal("0")
            t_nrev =  to_decimal("0")
            t_pax = 0
            t_cpax = 0

        # Rd, 11/9/2025
        # for loop query diganti manual
        # for test in query(test_data, filters=(lambda test: not matches(test.xx,r""))):
        for test in test_data:
            if test.xx == "":
                continue
            t_occ = 0
            t_hu = 0
            t_ooo = 0
            t_com = 0
            t_vac = 0
            t_sum = 0
            t_inact = 0
            t_rev =  to_decimal("0")
            t_nrev =  to_decimal("0")
            t_pax = 0
            t_cpax = 0

            for cl_list in query(cl_list_data, filters=(lambda cl_list: matches(cl_list.loc,test.xx))):

                if fact != 0 and fact != None:
                    tmp_value3 =  to_decimal(cl_list.rev) / to_decimal(fact)
                else:
                    tmp_value3 =  to_decimal("0")
                temp_loc = cl_list.loc
                cl_list.sum = cl_list.occ + cl_list.hu + cl_list.ooo + cl_list.com + cl_list.vac
                cl_list.nrev =  to_decimal(round (tmp_value3 , price_decimal))
                t_occ = t_occ + cl_list.occ
                t_hu = t_hu + cl_list.hu
                t_ooo = t_ooo + cl_list.ooo
                t_com = t_com + cl_list.com
                t_vac = t_vac + cl_list.vac
                t_sum = t_sum + cl_list.sum
                t_inact = t_inact + cl_list.inact
                t_rev =  to_decimal(t_rev) + to_decimal(cl_list.rev)
                t_nrev =  to_decimal(t_nrev) + to_decimal(cl_list.nrev)
                t_pax = t_pax + cl_list.pax
                t_cpax = t_cpax + cl_list.cpax

            cl_list = Cl_list()
            cl_list_data.append(cl_list)
            cl_list.flag = 1
            cl_list.loc = temp_loc + "-TOTAL"
            cl_list.etage = ""
            cl_list.occ = t_occ
            cl_list.hu = t_hu
            cl_list.ooo = t_ooo
            cl_list.com = t_com
            cl_list.vac = t_vac
            cl_list.sum = t_sum
            cl_list.inact = t_inact
            cl_list.rev =  to_decimal(t_rev)
            cl_list.nrev =  to_decimal(t_nrev)
            cl_list.pax = t_pax
            cl_list.cpax = t_cpax
            t_occ = 0
            t_hu = 0
            t_ooo = 0
            t_com = 0
            t_vac = 0
            t_sum = 0
            t_inact = 0
            t_rev =  to_decimal("0")
            t_nrev =  to_decimal("0")
            t_pax = 0
            t_cpax = 0


    def gr_tot():

        nonlocal msg_str, ci_date, price_decimal, long_digit, foreign_rate, curr_local, curr_foreign, exchg_rate, flag_t, t_occ, t_hu, t_ooo, t_com, t_vac, t_sum, t_inact, t_rev, t_nrev, t_pax, t_cpax, cl_list_data, fact, frate, ex_rate, lvcarea, htparam, waehrung, zimmer, artikel, res_line, reservation, arrangement, argt_line
        nonlocal pvilanguage


        nonlocal test, cl_list
        nonlocal test_data, cl_list_data

        tmp_cl:Decimal = to_decimal("0.0")
        t_etage:int = 0
        t_occ = 0
        t_hu = 0
        t_ooo = 0
        t_com = 0
        t_vac = 0
        t_sum = 0
        t_inact = 0
        t_rev =  to_decimal("0")
        t_nrev =  to_decimal("0")
        t_pax = 0
        t_cpax = 0

        for cl_list in query(cl_list_data, sort_by=[("etage",False)]):

            if fact != 0 and fact != None:
                tmp_cl =  to_decimal(cl_list.rev) / to_decimal(fact)
            else:
                tmp_cl =  to_decimal("0")
            cl_list.sum = cl_list.occ + cl_list.hu + cl_list.ooo + cl_list.com + cl_list.vac
            cl_list.nrev =  to_decimal(round (tmp_cl , price_decimal))
            t_occ = t_occ + cl_list.occ
            t_hu = t_hu + cl_list.hu
            t_ooo = t_ooo + cl_list.ooo
            t_com = t_com + cl_list.com
            t_vac = t_vac + cl_list.vac
            t_sum = t_sum + cl_list.sum
            t_inact = t_inact + cl_list.inact
            t_rev =  to_decimal(t_rev) + to_decimal(cl_list.rev)
            t_nrev =  to_decimal(t_nrev) + to_decimal(cl_list.nrev)
            t_pax = t_pax + cl_list.pax
            t_cpax = t_cpax + cl_list.cpax

        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 1
        cl_list.loc = "Gr. TOTAL"
        cl_list.etage = ""
        cl_list.occ = t_occ
        cl_list.hu = t_hu
        cl_list.ooo = t_ooo
        cl_list.com = t_com
        cl_list.vac = t_vac
        cl_list.sum = t_sum
        cl_list.inact = t_inact
        cl_list.rev =  to_decimal(t_rev)
        cl_list.nrev =  to_decimal(t_nrev)
        cl_list.pax = t_pax
        cl_list.cpax = t_cpax

        if t_etage == 0:
            t_etage = 999
        cl_list = Cl_list()
        cl_list_data.append(cl_list)

        cl_list.flag = 1
        cl_list.loc = ""
        cl_list.etage = "G.TOTAL"
        cl_list.occ = t_occ
        cl_list.hu = t_hu
        cl_list.ooo = t_ooo
        cl_list.com = t_com
        cl_list.vac = t_vac
        cl_list.sum = t_sum
        cl_list.inact = t_inact
        cl_list.rev =  to_decimal(t_rev)
        cl_list.nrev =  to_decimal(t_nrev)
        cl_list.pax = t_pax
        cl_list.cpax = t_cpax


        t_occ = 0
        t_hu = 0
        t_ooo = 0
        t_com = 0
        t_vac = 0
        t_sum = 0
        t_inact = 0
        t_rev =  to_decimal("0")
        t_nrev =  to_decimal("0")
        t_pax = 0
        t_cpax = 0

    htparam = get_cache (Htparam, {"paramnr": [(eq, 110)]})
    ci_date = htparam.fdate

    htparam = get_cache (Htparam, {"paramnr": [(eq, 491)]})
    price_decimal = htparam.finteger

    htparam = get_cache (Htparam, {"paramnr": [(eq, 246)]})
    long_digit = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 240)]})
    foreign_rate = htparam.flogical

    htparam = get_cache (Htparam, {"paramnr": [(eq, 152)]})
    curr_local = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})
    curr_foreign = htparam.fchar

    htparam = get_cache (Htparam, {"paramnr": [(eq, 144)]})

    waehrung = get_cache (Waehrung, {"wabkurz": [(eq, htparam.fchar)]})

    if waehrung:
        exchg_rate =  to_decimal(waehrung.ankauf) / to_decimal(waehrung.einheit)
    else:
        exchg_rate =  to_decimal("1")

    create_list()

    return generate_output()