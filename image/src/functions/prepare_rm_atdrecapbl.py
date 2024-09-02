from functions.additional_functions import *
import decimal
from datetime import date
from functions.calc_servtaxesbl import calc_servtaxesbl
from functions.argt_betrag import argt_betrag
import re
from models import Htparam, Waehrung, Zimmer, Artikel, Res_line, Reservation, Arrangement, Argt_line

def prepare_rm_atdrecapbl(pvilanguage:int):
    msg_str = ""
    ci_date = None
    price_decimal = 0
    long_digit = False
    foreign_rate = False
    curr_local = ""
    curr_foreign = ""
    exchg_rate = 0
    flag_t = False
    t_occ = 0
    t_hu = 0
    t_ooo = 0
    t_com = 0
    t_vac = 0
    t_sum = 0
    t_inact = 0
    t_rev = 0
    t_nrev = 0
    t_pax = 0
    t_cpax = 0
    cl_list_list = []
    fact:decimal = 0
    frate:decimal = 0
    ex_rate:decimal = 0
    lvcarea:str = "rm_ATdrecap"
    htparam = waehrung = zimmer = artikel = res_line = reservation = arrangement = argt_line = None

    test = cl_list = bzimmer = None

    test_list, Test = create_model("Test", {"xx":str, "yy":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":int, "loc":str, "etage":str, "inact":int, "occ":int, "hu":int, "ooo":int, "com":int, "vac":int, "sum":int, "pax":int, "cpax":int, "rev":decimal, "nrev":decimal})

    Bzimmer = Zimmer

    db_session = local_storage.db_session

    def generate_output():
        nonlocal msg_str, ci_date, price_decimal, long_digit, foreign_rate, curr_local, curr_foreign, exchg_rate, flag_t, t_occ, t_hu, t_ooo, t_com, t_vac, t_sum, t_inact, t_rev, t_nrev, t_pax, t_cpax, cl_list_list, fact, frate, ex_rate, lvcarea, htparam, waehrung, zimmer, artikel, res_line, reservation, arrangement, argt_line
        nonlocal bzimmer


        nonlocal test, cl_list, bzimmer
        nonlocal test_list, cl_list_list
        return {"msg_str": msg_str, "ci_date": ci_date, "price_decimal": price_decimal, "long_digit": long_digit, "foreign_rate": foreign_rate, "curr_local": curr_local, "curr_foreign": curr_foreign, "exchg_rate": exchg_rate, "flag_t": flag_t, "t_occ": t_occ, "t_hu": t_hu, "t_ooo": t_ooo, "t_com": t_com, "t_vac": t_vac, "t_sum": t_sum, "t_inact": t_inact, "t_rev": t_rev, "t_nrev": t_nrev, "t_pax": t_pax, "t_cpax": t_cpax, "cl-list": cl_list_list}

    def create_list():

        nonlocal msg_str, ci_date, price_decimal, long_digit, foreign_rate, curr_local, curr_foreign, exchg_rate, flag_t, t_occ, t_hu, t_ooo, t_com, t_vac, t_sum, t_inact, t_rev, t_nrev, t_pax, t_cpax, cl_list_list, fact, frate, ex_rate, lvcarea, htparam, waehrung, zimmer, artikel, res_line, reservation, arrangement, argt_line
        nonlocal bzimmer


        nonlocal test, cl_list, bzimmer
        nonlocal test_list, cl_list_list

        temp_loc:str = ""
        temp_et:str = ""
        status_vat:bool = False
        serv:decimal = 0
        vat:decimal = 0
        vat2:decimal = 0
        fact:decimal = 0
        serv_vat:bool = False
        argt_betrag:decimal = 0
        lodging:decimal = 0
        i:int = 0
        n:int = 0
        Bzimmer = Zimmer

        bzimmer = db_session.query(Bzimmer).filter(
                (not (Bzimmer.CODE.op("~")("")))).first()

        if bzimmer:
            flag_t = True

        for zimmer in db_session.query(Zimmer).all():

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.etage == to_string(zimmer.etage) and cl_list.loc == zimmer.CODE), first=True)

            if not cl_list:
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.loc = zimmer.CODE
                cl_list.etage = to_string(zimmer.etage)

            if zimmer.zistatus <= 2:
                cl_list.vac = cl_list.vac + 1

            elif zimmer.zistatus == 6:
                cl_list.ooo = cl_list.ooo + 1

            if not zimmer.sleeping:
                cl_list.inact = cl_list.inact + 1

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 127)).first()
        status_vat = htparam.flogical

        artikel = db_session.query(Artikel).filter(
                (Artikel.artnr == 99) &  (Artikel.departement == 0)).first()

        if artikel and status_vat :
            serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, artikel.artnr, artikel.departement, ci_date))
            vat = vat + vat2

        res_line_obj_list = []
        for res_line, zimmer in db_session.query(Res_line, Zimmer).join(Zimmer,(Zimmer.zinr == Res_line.zinr)).filter(
                ((Res_line.active_flag == 1) &  (Res_line.resstatus != 12)) &  (((Res_line.abreise > ci_date)) |  ((Res_line.ankunft == Res_line.abreise)))).all():
            if res_line._recid in res_line_obj_list:
                continue
            else:
                res_line_obj_list.append(res_line._recid)

            reservation = db_session.query(Reservation).filter(
                    (Reservation.resnr == res_line.resnr)).first()

            arrangement = db_session.query(Arrangement).filter(
                    (Arrangement == res_line.arrangement)).first()
            frate = 1

            if res_line.betriebsnr != 1:
                frate = exchg_rate

            elif res_line.adrflag:
                frate = 1

            elif res_line.reserve_dec != 0:
                frate = reserve_dec

            cl_list = query(cl_list_list, filters=(lambda cl_list :cl_list.etage == to_string(zimmer.etage) and cl_list.loc == zimmer.CODE), first=True)

            if res_line.gratis > 0 or (res_line.zipreis == 0 and res_line.erwachs > 0):

                if zimmer.sleeping:
                    cl_list.com = cl_list.com + 1
                else:
                    cl_list.hu = cl_list.hu + 1
                cl_list.cpax = cl_list.cpax + res_line.gratis + res_line.erwachs

                if res_line.zipreis == 0 and res_line.erwachs > 0:
                    msg_str = msg_str + chr(2) + "&W" + translateExtended ("RmNo ", lvcarea, "") + res_line.zinr + ": Rate  ==  0 and Adult  ==  " + to_string(res_line.erwachs) + " found."

            if res_line.zipreis > 0:
                lodging = res_line.zipreis

                for argt_line in db_session.query(Argt_line).filter(
                        (Argt_line.argtnr == arrangement.argtnr) &  (not Argt_line.kind2)).all():

                    artikel = db_session.query(Artikel).filter(
                            (Artikel.artnr == argt_line.argt_artnr) &  (Artikel.departement == argt_line.departement)).first()
                    argt_betrag, ex_rate = get_output(argt_betrag(res_line._recid, argt_line._recid))
                    lodging = lodging - argt_betrag
                lodging = round (lodging * frate, price_decimal)

                if foreign_rate and price_decimal == 0:

                    htparam = db_session.query(Htparam).filter(
                            (Htparam.paramnr == 145)).first()

                    if htparam.finteger != 0:
                        n = 1
                        for i in range(1,finteger + 1) :
                            n = n * 10
                        lodging = round(lodging / n, 0) * n
                cl_list.occ = cl_list.occ + 1
                cl_list.pax = cl_list.pax + res_line.erwachs + res_line.kind1
                cl_list.rev = cl_list.rev + lodging
        gr_tot()

        for cl_list in query(cl_list_list, filters=(lambda cl_list :not re.match("Gr. TOTAL",cl_list.loc))):

            test = query(test_list, filters=(lambda test :xx == cl_list.loc), first=True)

            if not test:
                test = Test()
                test_list.append(test)

                test.xx = cl_list.loc
                test.yy = ""

        for cl_list in query(cl_list_list, filters=(lambda cl_list :not re.match("G. TOTAL",cl_list.etage))):

            test = query(test_list, filters=(lambda test :yy == cl_list.etage), first=True)

            if not test:
                test = Test()
                test_list.append(test)

                test.yy = cl_list.etage
                test.xx = ""

        for test in query(test_list, filters=(lambda test :re.match("",test.xx) and not re.match("G.TOTAL",test.yy))):
            t_occ = 0
            t_hu = 0
            t_ooo = 0
            t_com = 0
            t_vac = 0
            t_sum = 0
            t_inact = 0
            t_rev = 0
            t_nrev = 0
            t_pax = 0
            t_cpax = 0

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.etage == test.yy)):
                temp_et = cl_list.etage
                temp_loc = cl_list.loc
                cl_list.sum = cl_list.occ + cl_list.hu + cl_list.ooo + cl_list.com + cl_list.vac
                cl_list.nrev = round (cl_list.rev / fact, price_decimal)
                t_occ = t_occ + cl_list.occ
                t_hu = t_hu + cl_list.hu
                t_ooo = t_ooo + cl_list.ooo
                t_com = t_com + cl_list.com
                t_vac = t_vac + cl_list.vac
                t_sum = t_sum + cl_list.sum
                t_inact = t_inact + cl_list.inact
                t_rev = t_rev + cl_list.rev
                t_nrev = t_nrev + cl_list.nrev
                t_pax = t_pax + cl_list.pax
                t_cpax = t_cpax + cl_list.cpax

            if not re.match("",temp_et):
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

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
                cl_list.rev = t_rev
                cl_list.nrev = t_nrev
                cl_list.pax = t_pax
                cl_list.cpax = t_cpax
            t_occ = 0
            t_hu = 0
            t_ooo = 0
            t_com = 0
            t_vac = 0
            t_sum = 0
            t_inact = 0
            t_rev = 0
            t_nrev = 0
            t_pax = 0
            t_cpax = 0

        for test in query(test_list, filters=(lambda test :not re.match("",test.xx))):
            t_occ = 0
            t_hu = 0
            t_ooo = 0
            t_com = 0
            t_vac = 0
            t_sum = 0
            t_inact = 0
            t_rev = 0
            t_nrev = 0
            t_pax = 0
            t_cpax = 0

            for cl_list in query(cl_list_list, filters=(lambda cl_list :re.match(test,cl_list.loc).xx)):
                temp_loc = cl_list.loc
                cl_list.sum = cl_list.occ + cl_list.hu + cl_list.ooo + cl_list.com + cl_list.vac
                cl_list.nrev = round (cl_list.rev / fact, price_decimal)
                t_occ = t_occ + cl_list.occ
                t_hu = t_hu + cl_list.hu
                t_ooo = t_ooo + cl_list.ooo
                t_com = t_com + cl_list.com
                t_vac = t_vac + cl_list.vac
                t_sum = t_sum + cl_list.sum
                t_inact = t_inact + cl_list.inact
                t_rev = t_rev + cl_list.rev
                t_nrev = t_nrev + cl_list.nrev
                t_pax = t_pax + cl_list.pax
                t_cpax = t_cpax + cl_list.cpax
            cl_list = Cl_list()
            cl_list_list.append(cl_list)

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
            cl_list.rev = t_rev
            cl_list.nrev = t_nrev
            cl_list.pax = t_pax
            cl_list.cpax = t_cpax
            t_occ = 0
            t_hu = 0
            t_ooo = 0
            t_com = 0
            t_vac = 0
            t_sum = 0
            t_inact = 0
            t_rev = 0
            t_nrev = 0
            t_pax = 0
            t_cpax = 0

    def gr_tot():

        nonlocal msg_str, ci_date, price_decimal, long_digit, foreign_rate, curr_local, curr_foreign, exchg_rate, flag_t, t_occ, t_hu, t_ooo, t_com, t_vac, t_sum, t_inact, t_rev, t_nrev, t_pax, t_cpax, cl_list_list, fact, frate, ex_rate, lvcarea, htparam, waehrung, zimmer, artikel, res_line, reservation, arrangement, argt_line
        nonlocal bzimmer


        nonlocal test, cl_list, bzimmer
        nonlocal test_list, cl_list_list

        t_etage:int = 0
        t_occ = 0
        t_hu = 0
        t_ooo = 0
        t_com = 0
        t_vac = 0
        t_sum = 0
        t_inact = 0
        t_rev = 0
        t_nrev = 0
        t_pax = 0
        t_cpax = 0

        for cl_list in query(cl_list_list):
            cl_list.sum = cl_list.occ + cl_list.hu + cl_list.ooo + cl_list.com + cl_list.vac
            cl_list.nrev = round (cl_list.rev / fact, price_decimal)
            t_occ = t_occ + cl_list.occ
            t_hu = t_hu + cl_list.hu
            t_ooo = t_ooo + cl_list.ooo
            t_com = t_com + cl_list.com
            t_vac = t_vac + cl_list.vac
            t_sum = t_sum + cl_list.sum
            t_inact = t_inact + cl_list.inact
            t_rev = t_rev + cl_list.rev
            t_nrev = t_nrev + cl_list.nrev
            t_pax = t_pax + cl_list.pax
            t_cpax = t_cpax + cl_list.cpax
            to_string(t_etage) = cl_list.etage
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

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
        cl_list.rev = t_rev
        cl_list.nrev = t_nrev
        cl_list.pax = t_pax
        cl_list.cpax = t_cpax

        if t_etage == 0:
            t_etage = 999
        cl_list = Cl_list()
        cl_list_list.append(cl_list)

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
        cl_list.rev = t_rev
        cl_list.nrev = t_nrev
        cl_list.pax = t_pax
        cl_list.cpax = t_cpax


        t_occ = 0
        t_hu = 0
        t_ooo = 0
        t_com = 0
        t_vac = 0
        t_sum = 0
        t_inact = 0
        t_rev = 0
        t_nrev = 0
        t_pax = 0
        t_cpax = 0


    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 110)).first()
    ci_date = htparam.fdate

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 491)).first()
    price_decimal = htparam.finteger

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 246)).first()
    long_digit = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 240)).first()
    foreign_rate = htparam.flogical

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 152)).first()
    curr_local = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()
    curr_foreign = fchar

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 144)).first()

    waehrung = db_session.query(Waehrung).filter(
            (Waehrung.wabkurz == htparam.fchar)).first()

    if waehrung:
        exchg_rate = waehrung.ankauf / waehrung.einheit
    else:
        exchg_rate = 1
    create_list()

    return generate_output()