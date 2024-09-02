from functions.additional_functions import *
import decimal
from datetime import date
from functions.htpint import htpint
from functions.calc_servtaxesbl import calc_servtaxesbl
import re
from models import Htparam, Umsatz, Artikel, Budget, Hoteldpt

def foumsz_create_listbl(from_dept:int, to_dept:int, first_date:date, from_date:date, to_date:date, totvatflag:bool):
    umsz_list_list = []
    vhp_limited:bool = False
    vat_str:str = ""
    vat_artnr:int = 0
    serv_artnr:int = 0
    price_decimal:int = 0
    htparam = umsatz = artikel = budget = hoteldpt = None

    umsz_list = cl_list = vat_list = gvat_list = not_avail_umstaz = bumsz = None

    umsz_list_list, Umsz_list = create_model("Umsz_list", {"artnr":str, "bezeich":str, "day_nett":str, "day_serv":str, "day_tax":str, "day_gros":str, "day_persen":str, "mtd_nett":str, "mtd_serv":str, "mtd_tax":str, "mtd_gros":str, "mtd_persen":str, "ytd_nett":str, "ytd_serv":str, "ytd_tax":str, "ytd_gros":str, "ytd_persen":str, "month_bud":str})
    cl_list_list, Cl_list = create_model("Cl_list", {"flag":str, "vat_proz":decimal, "artnr":int, "dept":int, "bezeich":str, "dnet":decimal, "proz1":decimal, "dserv":decimal, "dtax":decimal, "dgros":decimal, "proz2":decimal, "mnet":decimal, "mserv":decimal, "mtax":decimal, "mgros":decimal, "proz4":decimal, "ynet":decimal, "proz6":decimal, "yserv":decimal, "ytax":decimal, "ygros":decimal, "mbudget":decimal})
    vat_list_list, Vat_list = create_model("Vat_list", {"dptnr":int, "vat":decimal, "dtax":decimal, "dnet":decimal, "dgros":decimal, "dserv":decimal, "mtax":decimal, "mnet":decimal, "mserv":decimal, "mgros":decimal, "ytax":decimal, "yserv":decimal, "ynet":decimal, "ygros":decimal})
    gvat_list_list, Gvat_list = create_model("Gvat_list", {"dptnr":int, "vat":decimal, "dtax":decimal, "dnet":decimal, "dgros":decimal, "dserv":decimal, "mtax":decimal, "mnet":decimal, "mserv":decimal, "mgros":decimal, "ytax":decimal, "yserv":decimal, "ynet":decimal, "ygros":decimal})
    not_avail_umstaz_list, Not_avail_umstaz = create_model("Not_avail_umstaz", {"artnr":int, "depart":int, "bezeich":str})

    Bumsz = Umsatz

    db_session = local_storage.db_session

    def generate_output():
        nonlocal umsz_list_list, vhp_limited, vat_str, vat_artnr, serv_artnr, price_decimal, htparam, umsatz, artikel, budget, hoteldpt
        nonlocal bumsz


        nonlocal umsz_list, cl_list, vat_list, gvat_list, not_avail_umstaz, bumsz
        nonlocal umsz_list_list, cl_list_list, vat_list_list, gvat_list_list, not_avail_umstaz_list
        return {"umsz-list": umsz_list_list}

    def create_umsatz():

        nonlocal umsz_list_list, vhp_limited, vat_str, vat_artnr, serv_artnr, price_decimal, htparam, umsatz, artikel, budget, hoteldpt
        nonlocal bumsz


        nonlocal umsz_list, cl_list, vat_list, gvat_list, not_avail_umstaz, bumsz
        nonlocal umsz_list_list, cl_list_list, vat_list_list, gvat_list_list, not_avail_umstaz_list

        dnet:decimal = 0
        dserv:decimal = 0
        dtax:decimal = 0
        dgros:decimal = 0
        mnet:decimal = 0
        mserv:decimal = 0
        mtax:decimal = 0
        mgros:decimal = 0
        ynet:decimal = 0
        yserv:decimal = 0
        ytax:decimal = 0
        ygros:decimal = 0
        t_dnet:decimal = 0
        t_dserv:decimal = 0
        t_dtax:decimal = 0
        t_dgros:decimal = 0
        t_mnet:decimal = 0
        t_mserv:decimal = 0
        t_mtax:decimal = 0
        t_mgros:decimal = 0
        t_ynet:decimal = 0
        t_yserv:decimal = 0
        t_ytax:decimal = 0
        t_ygros:decimal = 0
        vat:decimal = 0
        vat2:decimal = 0
        all_vat:decimal = 0
        serv:decimal = 0
        it_exist:bool = False
        serv_vat:bool = False
        fact:decimal = 0
        nett_amt:decimal = 0
        nett_serv:decimal = 0
        nett_tax:decimal = 0
        nett_vat:decimal = 0
        mbugdet:decimal = 0
        tbudget:decimal = 0
        gtbudget:decimal = 0
        cr_umsatz:bool = False
        curr_artnr:int = 0
        curr_departement:int = 0
        fact1:decimal = 1
        do_it:bool = False
        counter:int = 0
        x_sum:decimal = 0
        x_sum2:decimal = 0
        y_sum:decimal = 0
        y_sum2:decimal = 0
        Bumsz = Umsatz

        htparam = db_session.query(Htparam).filter(
                (Htparam.paramnr == 479)).first()
        serv_vat = htparam.flogical
        umsz_list_list.clear()
        cl_list_list.clear()
        vat_list_list.clear()
        gvat_list_list.clear()
        t_dnet = 0


        t_dserv = 0
        t_dtax = 0
        t_dgros = 0
        t_mnet = 0
        t_mserv = 0
        t_mtax = 0
        t_mgros = 0
        t_ynet = 0
        t_yserv = 0
        t_ytax = 0
        t_ygros = 0
        gtbudget = 0

        for artikel in db_session.query(Artikel).filter(
                ((Artikel.artart == 0) |  (Artikel.artart == 8)) &  (Artikel.departement >= from_dept) &  (Artikel.departement <= to_dept)).all():

            umsatz = db_session.query(Umsatz).filter(
                    (Umsatz.artnr == artikel.artnr) &  (Umsatz.departement == artikel.departement) &  (Umsatz.datum >= from_date) &  (Umsatz.datum <= to_date)).first()

            if not umsatz:

                not_avail_umstaz = query(not_avail_umstaz_list, filters=(lambda not_avail_umstaz :not_avail_umstaz.artnr == artikel.artnr and not_avail_umstaz.depart == artikel.departement), first=True)

                if not_avail_umstaz:
                    pass
                else:
                    not_avail_umstaz = Not_avail_umstaz()
                    not_avail_umstaz_list.append(not_avail_umstaz)

                    not_avail_umstaz.artnr = artikel.artnr
                    not_avail_umstaz.depart = artikel.departement
                    not_avail_umstaz.bezeich = artikel.bezeich

        for umsatz in db_session.query(Umsatz).filter(
                (Umsatz.departement >= from_dept) &  (Umsatz.departement <= to_dept) &  (Umsatz.datum >= from_date) &  (Umsatz.datum <= to_date)).all():

            if curr_artnr == 0 or curr_artnr != umsatz.artnr or (curr_artnr == umsatz.artnr and curr_departement != umsatz.departement):

                artikel = db_session.query(Artikel).filter(
                        (Artikel.artnr == umsatz.artnr) &  (Artikel.departement == umsatz.departement) &  ((Artikel.artart == 0) |  (Artikel.artart == 8))).first()

                if artikel:

                    if curr_artnr != 0:
                        it_exist = False
                        serv = 0
                        vat = 0
                        tbudget = tbudget + mbudget


                    curr_artnr = umsatz.artnr
                    do_it = True


                else:
                    do_it = False

            if do_it :
                counter = counter + 1

                if (curr_departement != umsatz.departement) or counter == 1:

                    if counter != 1:

                        for not_avail_umstaz in query(not_avail_umstaz_list, filters=(lambda not_avail_umstaz :not_avail_umstaz.depart == curr_departement)):

                            budget = db_session.query(Budget).filter(
                                    (get_month(Budget.datum) == get_month(to_date)) &  (get_year(Budget.datum) == get_year(to_date)) &  (Budget.departement == not_avail_umstaz.depart) &  (Budget.artnr == not_avail_umstaz.artnr)).first()

                            if budget and budget.betrag != 0:

                                if not it_exist:
                                    it_exist = True
                                    cl_list = Cl_list()
                                    cl_list_list.append(cl_list)

                                    cl_list.artnr = not_avail_umstaz.artnr
                                    cl_list.dept = not_avail_umstaz.depart
                                    cl_list.bezeich = not_avail_umstaz.bezeich
                                    it_exist = False


                                mbudget = sum_budget(first_date, to_date, not_avail_umstaz.artnr, not_avail_umstaz.depart)
                                mbudget = round(mbudget, 1)
                                cl_list.mbudget = mbudget
                                tbudget = tbudget + mbudget


                        tbudget = round(tbudget, 1)

                        for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num)):

                            if dgros != 0:
                                cl_list.proz2 = cl_list.dgros / dgros * 100

                            if mgros != 0:
                                cl_list.proz4 = cl_list.mgros / mgros * 100

                            if ygros != 0:
                                cl_list.proz6 = cl_list.ygros / ygros * 100

                        if totvatflag:

                            for vat_list in query(vat_list_list, filters=(lambda vat_list :vat_list.vat == 0 or (vat_list.ytax == 0))):
                                vat_list_list.remove(vat_list)

                            for vat_list in query(vat_list_list, filters=(lambda vat_list :vat_list.dptnr == hoteldpt.num)):
                                cl_list = Cl_list()
                                cl_list_list.append(cl_list)

                                cl_list.flag = "**"
                                cl_list.bezeich = "TOTAL vat " + to_string(vat_list.vat * 100, ">>9.99") + " " + "%"
                                cl_list.dnet = vat_list.dnet
                                cl_list.dserv = vat_list.dserv
                                cl_list.dtax = vat_list.dtax
                                cl_list.dgros = vat_list.dgros
                                cl_list.mnet = vat_list.mnet
                                cl_list.mserv = vat_list.mserv
                                cl_list.mtax = vat_list.mtax
                                cl_list.mgros = vat_list.mgros
                                cl_list.ynet = vat_list.ynet
                                cl_list.yserv = vat_list.yserv
                                cl_list.ytax = vat_list.ytax
                                cl_list.ygros = vat_list.ygros


                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.flag = "**"
                        cl_list.bezeich = "T O T A L"
                        cl_list.dnet = dnet
                        cl_list.dserv = dserv
                        cl_list.dtax = dtax
                        cl_list.dgros = dgros
                        cl_list.mnet = mnet
                        cl_list.mserv = mserv
                        cl_list.mtax = mtax
                        cl_list.mgros = mgros
                        cl_list.ynet = ynet
                        cl_list.yserv = yserv
                        cl_list.ytax = ytax
                        cl_list.ygros = ygros
                        cl_list.mbudget = tbudget


                        gtbudget = gtbudget + tbudget

                        if dgros != 0:
                            cl_list.proz2 = 100

                        if mgros != 0:
                            cl_list.proz4 = 100

                        if ygros != 0:
                            cl_list.proz6 = 100

                    hoteldpt = db_session.query(Hoteldpt).filter(
                            (Hoteldpt.num == umsatz.departement)).first()

                    if hoteldpt:
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.flag = "*"
                        cl_list.bezeich = to_string(hoteldpt.num) + " - " + hoteldpt.depart
                        dnet = 0
                        dserv = 0
                        dtax = 0
                        dgros = 0
                        mnet = 0
                        mserv = 0
                        mtax = 0
                        mgros = 0
                        ynet = 0
                        yserv = 0
                        ytax = 0
                        ygros = 0
                        tbudget = 0


                    curr_departement = umsatz.departement


                serv, vat, vat2, fact = get_output(calc_servtaxesbl(1, umsatz.artnr, umsatz.departement, umsatz.datum))
                all_vat = vat + vat2

                vat_list = query(vat_list_list, filters=(lambda vat_list :vat_list.vat == vat and vat_list.dptnr == artikel.departement), first=True)

                if not vat_list:
                    vat_list = Vat_list()
                    vat_list_list.append(vat_list)

                    vat_list.vat = all_vat
                    vat_list.dptnr = artikel.departement

                if not it_exist:
                    it_exist = True
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.artnr = umsatz.artnr
                    cl_list.dept = umsatz.departement
                    cl_list.bezeich = artikel.bezeich
                    cl_list.vat_proz = all_vat

                if vat == 1 or (artikel.artnr == vat_artnr and artikel.departement == 0):
                    nett_amt = 0
                    nett_serv = 0
                    nett_tax = umsatz.betrag

                elif re.match(".*;" + to_string(artikel.artnr,vat_str) + ";*") and artikel.departement == 0:
                    nett_amt = 0
                    nett_serv = 0
                    nett_tax = umsatz.betrag

                elif serv == 1 or (artikel.artnr == serv_artnr and artikel.departement == 0):
                    nett_amt = 0
                    nett_tax = 0
                    nett_serv = umsatz.betrag


                else:
                    nett_amt = umsatz.betrag / fact
                    nett_serv = nett_amt * serv
                    nett_tax = nett_amt * vat
                    nett_amt = umsatz.betrag - nett_serv - nett_tax


                mbudget = sum_budget(first_date, to_date, artikel.artnr, artikel.departement)
                mbudget = round(mbudget, 1)
                cl_list.mbudget = mbudget

                if umsatz.datum == to_date:
                    cl_list.dnet = nett_amt / fact1
                    cl_list.dgros = umsatz.betrag / fact1
                    cl_list.dserv = nett_serv / fact1
                    cl_list.dtax = nett_tax / fact1
                    dnet = dnet + cl_list.dnet
                    dserv = dserv + cl_list.dserv
                    dtax = dtax + cl_list.dtax
                    dgros = dgros + cl_list.dgros
                    t_dnet = t_dnet + cl_list.dnet
                    t_dserv = t_dserv + cl_list.dserv
                    t_dtax = t_dtax + cl_list.dtax
                    t_dgros = t_dgros + cl_list.dgros

                if umsatz.datum == to_date and vat_list:
                    vat_list.dtax = vat_list.dtax + nett_tax / fact1
                    vat_list.dnet = vat_list.dnet + nett_amt / fact1
                    vat_list.dgros = vat_list.dgros + umsatz.betrag / fact1
                    vat_list.dserv = vat_list.dserv + nett_serv / fact1

                if umsatz.datum >= first_date and umsatz.datum <= to_date:
                    cl_list.mnet = cl_list.mnet + nett_amt / fact1
                    cl_list.mserv = cl_list.mserv + nett_serv / fact1
                    cl_list.mtax = cl_list.mtax + nett_tax / fact1
                    cl_list.mgros = cl_list.mgros + umsatz.betrag / fact1
                    mnet = mnet + nett_amt / fact1
                    mserv = mserv + nett_serv / fact1
                    mtax = mtax + nett_tax / fact1
                    mgros = mgros + umsatz.betrag / fact1
                    t_mnet = t_mnet + nett_amt / fact1
                    t_mserv = t_mserv + nett_serv / fact1
                    t_mtax = t_mtax + nett_tax / fact1
                    t_mgros = t_mgros + umsatz.betrag / fact1

                if umsatz.datum >= first_date and umsatz.datum <= to_date and vat_list:
                    vat_list.mtax = vat_list.mtax + nett_tax / fact1
                    vat_list.mnet = vat_list.mnet + nett_amt / fact1
                    vat_list.mserv = vat_list.mserv + nett_serv / fact1
                    vat_list.mgros = vat_list.mgros + umsatz.betrag / fact1


                cl_list.ynet = cl_list.ynet + nett_amt / fact1
                cl_list.yserv = cl_list.yserv + nett_serv / fact1
                cl_list.ytax = cl_list.ytax + nett_tax / fact1
                cl_list.ygros = cl_list.ygros + umsatz.betrag / fact1
                ynet = ynet + nett_amt / fact1
                yserv = yserv + nett_serv / fact1
                ytax = ytax + nett_tax / fact1
                ygros = ygros + umsatz.betrag / fact1
                t_ynet = t_ynet + nett_amt / fact1
                t_yserv = t_yserv + nett_serv / fact1
                t_ytax = t_ytax + nett_tax / fact1
                t_ygros = t_ygros + umsatz.betrag / fact1

                if vat_list:
                    vat_list.ytax = vat_list.ytax + nett_tax / fact1
                    vat_list.ynet = vat_list.ynet + nett_amt / fact1
                    vat_list.yserv = vat_list.yserv + nett_serv / fact1
                    vat_list.ygros = vat_list.ygros + umsatz.betrag / fact1

        if counter != 1:

            for not_avail_umstaz in query(not_avail_umstaz_list, filters=(lambda not_avail_umstaz :not_avail_umstaz.depart == curr_departement)):

                budget = db_session.query(Budget).filter(
                        (get_month(Budget.datum) == get_month(to_date)) &  (get_year(Budget.datum) == get_year(to_date)) &  (Budget.departement == not_avail_umstaz.depart) &  (Budget.artnr == not_avail_umstaz.artnr)).first()

                if budget and budget.betrag != 0:

                    if not it_exist:
                        it_exist = True
                        cl_list = Cl_list()
                        cl_list_list.append(cl_list)

                        cl_list.artnr = not_avail_umstaz.artnr
                        cl_list.dept = not_avail_umstaz.depart
                        cl_list.bezeich = not_avail_umstaz.bezeich
                        it_exist = False


                    mbudget = sum_budget(first_date, to_date, not_avail_umstaz.artnr, not_avail_umstaz.depart)
                    mbudget = round(mbudget, 1)
                    cl_list.mbudget = mbudget
                    tbudget = tbudget + mbudget


            tbudget = round(tbudget, 1)

            for cl_list in query(cl_list_list, filters=(lambda cl_list :cl_list.dept == hoteldpt.num)):

                if dgros != 0:
                    cl_list.proz2 = cl_list.dgros / dgros * 100

                if mgros != 0:
                    cl_list.proz4 = cl_list.mgros / mgros * 100

                if ygros != 0:
                    cl_list.proz6 = cl_list.ygros / ygros * 100

            if totvatflag:

                for vat_list in query(vat_list_list, filters=(lambda vat_list :vat_list.vat == 0 or (vat_list.ytax == 0))):
                    vat_list_list.remove(vat_list)

                for vat_list in query(vat_list_list, filters=(lambda vat_list :vat_list.dptnr == hoteldpt.num)):
                    cl_list = Cl_list()
                    cl_list_list.append(cl_list)

                    cl_list.flag = "**"
                    cl_list.bezeich = "TOTAL vat " + to_string(vat_list.vat * 100, ">>9.99") + " " + "%"
                    cl_list.dnet = vat_list.dnet
                    cl_list.dserv = vat_list.dserv
                    cl_list.dtax = vat_list.dtax
                    cl_list.dgros = vat_list.dgros
                    cl_list.mnet = vat_list.mnet
                    cl_list.mserv = vat_list.mserv
                    cl_list.mtax = vat_list.mtax
                    cl_list.mgros = vat_list.mgros
                    cl_list.ynet = vat_list.ynet
                    cl_list.yserv = vat_list.yserv
                    cl_list.ytax = vat_list.ytax
                    cl_list.ygros = vat_list.ygros


            cl_list = Cl_list()
            cl_list_list.append(cl_list)

            cl_list.flag = "**"
            cl_list.bezeich = "T O T A L"
            cl_list.dnet = dnet
            cl_list.dserv = dserv
            cl_list.dtax = dtax
            cl_list.dgros = dgros
            cl_list.mnet = mnet
            cl_list.mserv = mserv
            cl_list.mtax = mtax
            cl_list.mgros = mgros
            cl_list.ynet = ynet
            cl_list.yserv = yserv
            cl_list.ytax = ytax
            cl_list.ygros = ygros
            cl_list.mbudget = tbudget


            gtbudget = gtbudget + tbudget

            if dgros != 0:
                cl_list.proz2 = 100

            if mgros != 0:
                cl_list.proz4 = 100

            if ygros != 0:
                cl_list.proz6 = 100

        for cl_list in query(cl_list_list):

            if cl_list.flag.lower()  == "*":
                umsz_list = Umsz_list()
                umsz_list_list.append(umsz_list)

                umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
                umsz_list.bezeich = cl_list.bezeich


            else:

                if price_decimal == 2:
                    umsz_list = Umsz_list()
                    umsz_list_list.append(umsz_list)

                    umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
                    umsz_list.bezeich = cl_list.bezeich
                    umsz_list.day_nett = to_string(cl_list.dnet, "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_serv = to_string(cl_list.dserv, "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_tax = to_string(cl_list.dtax, "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_gros = to_string(cl_list.dgros, "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_persen = to_string(cl_list.proz2, "->>>>9.99")
                    umsz_list.mtd_nett = to_string(cl_list.mnet, "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_serv = to_string(cl_list.mserv, "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_tax = to_string(cl_list.mtax, "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_gros = to_string(cl_list.mgros, "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_persen = to_string(cl_list.proz4, "->>>>9.99")
                    umsz_list.ytd_nett = to_string(cl_list.ynet, "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_serv = to_string(cl_list.yserv, "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_tax = to_string(cl_list.ytax, "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_gros = to_string(cl_list.ygros, "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_persen = to_string(cl_list.proz6, "->>>>9.99")
                    umsz_list.month_bud = to_string(cl_list.mbudget, "->,>>>,>>>,>>>,>>9.99")


                else:
                    umsz_list = Umsz_list()
                    umsz_list_list.append(umsz_list)

                    umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
                    umsz_list.bezeich = cl_list.bezeich
                    umsz_list.day_nett = to_string(cl_list.dnet, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.day_serv = to_string(cl_list.dserv, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.day_tax = to_string(cl_list.dtax, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.day_gros = to_string(cl_list.dgros, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.day_persen = to_string(cl_list.proz2, "->>>>9.99")
                    umsz_list.mtd_nett = to_string(cl_list.mnet, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.mtd_serv = to_string(cl_list.mserv, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.mtd_tax = to_string(cl_list.mtax, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.mtd_gros = to_string(cl_list.mgros, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.mtd_persen = to_string(cl_list.proz4, "->>>>9.99")
                    umsz_list.ytd_nett = to_string(cl_list.ynet, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.ytd_serv = to_string(cl_list.yserv, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.ytd_tax = to_string(cl_list.ytax, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.ytd_gros = to_string(cl_list.ygros, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.ytd_persen = to_string(cl_list.proz6, "->>>>9.99")
                    umsz_list.month_bud = to_string(cl_list.mbudget, "->,>>>,>>>,>>>,>>9.99")

        if totvatflag:

            for vat_list in query(vat_list_list):

                gvat_list = query(gvat_list_list, filters=(lambda gvat_list :gvat_list.vat == vat_list.vat), first=True)

                if not gvat_list:
                    gvat_list = Gvat_list()
                    gvat_list_list.append(gvat_list)

                    gvat_list.vat = vat_list.vat


                gvat_list.dnet = gvat_list.dnet + vat_list.dnet
                gvat_list.dserv = gvat_list.dserv + vat_list.dserv
                gvat_list.dtax = gvat_list.dtax + vat_list.dtax
                gvat_list.dgros = gvat_list.dgros + vat_list.dgros
                gvat_list.mnet = gvat_list.mnet + vat_list.mnet
                gvat_list.mserv = gvat_list.mserv + vat_list.mserv
                gvat_list.mtax = gvat_list.mtax + vat_list.mtax
                gvat_list.mgros = gvat_list.mgros + vat_list.mgros
                gvat_list.ynet = gvat_list.ynet + vat_list.ynet
                gvat_list.yserv = gvat_list.yserv + vat_list.yserv
                gvat_list.ytax = gvat_list.ytax + vat_list.ytax
                gvat_list.ygros = gvat_list.ygros + vat_list.ygros

            for gvat_list in query(gvat_list_list):
                cl_list = Cl_list()
                cl_list_list.append(cl_list)

                cl_list.flag = "**"
                cl_list.bezeich = "GTOTAL vat " + to_string(gvat_list.vat * 100, ">>9.99") + " " + "%"
                cl_list.dnet = gvat_list.dnet
                cl_list.dserv = gvat_list.dserv
                cl_list.dtax = gvat_list.dtax
                cl_list.dgros = gvat_list.dgros
                cl_list.mnet = gvat_list.mnet
                cl_list.mserv = gvat_list.mserv
                cl_list.mtax = gvat_list.mtax
                cl_list.mgros = gvat_list.mgros
                cl_list.ynet = gvat_list.ynet
                cl_list.yserv = gvat_list.yserv
                cl_list.ytax = gvat_list.ytax
                cl_list.ygros = gvat_list.ygros


                umsz_list = Umsz_list()
                umsz_list_list.append(umsz_list)


                if price_decimal == 2:
                    umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
                    umsz_list.bezeich = cl_list.bezeich
                    umsz_list.day_nett = to_string(cl_list.dnet, "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_serv = to_string(cl_list.dserv, "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_tax = to_string(cl_list.dtax, "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_gros = to_string(cl_list.dgros, "->>>,>>>,>>>,>>9.99")
                    umsz_list.day_persen = to_string(cl_list.proz2, "->>>>9.99")
                    umsz_list.mtd_nett = to_string(cl_list.mnet, "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_serv = to_string(cl_list.mserv, "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_tax = to_string(cl_list.mtax, "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_gros = to_string(cl_list.mgros, "->>>,>>>,>>>,>>9.99")
                    umsz_list.mtd_persen = to_string(cl_list.proz4, "->>>>9.99")
                    umsz_list.ytd_nett = to_string(cl_list.ynet, "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_serv = to_string(cl_list.yserv, "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_tax = to_string(cl_list.ytax, "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_gros = to_string(cl_list.ygros, "->>>,>>>,>>>,>>9.99")
                    umsz_list.ytd_persen = to_string(cl_list.proz6, "->>>>9.99")
                    umsz_list.month_bud = to_string(cl_list.mbudget, "->,>>>,>>>,>>>,>>9.99")


                else:
                    umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
                    umsz_list.bezeich = cl_list.bezeich
                    umsz_list.day_nett = to_string(cl_list.dnet, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.day_serv = to_string(cl_list.dserv, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.day_tax = to_string(cl_list.dtax, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.day_gros = to_string(cl_list.dgros, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.day_persen = to_string(cl_list.proz2, "->>>>9.99")
                    umsz_list.mtd_nett = to_string(cl_list.mnet, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.mtd_serv = to_string(cl_list.mserv, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.mtd_tax = to_string(cl_list.mtax, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.mtd_gros = to_string(cl_list.mgros, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.mtd_persen = to_string(cl_list.proz4, "->>>>9.99")
                    umsz_list.ytd_nett = to_string(cl_list.ynet, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.ytd_serv = to_string(cl_list.yserv, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.ytd_tax = to_string(cl_list.ytax, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.ytd_gros = to_string(cl_list.ygros, "->>,>>>,>>>,>>>,>>9")
                    umsz_list.ytd_persen = to_string(cl_list.proz6, "->>>>9.99")
                    umsz_list.month_bud = to_string(cl_list.mbudget, "->,>>>,>>>,>>>,>>9.99")


        cl_list = Cl_list()
        cl_list_list.append(cl_list)

        cl_list.flag = "***"
        cl_list.bezeich = "GRAND TOTAL"
        cl_list.dnet = t_dnet
        cl_list.dserv = t_dserv
        cl_list.dtax = t_dtax
        cl_list.dgros = t_dgros
        cl_list.mnet = t_mnet
        cl_list.mserv = t_mserv
        cl_list.mtax = t_mtax
        cl_list.mgros = t_mgros
        cl_list.ynet = t_ynet
        cl_list.yserv = t_yserv
        cl_list.ytax = t_ytax
        cl_list.ygros = t_ygros
        cl_list.mbudget = gtbudget

        if t_dgros != 0:
            cl_list.proz2 = 100

        if t_mgros != 0:
            cl_list.proz4 = 100

        if t_ygros != 0:
            cl_list.proz6 = 100
        umsz_list = Umsz_list()
        umsz_list_list.append(umsz_list)


        if price_decimal == 2:
            umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
            umsz_list.bezeich = cl_list.bezeich
            umsz_list.day_nett = to_string(cl_list.dnet, "->>>,>>>,>>>,>>9.99")
            umsz_list.day_serv = to_string(cl_list.dserv, "->>>,>>>,>>>,>>9.99")
            umsz_list.day_tax = to_string(cl_list.dtax, "->>>,>>>,>>>,>>9.99")
            umsz_list.day_gros = to_string(cl_list.dgros, "->>>,>>>,>>>,>>9.99")
            umsz_list.day_persen = to_string(cl_list.proz2, "->>>>9.99")
            umsz_list.mtd_nett = to_string(cl_list.mnet, "->>>,>>>,>>>,>>9.99")
            umsz_list.mtd_serv = to_string(cl_list.mserv, "->>>,>>>,>>>,>>9.99")
            umsz_list.mtd_tax = to_string(cl_list.mtax, "->>>,>>>,>>>,>>9.99")
            umsz_list.mtd_gros = to_string(cl_list.mgros, "->>>,>>>,>>>,>>9.99")
            umsz_list.mtd_persen = to_string(cl_list.proz4, "->>>>9.99")
            umsz_list.ytd_nett = to_string(cl_list.ynet, "->>>,>>>,>>>,>>9.99")
            umsz_list.ytd_serv = to_string(cl_list.yserv, "->>>,>>>,>>>,>>9.99")
            umsz_list.ytd_tax = to_string(cl_list.ytax, "->>>,>>>,>>>,>>9.99")
            umsz_list.ytd_gros = to_string(cl_list.ygros, "->>>,>>>,>>>,>>9.99")
            umsz_list.ytd_persen = to_string(cl_list.proz6, "->>>>9.99")
            umsz_list.month_bud = to_string(cl_list.mbudget, "->,>>>,>>>,>>>,>>9.99")


        else:
            umsz_list.artnr = to_string(cl_list.artnr, ">>>>")
            umsz_list.bezeich = cl_list.bezeich
            umsz_list.day_nett = to_string(cl_list.dnet, "->>,>>>,>>>,>>>,>>9")
            umsz_list.day_serv = to_string(cl_list.dserv, "->>,>>>,>>>,>>>,>>9")
            umsz_list.day_tax = to_string(cl_list.dtax, "->>,>>>,>>>,>>>,>>9")
            umsz_list.day_gros = to_string(cl_list.dgros, "->>,>>>,>>>,>>>,>>9")
            umsz_list.day_persen = to_string(cl_list.proz2, "->>>>9.99")
            umsz_list.mtd_nett = to_string(cl_list.mnet, "->>,>>>,>>>,>>>,>>9")
            umsz_list.mtd_serv = to_string(cl_list.mserv, "->>,>>>,>>>,>>>,>>9")
            umsz_list.mtd_tax = to_string(cl_list.mtax, "->>,>>>,>>>,>>>,>>9")
            umsz_list.mtd_gros = to_string(cl_list.mgros, "->>,>>>,>>>,>>>,>>9")
            umsz_list.mtd_persen = to_string(cl_list.proz4, "->>>>9.99")
            umsz_list.ytd_nett = to_string(cl_list.ynet, "->>,>>>,>>>,>>>,>>9")
            umsz_list.ytd_serv = to_string(cl_list.yserv, "->>,>>>,>>>,>>>,>>9")
            umsz_list.ytd_tax = to_string(cl_list.ytax, "->>,>>>,>>>,>>>,>>9")
            umsz_list.ytd_gros = to_string(cl_list.ygros, "->>,>>>,>>>,>>>,>>9")
            umsz_list.ytd_persen = to_string(cl_list.proz6, "->>>>9.99")
            umsz_list.month_bud = to_string(cl_list.mbudget, "->,>>>,>>>,>>>,>>9.99")

    def sum_budget(from_date:date, to_date:date, artnr:int, deptno:int):

        nonlocal umsz_list_list, vhp_limited, vat_str, vat_artnr, serv_artnr, price_decimal, htparam, umsatz, artikel, budget, hoteldpt
        nonlocal bumsz


        nonlocal umsz_list, cl_list, vat_list, gvat_list, not_avail_umstaz, bumsz
        nonlocal umsz_list_list, cl_list_list, vat_list_list, gvat_list_list, not_avail_umstaz_list

        mbudget = 0

        def generate_inner_output():
            return mbudget

        if get_month(from_date) == get_month(to_date):

            for budget in db_session.query(Budget).filter(
                    (get_month(Budget.datum) == get_month(to_date)) &  (get_year(Budget.datum) == get_year(to_date)) &  (Budget.departement == deptno) &  (Budget.artnr == artnr)).all():
                mbudget = mbudget + budget.betrag


        return generate_inner_output()

    htparam = db_session.query(Htparam).filter(
            (Htparam.paramnr == 132)).first()
    vat_artnr = htparam.finteger
    vat_str = htparam.fchar

    if vat_str != "":

        if substring(vat_str, 0, 1) != ";":
            vat_str = ";" + vat_str

        if substring(vat_str, len(vat_str) - 1, 1) != ";":
            vat_str = vat_str + ";"
    serv_artnr = get_output(htpint(133))
    price_decimal = get_output(htpint(491))
    create_umsatz()

    return generate_output()